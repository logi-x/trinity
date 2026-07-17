---
title: "2026 06 10 buyer price event refund plan review"
date: "2026-06-10"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/reviews/2026-06-10-buyer-price-event-refund-plan-review.md"
---
# Review: #975 Buyer Price Breakdown + #966 Event Settlement/Refunds Plans

**Date:** 2026-06-10  
**Reviewer panel requested:** workflow-orchestrator, concept-architect, code-reviewer, architecture-reviewer, product-manager, general-purpose explorer  
**Reviewed docs:**

- `docs/superpowers/specs/2026-06-10-buyer-price-breakdown-design.md`
- `docs/superpowers/plans/2026-06-10-buyer-price-breakdown.md`
- `docs/superpowers/specs/2026-06-10-event-settlement-refunds-design.md`
- `docs/superpowers/reviews/spec-review-v2.md`
- `docs/superpowers/plans/2026-06-10-event-settlement-refunds.md`

**Execution order under review:** #975 buyer-price-breakdown -> merge -> #966 event-settlement-refunds.

## Verdict

Do not execute the plans as written.

#966 is broadly aligned with the current codebase and already captures many real traps, but #975 has a critical stale payment-basis assumption. If implemented unchanged, buyer-visible totals, gateway charges, coupon snapshots, invoices, and settlement metadata can diverge. Because #966 runs after #975, the event settlement plan must also be revised to consume event coupon snapshots introduced by #975.

## Critical Findings

### 1. #975 checkout charge basis is wrong

The buyer spec/plan says checkout charges `Number(price)` verbatim and gateways pass `input.amount` through. Current code does not do that. All three one-time payment gateways multiply the handler-provided amount by VAT using `displayPriceNumber(input.amount)`:

- `apps/experts-app/src/lib/payments/gateways/stripe/stripe.gateway.ts:26`
- `apps/experts-app/src/lib/payments/gateways/noon/noon.gateway.ts:69`
- `apps/experts-app/src/lib/payments/gateways/tabby/tabby.gateway.ts:111`
- `apps/experts-app/src/lib/utils.ts:127`

Current behavior for stored price `400`:

- Handler passes `400`
- Gateway charges `displayPriceNumber(400) = 460`

The buyer plan currently expects a 20% coupon to compute:

- Gateway input / charge basis: `400`
- Discount: `80`
- Charge: `320`
- Snapshot: `couponListPrice=400`, `couponDiscount=80`

But if handler passes `320`, gateway charges:

- `displayPriceNumber(320) = 368`

That means the buyer sees and pays `368`, while the settlement snapshot says list `400`, discount `80`. This corrupts scenario-A `priceOrder` accounting, because settlement gross is VAT-inclusive PSP/captured amount.

**Required amendment:** rewrite #975 pricing tasks around explicit bases:

- `storedPriceExVat`
- `listPriceIncVat`
- `discountIncVat`
- `gatewayInputAmountExVat`
- `grossPaidIncVat`

For stored price `400` and 20% coupon, the settlement-facing snapshot should likely be:

- `listPriceIncVat = 460`
- `discountAmount = 92`
- `grossPaidIncVat = 368`
- `gatewayInputAmountExVat = 320`

Alternative: deliberately refactor gateways to stop applying `displayPriceNumber`, but that is a larger behavior migration and should not be mixed in silently.

### 2. #975 invoice/ZATCA behavior is missing

The buyer plan changes checkout initiation and settlement, but completion still builds invoices from current catalog price rather than the captured/couponed amount:

- `apps/experts-app/src/lib/courses/enrollments/handlers/course-enrollment-complete.handler.ts`
- `apps/experts-app/src/lib/courses/enrollments/orchestrators/course-enrollment-complete.orchestrator.ts`
- `apps/experts-app/src/lib/events/handlers/event-registration-complete.handler.ts`
- `apps/experts-app/src/lib/billing/handlers/invoice-create.handler.ts`

The existing `CreateInvoiceCommand.discount` field exists but is not used by invoice creation.

**Required amendment:** add a #975 task before checkout handler changes that defines and tests a canonical purchase amount invariant:

`Payment.amount == Invoice.totalAmount == enrollment/registration.amountPaid == OrderSettlement.grossPaid`

The plan must update course and event completion/invoice code so discounted purchases produce invoices and ZATCA payloads matching the captured amount. Tests should assert the full chain: checkout amount -> provider verification amount -> `amountPaid` -> invoice total/payment amount -> settlement gross.

### 3. Currency groundwork is unsafe if threaded into checkout

The buyer plan adds `Course.currency` / `Event.currency` and passes those values to `createPaymentIntent`. Current payment contracts are SAR-only:

