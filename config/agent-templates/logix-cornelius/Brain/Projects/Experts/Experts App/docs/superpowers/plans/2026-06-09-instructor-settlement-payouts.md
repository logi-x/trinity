---
title: "2026 06 09 instructor settlement payouts"
date: "2026-06-09"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/plans/2026-06-09-instructor-settlement-payouts.md"
---
# Instructor Settlement Payouts & Surfaces (Plan B) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let creators see what they're owed and request payouts, let admins process those payouts (record-keeping, mirroring affiliates), and record **platform-only** settlements for subscription sales — completing #936.

**Architecture:** Adds the payout layer on top of Plan A's earnings ledger: a `CreatorBalance` DB view aggregates `CreatorEarning` lines; a creator request route links `approved` earnings to a new `CreatorPayout` (amount computed inside the link transaction); an admin process route walks the state machine (`pending`/`processing → completed|failed`, transitions allowed from both non-terminal states) with a #956 status-guarded write. Subscription completion **inline-calls** `recordOrderSettlement` (no queue — Plan A's B5 resolution), recorded platform-only (zero creator lines, platform-funded affiliate). Two surfaces (creator dashboard, admin queue) follow `experts-constellation`. Everything stays gated by `SETTLEMENT_LEDGER_ENABLED`; flipping it on is this plan's go-live step (D-8).

**Tech Stack:** Next.js 16 (App Router) · Prisma 7 (`billing` schema) · Vitest (node env) · HeroUI v3 + admin kit.

**Prerequisite:** **Plan A** (`docs/superpowers/plans/2026-06-09-instructor-settlement-ledger.md`) is merged — `OrderSettlement` + `CreatorEarning` exist and are being written/matured. Spec: `docs/superpowers/specs/2026-06-09-instructor-settlement-design.md`.

**Scope:** Payouts + surfaces + **platform-only** subscription settlement (subscriptions are platform memberships, no creator earns — spec §11). Event refund clawback is **not** here (needs an event refund flow to exist first — verify separately).

**Branch:** `feat/gh-936-settlement-payouts` (off `main` after Plan A lands). The final PR carries `Closes #936`.

---

## Template note (read before Phases 3–6)

The affiliate payout system is the **exact template**. Open these and mirror them, substituting symbols as the tasks specify — do **not** invent route logic from scratch:

- `app/api/v1/commerce/affiliates/payouts/request/route.ts` → creator request route (Task 3.1)
- `app/api/v1/admin/payouts/[id]/process/route.ts` → admin process route (Task 4.1)
- `src/lib/admin/payouts/payout-search.ts` + `AffiliatePayoutDTO` → DTOs + search (Tasks 5–6)
- The affiliate admin payouts page + the affiliate balance/earnings creator surface → the two surfaces (Tasks 5–6)

Run all commands from `apps/experts-app`. Tests need `DATABASE_URL=postgresql://localhost/experts_test`.

---

## File map

| File                                                     | Responsibility                                                                                  | Action           |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ---------------- |
| `prisma/schema.prisma`                                   | `CreatorPayout`, `CreatorPayoutMethod`, `CreatorBalance` view; `CreatorEarning.payout` relation | Modify (Phase 1) |
| `prisma/migrations/<ts>_creator_payouts/migration.sql`   | DDL incl. the view                                                                              | Create (Phase 1) |
| `src/lib/settlement/subscription-settlement.ts`          | Pure platform-only compute                                                                      | Create (Phase 2) |
| `src/lib/settlement/record-settlement.ts`                | Add `subscription` branch (zero lines)                                                          | Modify (Phase 2) |
| `.../subscription-checkout-complete.handler.ts`          | enqueue settlement after ZATCA                                                                  | Modify (Phase 2) |
| `src/lib/creator-payouts/dto.ts`                         | `CreatorPayoutDTO`, `CreatorEarningDTO`, `CreatorBalanceDTO`                                    | Create (Phase 3) |
| `app/api/v1/commerce/creators/payouts/request/route.ts`  | Creator payout request                                                                          | Create (Phase 3) |
| `app/api/v1/commerce/creators/payout-method/route.ts`    | Set/read payout method                                                                          | Create (Phase 3) |
| `app/api/v1/admin/creator-payouts/[id]/process/route.ts` | Admin process                                                                                   | Create (Phase 4) |
| `src/lib/admin/creator-payouts/payout-search.ts`         | Admin search/badge helpers                                                                      | Create (Phase 4) |
| `app/(i18n)/.../creator earnings dashboard`              | Creator surface                                                                                 | Create (Phase 5) |
| `app/(i18n)/_shared/admin/.../creator-payouts`           | Admin surface                                                                                   | Create (Phase 6) |

---

## Phase 1 — Payout data model + balance view

