---
title: "2026 06 09 instructor settlement design"
date: "2026-06-09"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/specs/2026-06-09-instructor-settlement-design.md"
---
# Instructor / Creator Settlement & Payouts — Design (#936)

**Date:** 2026-06-09
**Issue:** [#936](https://github.com/logi-x/experts/issues/936) — _No instructor/creator settlement or payout is implemented_
**Status:** Approved design, pre-implementation
**Scope of this spec:** the settlement **earnings ledger** + **instructor payout** flow (full #936). Discounts (#935) and the discount-UI decouple (#937) are explicit follow-on cycles.

---

## 1. Problem

On a paid sale the platform records the enrollment, invoices the buyer (full price + VAT), enqueues ZATCA, and optionally credits an affiliate — and **nothing else**. No platform/instructor split is computed, no instructor earning is recorded, and there is no instructor payout path. The system cannot answer "how much do we owe each instructor?" from the data it records. The split math (`priceOrder` / `settlement-config`, `DEFAULT_INSTRUCTOR_SPLIT_FRACTION = 0.8`) exists but is imported **only by React components** — it is a preview calculator, not the cash register.

## 2. Confirmed decisions (operator input)

| #   | Decision              | Value                                                                                          | Consequence                                                                                                                                                                                                                                                                       |
| --- | --------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D-1 | Operational reality   | **Greenfield** — no instructor payouts happen today; pre-revenue-share                         | No backfill, no reconciliation against money already owed; ledger starts clean at go-live                                                                                                                                                                                         |
| D-2 | Spec scope            | **Full #936** — ledger + payouts in one spec                                                   | Discounts (#935/#937) are separate cycles                                                                                                                                                                                                                                         |
| D-3 | Split granularity     | **Per-contributor by `revenueShare`**                                                          | One earning line per (order × contributor); subscriptions → single plan owner                                                                                                                                                                                                     |
| D-4 | Payout disbursement   | **Manual admin record-keeping**, mirror affiliate                                              | No PSP integration in v1                                                                                                                                                                                                                                                          |
| D-5 | Instructor tax docs   | **Internal ledger only**; self-billing deferred                                                | `CreatorPayoutMethod.vatRegistered` is the future attach point; flag for a compliance phase with a lawyer                                                                                                                                                                         |
| D-6 | Ledger architecture   | **Parent settlement + per-contributor lines** (Approach 1)                                     | Mirrors `Invoice`/`InvoiceLine`; platform revenue first-class                                                                                                                                                                                                                     |
| D-7 | Write delivery        | **Inline fault-isolated write** + reconciliation sweep (no worker) — _superseded D-7, see §11_ | Runs in the request context where Prisma works; cron-sweep backstop. (Original "worker, mirror ZATCA" was infeasible — see §11.)                                                                                                                                                  |
| D-8 | Ship gating (R3)      | **Behind an off-by-default kill-switch flag** (`SETTLEMENT_LEDGER_ENABLED`)                    | Plan A accrues nothing until the flag is flipped after Plan B deploys → no dark-ledger liability window.                                                                                                                                                                          |
| D-9 | v1 product scope (R3) | **Courses + subscriptions only — events EXCLUDED from v1**                                     | No event refund flow exists, so event earnings could not be clawed back (operator chose block-not-defer). Events (settlement + an event refund flow + clawback, shipped together) are a later phase. Subscriptions are platform-only → no creator earning → no clawback exposure. |

**Mental model (the four layers):**

> Parent settlement = financial truth of the order · Earning lines = payable obligations to creators · Payouts = payment execution · Balance view = reporting/projection.

## 3. Architecture

### 3.1 `priceOrder` becomes the single server-side source of truth

Relocate the split math from the components layer (`src/lib/orders/price-order.ts` + `src/lib/pricing/settlement-config.ts`) to a **server-importable** module (e.g. `src/lib/settlement/price-order.ts`) with **zero behavior change** (pure relocation + re-export, guarded by the existing `price-order.test.ts`). The creator preview UI and the new settlement writer then import the **same** function — preview and reality cannot drift.

> Clarification: `instructorSplitFraction` (0.8) is the **platform↔instructor** split. `revenueShare` (on `CourseInstructor`/`EventHost`, validated to sum to 1 at publish) divides the **instructor pool** among co-creators. They are different dimensions; the design uses both.

### 3.2 Settlement write slots into each completion orchestrator

The three completion paths (course / event / subscription) are copy-paste siblings. After the existing steps, add one new step that calls a **single shared settlement writer** (not pasted three times):

```
completion orchestrator (course / event / subscription)
  ├─ mark enrollment/registration/subscription completed   (exists)
  ├─ create Invoice + InvoiceLine                            (exists)
  ├─ enqueue ZATCA                                           (exists)
  ├─ affiliate attribution → Commission                     (exists)
  └─ enqueue settlement job → OrderSettlement + lines        (NEW)   ← idempotent
```

Writer (conceptual): `recordOrderSettlement({ sourceType, sourceId, buyerUserId, itemType, itemId, itemTitle, grossPaid, vatRate, affiliateCommissionAmount, contributors[] }) → void`.

## 4. Data model

All new models in the `billing` schema; money as `Decimal(10,2)`; status vocabularies mirror the affiliate analogs so the balance view reuses the same SQL shape.

### 4.1 `OrderSettlement` — financial truth of the order (one per sale)

```
id  ·  sourceType ("course"|"event"|"subscription")  ·  sourceId (enrollment/
registration/subscription row id)  ·  buyerUserId  ·  itemType/itemId/itemTitle  ·
currency  ·  grossPaid  ·  vatRate  ·  vatAmount  ·  netExVat  ·  gatewayFee  ·
gatewayFeeFraction  ·  distributable  ·  splitFraction  ·  platformShare  ·
instructorShare  ·  affiliatePayout  ·  discountInstructorCost (0 until #935)  ·
platformEarning  ·  instructorNetTotal  ·  status ("recorded"|"reversed")  ·
createdAt / updatedAt  ·  lines CreatorEarning[]
@@unique([sourceType, sourceId])          ← idempotency guard
@@schema("billing")
```

### 4.2 `CreatorEarning` — payable obligation to a creator (repurposes the empty `contributor_earnings` stub)

```
id  ·  settlementId (FK → OrderSettlement)  ·  creatorUserId  ·
role ("primary"|"secondary"|"host")  ·  itemType/itemId/itemTitle (denormalized)  ·
currency  ·  shareFraction (this creator's revenueShare)  ·
netAmount (= instructorEarning × shareFraction)  ·
status ("pending"→"approved"→"paid"|"cancelled")  ·  holdReason  ·  payableAt  ·
approvedAt  ·  payoutId (FK → CreatorPayout)  ·  createdAt / updatedAt
@@index([creatorUserId, status])     @@map("contributor_earnings")   @@schema("billing")
```

`approved` = past the refund window, payable. `paid` = included in a completed payout. `cancelled` = clawed back on refund.

### 4.3 `CreatorPayout` — payment execution (mirrors `AffiliatePayout` 1:1)

```
id · creatorUserId · amount · currency · method · status ("pending"→"processing"→
"completed"|"failed") · transactionId · notes · processedAt · processedBy ·
periodStart · periodEnd · createdAt · earnings CreatorEarning[]
@@index([creatorUserId, status, periodStart])    @@schema("billing")
```

### 4.4 `CreatorBalance` — projection (DB view, mirrors `AffiliateBalance`)

```
creatorUserId (PK) · totalAmount · pendingAmount (status=pending) ·
payableAmount (status=approved) · paidAmount (status=paid)
@@schema("billing")
```

### 4.5 Supporting additions

- **`CreatorPayoutMethod`** (`billing`): `creatorUserId · method · bank/IBAN details · vatRegistered (bool) · vatNumber?`. Gates a payout request the same way the `Affiliate` payment method gates affiliate payouts; `vatRegistered`/`vatNumber` are the deferred self-billing hook (D-5).
- **Reconciliation guard:** the writer asserts `Σ line.netAmount == settlement.instructorNetTotal` (within rounding tolerance) before commit — a misallocated split fails loudly rather than silently shorting a creator.

### 4.6 Migrations

New `OrderSettlement`, `CreatorPayout`, `CreatorPayoutMethod` models; expand `contributor_earnings` in place (safe — empty); `CreatorBalance` view. Hand-authored SQL per the repo's no-`prisma format` / drift-gate rules (`pnpm db:check:drift`).

## 5. The settlement write (money flow)

### 5.1 Resolving `contributors[]`

- **Course** → `CourseInstructor` rows (`revenueShare`, role).
- **Event** → `EventHost` rows (`revenueShare`, role).
- **Subscription** → the plan's single owner, `shareFraction = 1`.
- **Defensive fallback:** if shares don't sum to 1 (legacy/unpublished edge), attribute 100% to the primary contributor and emit a warning observation.

### 5.2 The math

Call server `priceOrder({ grossPaid: amountPaid, vatRate: 0.15, instructorSplitFraction: 0.8, gatewayFeeFraction: 0.025, affiliate })`. **The affiliate commission amount is passed in from the attribution step that just ran — not re-derived** — so `priceOrder`'s `instructorEarning` nets the instructor-funded affiliate payout **exactly once** (the explicit "net once, not twice" requirement from #936). Each line: `netAmount = instructorEarning × shareFraction`. Reconciliation guard checks the sum. Parent + lines write in one transaction.

### 5.3 `payableAt`

From the existing `revenue.service` helpers: `calculatePayableDate(completedAt)` (courses/subscriptions), `calculateEventPayableDate(eventEndDate)` (events) — 7-day refund window (`DEFAULT_REFUND_WINDOW_DAYS`). Lines are born `pending`.

### 5.4 Idempotency & delivery

`@@unique([sourceType, sourceId])` → re-running a completion no-ops (webhook + redirect both firing, retries, replays). Delivered as a **BullMQ worker job** keyed on `(sourceType, sourceId)`, mirroring `enqueueInvoiceZatca`: the job re-resolves order facts from the DB and writes the settlement; retriable; off the buyer's hot path. A **settlement-write failure must never turn the buyer's success response into a failure** (the `PaymentCapturedInvoiceError` lesson). A **reconciliation sweep cron** finds any completed sale lacking a settlement and enqueues it — the backstop.

## 6. Earning lifecycle & refund clawback

- **Maturation (`pending → approved`):** a cron flips lines whose `payableAt` has passed and whose source isn't refunded; stamps `approvedAt`. Uses a **status-guarded `updateMany`** (`where: status="pending"`) per the #956 TOCTOU lesson — never a blind update.
- **Refund clawback:** the existing `course-enrollment-refund-process.handler.ts` (#916) is extended **in the same atomic transaction** that flips the enrollment and cancels the affiliate commission: cancel this order's `CreatorEarning` lines (`pending`/`approved` only → `cancelled`, `holdReason="purchase_refunded"`) and mark the `OrderSettlement` `reversed`. **`paid` earnings are not auto-clawed** (money's out — manual decision, like affiliate). Wires into the **course** refund flow now; event/subscription clawback follows when those refund flows exist.

## 7. Payout flow (mirrors the affiliate machine 1:1)

- **Creator requests** (`POST .../creators/payouts/request`): guards — authenticated creator · `CreatorPayoutMethod` set · `CreatorBalance.payableAmount ≥ 100 SAR` (same threshold as affiliate) · no existing `pending` payout. Creates `CreatorPayout(pending)`, links all `approved`+unpaid earning lines via `payoutId`, sets the period window.
- **Admin processes** (`POST /admin/creator-payouts/[id]/process`): admin guard · status guard `pending → processing|completed|failed` · idempotent. On `completed`, one transaction marks the payout `completed` (`processedAt/By`, `transactionId`, `notes`) and flips its linked earnings to `paid`, using a **status-guarded `updateMany`** (#956) so a double-process can't double-pay.
- **`CreatorBalance` view** gates the request and powers reporting.

## 8. Surfaces (per `experts-constellation`)

- **Creator earnings dashboard:** `CreatorBalance` summary (pending/payable/paid `StatCard`s), earnings list (`DataTable` + status badges), **Request payout** action (gated on method + threshold), and a `CreatorPayoutMethod` form (bank/IBAN + `vatRegistered`). Full vertical slice — DTO → query → route → hook → component, four states, RTL/i18n (en+ar+es), a11y, node-env tests.
- **Admin creator-payouts queue:** mirrors the affiliate payouts admin surface — list + `buildAdminSearch` filter, detail drawer of linked earnings, **Process** action. New `CreatorPayoutDTO` / `CreatorEarningDTO` (parallel to `AffiliatePayoutDTO`, not shared). Every admin route enforces `requireAdmin()`.

## 9. Testing

- **Pure units:** split allocator (sum-reconciliation, rounding, primary-fallback), `payableAt` helpers, balance projection, status→badge.
- **Settlement writer:** idempotency on `(sourceType, sourceId)`, affiliate-netted-once, multi-contributor split sums to instructor net, single-contributor subscription, worker job + reconciliation-sweep-finds-gaps.
- **Lifecycle:** maturation TOCTOU guard; refund clawback cancels `pending`/`approved` only, leaves `paid`, reverses the settlement, atomic.
- **Payout:** request guards (threshold / method / one-pending); admin process state machine + double-process TOCTOU guard.
- **Surfaces:** `renderToStaticMarkup` component tests, stale-rows-on-error.

## 10. Out of scope (deferred, with hooks left in)

- **Discount redemption (#935) + UI decouple (#937)** — separate cycles. `discountInstructorCost` stays `0` until then.
- **Self-billing / instructor ZATCA tax document** — deferred to a compliance phase; `CreatorPayoutMethod.vatRegistered` is the attach point (D-5).
- **ALL EVENT settlement** — excluded from v1 (D-9). Events join in a later phase that ships event settlement **with** an event refund flow + clawback together. v1 = **courses + platform-only subscriptions**.
- **Subscription renewal settlement** — Plan B settles the initial subscription checkout; recurring renewals are a follow-on (verify whether a renewal makes a new `Subscription` row first).
- **Automated PSP disbursement** — manual admin record-keeping for v1 (D-4).
- **Per-content split override** — v1 uses the `0.8` platform/instructor default.

## 11. Implementation refinements (post-exploration, 2026-06-09)

Verified against the codebase while writing the implementation plan; these refine §5–§7 without changing the decisions:

- **Subscriptions are platform memberships (RESOLVED 2026-06-09).** Operator decision: subscription plans are platform-wide memberships, **no creator earns** from a subscription sale. So **Plan A settles courses + events only**, and subscription settlement moves to **Plan B** as a _platform-only_ path: an `OrderSettlement` with `platformEarning` = the whole net and **zero `CreatorEarning` lines**. No `Plan.ownerId` needed. Wrinkle: with no instructor to fund it, an affiliate commission on a subscription is **platform-funded** (reduces `platformEarning`), so subscriptions use a dedicated compute path, not the instructor-split `priceOrder` call.
- **Crons are internal API routes, not BullMQ-repeatable jobs.** The house pattern (storage-janitor) is a pure sweep function called by a thin worker **and** by a cron-sidecar-hit `POST /api/v1/internal/...` route. So maturation (`pending→approved`) and the reconciliation sweep are internal routes wrapping pure functions, not repeatable queue jobs.
- **Delivery is INLINE + a reconciliation sweep — there is no settlement worker (supersedes D-7).** The round-2 review caught that `tsup` bundles workers _framework-free (no Prisma)_, so a DB-re-resolving BullMQ worker would crash on its first query (the ZATCA worker is pure-compute fed a snapshot, not a DB reader). Resolution: `recordOrderSettlement({sourceType, sourceId})` is called **inline and fault-isolated** in the completion orchestrators (the Next.js request context has Prisma), and an internal `CRON_SECRET`-guarded reconciliation route backfills any inline failure. The writer re-resolves order facts (content → `CourseInstructor`/`EventHost` → affiliate `Commission`) from the DB, idempotent on `(sourceType, sourceId)` with **P2002-as-success**; the affiliate commission is re-queried (attribution returns `void`) and adapted to `AffiliateMetadata {commissionType:"fixed", commissionValue, fundedBy:"INSTRUCTOR"}` so it nets once. **Key invariants** (from the review): write only when source `status==="completed"`; clawback keyed on the settlement `(sourceType, sourceId)` not the buyer; `onDelete: Restrict` on ledger relations; a non-positive instructor net is recorded platform-only (zero lines). Course/event gross is read from the row; subscription gross from the `Invoice` (no `amountPaid` column).

## 12. Open questions for follow-up phases

- **Subscription renewals:** do recurring renewals flow through a completion handler (Stripe subscription webhooks)? Each renewal cycle would be its own (platform-only) settlement — Plan B settles the initial checkout; renewals are a follow-on.
- **Event refund clawback:** only the _course_ refund flow exists today (#916). Whether an event refund flow exists must be verified before extending earning clawback to events (Plan B/C).
- **Self-billing tax treatment:** requires a compliance advisor before building (D-5). **Operator warning:** until self-billing exists, do not process payouts to VAT-registered creators (the admin process UI must gate/warn on `CreatorPayoutMethod.vatRegistered`).

## 13. Round-3 review resolutions (2026-06-09)

An 8-lens panel (workflow, concept, code, architecture, product, exhaustive fact-check, db, money-path security) reviewed the revised docs. Zero remaining factual errors; all round-1/2 fixes confirmed folded. Resolutions now baked into the plans:

- **Ship behind `SETTLEMENT_LEDGER_ENABLED` (default off) (D-8).** The inline write and the cron routes no-op when the flag is off; flip on only after Plan B's payout path deploys. Eliminates the dark-ledger liability window the PM flagged.
- **Courses + subscriptions only; events excluded (D-9).** See §10.
- **State machine — payout `processing` was a dead-end.** The admin process route must allow transitions from `{pending, processing}`, not just `pending`, or a payout stuck in `processing` strands its earnings forever. Plus: a refund clawback on an earning already linked to a pending payout must also cancel/adjust that payout (Plan B refund-clawback extension).
- **Money correctness:** the affiliate `Commission` re-query excludes `paid` (`notIn:['cancelled','paid']`) so a late reconcile can't double-deduct an already-paid commission; the payout amount is computed **inside** the link transaction from the actually-linked earnings (not a stale balance read).
- **Prisma reality:** `updateMany` cannot filter by a relation — maturation is a two-step (`findMany` eligible ids → `updateMany` by id). Subscription settlement gates on **Invoice existence**, not `Subscription.status`. Subscriptions get their own reconciliation backstop.
- **DB:** `revenueShare` is `Decimal(5,2)` at source — the resolver must handle the **partial-null shares** case explicitly (warn + fallback, not silent 100%-primary); the `CreatorBalance` view uses bare `@db.Decimal` (mirror `AffiliateBalance`) and is null-coalesced for zero-earning creators; `OrderSettlement` carries an "internal ledger — not a ZATCA document" comment to justify the `recorded→reversed` status mutation.
- **Hardening:** stats route is `POST` + `CRON_SECRET` (unambiguous); payout-method zod-validates IBAN (`@db.VarChar(34)` + format); creator error responses do NOT mirror the affiliate `details` debug payload; refund observes `platformLossAmount` when paid earnings can't be clawed; the 100 SAR threshold becomes a named `settlement-config` constant.
- **Ops:** the three internal cron routes need Docker cron-sidecar wiring + `CRON_SECRET` in the deploy checklist (called out in the plans' final gate).
- **One real-DB integration test** for `recordOrderSettlement` (mocks hid the round-2 `Event.endDate` error).

## 13. Reference anchors (current code)

| Concept                   | File                                                                                                        | Notes                                                                          |
| ------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Split math                | `src/lib/orders/price-order.ts`, `src/lib/pricing/settlement-config.ts`                                     | `priceOrder → PriceOrderBreakdown`; component-only today                       |
| Course completion         | `src/lib/courses/enrollments/orchestrators/course-enrollment-complete.orchestrator.ts`                      | settlement step slots after affiliate attribution                              |
| Event completion          | `src/lib/events/handlers/event-registration-complete.handler.ts`                                            | sibling                                                                        |
| Subscription completion   | `src/lib/subscriptions/handlers/subscription-checkout-complete.handler.ts`                                  | sibling                                                                        |
| Affiliate payout template | `app/api/v1/commerce/affiliates/payouts/request/route.ts`, `app/api/v1/admin/payouts/[id]/process/route.ts` | state machine to mirror                                                        |
| Affiliate models          | `Commission`, `AffiliatePayout`, `AffiliateBalance` (view) — `prisma/schema.prisma`                         | analogs                                                                        |
| Earning stub              | `ContributorEarning` (`contributor_earnings`) — `prisma/schema.prisma`                                      | repurpose as `CreatorEarning`                                                  |
| Revenue helpers           | `src/modules/revenue/revenue.service.ts`                                                                    | `calculatePayableDate`, `calculateEventPayableDate`, `validateRevenueShareSum` |
| Revenue share             | `CourseInstructor.revenueShare`, `EventHost.revenueShare`                                                   | sum=1 at publish                                                               |
| Refund clawback           | `src/lib/courses/enrollments/handlers/course-enrollment-refund-process.handler.ts`                          | #916 pattern to extend                                                         |

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
