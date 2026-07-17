---
title: "2026 06 10 event settlement refunds"
date: "2026-06-10"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/plans/2026-06-10-event-settlement-refunds.md"
---
# Event Settlement & Refunds (#966) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Lift the D-9 event exclusion: ship the event refund flow (request → approve → process with credit note + ZATCA + clawback), the `"event"` settlement-writer branch, the shared settlement-clawback extraction, and the admin/attendee surfaces — one PR, `Closes #966`.

**Architecture:** Sibling-mirror of the course refund flow (spec E-5) under `src/lib/events/`, a polymorphic widening of `billing.refund_requests` (E-3), one extraction `src/lib/settlement/clawback-settlement.ts` both process handlers call, and an `"event"` branch in `recordOrderSettlement` reusing `priceOrder`/`resolveContributorShares`/`allocateEarnings`. Everything money-side stays flag-gated by `SETTLEMENT_LEDGER_ENABLED`.

**Tech Stack:** Next.js 16 App Router, Prisma 7 multi-schema (billing/public), vitest node-env with mocked prisma, HeroUI v3, next-intl (en/ar/es).

**Spec:** `docs/superpowers/specs/2026-06-10-event-settlement-refunds-design.md` (v4, operator decisions E-1..E-8). Read it before starting.

**ADDENDUM (2026-06-11) — rebase deltas from PR #998/#1001 (buyer price breakdown + coupon-at-checkout, Closes #975), which landed on main after this plan was written. These OVERRIDE the affected task snippets:**

- **Task 1:** `EventRegistration` now carries a coupon snapshot block (`couponCode` … `pricingBasis`, schema ~line 1099-1106) and the migration baseline includes `20260611102124_buyer_breakdown_currency_coupon_snapshot`. The inverse relation line still goes after `user`. The `git show HEAD:…schema.prisma` old-schema diff approach is unchanged.
- **Task 4 (`resolveEventFacts`):** `OrderFacts` gained `coupon: CouponMetadata | null`, `checkoutDiscountAmount?: number`, `listPriceIncVat?: number` (scenario A, instructor-funded checkout discount). `resolveEventFacts` MUST mirror `resolveCourseFacts`' coupon handling on current main verbatim: build `coupon` from the registration's persisted snapshot (`couponCode`/`couponDiscountType`/`couponDiscountValue`, `fundedBy: "INSTRUCTOR"`), and pass `checkoutDiscountAmount` from `couponDiscountAmount`, `listPriceIncVat` from `couponListPrice` — never re-read the event's mutable coupon config (TOCTOU). Add to the event tests a coupon-snapshot case mirroring the course coupon test #998 added in the same file.
- **Task 7:** the register handler now has THREE completion-capable paths (free event, NEW 100%-off coupon path, paid checkout). The E-6 `refunded` guard goes directly after the `completed` check (`existing` fetch is line 99, completed check line 103 on current main) — that placement precedes all three paths, which is required: the 100%-off path upserts `status: "completed"` and would otherwise recycle a refunded row. `__tests__/event-register.handler.test.ts` gained coupon tests in #998 — they must stay green.
- **Task 13:** `event-detail-sidebar.tsx` was modified by #998 (BuyerPriceBreakdown mounted); re-locate `RegisteredState`'s mount point by symbol, not the stale ~line 528 anchor.
- A settlement on a couponed event sale settles on the registration's `amountPaid` (gateway ex-VAT amount set at completion) exactly like courses — no extra event-side handling beyond the snapshot pass-through above.

**House rules that bind every task:**

- App work follows `experts-constellation` + `experts-galaxy`; lifecycle follows `experts-ship`.
- Verify with `pnpm typecheck:touched -- <files>` during implementation, never full `pnpm typecheck` first.
- Tests run from `apps/experts-app` with `DATABASE_URL=postgresql://localhost/experts_test`.
- NEVER run `npx prisma format`. Hand-edit schema matching surrounding 4-space style.
- Never chain a test run and a commit in one shell command (`… && git commit`).
- All work happens in `apps/experts-app/` unless a path says otherwise. All paths below are relative to `apps/experts-app/`.

**File structure (what gets created/modified):**

| File                                                                                        | Responsibility                                              |
| ------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `prisma/schema.prisma`                                                                      | RefundRequest widening + EventRegistration inverse relation |
| `prisma/migrations/<ts>_refund_requests_polymorphic/migration.sql`                          | hand-checked DDL                                            |
| `src/lib/events/registrations/event-refund-policy.ts` (new)                                 | pure eligibility (E-1, §2.1 timing, snapshot-at)            |
| `src/lib/settlement/clawback-settlement.ts` (new)                                           | shared clawback (spec §5)                                   |
| `src/lib/settlement/record-settlement.ts`                                                   | `"event"` in union + `resolveEventFacts`                    |
| `src/lib/settlement/reconcile-settlements.ts`                                               | third anti-join + fair budget                               |
| `src/lib/affiliate/helpers/affiliate.helper.ts`                                             | event holdUntil = max(+3d, eventStart)                      |
| `src/lib/affiliate/handlers/affiliate-attribution.handler.ts`                               | thread `eventStartsAt`                                      |
| `src/lib/events/handlers/event-register.handler.ts`                                         | E-6 refunded guard                                          |
| `src/lib/events/handlers/event-registration-complete.handler.ts`                            | inline settlement wire + pass eventStartsAt                 |
| `src/lib/events/registrations/commands/*.ts` (new)                                          | refund request/process commands+schemas                     |
| `src/lib/events/registrations/handlers/event-registration-refund-request.handler.ts` (new)  | attendee request                                            |
| `src/lib/events/registrations/handlers/event-registration-refund-process.handler.ts` (new)  | admin process                                               |
| `src/lib/courses/enrollments/handlers/course-enrollment-refund-process.handler.ts`          | refactor onto shared clawback                               |
| `src/lib/courses/enrollments/handlers/course-enrollment-refund-{approve,reject}.handler.ts` | widen observe payload (stay shared)                         |
| `app/api/v1/events/[id]/refund/route.ts` (new)                                              | POST request + GET eligibility                              |
| `app/api/v1/admin/refunds/[id]/process/route.ts`                                            | dispatch by sourceType                                      |
| `src/lib/billing/refunds/dto/refund-request.dto.ts` (new)                                   | discriminated admin DTO (moved)                             |
| `src/lib/billing/refunds/queries/refund-request.query.ts` (new)                             | widened admin query (moved)                                 |
| `app/(i18n)/_shared/admin/refunds/_components/refunds-table.tsx`                            | source chip + content column                                |
| `src/lib/events/detail/sections/event-refund-section.tsx` (new)                             | attendee refund UI (E-8)                                    |
| `src/lib/events/detail/sections/event-detail-sidebar.tsx`                                   | mount refund section in RegisteredState                     |
| `src/lib/ai/ask/ask-ai-assistant.ts`                                                        | fix stale 48h fact line                                     |
| `prisma/seeders/20-settlements.ts`                                                          | event settlement branch                                     |
| `src/i18n/messages/{en,ar,es}/{admin,events}.json`                                          | new strings                                                 |

---

### Task 0: Branch + worktree setup

- [ ] **Step 0.1:** From repo root: confirm `git branch --show-current` is clean main, `git fetch origin && git merge --ff-only origin/main`. Create the work branch: `git checkout -b feat/gh-966-event-settlement-refunds origin/main`. (If executing via worktree isolation, use `superpowers:using-git-worktrees` and copy `.env` files per root CLAUDE.md.)
- [ ] **Step 0.2:** Re-verify the branch before EVERY commit in this plan (`git branch --show-current`) — concurrent loops on this machine switch branches; pushes are always explicit `branch:branch`.

---

### Task 1: Schema widening + migration

**Files:**

- Modify: `prisma/schema.prisma` (RefundRequest model ~line 1690; EventRegistration model)
- Create: `prisma/migrations/<timestamp>_refund_requests_polymorphic/migration.sql`

- [ ] **Step 1.1: Edit the RefundRequest model** (hand-edit, 4-space indent, keep field alignment style):

```prisma
model RefundRequest {
    id             String             @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
    sourceType     String             @default("course") @map("source_type") @db.VarChar(20)
    enrollmentId   String?            @unique @map("enrollment_id") @db.Uuid
    registrationId String?            @unique @map("registration_id") @db.Uuid
    userId         String             @map("user_id") @db.Uuid
    reason         String?
    status         RefundStatus       @default(requested)
    requestedAt    DateTime           @default(now()) @map("requested_at") @db.Timestamptz(6)
    resolvedAt     DateTime?          @map("resolved_at") @db.Timestamptz(6)
    enrollment     CourseEnrollment?  @relation(fields: [enrollmentId], references: [id], onDelete: Cascade)
    registration   EventRegistration? @relation(fields: [registrationId], references: [id], onDelete: Cascade)
    user           User               @relation(fields: [userId], references: [id], onDelete: Cascade)

    @@index([userId])
    @@index([status])
    @@index([sourceType, status])
    @@map("refund_requests")
    @@schema("billing")
}
```