### Task 1.1: Add payout models, method, view, and the earning→payout relation

**Files:** Modify `prisma/schema.prisma`.

- [ ] **Step 1: Add the models** (match surrounding style; never `prisma format`). Mirror `AffiliatePayout` for `CreatorPayout`:

```prisma
model CreatorPayout {
  id            String   @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  creatorUserId String   @map("creator_user_id") @db.Uuid
  amount        Decimal  @db.Decimal(10, 2)
  currency      String   @default("SAR") @db.VarChar(10) // match AffiliatePayout.currency [DB-8]
  method        String   @db.VarChar(40)
  status        String   @default("pending") @db.VarChar(20) // pending|processing|completed|failed
  transactionId String?  @map("transaction_id")
  notes         String?
  processedAt   DateTime? @map("processed_at") @db.Timestamptz(6)
  processedBy   String?  @map("processed_by") @db.Uuid
  periodStart   DateTime @map("period_start") @db.Timestamptz(6)
  periodEnd     DateTime @map("period_end") @db.Timestamptz(6)
  createdAt     DateTime @default(now()) @map("created_at") @db.Timestamptz(6)
  earnings      CreatorEarning[]

  @@index([creatorUserId, status, periodStart])
  @@map("creator_payouts")
  @@schema("billing")
}

model CreatorPayoutMethod {
  creatorUserId String   @id @map("creator_user_id") @db.Uuid
  method        String   @db.VarChar(40) // "bank_transfer" | ...
  bankName      String?  @map("bank_name") @db.VarChar(100)
  accountName   String?  @map("account_name") @db.VarChar(100)
  iban          String?  @db.VarChar(34) // ISO 13616 max [DB-9]
  vatRegistered Boolean  @default(false) @map("vat_registered")
  vatNumber     String?  @map("vat_number") @db.VarChar(20)
  createdAt     DateTime @default(now()) @map("created_at") @db.Timestamptz(6)
  updatedAt     DateTime @updatedAt @map("updated_at") @db.Timestamptz(6)

  @@map("creator_payout_methods")
  @@schema("billing")
}

view CreatorBalance {
  // [DB-2] bare @db.Decimal (no precision) — mirror the existing AffiliateBalance
  // view exactly; Prisma view annotations are advisory and the SUMs return numeric.
  creatorUserId String  @id @map("creator_user_id") @db.Uuid
  totalAmount   Decimal @map("total_amount")
  pendingAmount Decimal @map("pending_amount")
  payableAmount Decimal @map("payable_amount")
  paidAmount    Decimal @map("paid_amount")

  @@map("creator_balances")
  @@schema("billing")
}
```

> **[DB-5] zero-earning creators have NO view row** (the view groups directly on `contributor_earnings`). Every consumer (`creatorBalance.findUnique`) MUST coalesce a `null` result to a zero-balance struct **before** the threshold check, or the payout-request route 500s. Add an explicit "creator with no earnings → 400 below-minimum (not 500)" test. (Do NOT also add a `users` LEFT-JOIN anchor — the coalesce is simpler for a greenfield ledger.)

- [ ] **Step 2: Add the `payoutId` column AND the relation to `CreatorEarning`.** Plan A deliberately did **not** add `payoutId` (two-PR seam — avoids a dangling column the drift gate flags). Add both here together. In the `CreatorEarning` model add:

```prisma
  payoutId      String?  @map("payout_id") @db.Uuid
  payout        CreatorPayout? @relation(fields: [payoutId], references: [id], onDelete: SetNull)
```

Also add `@@index([payoutId])` to `CreatorEarning` (payout linkage + the "clear on failed" sweep).

- [ ] **Step 3: Generate the migration** (same DB-free diff as Plan A Task 1.2 Step 3): produce `prisma/migrations/<ts>_creator_payouts/migration.sql` from `git show HEAD:...schema.prisma` vs the working schema.

- [ ] **Step 4: Author the view SQL by hand.** `prisma migrate diff` will not emit a correct view body — append this to the migration (the view aggregates earning lines; `payable` = `approved` and not yet linked to a payout):

```sql
CREATE OR REPLACE VIEW "billing"."creator_balances" AS
SELECT
  ce."creator_user_id" AS "creator_user_id",
  COALESCE(SUM(ce."net_amount") FILTER (WHERE ce."status" <> 'cancelled'), 0) AS "total_amount",
  COALESCE(SUM(ce."net_amount") FILTER (WHERE ce."status" = 'pending'), 0) AS "pending_amount",
  COALESCE(SUM(ce."net_amount") FILTER (WHERE ce."status" = 'approved' AND ce."payout_id" IS NULL), 0) AS "payable_amount",
  COALESCE(SUM(ce."net_amount") FILTER (WHERE ce."status" = 'paid'), 0) AS "paid_amount"
FROM "billing"."contributor_earnings" ce
GROUP BY ce."creator_user_id";
```