- `apps/experts-app/src/lib/payments/types.ts:3` has `currency: "SAR"`
- Course/event completion schemas accept literal `"SAR"`
- Noon and Tabby paths are SAR-pinned
- ZATCA remains SAR-constrained

There is also a schema-length mismatch:

- Spec says `@db.VarChar(3)`
- Plan uses `@db.VarChar(10)`
- Existing invoice / price-version currency fields use mixed conventions (`10` in many billing tables, `3` in settlement)

**Required amendment:** keep currency as schema/DTO/display groundwork only in #975, or widen the entire payment/completion/invoice/ZATCA/settlement currency contract in a separate explicit task. For this PR, safest rule:

- `Course.currency` and `Event.currency` default to `"SAR"`
- Checkout rejects non-SAR with a clear unsupported-currency error
- `createPaymentIntent` continues receiving `"SAR"`
- Multi-currency rollout remains doc-only

### 4. #966 event settlement must consume #975 event coupon snapshots

#975 adds coupon snapshots to `EventRegistration`, but its settlement task says courses only because events are excluded before #966. After #966 adds event settlement, event coupon snapshots must feed `priceOrder` the same way course snapshots do.

Collision point:

- `apps/experts-app/src/lib/settlement/record-settlement.ts`

**Required amendment:** in #966 Task 4, `resolveEventFacts` must select and return:

- `couponDiscount`
- `couponListPrice`
- any widened snapshot fields introduced by revised #975, such as `chargedAmount`, `currency`, `pricingBasis`

Then the shared `priceOrder` coupon block must apply for both `"course"` and `"event"`. Add an event settlement test for coupon snapshot -> scenario-A `discountInstructorCost`.

### 5. #966 event settlement is planned before invoice/ZATCA success

The event plan places `recordOrderSettlement({sourceType: "event"})` before the `pendingInvoice` flow completes. Current event completion creates invoice and queues ZATCA later in:

- `apps/experts-app/src/lib/events/handlers/event-registration-complete.handler.ts`

Course settlement runs after invoice work through the course completion orchestrator:

- `apps/experts-app/src/lib/courses/enrollments/orchestrators/course-enrollment-complete.orchestrator.ts`

If event invoice creation throws `PaymentCapturedInvoiceError`, the plan can still record host earnings.

**Required amendment:** move event settlement write after successful `handleInvoiceCreate` and `enqueueInvoiceZatca`, matching course behavior. Use reconcile for retry/replay paths rather than writing settlement before invoice success.

### 6. #966 event refund process does not re-check state inside the transaction

The spec says event refund process evaluates time gates against `requestedAt`, but re-checks state gates at process time. The current plan checks state outside the transaction, then unconditionally updates registration/refund request inside.

**Required amendment:** use guarded writes inside the transaction, for example:

```ts
await tx.eventRegistration.updateMany({
    where: {
        id: registration.id,
        status: 'completed',
        amountPaid: {gt: 0}
    },
    data: {status: 'refunded', cancelledAt: new Date()}
})
```

Abort if the guarded update count is `0`. Add tests for refund-vs-state-change races.

### 7. Event register route masks required handler errors

`apps/experts-app/app/api/v1/events/[id]/register/route.ts` currently returns a generic `"Event registration failed"` for handler errors. That will hide both:

- #975 `INVALID_COUPON`
- #966 E-6 refunded re-purchase guard

**Required amendment:** return the handler error body and status consistently:

```ts
return NextResponse.json({error: result.error, ...('code' in result ? {code: result.code} : {})}, {status: result.status})
```

Add route tests for invalid coupon and refunded re-purchase response bodies.

## Required Cross-Plan Sequencing

Keep the intended order, but make the branch/rebase rules explicit:

1. Amend #975 spec and plan.
2. Execute #975.
3. Merge #975.
4. Fast-forward local main.
5. Rebase/regenerate #966 migration and plan against merged #975 code.
6. Execute #966 from the coupon-aware settlement writer and merged schema.

Collision zones:

- `apps/experts-app/prisma/schema.prisma`
- `apps/experts-app/src/lib/settlement/record-settlement.ts`
- `apps/experts-app/src/lib/courses/enrollments/handlers/course-enroll.handler.ts`
- `apps/experts-app/src/lib/events/handlers/event-register.handler.ts`
- `apps/experts-app/src/lib/courses/enrollments/handlers/course-enrollment-complete.handler.ts`
- `apps/experts-app/src/lib/events/handlers/event-registration-complete.handler.ts`
- admin refunds query/table files after `RefundRequest` widening

## Additional Plan Amendments

### Buyer Price Breakdown (#975)

- Replace the current `computeChargeAmount` shape with a quote that separates gateway input from captured gross:
    - `gatewayInputAmountExVat`
    - `grossPaidIncVat`
    - `listPriceIncVat`
    - `discountAmountIncVat`
    - `couponApplied`