- [ ] **Step 1.2: Add the inverse relation on EventRegistration** — add one line to the model body (after `user`):

```prisma
    refundRequest      RefundRequest?
```

- [ ] **Step 1.3: Generate the migration SQL DB-free** (house pattern — Prisma 7 `--from-schema`):

```bash
git show HEAD:apps/experts-app/prisma/schema.prisma > /tmp/schema-old.prisma
cd apps/experts-app
npx prisma migrate diff --from-schema /tmp/schema-old.prisma --to-schema prisma/schema.prisma --script > /tmp/refunds-poly.sql
```

Create `prisma/migrations/$(date +%Y%m%d%H%M%S)_refund_requests_polymorphic/migration.sql` from the diff output, then hand-verify it contains exactly (order may differ):

```sql
-- AlterTable
ALTER TABLE "billing"."refund_requests" ADD COLUMN     "source_type" VARCHAR(20) NOT NULL DEFAULT 'course',
ADD COLUMN     "registration_id" UUID,
ALTER COLUMN "enrollment_id" DROP NOT NULL;

-- Explicit documentation backfill (no-op given the column default, kept for audit clarity)
UPDATE "billing"."refund_requests" SET "source_type" = 'course' WHERE "source_type" IS DISTINCT FROM 'course';

-- CreateIndex
CREATE UNIQUE INDEX "refund_requests_registration_id_key" ON "billing"."refund_requests"("registration_id");
CREATE INDEX "refund_requests_source_type_status_idx" ON "billing"."refund_requests"("source_type", "status");

-- AddForeignKey
ALTER TABLE "billing"."refund_requests" ADD CONSTRAINT "refund_requests_registration_id_fkey" FOREIGN KEY ("registration_id") REFERENCES "public"."event_registrations"("id") ON DELETE CASCADE ON UPDATE CASCADE;
```