> Compare against the existing `AffiliateBalance` view definition (find it in the migrations history) to match the column-aliasing/quoting conventions exactly.

- [ ] **Step 5: Regenerate client + drift check.**

Run:

```bash
pnpm db:generate
pnpm db:check:drift
```

Expected: in sync. Views can be drift-sensitive — if the drift gate complains about the view, align the schema `view` block's column names/types to the SQL exactly.

- [ ] **Step 6: Commit.**

```bash
git add prisma/schema.prisma prisma/migrations
git commit -m "feat(creator-payouts): payout + method models, balance view, earning relation (refs #936)"
```

---

## Phase 2 — Platform-only subscription settlement

### Task 2.1: Subscription compute (pure)

**Files:** Create `src/lib/settlement/subscription-settlement.ts` + `__tests__/subscription-settlement.test.ts`.

- [ ] **Step 1: Failing test.**

```ts
import {describe, expect, it} from 'vitest'
import {computeSubscriptionSettlement} from '../subscription-settlement'

describe('computeSubscriptionSettlement (platform-only)', () => {
    it('keeps the whole net as platform earning when there is no affiliate', () => {
        const s = computeSubscriptionSettlement({grossPaid: 115, vatRate: 0.15, gatewayFeeFraction: 0.025})
        expect(s.vatAmount).toBeCloseTo(15, 2)
        expect(s.netExVat).toBeCloseTo(100, 2)
        expect(s.gatewayFee).toBeCloseTo(2.875, 2)
        expect(s.distributable).toBeCloseTo(97.125, 2)
        expect(s.platformEarning).toBeCloseTo(97.125, 2)
        expect(s.instructorNetTotal).toBe(0)
    })

    it('funds the affiliate commission from the PLATFORM share (not an instructor)', () => {
        const s = computeSubscriptionSettlement({
            grossPaid: 115,
            vatRate: 0.15,
            gatewayFeeFraction: 0.025,
            affiliateCommissionAmount: 10
        })
        expect(s.affiliatePayout).toBe(10)
        expect(s.platformEarning).toBeCloseTo(87.125, 2) // distributable - affiliate
        expect(s.instructorNetTotal).toBe(0)
    })
})
```

- [ ] **Step 2: Run — verify fail.**
      Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm exec vitest run src/lib/settlement/__tests__/subscription-settlement.test.ts`
      Expected: FAIL.

- [ ] **Step 3: Implement.**

```ts
// src/lib/settlement/subscription-settlement.ts
const round2 = (v: number) => Math.round(v * 100) / 100

export type SubscriptionSettlement = {
    vatAmount: number
    netExVat: number
    gatewayFee: number
    distributable: number
    affiliatePayout: number
    platformShare: number
    platformEarning: number
    instructorNetTotal: number
}

/**
 * Subscriptions are platform memberships (no creator earns). The platform keeps
 * the full net; an affiliate commission is PLATFORM-funded (reduces platformEarning).
 */
