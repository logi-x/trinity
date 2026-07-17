---
title: "2026 06 09 instructor settlement ledger"
date: "2026-06-09"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/plans/2026-06-09-instructor-settlement-ledger.md"
---
# Instructor Settlement Ledger (Plan A) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** On every completed paid **course** sale, write an immutable per-order settlement (`OrderSettlement`) plus per-contributor payable obligations (`CreatorEarning`), matured after the refund window and clawed back on refund — so the platform can begin answering "what do we owe each creator?". **Behind an off-by-default flag; this does NOT close #936** (payouts + surfaces are Plan B). Intermediate PRs use `Refs #936`.

**Architecture:** A pure split-compute layer (reusing the existing `priceOrder`) feeds a DB writer `recordOrderSettlement({sourceType, sourceId})`, idempotent on `(sourceType, sourceId)` (P2002-as-success). The write is **INLINE and fault-isolated** in the course completion orchestrator (request context, Prisma available — no BullMQ worker; `tsup` bundles workers without Prisma). An internal `CRON_SECRET`-guarded reconciliation route backfills inline failures; a second matures earnings (`pending→approved`). The course refund handler is extended to cancel earnings and reverse the settlement atomically. **Everything is gated by `SETTLEMENT_LEDGER_ENABLED` (default off) (D-8)** so nothing accrues until Plan B deploys.

**Tech Stack:** Next.js 16 (App Router) · Prisma 7 (multi-schema, `billing`) · Vitest (node env).