- Store a richer pricing snapshot on pending enrollment/registration:
    - `couponCode`
    - `couponDiscountType`
    - `couponDiscountValue`
    - `couponDiscountAmount`
    - `couponListPrice`
    - `chargedAmount`
    - `currency`
    - `pricingBasis` or `pricingVersion`
- Clear stale coupon snapshot fields on no-code checkout retries.
- Define 100%-coupon policy explicitly:
    - provider should be `"free"` or a named internal provider
    - no PSP payment intent
    - no affiliate commission
    - no settlement
    - no invoice unless a zero-total receipt is intentionally required
    - coupon snapshot retained for audit/support
- Decide coupon secrecy:
    - If creator coupon codes are public promo metadata, DTO-driven preview is acceptable.
    - If private campaign codes are expected, replace client validation with a server quote/validate endpoint.
- Add UI tests for:
    - mobile bars
    - Arabic/RTL labels
    - invalid server rejection after client preview
    - TabbyPromo discounted vs undiscounted amount decision

### Event Settlement/Refunds (#966)

- Add a post-#975 merge preflight task:
    - confirm `EventRegistration` has coupon/pricing snapshot fields
    - confirm `record-settlement.ts` is coupon-aware
    - update event facts from the merged version, not from current main
- Add event settlement tests for:
    - coupon snapshot -> `priceOrder` scenario-A fields
    - course settlement regression
    - subscription settlement regression
    - `limit < 3` reconcile fairness
- Split affiliate date helpers:
    - `calculateReferralExpiresAt`
    - `calculateCommissionHoldUntil({itemType, createdAt, eventStartsAt})`

    `calculateHoldUntil` currently serves both referral expiry and commission hold behavior. Threading event start through the existing helper risks changing referral expiry semantics.

- Admin refunds queue should show enough operational context:
    - source chip
    - course/event title
    - event start date
    - registration/enrollment id
    - amount paid
    - provider/providerRef
    - invoice/credit-note id or link
    - request age
    - provider refund reference if manual/PSP refund tracking is added
- Clarify refund money movement:
    - Current course process marks app state refunded and creates credit note/ZATCA, but does not call Stripe/Noon/Tabby refund APIs.
    - #966 should either document a manual PSP refund prerequisite and capture a provider refund reference, or add provider refund execution/status tracking.

## Repo Process Amendments

Both plans must include the root `AGENTS.md` GitNexus requirements:

- Run impact analysis before editing any function/class/method/symbol.
- Warn and stop for HIGH/CRITICAL risk unless operator explicitly approves continuing.
- Run `gitnexus_detect_changes()` before committing.

High-risk symbols/routes to explicitly gate:

- `recordOrderSettlement`
- `handleCourseEnroll`
- `handleEventRegister`
- `handleCourseEnrollmentComplete`
- `handleEventRegistrationComplete`
- course/event refund process handlers
- admin refund process route
- affiliate attribution helpers

Fix command contexts:

- From repo root `/home/logix/experts`: use `pnpm experts:*`.
- From `apps/experts-app`: use app-local scripts such as `pnpm check`, `pnpm test`, `pnpm typecheck`, `pnpm typecheck:touched`.

Do not mix `apps/experts-app` cwd with root-only `pnpm experts:*` commands.

## Suggested Revision Checklist For Next Agent

- [ ] Revise #975 spec: replace stale "checkout charges raw stored price" premise with actual gateway VAT behavior.
- [ ] Revise #975 plan Tasks 1, 8, 9, 10 around explicit ex-VAT gateway input and inc-VAT captured/settlement amounts.
- [ ] Add invoice/completion tasks and tests to #975.
- [ ] Make #975 currency behavior SAR-only at checkout, or explicitly widen the full currency contract.
- [ ] Add stale snapshot clearing and 100%-coupon audit policy.
- [ ] Revise #966 Task 0 to branch only after #975 is merged and local main is fast-forwarded.
- [ ] Revise #966 Task 4 to consume event coupon/pricing snapshots in `resolveEventFacts`.
- [ ] Move #966 inline event settlement after invoice/ZATCA success.
- [ ] Add in-transaction guarded state re-checks to event refund process.
- [ ] Fix event register route error propagation.
- [ ] Add GitNexus impact/detect-changes gates to both plans.
- [ ] Fix command cwd/script mismatches.

## Bottom Line

The current #966 plan can become production-ready with targeted revisions. The current #975 plan needs a material rewrite before implementation because the core money basis is wrong against live code. The safest production path is to make #975 establish one canonical purchase snapshot that checkout, completion, invoice, settlement, and refunds all consume, then make #966 event settlement consume that same snapshot after #975 lands.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