export function computeSubscriptionSettlement(input: {
    grossPaid: number
    vatRate: number
    gatewayFeeFraction: number
    affiliateCommissionAmount?: number
}): SubscriptionSettlement {
    const {grossPaid, vatRate, gatewayFeeFraction} = input
    const netExVat = round2(grossPaid / (1 + vatRate))
    const vatAmount = round2(grossPaid - netExVat)
    const gatewayFee = round2(grossPaid * gatewayFeeFraction)
    const distributable = round2(netExVat - gatewayFee)
    const affiliatePayout = round2(input.affiliateCommissionAmount ?? 0)
    return {
        vatAmount,
        netExVat,
        gatewayFee,
        distributable,
        affiliatePayout,
        platformShare: distributable,
        platformEarning: round2(distributable - affiliatePayout),
        instructorNetTotal: 0
    }
}
```

- [ ] **Step 4: Run — verify pass.** Expected: PASS.
- [ ] **Step 5: Commit.**

```bash
git add src/lib/settlement/subscription-settlement.ts src/lib/settlement/__tests__/subscription-settlement.test.ts
git commit -m "feat(settlement): platform-only subscription settlement compute (refs #936)"
```

### Task 2.2: Add the `subscription` branch to the writer

**Files:** Modify `src/lib/settlement/record-settlement.ts` + its test. **Read it first** (Plan A built it).

- [ ] **Step 1: Failing test.** Add to `record-settlement.test.ts`: a subscription source writes an `OrderSettlement` with `instructorNetTotal: 0`, `splitFraction: 0`, and **no lines**.

```ts
it('records a platform-only settlement for a subscription (no creator lines)', async () => {
    mocks.prisma.subscription.findUnique.mockResolvedValue({
        id: 'sub-1',
        userId: 'buyer-1',
        planId: 'plan-1',
        status: 'active' // [B6] gate
    })
    mocks.prisma.plan.findUnique.mockResolvedValue({id: 'plan-1', name: 'Pro'})
    // [B4] Subscription has NO amountPaid column — gross comes from the Invoice.
    mocks.prisma.invoice.findFirst.mockResolvedValue({id: 'inv-1', totalAmount: 115})
    mocks.prisma.commission.findFirst.mockResolvedValue(null)

    await recordOrderSettlement({sourceType: 'subscription', sourceId: 'sub-1'})

    const arg = mocks.prisma.orderSettlement.create.mock.calls[0][0]
    expect(arg.data).toMatchObject({
        sourceType: 'subscription',
        itemType: 'subscription',
        grossPaid: 115,
        instructorNetTotal: 0,
        splitFraction: 0
    })
    expect(arg.data.lines?.create ?? []).toHaveLength(0)
})
```

(Extend the mocked prisma with `subscription.findUnique`, `plan.findUnique`, and `invoice.findFirst`.)

- [ ] **Step 2: Run — verify fail.** Expected: FAIL (subscription rejected/unknown).

- [ ] **Step 3: Implement.** Widen `SettlementSourceType` to include `"subscription"`. Add `resolveSubscriptionFacts(subscriptionId)`:
    - Read the `Subscription` row → `userId`, `planId` (do **NOT** gate on `Subscription.status` — `[R3]` a `paused`/`canceled` sub may still have been paid; the Invoice is the settlement signal, see below). Return null if no row.
    - **[B4]** Subscription has **no `amountPaid`/`currency` column** — source gross from the Invoice: `prisma.invoice.findFirst({where:{contentType:"subscription", contentId: subscriptionId}, select:{totalAmount:true}})` → `grossPaid = Number(invoice.totalAmount)` (inc-VAT gross). Return null if no invoice (nothing to settle yet).
    - Read `Plan` → `name` (the `itemTitle`); `itemId = planId`; `payableAt = calculatePayableDate(now)` (no event end).

    In `recordOrderSettlement`, branch for `subscription`: call `computeSubscriptionSettlement(...)` and write the `OrderSettlement` with `splitFraction: 0`, `instructorShare: 0`, `instructorNetTotal: 0`, **no `lines`**. Keep the idempotency check, affiliate re-query, and **wrap the `create` in the same P2002-as-success try/catch [B8]** the course/event path uses. Confirm the invoice `contentType` value used for subscriptions against `handleInvoiceCreate` (the completion handler maps `source.type:"subscription"` → `contentType`).

```ts
// inside recordOrderSettlement, after the existing/idempotency guard:
if (sourceType === 'subscription') {
    const facts = await resolveSubscriptionFacts(sourceId)
    if (!facts || facts.grossPaid <= 0) {
        observe('settlement.skip.no_facts_or_free', {sourceType, sourceId}, {level: 'warn'})
        return
    }
    // [R3] subscription commission: itemId omitted intentionally — Commission has a
    // partial unique (one subscription commission per user); excludes 'paid' too so a
    // late reconcile can't re-deduct an already-paid commission from platformEarning.
    const commission = await prisma.commission.findFirst({
        where: {userId: facts.buyerUserId, itemType: 'subscription', status: {notIn: ['cancelled', 'paid']}},
        select: {commissionAmount: true}
    })
    const s = computeSubscriptionSettlement({
        grossPaid: facts.grossPaid,
        vatRate: VAT_RATE,
        gatewayFeeFraction: DEFAULT_GATEWAY_FEE_FRACTION,
        affiliateCommissionAmount: commission ? Number(commission.commissionAmount) : 0
    })
    await prisma.orderSettlement.create({
        data: {
            sourceType,
            sourceId,
            buyerUserId: facts.buyerUserId,
            itemType: 'subscription',
            itemId: facts.itemId,
            itemTitle: facts.itemTitle,
            currency: 'SAR',
            grossPaid: facts.grossPaid,
            vatRate: VAT_RATE,
            vatAmount: s.vatAmount,
            netExVat: s.netExVat,
            gatewayFee: s.gatewayFee,
            gatewayFeeFraction: DEFAULT_GATEWAY_FEE_FRACTION,
            distributable: s.distributable,
            splitFraction: 0,
            platformShare: s.platformShare,
            instructorShare: 0,
            affiliatePayout: s.affiliatePayout,
            discountInstructorCost: 0,
            platformEarning: s.platformEarning,
            instructorNetTotal: 0,
            status: 'recorded'
        }
    })
    observe(
        'settlement.recorded',
        {sourceType, sourceId, lines: 0},
        {level: 'info', dedupeKey: `settlement.recorded:subscription:${sourceId}`}
    )
    return
}
```

> Subscription `itemId` = the plan id; `sourceId` = the `Subscription` row id (so idempotency is per subscription purchase). Confirm `Subscription` field names (`amountPaid`, `planId`, `userId`) against the schema.

- [ ] **Step 4: Run — verify pass.** Run the record-settlement suite. Expected: PASS (course/event tests still green).

- [ ] **Step 5: Commit.**

```bash
git add src/lib/settlement/record-settlement.ts src/lib/settlement/__tests__/record-settlement.test.ts
git commit -m "feat(settlement): platform-only subscription branch in the writer (refs #936)"
```

### Task 2.3: Wire subscription completion

**Files:** Modify `src/lib/subscriptions/handlers/subscription-checkout-complete.handler.ts`. **Read it first.**

> **[R3] There is NO `enqueueSettlement`.** Plan A's B5 resolution made settlement an **inline** call to `recordOrderSettlement` (no queue). Mirror Plan A Task 4.2 exactly.

- [ ] **Step 1:** After `await enqueueInvoiceZatca(invoice.id, requestId);`, add the fault-isolated **inline** call, mirroring Plan A Task 4.2:

```ts
import {recordOrderSettlement} from '@/lib/settlement/record-settlement'
// ...after the ZATCA enqueue:
try {
    await recordOrderSettlement({sourceType: 'subscription', sourceId: subscriptionRecordId})
} catch (err) {
    observe(
        'settlement.inline.failed',
        {sourceType: 'subscription', subscriptionId: subscriptionRecordId, error: err instanceof Error ? err.message : String(err)},
        {level: 'error', dedupeKey: `settlement.inline.failed:subscription:${subscriptionRecordId}`}
    )
}
```

(The writer no-ops when `SETTLEMENT_LEDGER_ENABLED` is off, and is idempotent on `(sourceType, sourceId)`.)

- [ ] **Step 2:** Extend the subscription completion test to assert `recordOrderSettlement({sourceType:"subscription", sourceId: subscriptionRecordId})` is called and that mocking it to reject once still returns success. Mock `@/lib/settlement/record-settlement`.
- [ ] **Step 3: Run.** `DATABASE_URL=postgresql://localhost/experts_test pnpm exec vitest run src/lib/subscriptions`. Expected: PASS.
- [ ] **Step 4: Commit.**

