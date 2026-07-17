---
title: "2026 06 10 multi currency plan"
date: "2026-06-10"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/specs/2026-06-10-multi-currency-plan.md"
---
# Multi-Currency Plan (deferred)

**Date:** 2026-06-10
**Status:** Plan only — no implementation. Groundwork (the `currency` column on
`Course`/`Event`, the `MoneyAmount` seam) shipped with the buyer price breakdown;
everything below is the path from there to multi-currency **display**.

## The one rule: SAR is the only processing currency

**The platform charges SAR. Always. Forever — until a real reason says otherwise.**
Multi-currency is a **display** concern only: convert the SAR price to a buyer's
preferred currency **for showing**, never for charging. The buyer is always
charged the SAR amount; non-SAR figures are clearly-marked estimates.

Why this is the right constraint:

- **PSP compatibility.** Noon, Moyasar, HyperPay, Tap, and Tabby are KSA-domestic
  and settle SAR. Keeping the charge in SAR means they keep processing
  Visa/Mastercard exactly as today — no new PSP, no new settlement currency, no
  FX risk on the platform, no reconciliation against a fluctuating rate.
- **ZATCA.** Saudi e-invoicing is SAR-denominated. A SAR-only charge means the
  invoice is trivially correct — no SAR-equivalent rate to record or reconcile.
- **Ledger / settlement.** `OrderSettlement` and `CreatorEarning` stay SAR. No
  per-currency ledger, no payout FX. Creator economics are unchanged.

> **Convert for display only, never for charge.** This is the whole plan in one
> line. Any future proposal to charge a non-SAR amount is a separate, much larger
> project (new PSP relationships, FX hedging, multi-currency ZATCA, payout FX) and
> is explicitly **out of scope** here.

## Shipped groundwork

- **`MoneyAmount`** (`src/components/ui/money-amount.tsx`) — the render seam.
  Today: SAR → `SaudiRiyal`. Tomorrow: a non-SAR display currency →
  `Intl.NumberFormat` of `sarAmount × rate`. One place to change.
- **`Course.currency` / `Event.currency`** (`@default("SAR")`) — records the
  **authoring** currency of the stored price. With SAR-only charging this stays
  `"SAR"` in practice; it exists so the seam and DTOs already carry a currency
  field and a future authoring-currency feature doesn't need a migration.

Nothing else changed: gateways, invoices, and settlement are SAR-pinned.

## The model: FX-at-display (the only model)

Store one **SAR** price. To show it in another currency, multiply by a fetched
rate and format for the buyer's locale. The displayed non-SAR amount is an
**estimate** — labelled as such ("≈ $X") — and the checkout/charge line always
shows and charges the **SAR** amount.

The previously-considered "price-per-currency / charge in the buyer's currency"
model is **rejected**: it would force non-SAR PSP settlement, FX risk, and
multi-currency ZATCA — all the things the SAR-only rule exists to avoid.

## Display currency is buyer-driven, not item-driven

Because the item is always priced and charged in SAR, the _display_ currency is a
property of the **buyer** (locale or an explicit preference), not the item. The
item's `currency` column stays `"SAR"`; the display layer picks the presentation
currency and converts from SAR at render time.

## Phased rollout (display only)

1. **Display seam** _(done)_ — `MoneyAmount`; SAR renders unchanged.
2. **Schema** _(done)_ — `currency` on `Course`/`Event`, default SAR, on the DTO
   and the order snapshot. (Authoring-currency groundwork; charge stays SAR.)
3. **Rate source** — a server-side FX rate provider (cached, with a sane refresh
   cadence and a hard fallback to SAR-only display if the feed is stale/unavailable).
   Rates are for **display math only**; they never touch a charge.
4. **Buyer preference** — locale-derived default display currency + an optional
   explicit picker. Persist the choice; it is purely presentational.
5. **Display conversion** — `MoneyAmount` (and listing/detail price surfaces)
   render `sarAmount × rate` via `Intl.NumberFormat`, **always** alongside or
   above the authoritative SAR figure, marked as an estimate.
6. **Checkout clarity** — the pay button and the price breakdown **Total** always
   show SAR (the charged amount). A non-SAR estimate may appear as secondary text
   ("≈ $X"), never as the charged line.

## Hard constraints (unchanged by display FX)

- ZATCA invoices: SAR (charge is SAR).
- Settlement / ledger / payouts: SAR.
- `priceOrder`: untouched (currency-agnostic; inputs are SAR).
- All PSPs: charged in SAR; no eligibility change needed (the SAR-only rule is
  what keeps Noon/Moyasar/etc. working for Visa/MC).

## Explicit non-goals

Charging any non-SAR amount; non-SAR PSP settlement; per-currency ledgers;
multi-currency payouts; non-SAR ZATCA; FX hedging. All of these follow only from
"charge in another currency", which this plan deliberately does **not** do.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