**Scope (R3 / D-9):** **COURSES ONLY.** Events are **excluded from v1** (no event refund flow exists → event earnings couldn't be clawed back). The compute layer (contributors resolver, allocator) is written generically so the later **Events phase** can reuse it, but no event settlement is wired. Subscriptions (platform-only), payouts, balance view, and surfaces are **Plan B** (`...-payouts.md`). Spec: `...specs/2026-06-09-instructor-settlement-design.md`. Supersedes spec D-7 (inline+sweep).

**Branch:** `feat/gh-936-settlement-ledger` (off fresh `main`). Ships via `experts-ship`.

---

## Review provenance

Folds round-1/2/3 findings (`docs/superpowers/reviews/`). Tags inline (`[B1]`, `[I3]`, `[R3-…]`, `[DB-1]`). R3 resolutions: ship-flag (D-8), courses-only (D-9), maturation two-step, commission `paid` exclusion, partial-null shares, P2002 test fix, sweep `$queryRaw` test, platform-loss observe, real-DB integration test, cron sidecar wiring.

---

## File map

| File                                                     | Responsibility                                                     | Action                       |
| -------------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------- |
| `src/lib/settlement/settlement-flag.ts`                  | `isSettlementLedgerEnabled()` kill-switch                          | Create (Phase 0)             |
| `src/lib/orders/price-order.ts`                          | Split math (existing, pure)                                        | Verify importable (Task 1.1) |
| `prisma/schema.prisma`                                   | `OrderSettlement` + expand `contributor_earnings`→`CreatorEarning` | Modify (Phase 1)             |
| `prisma/migrations/<ts>_settlement_ledger/migration.sql` | DDL                                                                | Create (Phase 1)             |
| `src/lib/settlement/contributors.ts`                     | Contributors → shares (generic; partial-null safe)                 | Create (Phase 2)             |
| `src/lib/settlement/allocate-earnings.ts`                | Pure split → earning lines (sum-reconciled)                        | Create (Phase 2)             |
| `src/lib/settlement/affiliate-metadata.ts`               | Fixed instructor-funded affiliate → `AffiliateMetadata`            | Create (Phase 2)             |
| `src/lib/settlement/record-settlement.ts`                | DB writer (course), idempotent, flag-gated                         | Create (Phase 3)             |
| `.../course-enrollment-complete.handler.ts`              | expose `enrollmentId` on the result                                | Modify (Phase 4)             |
| `.../course-enrollment-complete.orchestrator.ts`         | inline settle after affiliate+ZATCA (flag-gated)                   | Modify (Phase 4)             |
| `src/lib/settlement/reconcile-settlements.ts`            | Bounded anti-join sweep → settle missing                           | Create (Phase 5)             |
| `app/api/v1/internal/settlement/reconcile/route.ts`      | Cron route → sweep                                                 | Create (Phase 5)             |
| `app/api/v1/internal/settlement/stats/route.ts`          | Stopgap visibility (POST + CRON_SECRET)                            | Create (Phase 5)             |
| `src/lib/settlement/mature-earnings.ts`                  | Flip `pending→approved` past `payableAt` (two-step)                | Create (Phase 6)             |
| `app/api/v1/internal/creator-earnings/mature/route.ts`   | Cron route → maturation                                            | Create (Phase 6)             |
| `.../course-enrollment-refund-process.handler.ts`        | clawback earnings + reverse settlement                             | Modify (Phase 7)             |

Run all `pnpm`/`vitest` from `apps/experts-app`. Tests need `DATABASE_URL=postgresql://localhost/experts_test`.

---

## Phase 0 — Kill-switch flag `[R3 D-8]`

### Task 0.1: `isSettlementLedgerEnabled`

**Files:** Create `src/lib/settlement/settlement-flag.ts` + test.

- [ ] **Step 1: Implement.** Default OFF; truthy only for explicit `"true"`/`"1"`.

```ts
// src/lib/settlement/settlement-flag.ts
export function isSettlementLedgerEnabled(): boolean {
    const v = (process.env.SETTLEMENT_LEDGER_ENABLED ?? '').trim().toLowerCase()
    return v === 'true' || v === '1'
}
```

- [ ] **Step 2: Test** (`vi.stubEnv`): unset → false; `"true"` → true; `"false"` → false; `"1"` → true.
- [ ] **Step 3: Commit.** `git commit -m "feat(settlement): SETTLEMENT_LEDGER_ENABLED kill-switch (default off) (refs #936)"`

> Document `SETTLEMENT_LEDGER_ENABLED=false` in the env sample + the deploy checklist. It stays **off in prod until Plan B is deployed** (D-8).

---

## Phase 1 — Data model

### Task 1.1: Confirm `priceOrder` is server-importable

**Files:** read `src/lib/orders/price-order.ts`, `src/lib/pricing/settlement-config.ts`; create `src/lib/settlement/__tests__/price-order-server.test.ts`.

- [ ] **Step 1:** `grep -nE '"use client"|from "react"|window\.|document\.' src/lib/orders/price-order.ts src/lib/pricing/settlement-config.ts` → expect no matches.
- [ ] **Step 2:** test importing `priceOrder` from a node module; assert a known breakdown (gross 115 → vat 15, net 100, gatewayFee 2.875, instructorEarning>0, platformEarning>0).
- [ ] **Step 3:** `DATABASE_URL=postgresql://localhost/experts_test pnpm exec vitest run src/lib/settlement/__tests__/price-order-server.test.ts` → PASS.
- [ ] **Step 4: Commit.** `git commit -m "test(settlement): lock priceOrder as server-importable (refs #936)"`

### Task 1.2: Add `OrderSettlement` and expand `CreatorEarning`

**Files:** Modify `prisma/schema.prisma`. **Hand-edit only — never `prisma format`.**

- [ ] **Step 1: Migration preflight `[round-1]`.** If a dev/staging DB is reachable: `psql "$DATABASE_URL" -c 'SELECT count(*) FROM billing.contributor_earnings;'` → expect `0` (greenfield, D-1). Non-zero → STOP.

- [ ] **Step 2: Replace the `ContributorEarning` block.** No `payoutId` (added with the `CreatorPayout` relation in Plan B — two-PR seam). `onDelete: Restrict` `[B7]`. The `// internal ledger` comment forestalls a reflexive ZATCA-immutability objection `[DB-3]`.

```prisma
// Internal settlement ledger — NOT a ZATCA tax document. The recorded→reversed
// status mutation (+ reversedAt) is the audit trail for refunds; no row is deleted.
model OrderSettlement {
  id                     String   @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  sourceType             String   @map("source_type") @db.VarChar(20) // v1: "course" only
  sourceId               String   @map("source_id")  @db.Uuid          // enrollment row id
  buyerUserId            String   @map("buyer_user_id") @db.Uuid
  itemType               String   @map("item_type") @db.VarChar(20)
  itemId                 String   @map("item_id") @db.Uuid
  itemTitle              String   @map("item_title")
  currency               String   @default("SAR") @db.VarChar(3)
  grossPaid              Decimal  @map("gross_paid") @db.Decimal(10, 2)
  vatRate                Decimal  @map("vat_rate") @db.Decimal(5, 4)   // unit fraction (0.15), NOT integer percent like Invoice.taxRate [DB-7]
  vatAmount              Decimal  @map("vat_amount") @db.Decimal(10, 2)
  netExVat               Decimal  @map("net_ex_vat") @db.Decimal(10, 2)
  gatewayFee             Decimal  @map("gateway_fee") @db.Decimal(10, 2)
  gatewayFeeFraction     Decimal  @map("gateway_fee_fraction") @db.Decimal(5, 4)
  distributable          Decimal  @db.Decimal(10, 2)
  splitFraction          Decimal  @map("split_fraction") @db.Decimal(5, 4)
  platformShare          Decimal  @map("platform_share") @db.Decimal(10, 2)
  instructorShare        Decimal  @map("instructor_share") @db.Decimal(10, 2)
  affiliatePayout        Decimal  @default(0) @map("affiliate_payout") @db.Decimal(10, 2)
  discountInstructorCost Decimal  @default(0) @map("discount_instructor_cost") @db.Decimal(10, 2)
  platformEarning        Decimal  @map("platform_earning") @db.Decimal(10, 2)
  instructorNetTotal     Decimal  @map("instructor_net_total") @db.Decimal(10, 2)
  status                 String   @default("recorded") @db.VarChar(20) // "recorded" | "reversed"
  reversedAt             DateTime? @map("reversed_at") @db.Timestamptz(6)
  createdAt              DateTime @default(now()) @map("created_at") @db.Timestamptz(6)
  updatedAt              DateTime @updatedAt @map("updated_at") @db.Timestamptz(6)
  lines                  CreatorEarning[]

  @@unique([sourceType, sourceId], name: "order_settlement_source_unique")
  @@index([status])
  @@index([buyerUserId, itemType, itemId])
  @@map("order_settlements")
  @@schema("billing")
}

model CreatorEarning {
  id            String   @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  settlementId  String   @map("settlement_id") @db.Uuid
  creatorUserId String   @map("creator_user_id") @db.Uuid
  role          String   @db.VarChar(20) // InstructorRole/HostRole enum string, snapshot
  itemType      String   @map("item_type") @db.VarChar(20)
  itemId        String   @map("item_id") @db.Uuid
  itemTitle     String   @map("item_title")
  currency      String   @default("SAR") @db.VarChar(3)
  shareFraction Decimal  @map("share_fraction") @db.Decimal(5, 4) // snapshot; source revenueShare is 2dp [DB-1]
  netAmount     Decimal  @map("net_amount") @db.Decimal(10, 2)
  status        String   @default("pending") @db.VarChar(20) // pending|approved|paid|cancelled
  holdReason    String?  @map("hold_reason") @db.VarChar(50)
  payableAt     DateTime @map("payable_at") @db.Timestamptz(6)
  approvedAt    DateTime? @map("approved_at") @db.Timestamptz(6)
  cancelledAt   DateTime? @map("cancelled_at") @db.Timestamptz(6)
  createdAt     DateTime @default(now()) @map("created_at") @db.Timestamptz(6)
  updatedAt     DateTime @updatedAt @map("updated_at") @db.Timestamptz(6)
  settlement    OrderSettlement @relation(fields: [settlementId], references: [id], onDelete: Restrict)

  @@index([status, payableAt]) // maturation hot path [I4]
  @@index([settlementId])      // clawback by source [I2][I4]
  @@index([creatorUserId, status])
  @@map("contributor_earnings")
  @@schema("billing")
}
```

- [ ] **Step 3: Generate the migration DB-free.**

```bash
git show HEAD:apps/experts-app/prisma/schema.prisma > /tmp/old-schema.prisma
MIG_DIR="prisma/migrations/$(date -u +%Y%m%d%H%M%S)_settlement_ledger"
mkdir -p "$MIG_DIR"
pnpm exec prisma migrate diff --from-schema /tmp/old-schema.prisma --to-schema prisma/schema.prisma --script > "$MIG_DIR/migration.sql"
cat "$MIG_DIR/migration.sql"
```

- [ ] **Step 4: Review SQL.** `CREATE TABLE billing.order_settlements`; `contributor_earnings` column changes; unique `order_settlement_source_unique`; three `CreatorEarning` indexes. No `CONCURRENTLY`. FK `ON DELETE RESTRICT`. (Empty table → `ACCESS EXCLUSIVE` lock is contention-free.)
- [ ] **Step 5:** `pnpm db:generate && pnpm db:check:drift` → in sync.
- [ ] **Step 6: Commit.** `git commit -m "feat(settlement): OrderSettlement + CreatorEarning ledger models (restrict, indexes) (refs #936)"`

---

## Phase 2 — Pure settlement compute

### Task 2.1: Contributor resolver (partial-null safe `[DB-1]`)

**Files:** Create `src/lib/settlement/contributors.ts` + test. Real role enums: course primary = `"primary"` (`InstructorRole`); (events later use `"host"`). Generic for reuse.

- [ ] **Step 1: Failing test** — valid shares pass through; **all-null** → fallback to 100% primary; **partial-null** (one share set, one null) → ALSO fallback BUT the caller is told (return a `usedFallback` signal or the resolver throws a typed marker — see impl); no contributors → throws.

```ts
import {describe, expect, it} from 'vitest'
import {resolveContributorShares, type ContributorRow} from '../contributors'

describe('resolveContributorShares', () => {
    it('passes through valid shares summing to 1', () => {
        expect(
            resolveContributorShares(
                [
                    {userId: 'a', role: 'primary', revenueShare: 0.6},
                    {userId: 'b', role: 'co_instructor', revenueShare: 0.4}
                ],
                'primary'
            )
        ).toEqual({
            usedFallback: false,
            shares: [
                {creatorUserId: 'a', role: 'primary', shareFraction: 0.6},
                {creatorUserId: 'b', role: 'co_instructor', shareFraction: 0.4}
            ]
        })
    })
    it('[DB-1] flags fallback on PARTIAL-null shares (not silent)', () => {
        const r = resolveContributorShares(
            [
                {userId: 'a', role: 'primary', revenueShare: 0.6},
                {userId: 'b', role: 'co_instructor', revenueShare: null}
            ],
            'primary'
        )
        expect(r.usedFallback).toBe(true)
        expect(r.shares).toEqual([{creatorUserId: 'a', role: 'primary', shareFraction: 1}])
    })
    it('flags fallback on all-null shares', () => {
        const r = resolveContributorShares([{userId: 'a', role: 'primary', revenueShare: null}], 'primary')
        expect(r.usedFallback).toBe(true)
        expect(r.shares).toEqual([{creatorUserId: 'a', role: 'primary', shareFraction: 1}])
    })
    it('throws when there are no contributors', () => {
        expect(() => resolveContributorShares([], 'primary')).toThrow(/no contributors/i)
    })
})
```

- [ ] **Step 2: Run — FAIL. Step 3: Implement.**

```ts
// src/lib/settlement/contributors.ts
export type ContributorRow = {userId: string; role: string; revenueShare: number | null}
export type ResolvedShare = {creatorUserId: string; role: string; shareFraction: number}
export type ContributorResolution = {shares: ResolvedShare[]; usedFallback: boolean}

const SUM_TOLERANCE = 0.0001

/** Resolve contributor rows into shares of the instructor pool. revenueShare sums
 *  to 1 at publish; if ANY share is null or the set doesn't sum to 1 (incl. the
 *  partial-null case [DB-1]), fall back to 100% to the primary role and set
 *  usedFallback so the caller can observe a warning — never silent. */
export function resolveContributorShares(rows: ContributorRow[], primaryRole: string): ContributorResolution {
    if (rows.length === 0) throw new Error('Settlement: no contributors for content')
    const allHaveShares = rows.every((r) => typeof r.revenueShare === 'number')
    const sum = rows.reduce((acc, r) => acc + (r.revenueShare ?? 0), 0)
    if (allHaveShares && Math.abs(sum - 1) <= SUM_TOLERANCE) {
        return {
            usedFallback: false,
            shares: rows.map((r) => ({creatorUserId: r.userId, role: r.role, shareFraction: r.revenueShare as number}))
        }
    }
    const primary = rows.find((r) => r.role === primaryRole) ?? rows[0]
    return {usedFallback: true, shares: [{creatorUserId: primary.userId, role: primary.role, shareFraction: 1}]}
}
```

- [ ] **Step 4: Run — PASS. Step 5: Commit.** `git commit -m "feat(settlement): contributor resolver, partial-null safe with fallback signal (refs #936)"`

### Task 2.2: Earning allocator

**Files:** Create `src/lib/settlement/allocate-earnings.ts` + test. (Unchanged from prior round.)

- [ ] **Step 1: Failing test** — split by share, exact sum, largest line absorbs rounding drift; sole-contributor full line. (Use `co_instructor`/`contributor` roles.)
- [ ] **Step 2–3: Implement.**

```ts
// src/lib/settlement/allocate-earnings.ts
import type {ResolvedShare} from './contributors'
export type EarningLine = ResolvedShare & {netAmount: number}
const round2 = (v: number) => Math.round(v * 100) / 100
export function allocateEarnings(input: {instructorEarning: number; shares: ResolvedShare[]}): EarningLine[] {
    const {instructorEarning, shares} = input
    const lines: EarningLine[] = shares.map((s) => ({...s, netAmount: round2(instructorEarning * s.shareFraction)}))
    const allocated = round2(lines.reduce((sum, l) => sum + l.netAmount, 0))
    const drift = round2(instructorEarning - allocated)
    if (drift !== 0 && lines.length > 0) {
        const largest = lines.reduce((a, b) => (b.shareFraction > a.shareFraction ? b : a))
        largest.netAmount = round2(largest.netAmount + drift)
    }
    return lines
}
```

- [ ] **Step 4–5: Run + commit.** `git commit -m "feat(settlement): earning allocator with exact rounding (refs #936)"`

### Task 2.3: Affiliate metadata adapter `[B1]`

**Files:** Create `src/lib/settlement/affiliate-metadata.ts` + test.

- [ ] **Step 1: Failing test** — null/0 → null; positive → `{commissionType:"fixed", commissionValue, fundedBy:"INSTRUCTOR"}`; assert `priceOrder` nets it once (without.instructorEarning − with = amount).
- [ ] **Step 2–3: Implement.**

```ts
// src/lib/settlement/affiliate-metadata.ts
import type {AffiliateMetadata} from '@/lib/orders/price-order'
export function toInstructorFundedAffiliate(commissionAmount: number | null): AffiliateMetadata | null {
    if (!commissionAmount || commissionAmount <= 0) return null
    return {commissionType: 'fixed', commissionValue: commissionAmount, fundedBy: 'INSTRUCTOR'}
}
```

> Confirm `AffiliateMetadata`/`CommissionType` are exported from `price-order.ts`; if not, export the types (no behavior change).

- [ ] **Step 4–5: Run + commit.** `git commit -m "feat(settlement): fixed instructor-funded affiliate adapter (refs #936)"`

---

## Phase 3 — Settlement writer (course, inline-callable)

### Task 3.1: `recordOrderSettlement`

**Files:** Create `src/lib/settlement/record-settlement.ts` + unit test + a **real-DB integration test** `[R3]`. Folds: `[B6]` status gate, `[B8]` P2002-as-success, `[I3]` negative→platform-only, `[DB-1]` fallback observe, `[R3]` commission excludes `paid`.

- [ ] **Step 1: Failing unit tests** (prisma mocked). Note the **P2002 test must construct a real `Prisma.PrismaClientKnownRequestError`** `[R3]`, and the commission filter is `notIn:["cancelled","paid"]` `[R3]`.

```ts
import {beforeEach, describe, expect, it, vi} from 'vitest'
import {Prisma} from '@/generated/prisma/client'
const mocks = vi.hoisted(() => ({
    prisma: {
        courseEnrollment: {findUnique: vi.fn()},
        course: {findUnique: vi.fn()},
        commission: {findFirst: vi.fn()},
        orderSettlement: {findUnique: vi.fn(), create: vi.fn()},
        $transaction: vi.fn()
    },
    observe: vi.fn(),
    flag: vi.fn()
}))
vi.mock('@/lib/prisma', () => ({default: mocks.prisma, prisma: mocks.prisma}))
vi.mock('@/lib/observability', () => ({observe: (...a: unknown[]) => mocks.observe(...a)}))
vi.mock('@/lib/settlement/settlement-flag', () => ({isSettlementLedgerEnabled: () => mocks.flag()}))
import {recordOrderSettlement} from '../record-settlement'

const completed = {id: 'enr-1', userId: 'buyer-1', courseId: 'course-1', amountPaid: 115, status: 'completed', completedAt: new Date()}
const course = {id: 'course-1', title: 'Intro', instructors: [{userId: 'creator-1', role: 'primary', revenueShare: 1}]}
beforeEach(() => {
    vi.clearAllMocks()
    mocks.flag.mockReturnValue(true)
    mocks.prisma.$transaction.mockImplementation(async (fn: (tx: unknown) => unknown) => fn(mocks.prisma))
    mocks.prisma.orderSettlement.findUnique.mockResolvedValue(null)
    mocks.prisma.orderSettlement.create.mockResolvedValue({id: 'settle-1'})
    mocks.prisma.commission.findFirst.mockResolvedValue(null)
    mocks.prisma.courseEnrollment.findUnique.mockResolvedValue(completed)
    mocks.prisma.course.findUnique.mockResolvedValue(course)
})

it('[D-8] no-ops entirely when the flag is off', async () => {
    mocks.flag.mockReturnValue(false)
    await recordOrderSettlement({sourceType: 'course', sourceId: 'enr-1'})
    expect(mocks.prisma.orderSettlement.findUnique).not.toHaveBeenCalled()
})
it('[B8] idempotent: no-op when a settlement exists', async () => {
    mocks.prisma.orderSettlement.findUnique.mockResolvedValueOnce({id: 'existing'})
    await recordOrderSettlement({sourceType: 'course', sourceId: 'enr-1'})
    expect(mocks.prisma.orderSettlement.create).not.toHaveBeenCalled()
})
it('[B6] skips a non-completed (refunded) source', async () => {
    mocks.prisma.courseEnrollment.findUnique.mockResolvedValue({...completed, status: 'refunded'})
    await recordOrderSettlement({sourceType: 'course', sourceId: 'enr-1'})
    expect(mocks.prisma.orderSettlement.create).not.toHaveBeenCalled()
})
it('writes settlement + one full line for a single instructor', async () => {
    await recordOrderSettlement({sourceType: 'course', sourceId: 'enr-1'})
    const data = mocks.prisma.orderSettlement.create.mock.calls[0][0].data
    expect(data).toMatchObject({sourceType: 'course', sourceId: 'enr-1', buyerUserId: 'buyer-1', grossPaid: 115, status: 'recorded'})
    expect(data.lines.create).toHaveLength(1)
    expect(Number(data.lines.create[0].netAmount)).toBeCloseTo(Number(data.instructorNetTotal), 2)
})
it('[B8] treats a real P2002 as success', async () => {
    const p2002 = new Prisma.PrismaClientKnownRequestError('unique', {code: 'P2002', clientVersion: '7.8.0'})
    mocks.prisma.$transaction.mockRejectedValueOnce(p2002)
    await expect(recordOrderSettlement({sourceType: 'course', sourceId: 'enr-1'})).resolves.toBeUndefined()
})
it('[I3] platform-only (zero lines) when affiliate exceeds the instructor share', async () => {
    mocks.prisma.commission.findFirst.mockResolvedValue({commissionAmount: 200})
    await recordOrderSettlement({sourceType: 'course', sourceId: 'enr-1'})
    const data = mocks.prisma.orderSettlement.create.mock.calls[0][0].data
    expect(data.instructorNetTotal).toBe(0)
    expect(data.lines?.create ?? []).toHaveLength(0)
})
it('[R3] does NOT re-deduct a commission already paid out', async () => {
    await recordOrderSettlement({sourceType: 'course', sourceId: 'enr-1'})
    const where = mocks.prisma.commission.findFirst.mock.calls[0][0].where
    expect(where.status).toEqual({notIn: ['cancelled', 'paid']})
})
```

- [ ] **Step 2: Run — FAIL. Step 3: Implement.**

```ts
// src/lib/settlement/record-settlement.ts
import {Prisma} from '@/generated/prisma/client'
import prisma from '@/lib/prisma'
import {observe} from '@/lib/observability'
import {priceOrder} from '@/lib/orders/price-order'
import {DEFAULT_INSTRUCTOR_SPLIT_FRACTION, DEFAULT_GATEWAY_FEE_FRACTION} from '@/lib/pricing/settlement-config'
import {calculatePayableDate} from '@/modules/revenue/revenue.service'
import {resolveContributorShares, type ContributorRow} from './contributors'
import {allocateEarnings} from './allocate-earnings'
import {toInstructorFundedAffiliate} from './affiliate-metadata'
import {isSettlementLedgerEnabled} from './settlement-flag'

const VAT_RATE = 0.15
export type SettlementSourceType = 'course' // v1: courses only [D-9]; widen in the Events / Subscriptions phases

type OrderFacts = {
    buyerUserId: string
    itemId: string
    itemTitle: string
    grossPaid: number
    payableAt: Date
    contributors: ContributorRow[]
    primaryRole: string
}

async function resolveCourseFacts(enrollmentId: string): Promise<OrderFacts | null> {
    const e = await prisma.courseEnrollment.findUnique({where: {id: enrollmentId}})
    if (!e || e.status !== 'completed' || e.amountPaid == null) return null // [B6]
    const course = await prisma.course.findUnique({
        where: {id: e.courseId},
        include: {instructors: {select: {userId: true, role: true, revenueShare: true}}}
    })
    if (!course) return null
    return {
        buyerUserId: e.userId,
        itemId: e.courseId,
        itemTitle: course.title,
        grossPaid: Number(e.amountPaid),
        payableAt: calculatePayableDate(e.completedAt ?? new Date()),
        contributors: course.instructors.map((i) => ({
            userId: i.userId,
            role: i.role,
            revenueShare: i.revenueShare == null ? null : Number(i.revenueShare)
        })),
        primaryRole: 'primary'
    }
}

export async function recordOrderSettlement(input: {sourceType: SettlementSourceType; sourceId: string}): Promise<void> {
    if (!isSettlementLedgerEnabled()) return // [D-8] kill switch — accrues nothing until flipped
    const {sourceType, sourceId} = input

    const existing = await prisma.orderSettlement.findUnique({
        where: {order_settlement_source_unique: {sourceType, sourceId}},
        select: {id: true}
    })
    if (existing) {
        observe('settlement.skip.exists', {sourceType, sourceId}, {level: 'debug'})
        return
    }

    const facts = await resolveCourseFacts(sourceId)
    if (!facts) {
        observe('settlement.skip.no_facts', {sourceType, sourceId}, {level: 'warn'})
        return
    }
    if (facts.grossPaid <= 0) {
        observe('settlement.skip.free', {sourceType, sourceId}, {level: 'debug'})
        return
    }

    // [R3] exclude already-PAID commissions: a late reconcile must not re-deduct a
    // commission whose money already left via the affiliate payout.
    const commission = await prisma.commission.findFirst({
        where: {userId: facts.buyerUserId, itemType: sourceType, itemId: facts.itemId, status: {notIn: ['cancelled', 'paid']}},
        select: {commissionAmount: true}
    })
    const breakdown = priceOrder({
        grossPaid: facts.grossPaid,
        vatRate: VAT_RATE,
        instructorSplitFraction: DEFAULT_INSTRUCTOR_SPLIT_FRACTION,
        gatewayFeeFraction: DEFAULT_GATEWAY_FEE_FRACTION,
        affiliate: toInstructorFundedAffiliate(commission ? Number(commission.commissionAmount) : 0)
    })

    let lines: {creatorUserId: string; role: string; shareFraction: number; netAmount: number}[] = []
    if (breakdown.instructorEarning > 0) {
        const {shares, usedFallback} = resolveContributorShares(facts.contributors, facts.primaryRole)
        if (usedFallback && facts.contributors.length > 1) {
            observe(
                'settlement.shares.fallback_primary',
                {sourceType, sourceId, itemId: facts.itemId},
                {level: 'warn', dedupeKey: `settlement.shares.fallback:${sourceType}:${sourceId}`}
            )
        }
        lines = allocateEarnings({instructorEarning: breakdown.instructorEarning, shares})
    } else {
        observe(
            'settlement.instructor_net_nonpositive',
            {sourceType, sourceId, instructorEarning: breakdown.instructorEarning},
            {level: 'warn', dedupeKey: `settlement.nonpositive:${sourceType}:${sourceId}`}
        )
    }
    const instructorNetTotal = lines.reduce((s, l) => s + l.netAmount, 0)

    try {
        await prisma.$transaction(async (tx) => {
            await tx.orderSettlement.create({
                data: {
                    sourceType,
                    sourceId,
                    buyerUserId: facts.buyerUserId,
                    itemType: sourceType,
                    itemId: facts.itemId,
                    itemTitle: facts.itemTitle,
                    currency: 'SAR',
                    grossPaid: facts.grossPaid,
                    vatRate: VAT_RATE,
                    vatAmount: breakdown.vatAmount,
                    netExVat: breakdown.netExVat,
                    gatewayFee: breakdown.gatewayFee,
                    gatewayFeeFraction: DEFAULT_GATEWAY_FEE_FRACTION,
                    distributable: breakdown.distributable,
                    splitFraction: DEFAULT_INSTRUCTOR_SPLIT_FRACTION,
                    platformShare: breakdown.platformShare,
                    instructorShare: breakdown.instructorShare,
                    affiliatePayout: breakdown.affiliatePayout,
                    discountInstructorCost: breakdown.discountCostInstructor,
                    platformEarning: breakdown.platformEarning,
                    instructorNetTotal,
                    status: 'recorded',
                    lines: {
                        create: lines.map((l) => ({
                            creatorUserId: l.creatorUserId,
                            role: l.role,
                            itemType: sourceType,
                            itemId: facts.itemId,
                            itemTitle: facts.itemTitle,
                            currency: 'SAR',
                            shareFraction: l.shareFraction,
                            netAmount: l.netAmount,
                            status: 'pending',
                            payableAt: facts.payableAt
                        }))
                    }
                }
            })
        })
    } catch (err) {
        if (err instanceof Prisma.PrismaClientKnownRequestError && err.code === 'P2002') {
            observe('settlement.race.p2002', {sourceType, sourceId}, {level: 'debug'})
            return
        } // [B8]
        throw err
    }
    observe(
        'settlement.recorded',
        {sourceType, sourceId, itemId: facts.itemId, lines: lines.length, instructorNet: instructorNetTotal},
        {level: 'info', dedupeKey: `settlement.recorded:${sourceType}:${sourceId}`}
    )
}
```

> `tx.orderSettlement` types resolve after `pnpm db:generate` — no cast needed `[R3]`. Confirm `Course.instructors` relation name + the `Prisma` import path (`@/generated/prisma/client`, as in `invoice-create.handler.ts`).

- [ ] **Step 4: Run — PASS.**
- [ ] **Step 5: Real-DB integration test `[R3]`.** Create `src/lib/settlement/__tests__/record-settlement.integration.test.ts` that, with `SETTLEMENT_LEDGER_ENABLED=true` and the real `experts_test` DB, seeds a course + instructor + completed paid enrollment, calls `recordOrderSettlement`, and asserts an `order_settlements` row + one `contributor_earnings` line exist with the right amounts. This catches schema/field drift the mocks hide (how `Event.endDate` slipped in round 2). Gate it to run only when the test DB is reachable.
- [ ] **Step 6: Commit.** `git commit -m "feat(settlement): recordOrderSettlement (course, flag-gated, paid-excluded, P2002-safe) + integration test (refs #936)"`

---

## Phase 4 — Thread enrollment id + inline settle (flag-gated)

### Task 4.1: Expose `enrollmentId` from the completion handler `[B3]`

**Files:** Modify `src/lib/courses/enrollments/handlers/course-enrollment-complete.handler.ts`. `PendingInvoiceContext` exposes `{courseTitle, coursePrice, businessEntityId, courseId}` — not the enrollment id. The handler already `select`s `enrollment.id`; add `enrollmentId: string` to the context and populate it.

- [ ] **Step 1:** add `enrollmentId` to `PendingInvoiceContext`; set from `enrollment.id`. Extend the handler test to assert it.
- [ ] **Step 2: Run + commit.** `git commit -m "refactor(settlement): expose enrollmentId from course completion handler (refs #936)"`

### Task 4.2: Inline fault-isolated settle in the orchestrator `[B5]`

**Files:** Modify `src/lib/courses/enrollments/orchestrators/course-enrollment-complete.orchestrator.ts`. **Read it fully first.** After `await enqueueInvoiceZatca(invoice.id, command.requestId);`:

```ts
// #936 [B5][D-8]: settle inline (request context — Prisma available, no worker),
// fault-isolated (a settlement failure must not fail the already-enrolled buyer);
// the reconciliation sweep backfills any miss. The writer itself no-ops when the
// SETTLEMENT_LEDGER_ENABLED flag is off.
try {
    await recordOrderSettlement({sourceType: 'course', sourceId: completionResult.pendingInvoice.enrollmentId})
} catch (err) {
    observe(
        'settlement.inline.failed',
        {
            sourceType: 'course',
            enrollmentId: completionResult.pendingInvoice.enrollmentId,
            error: err instanceof Error ? err.message : String(err)
        },
        {level: 'error', dedupeKey: `settlement.inline.failed:course:${completionResult.pendingInvoice.enrollmentId}`}
    )
}
```

Add `import {recordOrderSettlement} from "@/lib/settlement/record-settlement";`.

- [ ] **Step 1:** apply the change.
- [ ] **Step 2:** extend the orchestrator test — assert `recordOrderSettlement` is called with `{sourceType:"course", sourceId: enrollmentId}` on a paid completion, and that mocking it to reject once still returns success (fault isolation). Mock `@/lib/settlement/record-settlement`.
- [ ] **Step 3: Run.** `... vitest run src/lib/courses/enrollments` → PASS.
- [ ] **Step 4: Commit.** `git commit -m "feat(settlement): inline fault-isolated settle on course completion (refs #936)"`

---

## Phase 5 — Reconciliation sweep + internal routes

### Task 5.1: Bounded sweep `[B9]`

**Files:** Create `src/lib/settlement/reconcile-settlements.ts` + test. Bounded `NOT EXISTS` anti-join (the `@@unique([sourceType, sourceId])` index serves it). **Test mocks `$queryRaw`, not model methods** `[R3]`.

- [ ] **Step 1: Failing test** — mock `prisma.$queryRaw` returning id rows; assert `recordOrderSettlement` called per id; per-row failure counted.

```ts
import {beforeEach, describe, expect, it, vi} from 'vitest'
const mocks = vi.hoisted(() => ({prisma: {$queryRaw: vi.fn()}, record: vi.fn(), observe: vi.fn()}))
vi.mock('@/lib/prisma', () => ({default: mocks.prisma, prisma: mocks.prisma}))
vi.mock('@/lib/settlement/record-settlement', () => ({recordOrderSettlement: (...a: unknown[]) => mocks.record(...a)}))
vi.mock('@/lib/observability', () => ({observe: (...a: unknown[]) => mocks.observe(...a)}))
import {runSettlementReconciliationSweep} from '../reconcile-settlements'

beforeEach(() => vi.clearAllMocks())
it('[B9] settles completed paid course sales lacking a settlement, bounded', async () => {
    mocks.prisma.$queryRaw.mockResolvedValueOnce([{id: 'enr-9'}, {id: 'enr-10'}])
    const res = await runSettlementReconciliationSweep({limit: 100})
    expect(mocks.record).toHaveBeenCalledWith({sourceType: 'course', sourceId: 'enr-9'})
    expect(res.settled).toBe(2)
})
it('counts per-row failures without aborting the sweep', async () => {
    mocks.prisma.$queryRaw.mockResolvedValueOnce([{id: 'enr-1'}, {id: 'enr-2'}])
    mocks.record.mockRejectedValueOnce(new Error('boom'))
    const res = await runSettlementReconciliationSweep({limit: 100})
    expect(res.settled).toBe(1)
    expect(res.failed).toBe(1)
})
```

- [ ] **Step 2: Run — FAIL. Step 3: Implement** (course only).

```ts
// src/lib/settlement/reconcile-settlements.ts
import prisma from '@/lib/prisma'
import {observe} from '@/lib/observability'
import {recordOrderSettlement} from './record-settlement'

export async function runSettlementReconciliationSweep(opts: {limit?: number} = {}) {
    const limit = opts.limit ?? 500
    const rows = await prisma.$queryRaw<{id: string}[]>`
    SELECT e.id FROM "public"."course_enrollments" e
    WHERE e.status = 'completed' AND e.amount_paid > 0
      AND NOT EXISTS (SELECT 1 FROM "billing"."order_settlements" s WHERE s.source_type = 'course' AND s.source_id = e.id)
    LIMIT ${limit}`
    let settled = 0,
        failed = 0
    for (const {id} of rows) {
        try {
            await recordOrderSettlement({sourceType: 'course', sourceId: id})
            settled++
        } catch (e) {
            failed++
            observe('settlement.reconcile.row_failed', {id, error: e instanceof Error ? e.message : String(e)}, {level: 'error'})
        }
    }
    observe('settlement.reconcile.swept', {settled, failed, limit}, {level: 'info'})
    return {settled, failed}
}
```

> Confirm the real table names (`public.course_enrollments`, `billing.order_settlements`) against the generated migrations. `recordOrderSettlement` already no-ops when the flag is off, so the sweep is a safe no-op until go-live.

- [ ] **Step 4–5: Run + commit.** `git commit -m "feat(settlement): bounded course reconciliation sweep (refs #936)"`

### Task 5.2: Reconcile internal route `[I5]`

**Files:** Create `app/api/v1/internal/settlement/reconcile/route.ts` + test. Verbatim `CRON_SECRET` guard from `app/api/v1/internal/storage-pending-reaper/route.ts`.

- [ ] **Step 1: Implement.**

```ts
import {NextRequest, NextResponse} from 'next/server'
import {getEnvOrSecret} from '@/lib/runtime-secrets'
import {timingSafeCompareCronSecret} from '@/lib/auth/cron-secret'
import {runSettlementReconciliationSweep} from '@/lib/settlement/reconcile-settlements'

export async function POST(request: NextRequest) {
    const cronSecret = getEnvOrSecret('CRON_SECRET', 'cron_secret')
    if (!cronSecret) return NextResponse.json({error: 'Service misconfigured'}, {status: 500})
    if (!timingSafeCompareCronSecret(request.headers.get('authorization') ?? '', `Bearer ${cronSecret}`)) {
        return NextResponse.json({error: 'Forbidden'}, {status: 403})
    }
    const result = await runSettlementReconciliationSweep({limit: 500})
    return NextResponse.json({ok: true, ...result})
}
```

> The sweep already swallows per-row errors and returns counts, so no route-level try/catch is needed (matches the storage-reaper template's shape).

- [ ] **Step 2: Test** — missing secret → 500; wrong bearer → 403; correct → calls sweep, returns counts.
- [ ] **Step 3–4: Run + commit.** `git commit -m "feat(settlement): CRON_SECRET-guarded reconciliation route (refs #936)"`

### Task 5.3: Stats route `[round-2 PM][R3]`

**Files:** Create `app/api/v1/internal/settlement/stats/route.ts` + test. **`POST` + the same `CRON_SECRET` guard** (NOT a GET, NOT `requireAdmin` — internal financial aggregate, must be unambiguous) `[R3 security]`.

- [ ] **Step 1: Implement** a `POST`, `CRON_SECRET`-guarded handler returning `prisma.creatorEarning.groupBy({by:["status"], _count:true, _sum:{netAmount:true}})` + `orderSettlement.groupBy({by:["status"], _count:true})`.
- [ ] **Step 2: Test + commit.** `git commit -m "feat(settlement): stopgap settlement stats route (POST + CRON_SECRET) (refs #936)"`

---

## Phase 6 — Earning maturation + internal route

### Task 6.1: Maturation (two-step `[R3]`)

**Files:** Create `src/lib/settlement/mature-earnings.ts` + test. **Prisma `updateMany` does NOT support relation filters** — use `findMany` (relation filter OK on reads) → bounded `updateMany` by id. Status-guarded `[#956]`.

- [ ] **Step 1: Failing test** — `findMany` returns eligible ids (where `status:"pending"`, `payableAt:{lte:now}`, `settlement:{status:"recorded"}`); then `updateMany({where:{id:{in:ids}, status:"pending"}, data:{status:"approved", approvedAt}})`; empty → no updateMany, returns `{approved:0}`.
- [ ] **Step 2–3: Implement.**

```ts
// src/lib/settlement/mature-earnings.ts
import prisma from '@/lib/prisma'
import {observe} from '@/lib/observability'
import {isSettlementLedgerEnabled} from './settlement-flag'

export async function runCreatorEarningMaturation() {
    if (!isSettlementLedgerEnabled()) return {approved: 0, skipped: 'flag_off'}
    const now = new Date()
    // updateMany can't filter by a relation [R3]; select eligible ids (read supports it), then update by id.
    const eligible = await prisma.creatorEarning.findMany({
        where: {status: 'pending', payableAt: {lte: now}, settlement: {status: 'recorded'}},
        select: {id: true},
        take: 5000
    })
    if (eligible.length === 0) return {approved: 0}
    const res = await prisma.creatorEarning.updateMany({
        where: {id: {in: eligible.map((e) => e.id)}, status: 'pending'}, // status guard closes the TOCTOU [#956]
        data: {status: 'approved', approvedAt: now}
    })
    observe('settlement.earnings.matured', {approved: res.count}, {level: 'info'})
    return {approved: res.count}
}
```

- [ ] **Step 4–5: Run + commit.** `git commit -m "feat(settlement): earning maturation (two-step, status-guarded, flag-gated) (refs #936)"`

### Task 6.2: Maturation internal route

**Files:** Create `app/api/v1/internal/creator-earnings/mature/route.ts` + test. Same `CRON_SECRET` guard as 5.2; `POST` → `runCreatorEarningMaturation()` → `{ok:true, ...result}`. Test 500/403/200. Commit.

---

## Phase 7 — Refund clawback `[I2]`

### Task 7.1: Extend the course refund transaction

**Files:** Modify `src/lib/courses/enrollments/handlers/course-enrollment-refund-process.handler.ts` + test. **Read it first.** Key the clawback on the **settlement** (sourceType, sourceId), not the buyer `[I2]`. (In v1 there is no `payoutId` on earnings, so no payout-linkage case yet — that extension lands in Plan B alongside `CreatorPayout`.)

- [ ] **Step 1: Failing test.** Mock setup MUST include `prisma.orderSettlement.findUnique` returning `{id:"settle-1"}` and `updateMany`, and `prisma.creatorEarning.updateMany` `[R3]`. Assert:

```ts
expect(mocks.prisma.creatorEarning.updateMany).toHaveBeenCalledWith({
    where: {settlementId: 'settle-1', status: {in: ['pending', 'approved']}},
    data: {status: 'cancelled', holdReason: 'purchase_refunded', cancelledAt: expect.any(Date)}
})
expect(mocks.prisma.orderSettlement.updateMany).toHaveBeenCalledWith({
    where: {sourceType: 'course', sourceId: enrollment.id, status: 'recorded'},
    data: {status: 'reversed', reversedAt: expect.any(Date)}
})
```

- [ ] **Step 2: Run — FAIL.**
- [ ] **Step 3: Implement.** Before the existing `prisma.$transaction([...])`, resolve the settlement id and compute the paid-earning loss for observability `[N5/R3]`:

```ts
const settlement = await prisma.orderSettlement.findUnique({
    where: {order_settlement_source_unique: {sourceType: 'course', sourceId: enrollment.id}},
    select: {id: true, lines: {where: {status: 'paid'}, select: {netAmount: true}}}
})
const platformLossAmount = (settlement?.lines ?? []).reduce((s, l) => s + Number(l.netAmount), 0)
```

Then add two ops to the existing array `$transaction` (guarded on `settlement`):

```ts
  ...(settlement ? [
    prisma.creatorEarning.updateMany({
      where: {settlementId: settlement.id, status: {in: ["pending", "approved"]}}, // paid NOT clawed
      data: {status: "cancelled", holdReason: "purchase_refunded", cancelledAt: new Date()},
    }),
    prisma.orderSettlement.updateMany({
      where: {sourceType: "course", sourceId: enrollment.id, status: "recorded"},
      data: {status: "reversed", reversedAt: new Date()},
    }),
  ] : []),
```

Add `cancelledEarnings.count` and `platformLossAmount` to the existing `observe("course.refund.processed", {...})` — `platformLossAmount > 0` means the platform refunded a buyer for money a creator already kept (manual finance review signal) `[N5]`.

- [ ] **Step 4: Run — PASS** (incl. `paid`-not-clawed). **Step 5: Commit.** `git commit -m "feat(settlement): claw back earnings + reverse settlement on course refund, keyed on source (refs #936)"`

---

## Final gate (before PR)

- [ ] **Verification:** `pnpm experts:test`; `pnpm experts:check`; `pnpm db:check:drift` (in sync); the real-DB integration test (Task 3.1 Step 5); the P2002 concurrent test; refund-after-settlement; cron-auth 500/403/200.
- [ ] **Deploy prerequisites (call out in the PR body) `[R3 ops]`:** (a) `SETTLEMENT_LEDGER_ENABLED=false` in all envs — stays **off in prod until Plan B deploys**; (b) wire the two internal cron routes (`/internal/settlement/reconcile`, `/internal/creator-earnings/mature`) into the cron sidecar (`docker/.../cron`, same pattern as storage-janitor) with the `Authorization: Bearer $CRON_SECRET` header; (c) confirm `CRON_SECRET` is set. The crons are safe no-ops while the flag is off.
- [ ] **In-routine reviewer panel** on `git diff origin/main`: `code-reviewer` + `qa-tester` + `security-auditor` (money path) → `release-manager` (GO/NO-GO). Ship via `experts-ship` (PR body: `Refs #936` — does NOT close it).

---

## Deferred to later phases (NOT in this plan)

- **Events** (D-9): event settlement + an event refund flow + event clawback ship **together** as the Events phase. The compute layer (contributors resolver with `primaryRole`, allocator) is already generic for reuse.
- **Subscriptions, payouts, `CreatorBalance` view, surfaces** → Plan B.
- **Subscription renewals, self-billing, automated PSP disbursement, discounts (#935/#937)** → see spec §10/§12.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