```bash
git add src/lib/subscriptions
git commit -m "feat(settlement): inline platform-only settlement on subscription completion (refs #936)"
```

### Task 2.4: Subscription reconciliation backstop `[R3 N3]`

**Files:** Modify `src/lib/settlement/reconcile-settlements.ts` + test. Plan A's sweep is course-only; subscriptions need their own backstop or an inline failure is never backfilled.

- [ ] **Step 1: Failing test** — `$queryRaw` returns subscription ids lacking a settlement; `recordOrderSettlement({sourceType:"subscription", sourceId})` called per id.
- [ ] **Step 2–3: Implement.** Add a second bounded `NOT EXISTS` query (subscription gross proven by an Invoice), and fold its ids into the same per-row loop:

```sql
SELECT s.id FROM "billing"."subscriptions" s
WHERE EXISTS (SELECT 1 FROM "billing"."invoices" i WHERE i.content_type = 'subscription' AND i.content_id = s.id AND i.total_amount > 0)
  AND NOT EXISTS (SELECT 1 FROM "billing"."order_settlements" os WHERE os.source_type = 'subscription' AND os.source_id = s.id)
LIMIT ${limit}
```

- [ ] **Step 4–5: Run + commit.** `git commit -m "feat(settlement): subscription reconciliation backstop (refs #936)"`

---

## Phase 3 — Creator payout request + method

### Task 3.1: DTOs

**Files:** Create `src/lib/creator-payouts/dto.ts`. Mirror `AffiliatePayoutDTO`/`CommissionDTO` shapes (ISO date strings, string-literal status unions). Define `CreatorEarningDTO` (`id, itemType, itemId, itemTitle, netAmount, shareFraction, status, payableAt, approvedAt?`), `CreatorPayoutDTO` (mirror `AffiliatePayoutDTO`, `creator` profile instead of `affiliate`, `earnings: CreatorEarningDTO[]`), `CreatorBalanceDTO` (`total, pending, payable, paid`). Commit.

### Task 3.2: Payout method route

**Files:** Create `app/api/v1/commerce/creators/payout-method/route.ts` + test.

