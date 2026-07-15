---
title: "2026 06 13 tax exemption design"
date: "2026-06-13"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/specs/2026-06-13-tax-exemption-design.md"
---
# Tax exemption for out-of-ZATCA-scope content

- **Issue:** #1040
- **Date:** 2026-06-13
- **Status:** Approved (design); pending implementation plan
- **Related:** #1038 (closed; abandoned branch `fix/gh-1038-foreign-currency-invoice` to salvage), #995 (separate, **not** resolved here), #1022, EXP-129 (TOCTOU snapshot pattern)

## Problem

Some content is sold outside ZATCA's jurisdiction — e.g. an event physically held
in Italy, priced in EUR via the existing multi-currency charge path. ZATCA
e-invoicing rules are out of scope for these supplies. They must be sold:

1. **without 15% VAT** in the price the buyer sees and pays,
2. **without a ZATCA e-invoice** being generated or reported,
3. invoiced **in the selected currency** at the **listed amount**.

Exemption is **not** something instructors may self-certify — it must be
platform-controlled. In rare cases even a SAR-priced item may be exempt, so
exemption is **decoupled from currency**: it is its own flag, not derived from the
order currency.

## Current state (verified against `origin/main`, 2026-06-13)

- VAT is a flat 0.15 (`src/lib/utils.ts`: `VAT_RATE`, `VAT_FACTOR = 1.15`,
  `displayPriceNumber(x) = round2(x * 1.15)`).
- Gateways charge `displayPriceNumber(gatewayInput)`; the buyer breakdown
  (`src/lib/pricing/buyer-price-breakdown.ts`) derives its displayed total from the
  _same_ function, so display ≡ snapshot ≡ PSP capture by construction.
- `handleInvoiceCreate` (`src/lib/billing/handlers/invoice-create.handler.ts`)
  hardcodes `taxRate: 15` and builds lines with a per-line `vatRate`.
- ZATCA is enqueued from the completion handlers / orchestrators via
  `enqueueInvoiceZatca(invoiceId)` and, on refund, `enqueueCreditNoteZatca(...)`
  (`src/modules/billing/zatca/services/zatca-queue.service.ts`).
