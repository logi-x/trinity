---
title: "2026 06 10 buyer price breakdown design"
date: "2026-06-10"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/specs/2026-06-10-buyer-price-breakdown-design.md"
---
# Buyer Price Breakdown + Coupon at Checkout + Currency Groundwork — Design

**Date:** 2026-06-10
**Scope:** `apps/experts-app` — paid course and event detail pages, enroll/register checkout flow, Course/Event schema.
**Status:** Approved by operator (this session). Implementation pending.

## Problem

Paid course/event detail pages show a single price number next to the payment buttons. Buyers see no breakdown of what the price contains (VAT) or what a coupon would do. Separately, creator-side coupon metadata (`couponEnabled`, `couponCode`, `couponDiscountType`, `couponDiscountValue`) exists on `CourseDTO`/`EventDTO` and feeds creator estimates and settlement metadata, but **checkout never applies coupons** — buyers are always charged full price. Finally, the platform is SAR-only with the currency hardcoded in many places; a future multi-currency system needs seams now.

### Review amendment: explicit VAT/payment bases

The 2026-06-10 review found that the original plan's checkout basis was stale. The checkout handlers pass `Number(price)` to `createPaymentIntent`, but Stripe, Noon, and Tabby gateway adapters then charge `displayPriceNumber(input.amount)` (`amount × 1.15`). Therefore stored catalog price is treated as **ex-VAT gateway input**, while buyer-visible paid gross, invoices, and settlement must be **VAT-inclusive**.

This work must use explicit names and snapshots:

- `storedPriceExVat`: the catalog value stored on `Course.price` / `Event.price`.
- `gatewayInputAmountExVat`: the amount sent to `createPaymentIntent`; gateways convert it to a VAT-inclusive charge.
- `listPriceIncVat`: `displayPriceNumber(storedPriceExVat)`.
- `discountAmountIncVat`: coupon discount on the VAT-inclusive list price.
- `grossPaidIncVat`: VAT-inclusive captured/buyer/invoice/settlement amount.

For stored price `400` and a 20% coupon, checkout sends `320` to gateways, the buyer pays `368`, and the persisted coupon snapshot records list `460`, discount `92`, charged/gross `368`.

## Decisions (operator-approved)

1. **Lines shown:** full receipt-style breakdown including discount math — list price, coupon discount (with code), VAT (15%), total.
2. **Placement:** inside the course/event detail sidebar card, directly above the payment buttons; compact total in the mobile bottom bars. Hidden for free items.
3. **Coupon at checkout is in scope:** buyer enters a code; server validates and charges the discounted amount.
4. **Currency groundwork:** add `currency` column to Course/Event (default `"SAR"`), thread through DTOs and the new components. No FX, no picker.
5. **VAT/payment basis:** gateways still receive ex-VAT input; buyer display, invoices, and settlement snapshots use VAT-inclusive totals.
6. **Architecture:** Approach A — shared pure pricing module + one shared component (vs. a price-quote endpoint or per-page duplication).

## Design

### 1. Pure pricing module — `src/lib/pricing/buyer-price-breakdown.ts`

```ts
export interface BuyerCouponInput {
    couponEnabled: boolean
    couponCode: string | null
    couponDiscountType: 'percent' | 'fixed' | null
    couponDiscountValue: number | null
}

export interface BuyerBreakdown {
    storedPriceExVat: number
    listPriceIncVat: number // displayPriceNumber(price) = price × VAT_FACTOR
    discountAmountIncVat: number // 0 when no coupon applied
    vatAmount: number // vatFromIncl(total)
    grossPaidIncVat: number // listPriceIncVat − discountAmountIncVat, clamped ≥ 0
    couponApplied: boolean
}

export function computeBuyerBreakdown(price: number, coupon: BuyerCouponInput, appliedCode?: string): BuyerBreakdown

export interface ChargeQuote {
    storedPriceExVat: number
    gatewayInputAmountExVat: number
    listPriceIncVat: number
    discountAmountIncVat: number
    grossPaidIncVat: number
    couponApplied: boolean
}
export function computeChargeQuote(price: number, coupon: BuyerCouponInput, appliedCode?: string): ChargeQuote | null // null = supplied code invalid/disabled
```

Rules (both functions):

- Coupon applies only when `couponEnabled`, a non-empty `couponCode` exists, and `appliedCode` matches case-insensitively after trim.
- `percent`: display/snapshot discount = `round2(listPriceIncVat × clampPercentFraction(value))` (values are unit fractions 0–1, matching `priceOrder`).
- `fixed`: discount = `round2(min(value, listPriceIncVat))` (fixed values are SAR amounts on the VAT-inclusive buyer basis).
- All rounding `round2` (matching `priceOrder`).
- `gatewayInputAmountExVat = round2(grossPaidIncVat / VAT_FACTOR)` so the existing gateways charge the intended VAT-inclusive gross.

### 2. Shared component — `src/lib/pricing/components/buyer-price-breakdown.tsx`