- [ ] **Step 1: Failing test** — `GET` returns the caller's method (or null); `PUT` upserts `CreatorPayoutMethod` for the authed user; unauthenticated → 401; an over-long/garbage IBAN → 400 `[R3 security]`.
- [ ] **Step 2–3:** Implement `GET` + `PUT` with `auth()` (creator session; `creatorUserId = session.user.id` ONLY — no body override), zod `safeParse`, `prisma.creatorPayoutMethod.upsert({where:{creatorUserId}, ...})`. **Explicit zod `[R3]`:** `method: z.enum(["bank_transfer"])`, `iban: z.string().max(34).regex(/^[A-Z]{2}\d{2}[A-Z0-9]{1,30}$/).optional()`, `bankName/accountName: z.string().max(100).optional()`, `vatRegistered: z.boolean()`, `vatNumber: z.string().max(20).optional()`. Generic errors via `safeErrorJson`.
- [ ] **Step 4: Run + commit.** `... pnpm exec vitest run app/api/v1/commerce/creators/payout-method`.

### Task 3.3: Payout request route (mirror affiliate)

**Files:** Create `app/api/v1/commerce/creators/payouts/request/route.ts` + test. **Mirror `affiliates/payouts/request/route.ts`** with these substitutions:

- [ ] **Step 1: Failing test** covering the guard ladder (each returns the right status):
    1. unauthenticated → 401;
    2. no `CreatorPayoutMethod` → 400 ("payment method required");
    3. a creator with **no balance row** (no earnings yet) → coalesce null → 400 "below minimum" (NOT 500) `[DB-5]`;
    4. `CreatorBalance.payableAmount < MINIMUM_CREATOR_PAYOUT_SAR` → 400 ("below minimum");
    5. an existing `CreatorPayout` in `pending` **or `processing`** for this creator → 409 ("payout already in progress") — **[I1]** the guard must cover `processing`, or a second request double-spends in-flight earnings;
    6. happy path → creates `CreatorPayout`, links all `approved`+`payoutId=null` earnings, returns the payout; `amount` equals the SUM of the linked rows (see [R3] below);
    7. unauthenticated → 401, and the creator id is taken ONLY from `session.user.id` (never a body/param — no IDOR) `[R3 security]`.

```ts
it('creates a payout and links approved earnings', async () => {
    // method set, balance payable = 250, no pending payout, 3 approved earnings
    const res = await POST(makeReq())
    expect(res.status).toBe(200)
    expect(mocks.prisma.creatorPayout.create).toHaveBeenCalled()
    expect(mocks.prisma.creatorEarning.updateMany).toHaveBeenCalledWith(
        expect.objectContaining({where: expect.objectContaining({creatorUserId: 'creator-1', status: 'approved', payoutId: null})})
    )
})
```

- [ ] **Step 2–3: Implement** by mirroring the affiliate request route, substituting: `affiliate`→creator (`session.user.id` only); `AffiliateBalance`→`CreatorBalance`; `Commission`→`CreatorEarning`; `AffiliatePayout`→`CreatorPayout`. Threshold = `MINIMUM_CREATOR_PAYOUT_SAR` (a named constant in `settlement-config.ts`, default `100` `[R3]`, NOT a magic literal). In-progress guard `status: {in: ["pending", "processing"]}` **[I1]**.

    **[R3 — amount race]** Do NOT set `amount = balance.payableAmount` (a stale read taken before the link). Inside ONE `prisma.$transaction`: (1) `findMany` the eligible earnings (`{creatorUserId, status:"approved", payoutId:null}`, `select:{id,netAmount}`); (2) if empty → 400; (3) `amount = Σ netAmount` of THOSE rows; (4) `creatorPayout.create({amount, ...})`; (5) `creatorEarning.updateMany({where:{id:{in: ids}}, data:{payoutId: payout.id}})`. This guarantees `CreatorPayout.amount` always equals the sum of its linked lines, even if maturation/clawback runs concurrently. (The `balance.payableAmount` read stays only for the pre-transaction threshold gate.)

    **[R3 — no info leak]** Do NOT mirror the affiliate template's `details` debug object in the no-earnings 400 response (it leaks pending/approved counts + the balance-vs-raw reconciliation). Return a plain user-facing message.

- [ ] **Step 4: Run + commit.** `... pnpm exec vitest run app/api/v1/commerce/creators/payouts`.

---

## Phase 4 — Admin payout process

### Task 4.1: Admin process route (mirror affiliate, #956 guard)

**Files:** Create `app/api/v1/admin/creator-payouts/[id]/process/route.ts` + test. **Mirror `admin/payouts/[id]/process/route.ts`.**