(Add the `UPDATE` line by hand — `migrate diff` won't emit it.)

- [ ] **Step 1.4: Regenerate client + drift gate:**

```bash
pnpm db:generate
pnpm db:check:drift
```

Expected: generate succeeds; drift gate green.

- [ ] **Step 1.5: Apply to dev DB and commit:**

```bash
pnpm prisma migrate deploy   # or the house dev-apply command if different — check package.json db:* scripts
git add prisma/schema.prisma prisma/migrations
git commit -m "feat(billing): widen RefundRequest polymorphically — sourceType + nullable registrationId FK (#966)"
```

---

### Task 2: `event-refund-policy.ts` (pure eligibility, E-1 + §2.1 + snapshot-at)

**Files:**

- Create: `src/lib/events/registrations/event-refund-policy.ts`
- Test: `src/lib/events/registrations/__tests__/event-refund-policy.test.ts`

- [ ] **Step 2.1: Write the failing tests** — eligibility matrix:

```ts
import {describe, it, expect} from 'vitest'
import {resolveEventStart, resolveEventEnd, evaluateEventRefundEligibility} from '@/lib/events/registrations/event-refund-policy'

const D = (s: string) => new Date(s)
const occ = (startsAt: string, endsAt: string, isCancelled = false) => ({
    startsAt: D(startsAt),
    endsAt: D(endsAt),
    isCancelled
})

describe('resolveEventStart / resolveEventEnd', () => {
    it('returns min start / max end over non-cancelled occurrences', () => {
        const occurrences = [
            occ('2026-07-10T10:00:00Z', '2026-07-10T12:00:00Z'),
            occ('2026-07-01T10:00:00Z', '2026-07-01T12:00:00Z'),
            occ('2026-06-01T10:00:00Z', '2026-09-01T12:00:00Z', true) // cancelled — ignored
        ]
        expect(resolveEventStart(occurrences)).toEqual(D('2026-07-01T10:00:00Z'))
        expect(resolveEventEnd(occurrences)).toEqual(D('2026-07-10T12:00:00Z'))
    })
    it('returns null when no usable occurrence exists', () => {
        expect(resolveEventStart([])).toBeNull()
        expect(resolveEventStart([occ('2026-07-01T10:00:00Z', '2026-07-01T12:00:00Z', true)])).toBeNull()
    })
})

describe('evaluateEventRefundEligibility', () => {
    const base = {
        status: 'completed',
        amountPaid: 100,
        registeredAt: D('2026-07-01T00:00:00Z'),
        occurrences: [occ('2026-07-20T10:00:00Z', '2026-07-20T12:00:00Z')]
    }
    it('eligible inside window, before start', () => {
        expect(evaluateEventRefundEligibility({...base, at: D('2026-07-03T00:00:00Z')})).toEqual({eligible: true})
    })
    it('window edge: day 7 inclusive, day 8 expired', () => {
        expect(evaluateEventRefundEligibility({...base, at: D('2026-07-08T00:00:00Z')})).toEqual({eligible: true})
        expect(evaluateEventRefundEligibility({...base, at: D('2026-07-08T00:00:01Z')})).toEqual({
            eligible: false,
            reason: 'windowExpired'
        })
    })
    it('started event is ineligible even inside the window', () => {
        const started = {
            ...base,
            occurrences: [occ('2026-07-02T10:00:00Z', '2026-07-02T12:00:00Z')],
            at: D('2026-07-02T10:00:01Z')
        }
        expect(evaluateEventRefundEligibility(started)).toEqual({eligible: false, reason: 'eventStarted'})
    })
    it('zero usable occurrences: start gate passes, window alone decides (spec §2.1)', () => {
        expect(evaluateEventRefundEligibility({...base, occurrences: [], at: D('2026-07-03T00:00:00Z')})).toEqual({eligible: true})
    })
    it('not completed / free / refunded are ineligible', () => {
        expect(evaluateEventRefundEligibility({...base, status: 'pending', at: D('2026-07-03T00:00:00Z')})).toEqual({
            eligible: false,
            reason: 'notCompleted'
        })
        expect(evaluateEventRefundEligibility({...base, amountPaid: 0, at: D('2026-07-03T00:00:00Z')})).toEqual({
            eligible: false,
            reason: 'freeRegistration'
        })
        expect(evaluateEventRefundEligibility({...base, status: 'refunded', at: D('2026-07-03T00:00:00Z')})).toEqual({
            eligible: false,
            reason: 'alreadyRefunded'
        })
    })
    it('cancelled occurrence does not gate start (multi-occurrence resolution)', () => {
        const r = evaluateEventRefundEligibility({
            ...base,
            occurrences: [
                occ('2026-07-02T10:00:00Z', '2026-07-02T12:00:00Z', true), // cancelled, in the past
                occ('2026-07-20T10:00:00Z', '2026-07-20T12:00:00Z')
            ],
            at: D('2026-07-03T00:00:00Z')
        })
        expect(r).toEqual({eligible: true})
    })
})
```

- [ ] **Step 2.2: Run to verify failure:**
      `DATABASE_URL=postgresql://localhost/experts_test npx vitest run src/lib/events/registrations/__tests__/event-refund-policy.test.ts` — Expected: FAIL (module not found).

- [ ] **Step 2.3: Implement:**

```ts
import {REFUND_WINDOW_DAYS} from '@/lib/courses/enrollments/refund-policy'

export type EventOccurrenceTiming = {startsAt: Date; endsAt: Date; isCancelled: boolean}

export type EventRefundIneligibilityReason = 'notCompleted' | 'alreadyRefunded' | 'freeRegistration' | 'windowExpired' | 'eventStarted'

export type EventRefundEligibility = {eligible: true} | {eligible: false; reason: EventRefundIneligibilityReason}

/** Spec §2.1: eventStart = min startsAt over non-cancelled occurrences; null when none. */
export function resolveEventStart(occurrences: EventOccurrenceTiming[]): Date | null {
    const usable = occurrences.filter((o) => !o.isCancelled)
    if (usable.length === 0) return null
    return new Date(Math.min(...usable.map((o) => o.startsAt.getTime())))
}

/** Spec §2.1: eventEnd = max endsAt over non-cancelled occurrences; null when none. */
export function resolveEventEnd(occurrences: EventOccurrenceTiming[]): Date | null {
    const usable = occurrences.filter((o) => !o.isCancelled)
    if (usable.length === 0) return null
    return new Date(Math.max(...usable.map((o) => o.endsAt.getTime())))
}

/**
 * E-1 eligibility, evaluated at `at` (snapshot-at-request — the process handler
 * passes the request's requestedAt so a timely request can't expire in the admin
 * queue; spec §4). Order of gates mirrors the course request handler: state gates
 * first, then time gates.
 */
export function evaluateEventRefundEligibility(input: {
    status: string
    amountPaid: number | null
    registeredAt: Date
    occurrences: EventOccurrenceTiming[]
    at: Date
}): EventRefundEligibility {
    if (input.status === 'refunded') return {eligible: false, reason: 'alreadyRefunded'}
    if (input.status !== 'completed') return {eligible: false, reason: 'notCompleted'}
    if (input.amountPaid == null || Number(input.amountPaid) <= 0) {
        return {eligible: false, reason: 'freeRegistration'}
    }

    const deadline = new Date(input.registeredAt)
    deadline.setDate(deadline.getDate() + REFUND_WINDOW_DAYS)
    if (input.at > deadline) return {eligible: false, reason: 'windowExpired'}

    const eventStart = resolveEventStart(input.occurrences)
    // Zero usable occurrences: no scheduled start, the gate passes (spec §2.1).
    if (eventStart !== null && input.at >= eventStart) return {eligible: false, reason: 'eventStarted'}

    return {eligible: true}
}
```

- [ ] **Step 2.4: Run tests** — Expected: PASS. Then `pnpm typecheck:touched -- src/lib/events/registrations/event-refund-policy.ts`.
- [ ] **Step 2.5: Commit:** `git add -A src/lib/events/registrations && git commit -m "feat(events): pure event refund eligibility policy — E-1 window∧start, snapshot-at (#966)"`

---

### Task 3: Shared clawback extraction + course handler refactor

**Files:**

- Create: `src/lib/settlement/clawback-settlement.ts`
- Modify: `src/lib/courses/enrollments/handlers/course-enrollment-refund-process.handler.ts:141-233`
- Test: `src/lib/settlement/__tests__/clawback-settlement.test.ts` (new); existing `src/lib/courses/enrollments/handlers/__tests__/course-enrollment-refund-admin.handlers.test.ts` must pass unchanged (behavior-preservation proof)

- [ ] **Step 3.1: Create the helper** — verbatim move of the settlement-side block (settlement read → payout cancel + re-read unlink → earnings cancel → settlement reverse). It takes the tx client; it imports NO course/event domain code:

```ts
import type {Prisma} from '@/generated/prisma/client'

const NO_MATCH_UUID = '00000000-0000-0000-0000-000000000000'

export type ClawbackResult = {
    cancelledEarningsCount: number
    platformLossAmount: number
}

/**
 * #936/#962 settlement clawback, shared by course and event refund process
 * handlers (spec #966 §5). MUST run inside the caller's interactive transaction
 * so the settlement read and the earning clawback share ONE snapshot (a
 * concurrent reconcile sweep could otherwise leave fresh earnings un-cancelled
 * on a reversed settlement).
 *
 * 1. Settlement lookup by (sourceType, sourceId); NO_MATCH_UUID fallback makes
 *    flag-off-era sales safe no-ops.
 * 2. Σ already-`paid` lines → platformLossAmount (finance signal; paid earnings
 *    are never clawed — Tier-2 policy).
 * 3. Status-guarded cancel of in-flight payouts linked to the to-be-cancelled
 *    earnings, then unlink ONLY payouts the guarded write actually cancelled
 *    (refund-vs-admin-complete race: if the admin's complete-transaction holds
 *    the row lock, our updateMany re-evaluates after their commit, sees
 *    `completed`, matches 0 — unlinking its just-paid earnings would return
 *    them to payable and double-pay them).
 * 4. Cancel pending/approved earnings on the settlement; reverse it.
 */
export async function clawbackSettlementForSource(
    tx: Prisma.TransactionClient,
    input: {
        sourceType: 'course' | 'event' | 'subscription'
        sourceId: string
        adminUserId: string | null
        refundRequestId: string
    }
): Promise<ClawbackResult> {
    const {sourceType, sourceId, adminUserId, refundRequestId} = input

    const settlement = await tx.orderSettlement.findUnique({
        where: {order_settlement_source_unique: {sourceType, sourceId}},
        select: {id: true, lines: {where: {status: 'paid'}, select: {netAmount: true}}}
    })
    const platformLossAmount = (settlement?.lines ?? []).reduce((sum, l) => sum + Number(l.netAmount), 0)

    const linkedPayoutRows = await tx.creatorEarning.findMany({
        where: {
            settlementId: settlement?.id ?? NO_MATCH_UUID,
            status: {in: ['pending', 'approved']},
            payoutId: {not: null}
        },
        select: {payoutId: true}
    })
    const payoutIds = [...new Set(linkedPayoutRows.map((r) => r.payoutId).filter((p): p is string => p != null))]
    if (payoutIds.length > 0) {
        await tx.creatorPayout.updateMany({
            where: {id: {in: payoutIds}, status: {in: ['pending', 'processing']}},
            data: {
                status: 'cancelled',
                notes: `refund_cancellation:${refundRequestId}`,
                processedAt: new Date(),
                processedBy: adminUserId ?? null
            }
        })
        const cancelledPayoutRows = await tx.creatorPayout.findMany({
            where: {id: {in: payoutIds}, status: 'cancelled'},
            select: {id: true}
        })
        const cancelledPayoutIds = cancelledPayoutRows.map((r) => r.id)
        if (cancelledPayoutIds.length > 0) {
            await tx.creatorEarning.updateMany({
                where: {payoutId: {in: cancelledPayoutIds}, status: {in: ['pending', 'approved']}},
                data: {payoutId: null}
            })
        }
    }

    const cancelledEarnings = await tx.creatorEarning.updateMany({
        where: {
            settlementId: settlement?.id ?? NO_MATCH_UUID,
            status: {in: ['pending', 'approved']}
        },
        data: {status: 'cancelled', holdReason: 'purchase_refunded', cancelledAt: new Date()}
    })
    await tx.orderSettlement.updateMany({
        where: {sourceType, sourceId, status: 'recorded'},
        data: {status: 'reversed', reversedAt: new Date()}
    })

    return {cancelledEarningsCount: cancelledEarnings.count, platformLossAmount}
}
```

- [ ] **Step 3.2: Refactor the course process handler** — replace the body of the `$transaction` callback (lines 147-233) with:

```ts
const {cancelledCommissions, cancelledEarningsCount, platformLossAmount} = await prisma.$transaction(async (tx) => {
    const clawback = await clawbackSettlementForSource(tx, {
        sourceType: 'course',
        sourceId: enrollment.id,
        adminUserId: adminUserId ?? null,
        refundRequestId: request.id
    })

    await tx.courseEnrollment.update({
        where: {id: enrollment.id},
        data: {status: 'refunded', cancelledAt: new Date()}
    })
    const cancelledCommissions = await tx.commission.updateMany({
        where: {
            userId: enrollment.userId,
            itemType: 'course',
            itemId: enrollment.courseId,
            status: {in: ['pending', 'approved']}
        },
        data: {status: 'cancelled', holdReason: 'purchase_refunded'}
    })
    await tx.refundRequest.update({
        where: {id: request.id},
        data: {status: 'processed', resolvedAt: new Date()}
    })

    return {cancelledCommissions, ...clawback}
})
```

Add the import `import {clawbackSettlementForSource} from "@/lib/settlement/clawback-settlement";`, delete the now-unused `NO_MATCH_UUID` const and the moved block, and update the observe payload field `cancelledEarnings: cancelledEarnings.count` → `cancelledEarnings: cancelledEarningsCount`. Keep the two explanatory comments (#916 / #936) above the transaction.

NOTE: the earnings-cancel + settlement-reverse now run BEFORE the enrollment/commission/refundRequest updates instead of after — same transaction, same snapshot, semantically identical. If any existing mocked test asserts _call order_ (rather than presence/args), update that assertion and say so in the commit body.

- [ ] **Step 3.3: Run the existing course suite (the behavior-preservation proof):**

```bash
DATABASE_URL=postgresql://localhost/experts_test npx vitest run src/lib/courses/enrollments/handlers/__tests__/course-enrollment-refund-admin.handlers.test.ts
```

Expected: PASS unchanged (or only order-assertion updates per the note above).

- [ ] **Step 3.4: Write direct tests** for `clawback-settlement.test.ts` mirroring the clawback cases in the course suite (mock tx client as a plain object of `vi.fn()`s): no-settlement no-op (NO_MATCH_UUID path), paid-lines platformLoss sum, payout cancel + only-actually-cancelled unlink (mock the re-read returning a subset), earnings cancel + settlement reverse args. Run: PASS.
- [ ] **Step 3.5: Gate + commit:** `pnpm typecheck:touched -- src/lib/settlement/clawback-settlement.ts src/lib/courses/enrollments/handlers/course-enrollment-refund-process.handler.ts` then commit `"refactor(settlement): extract shared refund clawback helper from course process handler (#966)"`.

---

### Task 4: Settlement writer — the `"event"` branch

**Files:**

- Modify: `src/lib/settlement/record-settlement.ts`
- Test: extend `src/lib/settlement/__tests__/record-settlement.test.ts` (event cases) and re-run the whole existing file (regression)

- [ ] **Step 4.1: Widen the union and dispatch.** In `record-settlement.ts`:
    - Line 20: `export type SettlementSourceType = "course" | "event" | "subscription";` and update the comment (events included per #966; D-9 lifted).
    - In `recordOrderSettlement` replace `const facts = await resolveCourseFacts(sourceId);` with:

```ts
const facts = sourceType === 'event' ? await resolveEventFacts(sourceId) : await resolveCourseFacts(sourceId)
```

- [ ] **Step 4.2: Add `resolveEventFacts`** below `resolveCourseFacts`:

```ts
async function resolveEventFacts(registrationId: string): Promise<OrderFacts | null> {
    const r = await prisma.eventRegistration.findUnique({where: {id: registrationId}})
    if (!r || r.status !== 'completed' || r.amountPaid == null) return null // status gate
    const event = await prisma.event.findUnique({
        where: {id: r.eventId},
        include: {
            hosts: {select: {userId: true, role: true, revenueShare: true}},
            occurrences: {where: {isCancelled: false}, select: {endsAt: true}}
        }
    })
    if (!event || event.hosts.length === 0) return null
    // Spec §2.1: payableAt anchors on max non-cancelled endsAt; zero usable
    // occurrences → skip recording (reconcile retries once one exists).
    if (event.occurrences.length === 0) {
        observe(
            'settlement.event.no_occurrence',
            {sourceId: registrationId, eventId: r.eventId},
            {level: 'warn', dedupeKey: `settlement.event.no_occurrence:${registrationId}`}
        )
        return null
    }
    const eventEnd = new Date(Math.max(...event.occurrences.map((o) => o.endsAt.getTime())))
    return {
        buyerUserId: r.userId,
        itemId: r.eventId,
        itemTitle: event.title,
        grossPaid: Number(r.amountPaid),
        payableAt: calculateEventPayableDate(eventEnd),
        contributors: event.hosts.map((h) => ({
            userId: h.userId,
            role: h.role,
            revenueShare: h.revenueShare == null ? null : Number(h.revenueShare)
        })),
        // HostRole primary is "host" — NOT the course "primary" (passing the wrong
        // role fires the fallback warn on every single-host event).
        primaryRole: 'host'
    }
}
```

Add `calculateEventPayableDate` to the existing `@/modules/revenue/revenue.service` import.

- [ ] **Step 4.3: Tests** (mirror existing course writer tests in the same file):
    - single host (`role: "host"`, `revenueShare: 1`) → one line, NO `settlement.shares.fallback_primary` observe;
    - two hosts 0.6/0.4 → split lines;
    - partial-null shares (two hosts, one null) → fallback to the `"host"` row + warn observe;
    - `payableAt` = max endsAt + 7d (assert exact date math, cancelled occurrence excluded via the `where: {isCancelled: false}` mock);
    - zero occurrences → no create + `settlement.event.no_occurrence` observe;
    - P2002 on create → swallowed as success;
    - affiliate deduction: mock `commission.findFirst` returning `{commissionAmount: 50}` and assert `affiliatePayout` flows into the created settlement (writer queries `itemType: sourceType` = `"event"`, `itemId: eventId`).
- [ ] **Step 4.4: Run the ENTIRE existing writer suite** (course + subscription regression, not just event tests): `DATABASE_URL=postgresql://localhost/experts_test npx vitest run src/lib/settlement/` — Expected: PASS.
- [ ] **Step 4.5: Commit:** `"feat(settlement): event branch in the settlement writer — hosts earn via the ledger (#966)"`

---

### Task 5: Reconcile sweep — third anti-join + fair budget

**Files:**

- Modify: `src/lib/settlement/reconcile-settlements.ts`
- Test: extend `src/lib/settlement/__tests__/reconcile-settlements.test.ts`

- [ ] **Step 5.1: Replace the budget logic.** Three bounded anti-joins sharing `limit` fairly (⌊limit/3⌋ each, spillover in order course → subscription → event):

```ts
export async function runSettlementReconciliationSweep(opts: {limit?: number} = {}) {
  const limit = opts.limit ?? 500;
  // Fair split so one populous source can't starve the others (spec #966 §6):
  // each source gets ⌊limit/3⌋; unused budget spills to the next source in order.
  const baseBudget = Math.floor(limit / 3);

  const courseBudget = baseBudget;
  const courseRows = await prisma.$queryRaw<{id: string}[]>`
    SELECT e.id FROM "public"."course_enrollments" e
    WHERE e.status = 'completed' AND e.amount_paid > 0
      AND NOT EXISTS (
        SELECT 1 FROM "billing"."order_settlements" s
        WHERE s.source_type = 'course' AND s.source_id = e.id
      )
    LIMIT ${courseBudget}`;

  const subscriptionBudget = baseBudget + (courseBudget - courseRows.length);
  const subscriptionRows =
    subscriptionBudget > 0
      ? await prisma.$queryRaw<{id: string}[]>`
    SELECT sub.id FROM "billing"."subscriptions" sub
    WHERE EXISTS (
        SELECT 1 FROM "billing"."invoices" i
        WHERE i.content_type = 'subscription' AND i.content_id = sub.id
          AND i.status = 'paid' AND i.total_amount > 0
      )
      AND NOT EXISTS (
        SELECT 1 FROM "billing"."order_settlements" s
        WHERE s.source_type = 'subscription' AND s.source_id = sub.id
      )
    LIMIT ${subscriptionBudget}`
      : [];

  const eventBudget = limit - courseRows.length - subscriptionRows.length;
  const eventRows =
    eventBudget > 0
      ? await prisma.$queryRaw<{id: string}[]>`
    SELECT r.id FROM "public"."event_registrations" r
    WHERE r.status = 'completed' AND r.amount_paid > 0
      AND NOT EXISTS (
        SELECT 1 FROM "billing"."order_settlements" s
        WHERE s.source_type = 'event' AND s.source_id = r.id
      )
    LIMIT ${eventBudget}`
      : [];

  const work: {sourceType: "course" | "subscription" | "event"; id: string}[] = [
    ...courseRows.map(({id}) => ({sourceType: "course" as const, id})),
    ...subscriptionRows.map(({id}) => ({sourceType: "subscription" as const, id})),
    ...eventRows.map(({id}) => ({sourceType: "event" as const, id})),
  ];
  // …loop + observe unchanged
```

(Keep the existing loop/observe tail exactly as-is.)

- [ ] **Step 5.2: Tests:** extend the existing reconcile suite — assert the event anti-join SQL fires when budget remains (assert by mock `$queryRaw` call count/args), event rows dispatch `recordOrderSettlement({sourceType: "event", …})`, and budget math: `limit: 9` with 1 course row + 2 sub rows → eventBudget 6.
- [ ] **Step 5.3: Run + commit:** full `src/lib/settlement/` suite green → `"feat(settlement): reconcile event registrations + fair budget split across sources (#966)"`

---

### Task 6: Affiliate holdUntil fix + `eventStartsAt` threading

**Files:**

- Modify: `src/lib/affiliate/helpers/affiliate.helper.ts` (`calculateHoldUntil` ~line 127, `createCommission` ~line 187)
- Modify: `src/lib/affiliate/handlers/affiliate-attribution.handler.ts` (input type + commission call)
- Modify: `src/lib/events/handlers/event-registration-complete.handler.ts` (~line 175: pass `eventStartsAt`)
- Test: extend the existing affiliate helper/handler suites (find them: `grep -rl "calculateHoldUntil" --include="*.test.ts" src/`)

- [ ] **Step 6.1: Widen `calculateHoldUntil`** — add an optional anchor; ONLY the event case uses it:

```ts
export function calculateHoldUntil(itemType: string, createdAt: Date, opts?: {eventStartsAt?: Date | null}): Date {
    const holdUntil = new Date(createdAt)
    switch (itemType) {
        case 'event': {
            // #966: the event refund window stays open until event start (E-1), so the
            // commission must not mature before it. Fallback to the legacy 3-day hold
            // when no occurrence exists yet (spec §5.1).
            holdUntil.setDate(holdUntil.getDate() + 3)
            if (opts?.eventStartsAt && opts.eventStartsAt > holdUntil) {
                return new Date(opts.eventStartsAt)
            }
            return holdUntil
        }
        // …existing course/subscription cases unchanged
    }
}
```

(Adapt to the file's existing switch shape — course/subscription branches must not change. `referral.expiresAt`'s call site stays as-is: click-attribution expiry, not refund exposure.)

- [ ] **Step 6.2: Thread the anchor.** In `affiliate-attribution.handler.ts`: add `eventStartsAt?: Date | null;` to `input.source`; where `createCommission`/`calculateHoldUntil` is invoked for the commission, pass `{eventStartsAt: input.source.type === "event" ? (input.source.eventStartsAt ?? null) : null}`. Add the DB fallback right before, inside the handler:

```ts
let eventStartsAt = input.source.type === 'event' ? (input.source.eventStartsAt ?? null) : null
if (input.source.type === 'event' && !eventStartsAt) {
    const firstOccurrence = await prisma.eventOccurrence.findFirst({
        where: {eventId: input.source.id, isCancelled: false},
        orderBy: {startsAt: 'asc'},
        select: {startsAt: true}
    })
    eventStartsAt = firstOccurrence?.startsAt ?? null
}
```

`createCommission` gains the same optional `opts` pass-through to `calculateHoldUntil` (it computes `holdUntil` at its line ~187).

- [ ] **Step 6.3: Pass from the completion handler.** In `event-registration-complete.handler.ts` ~line 175 the attribution call's source becomes:

```ts
        source: {
          type: "event",
          id: eventId,
          title: registration.event.title,
          eventStartsAt: registration.event.occurrences[0]?.startsAt ?? null,
        },
```

(The select at ~line 102 already fetches `occurrences[0].startsAt`.)

- [ ] **Step 6.4: Tests:** event commission holdUntil = eventStart when start > createdAt+3d; = createdAt+3d when start sooner or null; course/subscription branches unchanged (regression assertions). Run affected suites, commit `"fix(affiliate): event commission holdUntil covers the full refund window (#966)"`.

---

### Task 7: E-6 register guard + inline settlement wire

**Files:**

- Modify: `src/lib/events/handlers/event-register.handler.ts` (~line 101)
- Modify: `src/lib/events/handlers/event-registration-complete.handler.ts` (after the `event.registration.success` observe, ~line 199)
- Test: extend `src/lib/events/handlers/__tests__/` register + complete suites

- [ ] **Step 7.1: The E-6 guard** — directly after the existing `completed` check:

```ts
if (existing?.status === 'refunded') {
    // E-6 (#966): a refunded registration must not be recycled — the settlement
    // unique ("event", registrationId) and the commission key would treat the
    // re-purchase as already-settled/attributed. Re-purchase support is a
    // named follow-on (new-row-per-purchase model).
    return {error: 'This registration was refunded and cannot be repurchased', status: 400 as const}
}
```

- [ ] **Step 7.2: The settlement wire.** Add to the imports: `import {recordOrderSettlement} from "@/lib/settlement/record-settlement";`. Insert AFTER the `observe("event.registration.success", …)` block and BEFORE `if (pendingInvoice === undefined) return;` (so it also runs on the invoice-already-existed re-delivery path — deliberate deviation from "after ZATCA enqueue", noted in the PR):

```ts
// #966: settle the sale — fault-isolated (a settlement failure must never fail
// the registration), idempotent (P2002-as-success), flag-gated inside the
// writer. Registration id via the (eventId, userId) unique — E-6 guarantees
// one paid lifecycle per row.
try {
    const settledRegistration = await prisma.eventRegistration.findUnique({
        where: {eventId_userId: {eventId, userId}},
        select: {id: true}
    })
    if (settledRegistration) {
        await recordOrderSettlement({sourceType: 'event', sourceId: settledRegistration.id})
    }
} catch (e) {
    observe(
        'settlement.inline.failed',
        {sourceType: 'event', eventId, userId, error: e instanceof Error ? e.message : String(e)},
        {level: 'error', dedupeKey: `settlement.inline.failed:event:${eventId}:${userId}`}
    )
}
```

- [ ] **Step 7.3: Tests:** register handler — `refunded` existing row → 400 with the exact error string; happy paths (no row, `cancelled` row, pending row) unchanged. Complete handler — settlement called with the registration id on success; a writer throw does NOT fail the handler (observe fired instead); free-event path: writer still safe (flag/grossPaid gates inside). Run, commit `"feat(events): block re-purchase after refund + inline settlement on completion (#966)"`.

---

### Task 8: Attendee refund request — commands, handler, route (POST + GET)

**Files:**

- Create: `src/lib/events/registrations/commands/event-registration-refund-request.command.ts` + `.schema.ts`
- Create: `src/lib/events/registrations/handlers/event-registration-refund-request.handler.ts`
- Create: `app/api/v1/events/[id]/refund/route.ts`
- Test: `src/lib/events/registrations/__tests__/event-registration-refund-request.handler.test.ts`, `app/api/v1/events/[id]/refund/__tests__/route.test.ts`

- [ ] **Step 8.1: Command + schema** (mirror the course pair):

```ts
// event-registration-refund-request.command.ts
export interface EventRegistrationRefundRequestCommand {
    requestId?: string
    userId: string
    eventId: string
    reason?: string | null
}
```

```ts
// event-registration-refund-request.schema.ts
import {z} from 'zod'

export const EventRegistrationRefundRequestSchema = z.object({
    requestId: z.uuid().optional(),
    userId: z.uuid(),
    eventId: z.uuid(),
    reason: z.string().min(3).nullable().optional()
})

export type EventRegistrationRefundRequestInput = z.infer<typeof EventRegistrationRefundRequestSchema>
```

- [ ] **Step 8.2: Request handler:**

```ts
import {prisma} from '@/lib/prisma'
import {observe} from '@/lib/observability'
import type {EventRegistrationRefundRequestCommand} from '@/lib/events/registrations/commands/event-registration-refund-request.command'
import {evaluateEventRefundEligibility} from '@/lib/events/registrations/event-refund-policy'
import {PrismaClientKnownRequestError} from '@prisma/client/runtime/client'

const INELIGIBILITY_MESSAGES: Record<string, string> = {
    notCompleted: 'Registration is not eligible for refund',
    alreadyRefunded: 'Registration is already refunded',
    freeRegistration: 'Free registrations are not refundable',
    windowExpired: 'Refund window has expired',
    eventStarted: 'Event has already started'
}

export async function handleEventRegistrationRefundRequest(command: EventRegistrationRefundRequestCommand) {
    const registration = await prisma.eventRegistration.findUnique({
        where: {eventId_userId: {eventId: command.eventId, userId: command.userId}},
        select: {
            id: true,
            status: true,
            amountPaid: true,
            registeredAt: true,
            userId: true,
            eventId: true,
            event: {
                select: {
                    occurrences: {select: {startsAt: true, endsAt: true, isCancelled: true}}
                }
            }
        }
    })

    if (!registration) {
        observe(
            'event.refund.request.not_found',
            {requestId: command.requestId, userId: command.userId, eventId: command.eventId},
            {level: 'warn', dedupeKey: `event.refund.request.not_found:${command.eventId}:${command.userId}`}
        )
        return {error: 'Registration not found', status: 404 as const}
    }

    const eligibility = evaluateEventRefundEligibility({
        status: registration.status,
        amountPaid: registration.amountPaid == null ? null : Number(registration.amountPaid),
        registeredAt: registration.registeredAt,
        occurrences: registration.event.occurrences,
        at: new Date()
    })
    if (!eligibility.eligible) {
        return {error: INELIGIBILITY_MESSAGES[eligibility.reason], status: 400 as const}
    }

    const existingRequest = await prisma.refundRequest.findFirst({
        where: {registrationId: registration.id},
        select: {id: true, status: true}
    })
    if (existingRequest) {
        // E-7: one refund request per registration, ever (any status blocks).
        return {error: 'Refund request already exists', status: 400 as const}
    }

    let refundRequest
    try {
        refundRequest = await prisma.refundRequest.create({
            data: {
                sourceType: 'event',
                registrationId: registration.id,
                userId: registration.userId,
                reason: command.reason ?? null,
                status: 'requested'
            }
        })
    } catch (error) {
        const errorCode = error instanceof PrismaClientKnownRequestError ? error.code : (error as {code?: string} | null)?.code
        if (errorCode === 'P2002') {
            return {error: 'Refund request already exists', status: 400 as const}
        }
        throw error
    }

    observe(
        'event.refund.requested',
        {
            requestId: command.requestId,
            refundRequestId: refundRequest.id,
            userId: registration.userId,
            eventId: registration.eventId
        },
        {level: 'warn', dedupeKey: `event.refund.requested:${registration.eventId}:${registration.userId}`}
    )

    return {data: {requested: true, refundRequestId: refundRequest.id}, status: 201 as const}
}
```

- [ ] **Step 8.3: Route** — POST mirrors the course refund route; GET serves the E-8 eligibility pre-check:

```ts
import {NextRequest, NextResponse} from 'next/server'
import {auth} from '@/lib/auth'
import {prisma} from '@/lib/prisma'
import {EventRegistrationRefundRequestSchema} from '@/lib/events/registrations/commands/event-registration-refund-request.schema'
import {handleEventRegistrationRefundRequest} from '@/lib/events/registrations/handlers/event-registration-refund-request.handler'
import {evaluateEventRefundEligibility} from '@/lib/events/registrations/event-refund-policy'
import {z} from 'zod'

export async function POST(request: NextRequest, {params}: {params: Promise<{id: string}>}) {
    const {id: eventId} = await params
    const session = await auth()
    const body = await request.json()

    if (!session?.user?.id) {
        return NextResponse.json({error: 'Unauthorized'}, {status: 401})
    }

    const parsed = EventRegistrationRefundRequestSchema.safeParse({
        requestId: body.requestId,
        userId: session.user.id,
        eventId,
        reason: body.reason ?? null
    })
    if (!parsed.success) {
        return NextResponse.json({error: 'Invalid payload', issues: z.treeifyError(parsed.error)}, {status: 400})
    }

    const result = await handleEventRegistrationRefundRequest(parsed.data)
    if ('error' in result) {
        return NextResponse.json({error: result.error}, {status: result.status})
    }
    return NextResponse.json(result.data, {status: result.status})
}

/** E-8 eligibility pre-check + request-status display for the attendee UI. */
export async function GET(_: NextRequest, {params}: {params: Promise<{id: string}>}) {
    const {id: eventId} = await params
    const session = await auth()
    if (!session?.user?.id) {
        return NextResponse.json({error: 'Unauthorized'}, {status: 401})
    }

    const registration = await prisma.eventRegistration.findUnique({
        where: {eventId_userId: {eventId, userId: session.user.id}},
        select: {
            id: true,
            status: true,
            amountPaid: true,
            registeredAt: true,
            event: {select: {occurrences: {select: {startsAt: true, endsAt: true, isCancelled: true}}}},
            refundRequest: {select: {id: true, status: true, requestedAt: true}}
        }
    })
    if (!registration) {
        return NextResponse.json({eligible: false, reason: 'notRegistered', request: null}, {status: 200})
    }

    const eligibility = evaluateEventRefundEligibility({
        status: registration.status,
        amountPaid: registration.amountPaid == null ? null : Number(registration.amountPaid),
        registeredAt: registration.registeredAt,
        occurrences: registration.event.occurrences,
        at: new Date()
    })

    return NextResponse.json(
        {
            eligible: eligibility.eligible && !registration.refundRequest,
            reason: eligibility.eligible ? null : eligibility.reason,
            request: registration.refundRequest
                ? {
                      id: registration.refundRequest.id,
                      status: registration.refundRequest.status,
                      requestedAt: registration.refundRequest.requestedAt.toISOString()
                  }
                : null
        },
        {status: 200}
    )
}
```

- [ ] **Step 8.4: Tests** mirroring `course-enrollment-refund-request.handler.test.ts` (mock prisma module with both named + default exports — house trap): 404 no registration; each ineligibility reason → 400 with its message; existing request any-status → 400; P2002 → 400; happy path → 201 + create args (`sourceType: "event"`, `registrationId`). Route tests: 401 unauth (both verbs); GET shapes (eligible, ineligible reason, existing request). Run: PASS.
- [ ] **Step 8.5: Commit:** `"feat(events): attendee event refund request — handler + POST/GET route (#966)"`

---

### Task 9: Event refund process handler (+ approve/reject stay shared)

**Files:**

- Create: `src/lib/events/registrations/commands/event-registration-refund-process.command.ts` + `.schema.ts` (mirror course: `{requestId?, refundRequestId}`)
- Create: `src/lib/events/registrations/handlers/event-registration-refund-process.handler.ts`
- Modify: `src/lib/courses/enrollments/handlers/course-enrollment-refund-approve.handler.ts` + `…-reject.handler.ts` (observe payload only)
- Test: `src/lib/events/registrations/__tests__/event-registration-refund-process.handler.test.ts`

**Design note (deviation from spec §7 wording, rationale: DRY):** the approve/reject handlers are already source-agnostic — they only flip `RefundRequest.status` and never touch the enrollment. They stay SHARED; each gains `sourceType: true, registrationId: true` in its select and includes both ids in the observe payload. Only **process** gets an event sibling.

- [ ] **Step 9.1: Approve/reject widening** — in both handlers, the `findUnique` select adds `sourceType: true, registrationId: true`; the observe payload adds `sourceType: request.sourceType, registrationId: request.registrationId`. Existing tests must pass unchanged.

- [ ] **Step 9.2: The process handler** (the money path — mirror the course handler structure exactly, with the event gates):

```ts
import {prisma} from '@/lib/prisma'
import {observe} from '@/lib/observability'
import {requireAdmin} from '@/lib/permissions'
import type {EventRegistrationRefundProcessCommand} from '@/lib/events/registrations/commands/event-registration-refund-process.command'
import {generateCreditNoteNumberWithSequence} from '@/lib/billing/helpers/credit-note.helper'
import {enqueueCreditNoteZatca} from '@/modules/billing/zatca/services/zatca-queue.service'
import {evaluateEventRefundEligibility} from '@/lib/events/registrations/event-refund-policy'
import {clawbackSettlementForSource} from '@/lib/settlement/clawback-settlement'
import {Prisma} from '@/generated/prisma/client'

export async function handleEventRegistrationRefundProcess(command: EventRegistrationRefundProcessCommand) {
    const {authorized, error: authError, userId: adminUserId} = await requireAdmin()
    if (!authorized) {
        return {
            error: authError || 'Forbidden',
            status: authError?.includes('Unauthorized') ? 401 : (403 as const)
        }
    }

    const request = await prisma.refundRequest.findUnique({
        where: {id: command.refundRequestId},
        select: {id: true, status: true, sourceType: true, registrationId: true, userId: true, requestedAt: true}
    })
    if (!request) {
        return {error: 'Refund request not found', status: 404 as const}
    }
    if (request.sourceType !== 'event' || !request.registrationId) {
        return {error: 'Refund request is not an event refund', status: 400 as const}
    }
    if (request.status !== 'approved') {
        return {error: 'Refund request is not approved', status: 400 as const}
    }

    const registration = await prisma.eventRegistration.findUnique({
        where: {id: request.registrationId},
        select: {
            id: true,
            eventId: true,
            userId: true,
            status: true,
            amountPaid: true,
            registeredAt: true,
            event: {select: {occurrences: {select: {startsAt: true, endsAt: true, isCancelled: true}}}}
        }
    })
    if (!registration) {
        return {error: 'Registration not found', status: 404 as const}
    }

    // Snapshot-at-request (spec §4 / EXP-129): time gates evaluate against
    // requestedAt — a timely request never expires in the admin queue. State
    // gates (still completed, paid) re-check current reality below via the
    // policy's status/amount fields read NOW.
    const eligibility = evaluateEventRefundEligibility({
        status: registration.status,
        amountPaid: registration.amountPaid == null ? null : Number(registration.amountPaid),
        registeredAt: registration.registeredAt,
        occurrences: registration.event.occurrences,
        at: request.requestedAt
    })
    if (!eligibility.eligible) {
        return {error: 'Registration is not eligible for refund', status: 400 as const}
    }

    const invoice = await prisma.invoice.findFirst({
        where: {
            userId: registration.userId,
            contentType: 'event',
            contentId: registration.eventId
        },
        orderBy: {createdAt: 'desc'},
        select: {id: true, totalAmount: true, billingAddress: true, issuedAt: true}
    })
    if (!invoice) {
        return {error: 'Invoice not found', status: 404 as const}
    }

    const existingCredit = await prisma.creditNote.findFirst({
        where: {invoiceId: invoice.id},
        select: {id: true}
    })
    let creditNoteId = existingCredit?.id ?? null
    if (!creditNoteId) {
        const {creditNoteNumber, creditNoteSequence, creditNoteYear} = await generateCreditNoteNumberWithSequence(
            prisma,
            'CRN',
            invoice.issuedAt.getFullYear()
        )
        const creditNote = await prisma.creditNote.create({
            data: {
                invoiceId: invoice.id,
                creditNoteNumber,
                creditNoteSequence,
                creditNoteYear,
                creditNotePrefix: 'CRN',
                amount: invoice.totalAmount,
                reason: 'Event refund',
                issuedAt: new Date(),
                billingAddress: invoice.billingAddress as Prisma.InputJsonValue
            }
        })
        creditNoteId = creditNote.id
    }

    // Interactive tx — same snapshot rationale as the course handler (#936/#962).
    const {cancelledCommissions, cancelledEarningsCount, platformLossAmount} = await prisma.$transaction(async (tx) => {
        const clawback = await clawbackSettlementForSource(tx, {
            sourceType: 'event',
            sourceId: registration.id,
            adminUserId: adminUserId ?? null,
            refundRequestId: request.id
        })

        await tx.eventRegistration.update({
            where: {id: registration.id},
            data: {status: 'refunded', cancelledAt: new Date()}
        })
        // #916 mirror: claw back the affiliate commission in the SAME transaction.
        const cancelledCommissions = await tx.commission.updateMany({
            where: {
                userId: registration.userId,
                itemType: 'event',
                itemId: registration.eventId,
                status: {in: ['pending', 'approved']}
            },
            data: {status: 'cancelled', holdReason: 'purchase_refunded'}
        })
        await tx.refundRequest.update({
            where: {id: request.id},
            data: {status: 'processed', resolvedAt: new Date()}
        })

        return {cancelledCommissions, ...clawback}
    })

    if (creditNoteId) {
        await enqueueCreditNoteZatca(creditNoteId, command.requestId)
    }

    observe(
        'event.refund.processed',
        {
            requestId: command.requestId,
            refundRequestId: request.id,
            registrationId: registration.id,
            creditNoteId,
            cancelledCommissions: cancelledCommissions.count,
            cancelledEarnings: cancelledEarningsCount,
            platformLossAmount
        },
        {level: 'warn', dedupeKey: `event.refund.processed:${request.id}`}
    )

    return {data: {processed: true, creditNoteId}, status: 200 as const}
}
```

- [ ] **Step 9.3: Tests** mirroring the course admin-handlers suite (interactive-`$transaction` mock supporting the callback form): 401/403; 404 request; wrong sourceType → 400; not-approved → 400; snapshot semantics — request filed in-window but processed AFTER event start → STILL processes (assert `at` = `requestedAt`); registration now `refunded` (state gate) → 400 via `alreadyRefunded`; invoice 404; existing credit note reused (no create); clawback called with `("event", registrationId)`; commission updateMany args (`itemType: "event"`); registration flipped to `refunded` (NOT `cancelled`); ZATCA enqueue after tx; observe payload fields.
- [ ] **Step 9.4: Run + commit:** `"feat(events): event refund process handler — credit note + ZATCA + shared clawback + commission clawback (#966)"`

---

### Task 10: Admin route dispatch by sourceType

**Files:**

- Modify: `app/api/v1/admin/refunds/[id]/process/route.ts`
- Test: extend its existing route tests (or create `app/api/v1/admin/refunds/[id]/process/__tests__/route.test.ts` if none)

- [ ] **Step 10.1:** After the existing zod parse, load the request's `sourceType` and dispatch (course handlers keep their non-null `enrollmentId` assumption):

```ts
import {prisma} from '@/lib/prisma'
import {handleEventRegistrationRefundProcess} from '@/lib/events/registrations/handlers/event-registration-refund-process.handler'
// existing imports stay

const refundRequest = await prisma.refundRequest.findUnique({
    where: {id},
    select: {sourceType: true}
})
if (!refundRequest) {
    return NextResponse.json({error: 'Refund request not found'}, {status: 404})
}

const result =
    refundRequest.sourceType === 'event'
        ? await handleEventRegistrationRefundProcess(parsed.data)
        : await handleCourseEnrollmentRefundProcess(parsed.data)
```

Approve/reject routes are untouched (their handlers are shared per Task 9).

- [ ] **Step 10.2: Tests:** event-sourced id dispatches to the event handler; course-sourced to the course handler; unknown id → 404. Run, then `pnpm typecheck:touched -- app/api/v1/admin/refunds/[id]/process/route.ts`. Commit `"feat(admin): refund process route dispatches by sourceType (#966)"`.

---

### Task 11: Neutral admin refunds query + discriminated DTO (module move)

**Files:**

- Create: `src/lib/billing/refunds/dto/refund-request.dto.ts`
- Create: `src/lib/billing/refunds/queries/refund-request.query.ts`
- Delete: `src/lib/courses/enrollments/dto/refund-request.dto.ts`, `src/lib/courses/enrollments/queries/refund-request.query.ts` (after re-pointing importers — find them ALL with `grep -rln "enrollments/dto/refund-request.dto\|enrollments/queries/refund-request.query" app/ src/`)
- Modify: `app/api/v1/admin/refunds/route.ts` (import path), `app/(i18n)/_shared/admin/refunds/_components/refunds-table.tsx` (import path; UI in Task 12)
- Test: move + extend the existing query tests under `src/lib/billing/refunds/__tests__/refund-request.query.test.ts`

- [ ] **Step 11.1: Discriminated DTO:**

```ts
export type RefundRequestAdminDTO = {
    id: string
    sourceType: 'course' | 'event'
    status: string
    reason: string | null
    requestedAt: string
    resolvedAt: string | null
    /** Course-sourced rows only. */
    enrollment: {id: string; status: string; progress: number; enrolledAt: string} | null
    course: {id: string; title: string; publishingStatus: string} | null
    /** Event-sourced rows only. */
    registration: {id: string; status: string; registeredAt: string} | null
    event: {id: string; title: string; startsAt: string | null} | null
    user: {id: string; email: string | null; username: string | null; fullName: string | null}
}
```

- [ ] **Step 11.2: Widened query** — same skeleton as the current `getRefundRequests`, with these exact deltas:
    - `baseWhere` becomes source-aware (the §7 trap: the publishingStatus relation filter must apply to COURSE rows only or every event row is silently hidden):

```ts
const baseWhere: Prisma.RefundRequestWhereInput = {
    OR: [{sourceType: 'course', enrollment: {course: {publishingStatus: 'published'}}}, {sourceType: 'event'}],
    ...(input.status ? {status: input.status} : {})
}
```

- `select` adds `sourceType: true` and the event side:

```ts
        registration: {
          select: {
            id: true,
            status: true,
            registeredAt: true,
            event: {
              select: {
                id: true,
                title: true,
                occurrences: {
                  where: {isCancelled: false},
                  orderBy: {startsAt: "asc"},
                  take: 1,
                  select: {startsAt: true},
                },
              },
            },
          },
        },
```

- search: `uuid` list adds `"registrationId"`; `text` list adds `"registration.event.title"`; the invoice-correlation block widens — query invoices with `contentType: {in: ["course", "event"]}` and map matches to `OR` clauses: course `{userId, enrollment: {courseId: contentId}}`, event `{userId, registration: {eventId: contentId}}` (select `contentType` too and branch on it).
- mapper emits the discriminated shape (`enrollment`/`course` null on event rows and vice versa; `event.startsAt` from `occurrences[0]?.startsAt?.toISOString() ?? null`).
- [ ] **Step 11.3:** Re-point ALL importers to `@/lib/billing/refunds/...`, delete the old files, and prove no stragglers: `pnpm typecheck:touched -- app/api/v1/admin/refunds/route.ts "app/(i18n)/_shared/admin/refunds/_components/refunds-table.tsx" src/lib/billing/refunds/queries/refund-request.query.ts` plus `grep -rn "enrollments/dto/refund-request\|enrollments/queries/refund-request" app/ src/` → zero hits.
- [ ] **Step 11.4: Tests:** course rows render exactly as today (regression: same DTO fields populated); event rows appear WITHOUT the publishingStatus filter (mock both kinds); archived-course rows still excluded; search by event title and by registrationId. Run + commit `"refactor(billing): neutral refunds admin query/DTO with discriminated course|event shape (#966)"`.

---

### Task 12: Admin refunds table UI + i18n

**Files:**

- Modify: `app/(i18n)/_shared/admin/refunds/_components/refunds-table.tsx`
- Modify: `src/i18n/messages/en/admin.json`, `ar/admin.json`, `es/admin.json` (`refunds` namespace)
- Test: extend the existing refunds-table test (renderToStaticMarkup convention)

- [ ] **Step 12.1:** Add a `source` chip column and replace the course-title column with a generic content column:

```tsx
  // in the columns array
  {
    key: "source",
    header: t("sourceHeader"),
    cell: (refund) => (
      <StatusBadge status="neutral">
        {refund.sourceType === "event" ? t("sourceEvent") : t("sourceCourse")}
      </StatusBadge>
    ),
  },
  {
    key: "content",
    header: t("contentHeader"),
    cell: (refund) => refund.course?.title ?? refund.event?.title ?? "—",
  },
```

All `refund.course.title` / `refund.enrollment.…` accesses become null-safe (`?.` with `"—"` fallback) — tsc enforces this after Task 11's DTO change. Process/approve/reject action buttons are unchanged (same routes; dispatch happens server-side).

- [ ] **Step 12.2: i18n** — add to `admin.json` `refunds` in all three locales:

```json
"sourceHeader": "Source",
"contentHeader": "Content",
"sourceCourse": "Course",
"sourceEvent": "Event"
```

(ar: `"المصدر"`, `"المحتوى"`, `"دورة"`, `"فعالية"`; es: `"Origen"`, `"Contenido"`, `"Curso"`, `"Evento"`.)

- [ ] **Step 12.3:** Update/extend the table test: an event-sourced DTO row renders the event title + Event chip; a course row renders identically to before. Run + `pnpm typecheck:touched`. Commit `"feat(admin): refunds queue renders event refunds — source chip + content column (#966)"`.

---

### Task 13: Attendee refund UI (E-8)

**Files:**

- Create: `src/lib/events/detail/sections/event-refund-section.tsx`
- Modify: `src/lib/events/detail/sections/event-detail-sidebar.tsx` (mount inside `RegisteredState`, ~line 528)
- Modify: `src/i18n/messages/{en,ar,es}/events.json` (`detail.refund` namespace)
- Test: `src/lib/events/detail/sections/__tests__/event-refund-section.test.tsx`

- [ ] **Step 13.1: The section component** (constellation rules: error-before-skeleton, eligibility-aware, friendly states):

```tsx
'use client'

import {useState} from 'react'
import {Button} from '@heroui/react'
import {useTranslations} from 'next-intl'
import {toast} from 'sonner'
import {useApiQuery} from '@/lib/api/use-api-query'

type RefundEligibilityDTO = {
    eligible: boolean
    reason: string | null
    request: {id: string; status: string; requestedAt: string} | null
}

export function EventRefundSection({eventId}: {eventId: string}) {
    const t = useTranslations('events.detail.refund')
    const [submitting, setSubmitting] = useState(false)
    const {data, error, mutate} = useApiQuery<RefundEligibilityDTO>(`/api/v1/events/${eventId}/refund`, {revalidateOnFocus: false})

    // Quiet section: fetch failure or still loading → render nothing (the refund
    // affordance is secondary; never block the registered state on it).
    if (error || !data) return null

    if (data.request) {
        return (
            <p className="text-muted-foreground text-xs" data-testid="refund-status">
                {t('statusLabel')} {t(`status.${data.request.status}`)}
            </p>
        )
    }

    if (!data.eligible) return null

    const onRequest = async () => {
        setSubmitting(true)
        try {
            const res = await fetch(`/api/v1/events/${eventId}/refund`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({})
            })
            const body = await res.json().catch(() => ({}))
            if (!res.ok) {
                toast.error(body.error ?? t('requestFailed'))
                return
            }
            toast.success(t('requested'))
            await mutate()
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <Button variant="ghost" size="sm" className="w-full" isDisabled={submitting} onPress={onRequest}>
            {t('requestRefund')}
        </Button>
    )
}
```

(Match the file's actual Button import/variant conventions to the surrounding sidebar code — it uses `buttonVariants` from the local cn/button utilities in places; follow whichever pattern `event-detail-sidebar.tsx` already uses for secondary actions.)

- [ ] **Step 13.2: Mount it** at the bottom of `RegisteredState` in `event-detail-sidebar.tsx` (inside the outer `div`, after the joining-instructions block). `RegisteredState` receives `event: EventDTO` — pass `eventId={event.id}`:

```tsx
<EventRefundSection eventId={event.id} />
```

- [ ] **Step 13.3: i18n** — `events.json` → `detail.refund` in en/ar/es:

```json
"refund": {
  "requestRefund": "Request refund",
  "requested": "Refund request submitted",
  "requestFailed": "Could not submit the refund request",
  "statusLabel": "Refund:",
  "status": {
    "requested": "requested — under review",
    "approved": "approved — processing",
    "processed": "processed",
    "rejected": "rejected"
  }
}
```

(Provide real ar/es translations, not transliterations — ar e.g. `"طلب استرداد"`, `"تم إرسال طلب الاسترداد"`, `"تعذر إرسال طلب الاسترداد"`, `"الاسترداد:"`, statuses `"قيد المراجعة"`, `"تمت الموافقة — قيد المعالجة"`, `"تم الاسترداد"`, `"مرفوض"`.)

- [ ] **Step 13.4: Test** via the house `renderToStaticMarkup` convention (mock `useApiQuery`, `next-intl`, HeroUI): request-exists → status line; eligible → button markup; ineligible/error → renders nothing. Run + commit `"feat(events): attendee refund request UI on the event detail registered state (#966)"`.

---

### Task 14: AI fact line + seeder event branch

**Files:**

- Modify: `src/lib/ai/ask/ask-ai-assistant.ts:77`
- Modify: `prisma/seeders/20-settlements.ts`

- [ ] **Step 14.1:** Replace the stale 48h fact (line 77) with:

```ts
      "Live events follow the same seven (7) day refund window measured from registration, and the request must be made before the event's first occurrence starts; once the event has started or taken place, no refund is issued.",
```

- [ ] **Step 14.2: Seeder** — in `20-settlements.ts`, after the subscription settle loop, add an event pass (same shape as the course pass: real writer, bounded):

```ts
const eventRegistrations = await prisma.eventRegistration.findMany({
    where: {status: 'completed', amountPaid: {gt: 0}},
    select: {id: true},
    take: 100
})
for (const r of eventRegistrations) {
    await recordOrderSettlement({sourceType: 'event', sourceId: r.id})
}
```

(Adapt variable naming/log lines to the file's existing logSection/logSuccess style and include the count in the returned summary object.)

- [ ] **Step 14.3:** `pnpm typecheck:touched -- src/lib/ai/ask/ask-ai-assistant.ts prisma/seeders/20-settlements.ts`, commit `"chore(events): AI refund fact realignment + seeder event settlements (#966)"`.

---

### Task 15: Full gates, reviewer panel, ship

- [ ] **Step 15.1: Full app gate:**

```bash
cd apps/experts-app
DATABASE_URL=postgresql://localhost/experts_test pnpm experts:test
pnpm experts:check        # FORMAT/LINT/TYPECHECK — on failure: pnpm experts:check:fix, re-run
pnpm db:check:drift
```

All green before anything else.

- [ ] **Step 15.2: Reviewer panel (mandatory, BEFORE push):** spawn in parallel on `git diff origin/main`: `code-reviewer`, `qa-tester`, AND `security-auditor` (money path). Triage: fix real findings before push; re-run the gate after fixes. Then `release-manager` LAST on the committed state for GO/NO-GO.
- [ ] **Step 15.3: Ship per experts-ship:** verify branch (`git branch --show-current`), push explicit `git push -u origin feat/gh-966-event-settlement-refunds:feat/gh-966-event-settlement-refunds`, verify remote SHA (`git ls-remote`), open PR with body covering: spec/plan links, the E-1..E-8 decisions, the Task 3 ordering note, the Task 7 wire-placement note, the Task 9 approve/reject-stay-shared note, a **Functional Impact** section (house rule for guard-adding changes: enumerates previously-working flows touched — registration upsert paths, admin queue, course refund regression), and `Closes #966`. Watch CI → squash-merge → **sentinel-verify on origin/main** (grep `clawbackSettlementForSource` in the merged tree — never trust state=MERGED) → resync + `npx gitnexus analyze`.

---

## Self-review (done at write time)

- **Spec coverage:** E-1/§2.1 → Task 2; E-2 flow → Tasks 8-10; E-3 schema → Task 1; E-4 payableAt → Task 4; E-5 extraction → Task 3; E-6 → Task 7; E-7 → Task 8 (any-status block + plain unique); E-8 → Task 13; §5.1 commission clawback + holdUntil → Tasks 6, 9; §6 writer/reconcile/rollout → Tasks 4-5 (flag posture needs no code — writer already gates); §7 admin dispatch/queue/AI fact → Tasks 10-12, 14; cleanup handler → no code change (table-wide already; spec-confirmed); §9 testing → embedded per task incl. regression + snapshot + race cases; §10 sequencing → task order.
- **Known intentional deviations (each flagged in its task + the PR body):** Task 3 in-tx operation order; Task 7 wire placement before the early-return rather than after ZATCA enqueue; Task 9 approve/reject staying shared.
- **Type consistency:** `clawbackSettlementForSource` returns `{cancelledEarningsCount, platformLossAmount}` — used with those exact names in Tasks 3 and 9. `evaluateEventRefundEligibility` input/return shapes match across Tasks 2, 8, 9. DTO field names in Task 11 match the Task 12 cell accessors.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
