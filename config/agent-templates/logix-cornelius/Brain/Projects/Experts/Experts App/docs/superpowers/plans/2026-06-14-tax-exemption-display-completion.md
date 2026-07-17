---
title: "2026 06 14 tax exemption display completion"
date: "2026-06-14"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/plans/2026-06-14-tax-exemption-display-completion.md"
---
# Tax-exemption display-layer completion Plan

> Completes #1040 (PR #1041). The charge/invoice/settlement paths are exempt-aware;
> the **display** layer is not, so exempt items still show VAT on the pay-now button,
> creator payout breakdown, creator view price breakdown, and creator summary.

**Goal:** No VAT shown or implied anywhere for a tax-exempt course/event; consolidate
money rendering onto `MoneyAmount` and remove the VAT-math footgun from `SaudiRiyal`.

**Root cause:** `SaudiRiyal type="display"` silently multiplies value × `VAT_FACTOR`
(a _renderer_ doing _tax math_). Every `type="display"` caller is structurally blind
to `taxExempt`. `MoneyAmount` already documents the correct contract ("amount is the
FINAL figure; SAR renders raw, no ×1.15") — converge on it.

**Single chokepoint:** reuse the existing `gatewayChargeAmount(exVat, taxExempt)`
(`src/lib/payments/shared/gateway-charge-amount.ts`) as the one "inc-VAT figure to
display" — guarantees display == charge.

---

## Task 1: Remove `type="display"` from `SaudiRiyal`

**Files:** `src/components/ui/saudi-riyal.tsx`

- Drop the `display` case + the `displayPrice` import. Union → `"format" | "paid"`.
- `SaudiRiyal` becomes a pure SAR formatter (still `MoneyAmount`'s SAR backend).

## Task 2: Pay-now / Tabby (the headline bug)

**Files:** `src/lib/courses/detail/course-detail-page.tsx:141`,
`src/lib/events/detail/event-detail-page.tsx:147`

- `payableAmountIncVat = gatewayChargeAmount(payableAmountExVat, <entity>.taxExempt)`.
- Import `gatewayChargeAmount`; drop now-unused `displayPriceNumber` if unused.

## Task 3: Creator "Estimated payout breakdown"

**Files:** `src/lib/pricing/components/creator-price-breakdown.tsx`,
`src/lib/courses/catalog/forms/sections/course-pricing-section.tsx:631`,
`src/lib/events/forms/sections/event-pricing-section.tsx:461`

- Add `taxExempt?: boolean` + `messages.vatNotApplicable`.
- `vatRate: taxExempt ? 0 : VAT_RATE`. When exempt: render a "VAT not applicable"
  row (em-dash) instead of the `vatIncluded` row.
- Thread `taxExempt={taxExempt}` + the new message from both sections.

## Task 4: Creator summary (sidebar) sections

**Files:** `src/lib/courses/catalog/forms/sections/course-summary-section.tsx`,
`src/lib/events/forms/sections/event-summary-section.tsx`,
`src/lib/courses/catalog/forms/course-form.tsx:276`, `src/lib/events/forms/event-form.tsx:418`

- Add `taxExempt?: boolean`. When exempt && !isFree: show only the total (price) +
  a "VAT not applicable" note; skip the excl/VAT/incl sub-rows. Thread from the forms.

## Task 5: Creator VIEW price breakdown (detail pages)

**Files:** `app/(i18n)/_shared/creator/courses/[id]/page.tsx` (~452-462),
`app/(i18n)/_shared/creator/events/[id]/page.tsx` (~566-580)

- `displayPriceNumber(price)` → `gatewayChargeAmount(price, taxExempt)`; hide VAT
  sub-rows + show note when exempt.

## Task 6: Creator revenue stat cards

**Files:** `app/(i18n)/_shared/creator/courses/[id]/page.tsx:551`,
`app/(i18n)/_shared/creator/events/[id]/page.tsx:718`

- `revenue` (= count × ex-VAT price) → `MoneyAmount({gatewayChargeAmount(revenue,
taxExempt)}, currency)`. (Exempt buyers paid no VAT.)

## Task 7: Creator events list price chip

**Files:** `app/(i18n)/_shared/creator/events/_components/events-results.tsx:718`

- `MoneyAmount({gatewayChargeAmount(event.price, event.taxExempt)}, event.currency)`.

## Task 8: Out-of-scope display sites (preserve behavior, drop the footgun mode)

**Files:** `app/(i18n)/_shared/creator/dashboard/page.tsx:149` (aggregate time-series),
`app/(i18n)/_shared/pricing/page.tsx:411` (subscription savings — `t.rich` children)

- Replace `type="display"` with `displayPriceNumber(...)` computed upstream:
  dashboard → `MoneyAmount` SAR; pricing → `SaudiRiyal type="format"` (keeps children).

## Task 9: i18n (en/ar/es)

- `pricing.breakdown.vatNotApplicable` already exists (buyer). Add creator-breakdown
    - summary "VAT not applicable" copy in all three locales for the namespaces used.

## Task 10: Tests

- `creator-price-breakdown.test.tsx`: exempt → vatRate 0, no VAT row.
- summary section exempt render (no VAT subrows + note).
- `gatewayChargeAmount` already property-tested; add a display-parity assertion if missing.
- Update/remove any test asserting `SaudiRiyal type="display"`.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