- Receipt rows: list price / coupon (code chip, shown only when applied) / VAT (15%) / divider / total.
- Money rendering behind a small seam: `MoneyAmount` (props `{amount, currency, ...}`) renders `SaudiRiyal` when `currency === "SAR"`, otherwise `Intl.NumberFormat(locale, {style: "currency", currency})`. This is the multi-currency plug-in point.
- "Have a coupon?" input (only when `couponEnabled`): client previews against the DTO's `couponCode` for instant feedback; **server is authoritative** at enroll. Applied code is lifted to the sidebar so the enroll request includes it.
- RTL-safe (logical properties only), keyboard/screen-reader accessible (labelled input, `aria-live` on the updated total), HeroUI v3 + kit primitives per experts-constellation.
- i18n: new shared `pricing.breakdown.*` keys in en/ar/es message files (`pricing.json` namespace).
- Rendered in: `course-detail-sidebar.tsx`, `event-detail-sidebar.tsx` (above payment options), compact total in `course-detail-mobile-bar.tsx` / `event-detail-mobile-bar.tsx`. Hidden when `isFree || price <= 0`.

### 3. Coupon at checkout

- `CourseEnrollSchema` / event register schema: optional `couponCode` — trimmed, max length 64, string.
- Enroll/register handlers:
    - No `couponCode` in request → **byte-identical behavior to today** (happy-path regression guard; coupon logic activates only on presence of a code).
    - Code present → validate via `computeChargeAmount`. Invalid/disabled/mismatched → `400` with a distinct error code (`INVALID_COUPON`); never silently charge full price.
    - Valid → `createPaymentIntent` with `amount = gatewayInputAmountExVat`; **snapshot** `{couponCode, couponDiscountType, couponDiscountValue, couponDiscountAmount, couponListPrice, chargedAmount, currency, pricingBasis}` onto the pending enrollment/registration record at initiation. Completion paths (verify, webhooks) read the snapshot, never re-read mutable coupon config (TOCTOU rule, EXP-129 pattern).
    - 100%-discount edge (chargeAmount = 0): route through the existing free-enrollment path explicitly, with the snapshot still recorded.
- Settlement: pass scenario-A inputs from the snapshot — `checkoutDiscountAmount = couponDiscountAmount`, `listPriceIncVatInput = couponListPrice`, `grossPaid = chargedAmount` — into the existing `priceOrder` coupon metadata flow in `record-settlement.ts`.
- Symmetric siblings rule: courses and events change in the same diff.
- Storage for the snapshot: new nullable columns on the enrollment/registration (or their payment-pending rows) — exact placement decided at planning time after reading the pending-row models; must survive the pending→completed transition and be readable by verify/webhook/settlement.

### 4. Currency schema groundwork

- `currency String @default("SAR") @db.VarChar(3)` on `Course` and `Event` (hand-edited model blocks — **never** `prisma format`; migration generated with `prisma migrate diff --from-schema … --to-schema … --script`, idempotent, then `pnpm db:check:drift`).
- Thread `currency: string` into `CourseDTO`/`EventDTO` + mappers.
- Checkout rejects non-SAR with a clear unsupported-currency error and continues passing `"SAR"` to `createPaymentIntent`; full payment/invoice/ZATCA multi-currency widening is out of scope.
- Breakdown component and `MoneyAmount` consume `currency` from the DTO.
- No admin/creator UI to change currency yet; column is groundwork only.

### 5. Multi-currency plan doc (no implementation)

Separate doc `docs/superpowers/specs/2026-06-10-multi-currency-plan.md`. **Operator decision (2026-06-10): multi-currency is DISPLAY-ONLY — the processing/charge currency is always SAR; convert for display, never for charge.** This keeps Noon/Moyasar/HyperPay/Tabby processing Visa/MC unchanged, keeps ZATCA + the ledger SAR, and carries zero FX/settlement risk. The plan covers: the FX-at-display model (the only model; price-per-currency charging is rejected); display currency as a buyer/locale property (not item-level); a cached FX rate source used for display math only; and a phased rollout (display seam → schema → rate source → buyer preference → display conversion → checkout always shows/charges SAR).

### 6. Error handling

- Component: no async data (DTO-driven) → no loading state; invalid coupon preview shows inline field error; zero/free → component absent.
- Handlers: `INVALID_COUPON` 400; all other behavior unchanged; `safeErrorJson` conventions preserved; `observe()` events for coupon applied/rejected.

### 7. Testing

- Unit: `computeBuyerBreakdown` / `computeChargeAmount` — percent, fixed, fixed > basis, 100% coupon, rounding, disabled coupon, code mismatch, case-insensitivity.
- Component (node-env `renderToStaticMarkup` + string asserts, per house convention): paid no-coupon, coupon applied, free hidden, ar locale render.
- Handlers: coupon accept (amount + snapshot), reject (400, no intent created), absent code (existing tests untouched and green), 100% discount → free path.
- Settlement: snapshot → scenario-A `priceOrder` inputs.
- Gate: `pnpm experts:check` + `db:check:drift` before commit.

## Out of scope

- Fixing the ×1.15 display/charge discrepancy (issue filed instead).
- FX rates, currency picker, non-SAR payments.
- Subscriptions pricing breakdown.
- Creator UI changes (CreatorPriceBreakdown untouched).

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