- Multi-currency **charging** is live: an FX lock snapshots `chargedSar` (SAR,
  ex-VAT) at checkout for ledger/payout/settlement. Multi-currency **invoice
  minting** (foreign-currency invoice document) is **NOT** on main — it exists only
  in the abandoned #1038 branch. Today an Italy/EUR order is charged in EUR but the
  invoice document is SAR-denominated with the EUR amount as a note (#1022).

## Decisions (locked)

| Decision             | Choice                                                                                                                 |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Who marks exempt     | **Admin-only** checkbox + required reason on the content. Instructor sees read-only status.                            |
| Where the flag lives | **Per content item** (course/event), snapshotted onto the order at checkout (TOCTOU-safe).                             |
| Invoice currency     | **Foreign-currency invoice for the exempt path only** — salvage #1038 currency rendering; **no SAR mirror, no ZATCA**. |

## Design

### 1. Data model

**Catalog — `Course`, `Event`** (admin-owned):

- `taxExempt Boolean @default(false) @map("tax_exempt")`
- `taxExemptReason String? @map("tax_exempt_reason")` — required when `taxExempt = true`, enforced at the admin mutation (not a DB constraint).
- `taxExemptUpdatedById String? @db.Uuid` + `taxExemptUpdatedAt DateTime?` — accountability trail (which admin set it, when).

**Order snapshot — `enrollment`, `event registration`** (TOCTOU-safe, mirrors the coupon/FX lock):

- `taxExempt Boolean @default(false)` — copied from the catalog **at checkout** and never re-read after. If an admin flips the catalog flag between checkout and completion, the snapshot wins.

**`Invoice`**:

- `taxExempt Boolean @default(false) @map("tax_exempt")`
- `taxExemptReason String? @map("tax_exempt_reason")`
- When exempt: `taxRate = 0`, `taxAmount = 0`, `currency = order's locked currency`.

### 2. The bypass, layer by layer

- **Pricing breakdown** (`buyer-price-breakdown.ts`): add an `exempt` mode that does
  not apply `VAT_FACTOR`. Then `list == total`, there is no VAT line, and the gateway
  input equals the listed amount as-is. The buyer breakdown renders a
  "VAT not applicable" row instead of "VAT 15%". No-exempt path stays
  byte-identical to today (regression guard).
- **Invoice mint** (`invoice-create.handler.ts`): `taxRate`/`taxAmount` become
  `exempt ? 0 : 15`; lines get `vatRate 0`; `currency` = the order's locked currency.
  Salvage #1038's currency-aware PDF/HTML/view-model rendering for the foreign
  document (drop its SAR-mirror logic — not needed without ZATCA).
- **ZATCA**: single chokepoint — `enqueueInvoiceZatca` / `enqueueCreditNoteZatca`
  early-return when the invoice (or the credit note's parent invoice) is
  `taxExempt`. No e-invoice document is ever created or reported.

### 3. Settlement invariant (subtle, money-critical)

The SAR mirror (`chargedSar`) **stays** — it is still required for ledger / payout /
settlement, only _not_ for ZATCA. Three money sites must branch on `exempt`:

**(a) Paid-amount reconciliation guard** in the completion handlers — currently
`expectedPaid = displayPriceNumber(lockedSar)` (× 1.15) — must branch:

```
expectedPaid = exempt ? lockedSar : displayPriceNumber(lockedSar)
```

For an exempt order the listed amount **is** the net (no VAT to add). Property-test
target: for any price `p`, an exempt order charges exactly `p` (no 0.01 drift) and a
non-exempt order charges exactly `displayPriceNumber(p)`.

**(b) Invoice-charge resolution** (`resolveInvoiceCharge`) compares
`amountPaid < displayPriceNumber(chargedSar)` to detect PSP under-capture. For exempt
`amountPaid == chargedSar` (no ×1.15), which would falsely trip the under-capture
branch and divide an already-ex-VAT amount by 1.15. The exempt path must **bypass
`resolveInvoiceCharge`**: mint the invoice line from the snapshotted authoring amount
(`chargedAmount`, VAT-free) with `vatRate 0`, in the authoring `currency`, and **no FX
anchor note** (the invoice _is_ in the authoring currency — there is no SAR mirror to
footnote). The `chargeIntegrity` alarm still covers SAR capture drift.

**(c) Settlement writer** (`record-settlement.ts`) hard-codes `vatRate: 0.15` and
splits `grossPaid` into VAT + net. For exempt it must use `vatRate 0` →
`vatAmount 0`, `netExVat = grossPaid`, so the instructor's revenue share is computed
on the full (VAT-free) amount and no phantom VAT is recorded.

The `taxExempt` snapshot — plus the authoring `currency` and `chargedAmount`, which
today are only persisted when a coupon applies and so must be persisted **always for
exempt orders** — flows from checkout → completion so the guard, the invoice mint,
and settlement all branch on the same snapshotted values. The `taxExemptReason` shown
on the invoice is read from the catalog at completion (descriptive text, not money —
no extra snapshot column).

### 3a. Invoice minting site (architecture note)

The invoice is **not** minted in the completion handler for courses. For **courses**
it is minted in `course-enrollment-complete.orchestrator.ts` (the handler returns a
`PendingInvoiceContext`); for **events** the completion handler mints it inline. The
`PendingInvoiceContext` (course path) gains `taxExempt`, `invoiceCurrency`,
`taxExemptReason`, and an exempt-aware `invoiceExVat`; the orchestrator passes
`vatRate: exempt ? 0 : 15`, `currency: invoiceCurrency`, and the exempt note.
Non-exempt minting stays byte-identical (currency `command.payment.currency`,
`vatRate 15`, FX anchor as today).

### 4. Admin & instructor UI

- **Admin console** content editor: the `taxExempt` checkbox + reason field, plus a
  "last changed by / at" line. Reason is required to enable exemption.
- **Instructor** content form: **read-only** — "Tax status: Standard (15% VAT)" or
  "Exempt — _reason_". Instructors cannot toggle it.
- Both surfaces are RTL-first, next-intl (en/ar/es), per experts-constellation.

### 5. Refunds

Exempt refund → credit note in the **same currency**, **no** `enqueueCreditNoteZatca`.
The credit note inherits `taxExempt` from its parent invoice.

## Scope boundaries

**In scope:** courses + events; buyer breakdown; exempt foreign-currency invoice
mint; ZATCA skip; exempt refund credit notes; the settlement reconciliation
invariant; SAR mirror retained for settlement.

**Out of scope:** subscriptions (consistent with #1038); reviving the full #1038
SAR-mirror path; historical re-mint of existing invoices; non-SAR PSP settlement
(charge still rides the existing FX-lock path).

**Not resolved here:** #995 (creator-form ex-VAT-vs-inc-VAT basis) — kept distinct;
this feature does not touch the creator pricing form's VAT basis.

## Counsel flag (not a blocker)

ZATCA distinguishes _out-of-scope_ supplies from _zero-rated / export_ supplies, and
the documentation obligations differ. "Issue nothing to ZATCA" is the product owner's
call for this feature; `taxExemptReason` provides the audit trail. Flagged for
`legal-compliance-advisor` review before GA.

## Risks & mitigations

- **Silent mischarge** if the settlement invariant is wrong → property test on
  exempt vs non-exempt charge amounts.
- **TOCTOU** if exemption is re-read at completion instead of snapshotted → snapshot
  at checkout, never re-read (EXP-129 pattern); re-checkout re-snapshots.
- **Happy-path regression** for non-exempt orders → no-exempt path must be
  byte-identical; add a regression guard test (per scanner-fix lesson).
- **ZATCA leak** if any enqueue site is missed → centralize the skip inside the two
  `enqueue*` functions (single chokepoint), not at each call site.

## Test plan (high level)

- Pricing: exempt vs non-exempt breakdown; display ≡ charge property for both;
  non-exempt byte-identical regression.
- Invoice mint: exempt → `taxRate 0`, foreign currency, lines `vatRate 0`.
- ZATCA: exempt invoice/credit note → enqueue is a no-op; non-exempt unchanged.
- Settlement: reconciliation invariant property test.
- Snapshot: catalog flip after checkout does not change the order's charge/invoice.
- Refund: exempt credit note in selected currency, no ZATCA.
- UI: admin can toggle + reason required; instructor read-only;
  `renderToStaticMarkup` string asserts (node-env convention).

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