- [ ] **Step 1: Failing test:**
    1. non-admin → 401/403;
    2. **[R3 N1] transitions are allowed from `{pending, processing}`** (NOT pending-only — else a payout stuck in `processing` can never reach `completed`/`failed` and strands its earnings). A payout already `completed`/`failed` → 400 (terminal, no re-process);
    3. `processing → completed` and `pending → completed` both work: mark completed (`processedAt/By`, `transactionId`, `notes`) **and** flip linked earnings to `paid` in one transaction;
    4. `processing → failed` and `pending → failed` both clear `payoutId` (I1);
    5. **double-process guard:** the payout status write is status-guarded `updateMany({where:{id, status:{in:["pending","processing"]}}})` (the #956 lesson) — a second concurrent call matching 0 rows returns 409, no double-pay.

```ts
it('completes a payout and marks its earnings paid, guarded against double-process', async () => {
    // payout status pending; admin marks completed
    const res = await POST(makeReq({status: 'completed', transactionId: 'txn-1'}), {params})
    expect(res.status).toBe(200)
    expect(mocks.prisma.creatorEarning.updateMany).toHaveBeenCalledWith(
        expect.objectContaining({
            where: expect.objectContaining({payoutId: 'payout-1', status: 'approved'}),
            data: expect.objectContaining({status: 'paid'})
        })
    )
})
```

- [ ] **Step 2–3: Implement** mirroring the affiliate process route, substituting `AffiliatePayout`→`CreatorPayout`, `Commission`→`CreatorEarning`. `requireAdmin()` first. Apply the **#956** discipline: the payout transition uses `updateMany({where:{id, status:{in:["pending","processing"]}}})` and returns 409 on `count===0` **[R3 N1]**. In the **same transaction**, branch on the target status:
    - `completed` → flip linked earnings (`where:{payoutId:id, status:"approved"}`) to `paid`. **[R3]** also compute `Σ netAmount` of the linked rows and, if it diverges from `payout.amount` by > 0.01 SAR, emit a `warn` observation (do not reject — admin may have adjusted) — an audit signal, not a block.
    - **`failed` [I1]** → **clear** `payoutId` on the linked earnings and leave them `approved`: `creatorEarning.updateMany({where:{payoutId:id}, data:{payoutId:null}})`. Otherwise those lines satisfy neither `payable` (`payout_id IS NULL`) nor `paid` — stranded.
    - `processing` (from `pending`) → just set status; linkage intact.
- [ ] **Step 3b: Failed-from-processing test** — `processing → failed` clears `payoutId` and leaves earnings `approved` (back to `payable`). Plus a `processing → completed` test.
- [ ] **Step 4: Run + commit.** `... pnpm exec vitest run app/api/v1/admin/creator-payouts`.

### Task 4.1b: Extend the course refund clawback to cancel a linked pending payout `[R3 — missing flow]`

**Files:** Modify `src/lib/courses/enrollments/handlers/course-enrollment-refund-process.handler.ts` + test. Plan A's Phase-7 clawback cancels earnings keyed on the settlement — but Plan A had no `payoutId`. Now that earnings can be linked to a `CreatorPayout`, a refund that cancels an `approved` earning **already linked to a pending/processing payout** corrupts that payout (its `amount` no longer matches its now-cancelled lines, and an admin could pay against nothing).

- [ ] **Step 1: Failing test** — an `approved` earning linked to a `pending` `CreatorPayout` is refunded → the earning is `cancelled` AND its `CreatorPayout` is `cancelled` (or `failed` with a reason) and its OTHER still-valid linked earnings have `payoutId` cleared (returned to `payable`).
- [ ] **Step 2–3: Implement.** In the refund clawback (extending Plan A Phase 7), after resolving the settlement, find any `pending`/`processing` `CreatorPayout` ids referenced by the earnings being cancelled; in the same transaction: set those payouts to `cancelled` (`notes: "refund_cancellation"`) and clear `payoutId` on all their earnings that are NOT being cancelled (so unaffected earnings return to `payable`). Guard the payout status write with `status:{in:["pending","processing"]}`.
- [ ] **Step 4: Run + commit.** `git commit -m "feat(settlement): refund clawback cancels a linked pending creator payout (refs #936)"`

### Task 4.2: Admin search/badge helpers

**Files:** Create `src/lib/admin/creator-payouts/payout-search.ts` mirroring `src/lib/admin/payouts/payout-search.ts` (status→badge map; client-side `matchesPayoutSearch` over creator name/email/method/status/transactionId/amount, typed on `CreatorPayoutDTO`). Unit-test the pure helpers. Commit.

---

## Phase 5 — Creator earnings dashboard (per experts-constellation)

### Task 5.1: Read DTO + query + route

**Files:** `src/lib/creator-payouts/queries/creator-earnings.query.ts`, `app/api/v1/commerce/creators/earnings/route.ts` (+ tests).

- [ ] **Step 1:** Query returns `{balance: CreatorBalanceDTO, earnings: CreatorEarningDTO[], hasPayoutMethod: boolean, pendingPayout: CreatorPayoutDTO | null}` for the authed creator (`CreatorBalance.findUnique` + recent `CreatorEarning.findMany` + method existence + any pending payout). Route: `auth()` (creator), call query, `NextResponse.json`. Test the query mapping + the route auth.
- [ ] **Step 2: Run + commit.**

### Task 5.2: Dashboard component

**Files:** the creator earnings page under `app/(i18n)/...` (+ `renderToStaticMarkup` tests). Full vertical slice per `experts-constellation`:

- [ ] **Step 1:** `StatCard`s (pending / payable / paid from `CreatorBalanceDTO`, skeleton-gated on `isAwaitingFirstData`), a `DataTable` of earnings (status badges; **surface the per-order `affiliatePayout`/deduction so a creator understands why net < gross split** `[R3]`), a **Request payout** button (disabled unless `hasPayoutMethod && balance.payable >= MINIMUM_CREATOR_PAYOUT_SAR && !pendingPayout`, with a tooltip explaining why), and the `CreatorPayoutMethod` form. Four states; RTL/i18n (en+ar+es); a11y; numbers `dir="ltr"`. Use `useApiQuery` + `jsonFetcher`.
- [ ] **Step 2:** Tests via `renderToStaticMarkup` with HeroUI/next-intl/`useIsRTL` mocked; assert the gate logic (button disabled states) via an extracted pure `canRequestPayout(balance, hasMethod, pendingPayout)` helper unit-tested directly.
- [ ] **Step 3: Run + commit.** Validate all three locale JSONs parse.

---

## Phase 6 — Admin creator-payouts queue (per experts-constellation)

### Task 6.1: Admin DTO + query + route

**Files:** `src/lib/admin/creator-payouts/queries/...`, `app/api/v1/admin/creator-payouts/route.ts` (+ tests).

- [ ] **Step 1:** Admin list query (paginated, `buildAdminSearch` over creator name/email/method/status) returning `CreatorPayoutDTO[]` with linked earnings + counts. Route enforces `requireAdmin()`, zod-validates query params. Test auth + search composition.
- [ ] **Step 2: Run + commit.**

### Task 6.2: Admin queue surface

**Files:** the admin creator-payouts page under `app/(i18n)/_shared/admin/...` (+ tests). **Mirror the affiliate admin payouts page**:

- [ ] **Step 1:** `AdminPageHeader` + `FilterBar` (status + omni-search) + `DataTable` of payouts + a `DetailDrawer` showing the linked earnings and the **Process** action (mark processing/completed/failed + `transactionId`/notes, posting to Task 4.1's route). Four states, RTL/i18n, a11y, `requireAdmin` on the route.
- [ ] **Step 2:** `renderToStaticMarkup` tests; status→badge via the Task 4.2 helper.
- [ ] **Step 3: Run + commit.**

---

## Final gate (before PR) + go-live

- [ ] **Full suite + gate** from repo root: `pnpm experts:test` and `pnpm experts:check`; `pnpm db:check:drift` in sync. **Verify the `CreatorBalance` view by hand** after applying the migration: `psql "$DATABASE_URL" -c '\d billing.creator_balances'` — the drift gate does NOT compare view SQL bodies `[DB-2]`, so a wrong column name only surfaces at runtime.
- [ ] **In-routine reviewer panel** on `git diff origin/main`: `code-reviewer` + `qa-tester` (always) + `security-auditor` (money path — payout IDOR, double-pay, the amount-in-tx race) in parallel; triage; then `release-manager` (GO/NO-GO).
- [ ] Ship via `experts-ship`. PR body: **`Closes #936`** (completes the issue: course ledger from Plan A + payouts/surfaces/platform-subscriptions here).
- [ ] **GO-LIVE (D-8):** flipping **`SETTLEMENT_LEDGER_ENABLED=true`** is the deliberate switch that starts accrual — do it only AFTER this PR is deployed and the cron sidecar routes (Plan A) are wired and confirmed reachable. Before flipping: run the reconciliation route once to confirm it returns `{ok:true}`. This is the moment the ledger goes live; there is no dark-ledger window because Plan A shipped with the flag off.
- [ ] **Operator gate:** do NOT process payouts to `vatRegistered` creators until self-billing exists (spec §12) — the admin Process action must warn on `vatRegistered`.

---

## Explicitly NOT in Plan B (follow-ons)

- **ALL events** (settlement + event refund flow + clawback) — the Events phase (spec D-9).
- **Subscription renewal settlement** — Plan B settles the initial subscription checkout; recurring renewals (Stripe webhooks) are a follow-on (verify first whether a renewal creates a new `Subscription` row → new settlement, or updates the existing one).
- **Self-billing / instructor ZATCA tax document** — compliance phase; `CreatorPayoutMethod.vatRegistered`/`vatNumber` are the attach point.
- **Automated PSP disbursement** — payouts remain manual admin record-keeping.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
