---
title: "2026 06 13 tax exemption"
date: "2026-06-13"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/plans/2026-06-13-tax-exemption.md"
---
# Tax Exemption Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let admins mark a course/event tax-exempt (out of ZATCA scope) so the buyer pays the listed amount with **no 15% VAT**, the invoice is minted **in the selected currency** with `taxRate 0`, and **no ZATCA e-invoice** is ever generated.

**Architecture:** A per-content admin-only `taxExempt` flag is snapshotted onto the order at checkout (TOCTOU-safe, EXP-129 pattern), then flows to (a) the gateway charge — skip the `×1.15` multiply, (b) the invoice mint — `taxRate 0`, foreign currency, (c) the ZATCA enqueue chokepoint — early-return. The SAR mirror (`chargedSar`) stays for settlement/payout; it is simply never reported to ZATCA.

**Tech Stack:** Next.js 16, Prisma/Postgres (multi-schema: `public` catalog, `billing`), Vitest (node env, `renderToStaticMarkup` for components), next-intl (en/ar/es), BullMQ ZATCA queue.

**Issue:** #1040 · **Branch:** `feat/gh-1040-tax-exemption` · **Spec:** `docs/superpowers/specs/2026-06-13-tax-exemption-design.md`

---

## Pre-flight (read before Task 1)

- `pnpm experts:check` must pass before you start (baseline green).
- Vitest run needs `DATABASE_URL=postgresql://localhost/experts_test` in env (see memory: experts-app vitest is node env).
- **Prisma rules (critical):** NEVER run `npx prisma format` (it rewrites all ~4576 lines). Hand-edit model blocks matching surrounding style. Index/column migrations: declare in `schema.prisma`, then generate exact SQL DB-free with `prisma migrate diff --from-schema-datamodel <old> --to-schema-datamodel <new> --script`, make it idempotent, then `pnpm db:check:drift`. Run `npx prisma generate` after schema edits (generated client is gitignored).
- All work happens in `apps/experts-app/`. Paths below are relative to that unless noted.
- Commit after every task. Use `git commit` (lint-staged/husky will run — do not bypass).

## File map (what each task touches)

| Area                           | Files                                                                                                                                                                                                                                                      |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Schema + migration             | `prisma/schema.prisma` (Course, Event, CourseEnrollment, EventRegistration, Invoice), new `prisma/migrations/<ts>_tax_exemption/migration.sql`                                                                                                             |
| Pricing core                   | `src/lib/pricing/buyer-price-breakdown.ts` (+ test)                                                                                                                                                                                                        |
| Gateway charge                 | `src/lib/payments/shared/gateway-charge-amount.ts` (new, + test), `src/lib/payments/gateways/{noon,tabby,stripe}/*.gateway.ts`, the gateway `input` type                                                                                                   |
| Charge type plumbing           | `src/lib/payments/payment.service.ts`, `src/lib/payments/types` (PaymentIntentInput)                                                                                                                                                                       |
| Checkout snapshot              | `src/lib/courses/enrollments/handlers/course-enroll.handler.ts`, `src/lib/events/handlers/event-register.handler.ts`                                                                                                                                       |
| Completion + invoice mint      | `src/lib/courses/enrollments/handlers/course-enrollment-complete.handler.ts`, `src/lib/events/handlers/event-registration-complete.handler.ts`, `src/lib/billing/handlers/invoice-create.handler.ts`, `src/lib/billing/commands/invoice-create.command.ts` |
| Invoice render (salvage #1038) | `src/modules/billing/invoices/renderers/invoice/pdf/invoice-pdf.money.tsx` (new, from #1038), `.../map-invoice-to-view-model.ts`, `.../invoice-view-model.ts`, `.../pdf/invoice-pdf.tsx`, `.../html/invoice-html.tsx`                                      |
| ZATCA skip                     | `src/modules/billing/zatca/services/zatca-queue.service.ts` (+ test)                                                                                                                                                                                       |
| Buyer breakdown UI             | `src/lib/pricing/components/buyer-price-breakdown.tsx` (+ test)                                                                                                                                                                                            |
| Admin/instructor UI + i18n     | admin content editor, instructor content form, `messages/{en,ar,es}.json`                                                                                                                                                                                  |

---

## Task 1: Schema — add `taxExempt` to catalog, order snapshot, invoice

**Files:**

- Modify: `prisma/schema.prisma` (models `Course`, `Event`, `CourseEnrollment`, `EventRegistration`, `Invoice`)
- Create: `prisma/migrations/<timestamp>_tax_exemption/migration.sql`

- [ ] **Step 1: Locate each model's coupon/currency block as the insertion anchor**

Run: `grep -nE "model Course |model Event |model CourseEnrollment |model EventRegistration |model Invoice " prisma/schema.prisma`
Then read each block. Add fields immediately after the existing `coupon*` fields (Course/Event) and after `chargedSar`/`fxRate` (the order models), matching surrounding `@map`/alignment style by hand.

- [ ] **Step 2: Add catalog fields to `Course` and `Event`**

In both models, after the coupon fields, add:

```prisma
    taxExempt           Boolean   @default(false) @map("tax_exempt")
    taxExemptReason     String?   @map("tax_exempt_reason")
    taxExemptUpdatedById String?  @map("tax_exempt_updated_by_id") @db.Uuid
    taxExemptUpdatedAt  DateTime? @map("tax_exempt_updated_at") @db.Timestamptz(6)
```

- [ ] **Step 3: Add snapshot field to `CourseEnrollment` and `EventRegistration`**

In both models, after the `chargedSar`/`fxRate` lock fields, add:

```prisma
    taxExempt    Boolean  @default(false) @map("tax_exempt")
```

- [ ] **Step 4: Add invoice fields to `Invoice`**

After `taxAmount` in `model Invoice`, add:

```prisma
    taxExempt        Boolean        @default(false) @map("tax_exempt")
    taxExemptReason  String?        @map("tax_exempt_reason")
```

- [ ] **Step 5: Generate the migration SQL DB-free (idempotent)**

Snapshot the pre-edit schema from git, then diff:

```bash
git show origin/main:apps/experts-app/prisma/schema.prisma > /tmp/old.prisma
mkdir -p prisma/migrations/$(date -u +%Y%m%d%H%M%S)_tax_exemption
npx prisma migrate diff \
  --from-schema-datamodel /tmp/old.prisma \
  --to-schema-datamodel prisma/schema.prisma \
  --script > prisma/migrations/<the-dir>/migration.sql
```

Then make every statement idempotent — edit the generated file so each column add reads:

```sql
ALTER TABLE "public"."courses" ADD COLUMN IF NOT EXISTS "tax_exempt" BOOLEAN NOT NULL DEFAULT false;
ALTER TABLE "public"."courses" ADD COLUMN IF NOT EXISTS "tax_exempt_reason" TEXT;
ALTER TABLE "public"."courses" ADD COLUMN IF NOT EXISTS "tax_exempt_updated_by_id" UUID;
ALTER TABLE "public"."courses" ADD COLUMN IF NOT EXISTS "tax_exempt_updated_at" TIMESTAMPTZ(6);
-- ...repeat for events, course_enrollments, event_registrations (tax_exempt only), billing.invoices (tax_exempt, tax_exempt_reason)
```

(Confirm the real table/schema names from the generated diff — events may be `public."events"`, invoices are `billing."invoices"`.)

- [ ] **Step 6: Regenerate client and verify drift parity**

Run: `npx prisma generate && pnpm db:check:drift`
Expected: drift check passes (schema ≡ migrations). Fix the migration SQL until it does.

- [ ] **Step 7: Typecheck**

Run: `pnpm experts:check` (or at minimum the typecheck step)
Expected: PASS (new optional fields don't break existing code yet).

- [ ] **Step 8: Commit**

```bash
git add prisma/schema.prisma prisma/migrations
git commit -m "feat(billing): add taxExempt to catalog, order snapshot, invoice (#1040)"
```

---

## Task 2: Pricing core — exempt mode in `buyer-price-breakdown.ts`

The exempt quote skips VAT entirely: `list == total == gatewayInput == price`, `vatAmount == 0`, no coupon stacking question (coupons still apply, just on a VAT-free basis). Keep the non-exempt path **byte-identical**.

**Files:**

- Modify: `src/lib/pricing/buyer-price-breakdown.ts`
- Test: `src/lib/pricing/__tests__/buyer-price-breakdown.test.ts`

- [ ] **Step 1: Write failing tests**

Append to the test file:

```ts
import {computeBuyerBreakdown, computeChargeQuote} from '../buyer-price-breakdown'

const NO_COUPON = {
    couponEnabled: false,
    couponCode: null,
    couponDiscountType: null,
    couponDiscountValue: null
} as const

describe('tax-exempt pricing', () => {
    it('exempt: list == total == price, zero VAT, no coupon', () => {
        const b = computeBuyerBreakdown(400, NO_COUPON, null, {taxExempt: true})
        expect(b.listPriceIncVat).toBe(400)
        expect(b.grossPaidIncVat).toBe(400)
        expect(b.vatAmount).toBe(0)
    })

    it('exempt charge quote: gateway input equals the listed price (no x1.15)', () => {
        const q = computeChargeQuote(400, NO_COUPON, null, {taxExempt: true})
        expect(q?.gatewayInputAmountExVat).toBe(400)
        expect(q?.grossPaidIncVat).toBe(400)
    })

    it('non-exempt path is unchanged (regression guard)', () => {
        const exempt = computeBuyerBreakdown(400, NO_COUPON, null, {taxExempt: false})
        const legacy = computeBuyerBreakdown(400, NO_COUPON, null)
        expect(exempt).toEqual(legacy)
    })

    it('exempt + percent coupon discounts on the VAT-free basis', () => {
        const coupon = {
            couponEnabled: true,
            couponCode: 'SAVE10',
            couponDiscountType: 'percent' as const,
            couponDiscountValue: 10
        }
        const q = computeChargeQuote(400, coupon, 'SAVE10', {taxExempt: true})
        expect(q?.gatewayInputAmountExVat).toBe(360)
        expect(q?.grossPaidIncVat).toBe(360)
    })
})
```

- [ ] **Step 2: Run to verify fail**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/pricing/__tests__/buyer-price-breakdown.test.ts`
Expected: FAIL (4th positional arg / `taxExempt` option not supported).

- [ ] **Step 3: Implement the exempt option**

Add an options bag to the three public functions and branch the quote. Edit `buyer-price-breakdown.ts`:

```ts
export interface BuyerQuoteOptions {
    taxExempt?: boolean
}
```

In `quoteFor`, change the signature and add the exempt branch at the top of the function body (before `couponMatches`):

```ts
function quoteFor(price: number, coupon: BuyerCouponInput, appliedCode?: string | null, options?: BuyerQuoteOptions): ChargeQuote {
    const storedPriceExVat = round2(price)

    if (options?.taxExempt) {
        // Out-of-ZATCA-scope: no VAT. The listed price IS the total the buyer pays.
        // Coupons still apply, on the VAT-free basis.
        const matched = couponMatches(coupon, appliedCode)
        const gatewayInputAmountExVat = matched
            ? Math.max(0, round2(storedPriceExVat - discountFor(storedPriceExVat, coupon)))
            : storedPriceExVat
        return {
            storedPriceExVat,
            gatewayInputAmountExVat,
            listPriceIncVat: storedPriceExVat,
            discountAmountIncVat: round2(storedPriceExVat - gatewayInputAmountExVat),
            grossPaidIncVat: gatewayInputAmountExVat,
            couponApplied: matched
        }
    }

    const listPriceIncVat = displayPriceNumber(price)
    // ...existing non-exempt body unchanged...
}
```

Thread `options` through `computeBuyerBreakdown`, `computeChargeQuote`, and `buyerGatewayAmountExVat` (each gains a trailing `options?: BuyerQuoteOptions` param and passes it to `quoteFor`/`computeChargeQuote`). In `computeBuyerBreakdown`, `vatAmount` must be `0` when exempt — replace `vatAmount: vatFromIncl(q.grossPaidIncVat)` with:

```ts
    vatAmount: options?.taxExempt ? 0 : vatFromIncl(q.grossPaidIncVat),
```

- [ ] **Step 4: Run to verify pass**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/pricing/__tests__/buyer-price-breakdown.test.ts`
Expected: PASS (all, including regression guard).

- [ ] **Step 5: Commit**

```bash
git add src/lib/pricing
git commit -m "feat(pricing): tax-exempt mode in buyer price breakdown (#1040)"
```

---

## Task 3: Gateway charge — skip `×1.15` for exempt orders

VAT is applied in each gateway adapter via `displayPriceNumber(input.amount)`. Centralize the branch in one helper and route the exempt flag through `PaymentIntentInput`.

**Files:**

- Create: `src/lib/payments/shared/gateway-charge-amount.ts`
- Test: `src/lib/payments/shared/__tests__/gateway-charge-amount.test.ts`
- Modify: `src/lib/payments/gateways/noon/noon.gateway.ts` (lines ~69, ~177), `.../tabby/tabby.gateway.ts` (~111), `.../stripe/stripe.gateway.ts` (~26); the gateway `input` type; `src/lib/payments/payment.service.ts`

- [ ] **Step 1: Write failing test for the helper**

```ts
import {gatewayChargeAmount} from '../gateway-charge-amount'

describe('gatewayChargeAmount', () => {
    it('applies 15% VAT when not exempt', () => {
        expect(gatewayChargeAmount(400, false)).toBe(460)
    })
    it('charges the amount verbatim when exempt', () => {
        expect(gatewayChargeAmount(400, true)).toBe(400)
    })
    it('rounds exempt amounts to 2dp', () => {
        expect(gatewayChargeAmount(99.999, true)).toBe(100)
    })
})
```

- [ ] **Step 2: Run to verify fail**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/payments/shared/__tests__/gateway-charge-amount.test.ts`
Expected: FAIL (module not found).

- [ ] **Step 3: Implement the helper**

`src/lib/payments/shared/gateway-charge-amount.ts`:

```ts
import {displayPriceNumber, round2} from '@/lib/utils'

/**
 * The amount a gateway should actually charge for an ex-VAT base `amount`.
 * Standard supplies add 15% VAT (`displayPriceNumber`); out-of-ZATCA-scope
 * tax-exempt supplies are charged verbatim (the listed amount IS the total).
 */
export function gatewayChargeAmount(amountExVat: number, taxExempt?: boolean): number {
    return taxExempt ? round2(amountExVat) : displayPriceNumber(amountExVat)
}
```

(If `round2` is not exported from `@/lib/utils`, inline `Math.round(amountExVat * 100) / 100`.)

- [ ] **Step 4: Run to verify pass**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/payments/shared/__tests__/gateway-charge-amount.test.ts`
Expected: PASS.

- [ ] **Step 5: Add `taxExempt` to the payment-intent input type**

Find the input type for `createPaymentIntent` (`grep -n "PaymentIntentInput\|export interface.*Input" src/lib/payments/payment.service.ts src/lib/payments/types*`). Add an optional field:

```ts
  /** Out-of-ZATCA-scope supply: charge the amount verbatim, no 15% VAT. */
  taxExempt?: boolean;
```

Ensure `payment.service.ts` forwards `taxExempt` into each gateway's `input` (it typically spreads the input object — confirm by reading the dispatch).

- [ ] **Step 6: Swap the multiply in all three gateways**

In `noon.gateway.ts` (both call sites), `tabby.gateway.ts`, and `stripe.gateway.ts`, replace:

```ts
const amount = displayPriceNumber(input.amount)
```

with:

```ts
const amount = gatewayChargeAmount(input.amount, input.taxExempt)
```

and for stripe's inline form:

```ts
unit_amount: toMinorUnits(gatewayChargeAmount(input.amount, input.taxExempt)),
```

Add `import {gatewayChargeAmount} from "@/lib/payments/shared/gateway-charge-amount";` to each; leave the subscription-description `displayPriceNumber` in noon (line ~311) untouched (subscriptions are out of scope).

- [ ] **Step 7: Typecheck + existing gateway tests**

Run: `pnpm experts:check` and `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/payments`
Expected: PASS (non-exempt callers pass `undefined` → identical behavior).

- [ ] **Step 8: Commit**

```bash
git add src/lib/payments
git commit -m "feat(payments): skip VAT multiply for tax-exempt charges (#1040)"
```

---

## Task 4: Checkout snapshot — course handler

Read `course.taxExempt`, pass it to the pricing quote and the payment intent, and snapshot it onto the pending enrollment. Mirrors the coupon snapshot exactly.

**Files:**

- Modify: `src/lib/courses/enrollments/handlers/course-enroll.handler.ts`
- Test: `src/lib/courses/enrollments/handlers/__tests__/course-enroll.handler.test.ts`

- [ ] **Step 1: Write failing tests**

Add cases (mirror the existing coupon test setup in this file — reuse its prisma/course mocks):

```ts
it('exempt course: charges listed amount (no VAT) and snapshots taxExempt', async () => {
    // course mock with price 400, taxExempt: true, couponEnabled: false
    // assert createPaymentIntent called with amount derived from 400 (not 460) and taxExempt: true
    // assert courseEnrollment.upsert data contains taxExempt: true
})

it('non-exempt course still snapshots taxExempt: false', async () => {
    // assert upsert data contains taxExempt: false
})
```

(Use the file's existing mock harness; assert on `createPaymentIntent.mock.calls` and `prisma.courseEnrollment.upsert.mock.calls`.)

- [ ] **Step 2: Run to verify fail**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/courses/enrollments/handlers/__tests__/course-enroll.handler.test.ts`
Expected: FAIL.

- [ ] **Step 3: Read `course.taxExempt` and thread it through**

In `course-enroll.handler.ts`:

1. Ensure the `prisma.course.findUnique` select/include returns `taxExempt` (add `taxExempt: true` to the select if it uses one; if it returns the full row, it's already present).
2. Define the option once after the course is loaded:

```ts
const exemptOpts = {taxExempt: course.taxExempt} as const
```

3. Pass to the quote (both call sites):

```ts
const quote = computeChargeQuote(Number(course.price), couponInput, appliedCode, exemptOpts)
```

4. Add `taxExempt: course.taxExempt` to **every** `couponData` object branch (the applied, the cleared, and the 100%-off path's data) so it's persisted on the row.
5. Pass to the charge + payment intent:

```ts
const charge = await resolveCheckoutCharge(quote.gatewayInputAmountExVat, course.currency)
// ...
const payment = await createPaymentIntent({
    provider,
    amount: charge.sarAmount,
    currency: 'SAR',
    taxExempt: course.taxExempt
    // ...rest unchanged
})
```

- [ ] **Step 4: Run to verify pass**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/courses/enrollments/handlers/__tests__/course-enroll.handler.test.ts`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/lib/courses/enrollments/handlers
git commit -m "feat(courses): snapshot taxExempt at checkout + VAT-free charge (#1040)"
```

---

## Task 5: Checkout snapshot — event handler (symmetric sibling)

`event-register.handler.ts` is the copy-paste sibling of the course handler. Apply the **identical** changes from Task 4 (read `event.taxExempt`, thread `exemptOpts` into the quote, add `taxExempt` to every snapshot data branch, pass `taxExempt` to `createPaymentIntent`). Per memory: fix the symmetric sibling in the same feature even when only one was flagged.

**Files:**

- Modify: `src/lib/events/handlers/event-register.handler.ts`
- Test: `src/lib/events/handlers/__tests__/event-register.handler.test.ts`

- [ ] **Step 1:** Write the same two failing tests as Task 4, adapted to the event mock harness.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Apply the Task-4 changes verbatim, substituting `event` for `course` and the event's registration model for `courseEnrollment`. Confirm the event row select returns `taxExempt`.
- [ ] **Step 4:** Run → PASS: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/events/handlers/__tests__/event-register.handler.test.ts`
- [ ] **Step 5: Commit**

```bash
git add src/lib/events/handlers
git commit -m "feat(events): snapshot taxExempt at checkout + VAT-free charge (#1040)"
```

---

## Task 6: Invoice mint — `taxRate 0` + currency + exempt fields

**Files:**

- Modify: `src/lib/billing/commands/invoice-create.command.ts`, `src/lib/billing/handlers/invoice-create.handler.ts`
- Test: `src/lib/billing/handlers/__tests__/invoice-create.handler.test.ts` (create if absent)

- [ ] **Step 1: Write failing test**

```ts
it('exempt invoice: taxRate 0, taxAmount 0, currency from command, lines vatRate 0', async () => {
    // call handleInvoiceCreate with taxExempt: true, currency: "EUR",
    // lines: [{name, quantity:1, unitPriceExVat:400, vatRate:0}]
    // assert prisma.invoice.create data: {taxRate:0, taxAmount:0, currency:"EUR", taxExempt:true}
    // assert line.vatAmount === 0, line.lineIncVat === 400
})
it('non-exempt invoice unchanged: taxRate 15', async () => {
    /* ...taxRate 15 */
})
```

- [ ] **Step 2: Run → FAIL.**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/billing/handlers/__tests__/invoice-create.handler.test.ts`

- [ ] **Step 3: Add fields to the command**

In `invoice-create.command.ts`, add to `CreateInvoiceCommand`:

```ts
  taxExempt?: boolean;
  taxExemptReason?: string | null;
```

- [ ] **Step 4: Branch the handler**

In `invoice-create.handler.ts`, after `const amounts = calculateInvoice(lines);` add:

```ts
const exempt = command.taxExempt === true
const invoiceTaxRate = exempt ? 0 : 15
```

In `prisma.invoice.create({data:{...}})` replace `taxRate: 15` and add the currency + exempt fields:

```ts
          currency: command.currency,
          subtotal: amounts.subtotal,
          taxRate: invoiceTaxRate,
          taxAmount: amounts.taxAmount,
          totalAmount: amounts.totalAmount,
          taxExempt: exempt,
          taxExemptReason: command.taxExemptReason ?? null,
```

(The lines already compute VAT from each line's `vatRate`; callers pass `vatRate: 0` for exempt — see Tasks 7/8 — so `amounts.taxAmount` is naturally 0. Also fix the `payments.create.currency` to `command.currency` so a foreign exempt order records the foreign charge currency, matching the #1038 salvage.)

- [ ] **Step 5: Run → PASS.**
- [ ] **Step 6: Commit**

```bash
git add src/lib/billing/handlers src/lib/billing/commands
git commit -m "feat(billing): mint tax-exempt invoices (taxRate 0, selected currency) (#1040)"
```

---

## Task 7: Completion handler — course (settlement invariant + invoice command)

The money-critical task. The completion handler reconciles the captured amount and builds the invoice command. Both must branch on the snapshotted `enrollment.taxExempt`.

**Files:**

- Modify: `src/lib/courses/enrollments/handlers/course-enrollment-complete.handler.ts`
- Test: `src/lib/courses/enrollments/handlers/__tests__/course-enrollment-complete.handler.test.ts`

- [ ] **Step 1: Write failing property-style tests**

```ts
import {displayPriceNumber} from '@/lib/utils'

it.each([1, 99.99, 400, 1234.5])('exempt order reconciles expectedPaid == lockedSar (no VAT) for %s', async (p) => {
    // enrollment mock: chargedSar: p, taxExempt: true, amountPaid: p
    // assert NO mismatch observed; invoice command built with taxExempt:true, vatRate:0, currency: enrollment.currency
})

it.each([1, 99.99, 400])('non-exempt order still reconciles expectedPaid == displayPriceNumber(lockedSar) for %s', async (p) => {
    // enrollment mock: chargedSar: p, taxExempt: false, amountPaid: displayPriceNumber(p)
    // assert no mismatch; invoice command taxRate path vatRate:15
})
```

- [ ] **Step 2: Run → FAIL.**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/courses/enrollments/handlers/__tests__/course-enrollment-complete.handler.test.ts`

- [ ] **Step 3: Ensure `taxExempt` is selected**

Add `taxExempt: true` to the enrollment `select` block (near the `currency: true, chargedAmount: true` selects around line 119).

- [ ] **Step 4: Branch the reconciliation guard**

Find the reconciliation around line 190 (`expectedPaid: displayPriceNumber(lockedSar)`). Introduce:

```ts
const exempt = enrollment.taxExempt === true
const expectedPaid = exempt ? lockedSar : displayPriceNumber(lockedSar)
```

and use `expectedPaid` wherever `displayPriceNumber(lockedSar)` was used for the captured-amount comparison.

- [ ] **Step 5: Build the invoice command with exempt fields**

Where the handler constructs the `CreateInvoiceCommand` (the `lines` + `currency` + invoice mint call), set:

```ts
  currency: enrollment.currency ?? "SAR",
  taxExempt: exempt,
  taxExemptReason: null,
  lines: [{name: course.title, quantity: 1, unitPriceExVat: <netExVat>, vatRate: exempt ? 0 : 15}],
```

Use the existing net-ex-VAT figure the handler already derives for the line (the value it currently feeds as `unitPriceExVat`); only the `vatRate` and `currency`/`taxExempt` change.

- [ ] **Step 6: Run → PASS.**
- [ ] **Step 7: Commit**

```bash
git add src/lib/courses/enrollments/handlers
git commit -m "feat(courses): tax-exempt settlement invariant + invoice command (#1040)"
```

---

## Task 8: Completion handler — event (symmetric sibling)

Apply Task 7's changes to the event completion handler. Same reconciliation branch, same invoice-command fields.

**Files:**

- Modify: `src/lib/events/handlers/event-registration-complete.handler.ts`
- Test: `src/lib/events/handlers/__tests__/event-registration-complete.handler.test.ts`

- [ ] **Step 1:** Write the same property tests, event harness.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Apply Task-7 changes (select `taxExempt`, `expectedPaid` branch, invoice-command `vatRate`/`currency`/`taxExempt`).
- [ ] **Step 4:** Run → PASS.
- [ ] **Step 5: Commit**

```bash
git add src/lib/events/handlers
git commit -m "feat(events): tax-exempt settlement invariant + invoice command (#1040)"
```

---

## Task 9: ZATCA chokepoint — skip exempt invoices and their credit notes

Single chokepoint. `enqueueInvoiceZatca` early-returns if the invoice is exempt; `enqueueCreditNoteZatca` early-returns if its parent invoice is exempt. No e-invoice document is ever created (place the check **before** `ensureZatcaDocument`).

**Files:**

- Modify: `src/modules/billing/zatca/services/zatca-queue.service.ts`
- Test: `src/modules/billing/zatca/services/__tests__/zatca-queue.service.test.ts` (create if absent)

- [ ] **Step 1: Write failing tests**

```ts
it('exempt invoice: enqueue is a no-op (no ZATCA doc, no job)', async () => {
    // prisma.invoice.findUnique → {taxExempt: true}
    // assert ensureZatcaDocument NOT called, enqueueZatcaJob NOT called, observe('zatca.invoice.enqueue.skipped' exempt)
})
it('non-exempt invoice: enqueues as before', async () => {
    /* ensureZatcaDocument + job called */
})
it('credit note whose parent invoice is exempt: no-op', async () => {
    /* ... */
})
```

- [ ] **Step 2: Run → FAIL.**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/modules/billing/zatca/services`

- [ ] **Step 3: Add the guards**

At the top of `enqueueInvoiceZatca`, before `ensureZatcaDocument`:

```ts
const invoice = await prisma.invoice.findUnique({
    where: {id: invoiceId},
    select: {taxExempt: true}
})
if (invoice?.taxExempt) {
    observe(
        'zatca.invoice.enqueue.skipped',
        {requestId, invoiceId, reason: 'tax_exempt'},
        {level: 'info', dedupeKey: `zatca.invoice.enqueue.skipped:tax_exempt:${invoiceId}`}
    )
    return
}
```

At the top of `enqueueCreditNoteZatca`, before `ensureZatcaDocument`:

```ts
const creditNote = await prisma.creditNote.findUnique({
    where: {id: creditNoteId},
    select: {invoice: {select: {taxExempt: true}}}
})
if (creditNote?.invoice?.taxExempt) {
    observe(
        'zatca.creditNote.enqueue.skipped',
        {requestId, creditNoteId, reason: 'tax_exempt'},
        {level: 'info', dedupeKey: `zatca.creditNote.enqueue.skipped:tax_exempt:${creditNoteId}`}
    )
    return
}
```

(Confirm the `creditNote` → `invoice` relation name in `schema.prisma`; adjust the select if it differs.)

- [ ] **Step 4: Run → PASS.**
- [ ] **Step 5: Commit**

```bash
git add src/modules/billing/zatca/services
git commit -m "feat(zatca): skip e-invoicing for tax-exempt invoices + credit notes (#1040)"
```

---

## Task 10: Invoice rendering — foreign currency (salvage #1038)

Bring across only #1038's currency-rendering plumbing so the exempt foreign invoice prints in its currency. **Drop** the SAR-mirror / settlement-footnote parts (no SAR mirror exists for exempt).

**Files:**

- Create: `src/modules/billing/invoices/renderers/invoice/pdf/invoice-pdf.money.tsx` (copy from #1038 branch)
- Modify: `.../invoice/map-invoice-to-view-model.ts`, `.../invoice/pdf/invoice-pdf.tsx`, `.../invoice/html/invoice-html.tsx`
- Test: existing renderer tests + a new exempt-currency assertion

- [ ] **Step 1: Copy the `PdfMoney` component from #1038**

```bash
git show origin/fix/gh-1038-foreign-currency-invoice:apps/experts-app/src/modules/billing/invoices/renderers/invoice/pdf/invoice-pdf.money.tsx \
  > src/modules/billing/invoices/renderers/invoice/pdf/invoice-pdf.money.tsx
```

It renders `${formatted} ${currency}` for non-SAR and the SAR icon for SAR. No SAR-mirror logic in this file — keep as-is.

- [ ] **Step 2: Render money via `PdfMoney`/currency in the PDF + HTML**

In `invoice-pdf.tsx` and `invoice-html.tsx`, replace the hardcoded SAR money rendering for totals/lines with the currency-aware path (use `PdfMoney` in the PDF; in HTML, show `${amount} ${currency}` when `currency !== "SAR"`). Reference the #1038 diff for the exact swap:

```bash
git diff origin/main...origin/fix/gh-1038-foreign-currency-invoice -- \
  apps/experts-app/src/modules/billing/invoices/renderers/invoice/pdf/invoice-pdf.tsx \
  apps/experts-app/src/modules/billing/invoices/renderers/invoice/html/invoice-html.tsx
```

Take only the currency-rendering hunks; **skip** any `settlementFootnote` / `sarTotalAmount` hunks.

- [ ] **Step 3: View model passes currency through**

In `map-invoice-to-view-model.ts`, ensure `currency: inv.currency ?? "SAR"` flows to the view model (already does). Do **not** add the `settlementFootnote` block from #1038. Add an exempt note instead: if `inv.taxExempt`, set a `taxExemptNote` (wire a string in `invoice-view-model.ts`) rendered in place of the VAT line — value from i18n (Task 12) or a literal "VAT not applicable (out of scope)" fallback.

- [ ] **Step 4: Add/extend a renderer test**

Assert: an exempt EUR invoice view model renders `400 EUR` (not the SAR glyph) and shows the exempt note, no VAT line.

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/modules/billing/invoices`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/modules/billing/invoices
git commit -m "feat(billing): foreign-currency + exempt-note invoice rendering (#1040)"
```

---

## Task 11: Buyer breakdown UI — drop the VAT line when exempt

**Files:**

- Modify: `src/lib/pricing/components/buyer-price-breakdown.tsx`
- Test: `src/lib/pricing/components/__tests__/buyer-price-breakdown.test.tsx`
- Modify (data hooks): `src/lib/courses/detail/use-course-detail.ts`, `src/lib/events/detail/use-event-detail.ts` (pass `taxExempt` into the breakdown computation/props)

- [ ] **Step 1: Write failing render tests**

```ts
it("exempt: renders no VAT row and 'VAT not applicable'", () => {
  const html = renderToStaticMarkup(<BuyerPriceBreakdown {...exemptProps} />);
  expect(html).not.toContain("15%");
  expect(html).toContain("VAT not applicable"); // or the i18n key's en value
});
it("non-exempt: still renders the VAT 15% row", () => {
  const html = renderToStaticMarkup(<BuyerPriceBreakdown {...standardProps} />);
  expect(html).toContain("15%");
});
```

- [ ] **Step 2: Run → FAIL.**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/pricing/components/__tests__/buyer-price-breakdown.test.tsx`

- [ ] **Step 3: Implement**

Add a `taxExempt?: boolean` prop. Compute the breakdown with `{taxExempt}`. When exempt, render a "VAT not applicable" row (i18n `pricing.vatNotApplicable`) instead of the `VAT 15%` row; `total === list`. Pass `taxExempt` from `use-course-detail.ts` / `use-event-detail.ts` (they already pass the coupon inputs — add `taxExempt` from the course/event DTO; ensure the DTO/query carries `taxExempt` — extend the detail query `select` + DTO if missing).

- [ ] **Step 4: Run → PASS.**
- [ ] **Step 5: Commit**

```bash
git add src/lib/pricing/components src/lib/courses/detail src/lib/events/detail
git commit -m "feat(pricing): buyer breakdown hides VAT for tax-exempt content (#1040)"
```

---

## Task 12: Admin checkbox + instructor read-only + i18n

Exemption is **admin-only**. The admin content editor gets a checkbox + required reason; the instructor form shows read-only status. Mirror the existing `couponEnabled` checkbox field already present on these forms.

**Files:**

- Modify: the admin course/event editor form + its mutation/route (set `taxExempt`, `taxExemptReason`, `taxExemptUpdatedById = adminUserId`, `taxExemptUpdatedAt = now`)
- Modify: the instructor course/event form (read-only status display)
- Modify: `messages/en.json`, `messages/ar.json`, `messages/es.json`
- Test: the admin mutation test (reason required when enabling); a form render test

- [ ] **Step 1: Locate the surfaces**

```bash
grep -rln "couponEnabled" src/app src/lib --include=*.tsx | grep -iE "admin|creator|instructor|form|edit"
grep -rln "requireAdmin" src/app/api/v1/admin | head
```

The admin mutation lives under `/api/v1/admin/**` — confirm it calls `requireAdmin()` (per memory: admin API routes are NOT covered by the proxy page guard; each needs `requireAdmin()`).

- [ ] **Step 2: Write failing mutation test**

```ts
it('rejects taxExempt:true with empty reason', async () => {
    // call admin update with {taxExempt:true, taxExemptReason:""} → 400
})
it('sets taxExempt + reason + updatedBy/At when admin enables it', async () => {
    // assert prisma update data has taxExempt:true, reason, taxExemptUpdatedById, taxExemptUpdatedAt
})
```

- [ ] **Step 3: Run → FAIL.**
- [ ] **Step 4: Implement**

- Extend the admin update zod schema: `taxExempt: z.boolean().optional()`, `taxExemptReason: z.string().trim().min(1).nullable().optional()`, with a `.refine()` that `taxExemptReason` is non-empty when `taxExempt === true`.
- In the admin handler, when `taxExempt` is provided, write `taxExempt`, `taxExemptReason`, `taxExemptUpdatedById: session.user.id`, `taxExemptUpdatedAt: new Date()`.
- Admin form: add the checkbox + reason input (mirror the `couponEnabled` HeroUI field block in the same form, including the conditional reveal of the reason input).
- Instructor form: render read-only text — `taxExempt ? t("pricing.taxStatusExempt", {reason}) : t("pricing.taxStatusStandard")`. No editable control.

- [ ] **Step 5: Add i18n keys (en/ar/es, all three together)**

Add to each `messages/*.json` under `pricing` (and `admin` where the form labels live):

```json
"pricing": {
  "vatNotApplicable": "VAT not applicable (out of scope)",
  "taxStatusStandard": "Tax status: Standard (15% VAT)",
  "taxStatusExempt": "Tax status: Exempt — {reason}"
},
"admin": {
  "taxExemptLabel": "Tax-exempt (out of ZATCA scope)",
  "taxExemptReasonLabel": "Exemption reason",
  "taxExemptReasonRequired": "A reason is required to mark content tax-exempt"
}
```

Provide proper Arabic and Spanish translations (do not leave English in `ar.json`/`es.json` — per i18n rules no English leaks into Arabic surfaces).

- [ ] **Step 6: Run → PASS + full gate**

Run: `pnpm experts:check` and the relevant vitest paths.
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/app src/lib messages
git commit -m "feat(admin): admin-only tax-exempt toggle + instructor read-only + i18n (#1040)"
```

---

## Task 13: Refund credit-note path (verify, no charge change)

Refunds already route through `enqueueCreditNoteZatca`, which Task 9 now skips for exempt parents. The credit note must carry the exempt currency. Verify and add coverage; no new charge math.

**Files:**

- Modify (if needed): `src/lib/courses/enrollments/handlers/course-enrollment-refund-process.handler.ts`, `src/lib/events/registrations/handlers/event-registration-refund-process.handler.ts`
- Test: the two refund handler tests

- [ ] **Step 1: Write a failing test** asserting an exempt refund creates a credit note in the invoice's currency and does **not** enqueue ZATCA (the enqueue is mocked; assert it's called but no-ops, or assert the handler skips — match the existing test style).
- [ ] **Step 2: Run → FAIL** (if currency/exempt not propagated) **or PASS** (if already inherited). If it passes, the path is already correct — record that and skip to commit with a note.
- [ ] **Step 3: Implement** only if needed: ensure the credit note inherits `currency` and that no separate VAT is recomputed for exempt parents.
- [ ] **Step 4: Run → PASS.**
- [ ] **Step 5: Commit**

```bash
git add src/lib/courses/enrollments/handlers src/lib/events/registrations/handlers
git commit -m "test(billing): tax-exempt refund credit notes skip ZATCA, keep currency (#1040)"
```

---

## Task 14: Full gate + in-routine review + finish

- [ ] **Step 1: Full gate**

Run: `pnpm experts:check`
Expected: FORMAT / LINT / TYPECHECK clean. If any fail, `pnpm experts:check:fix` then re-run.

- [ ] **Step 2: Full test sweep for touched areas**

Run:

```bash
DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run \
  src/lib/pricing src/lib/payments src/lib/billing \
  src/lib/courses/enrollments src/lib/events \
  src/modules/billing
```

Expected: all green.

- [ ] **Step 3: gitnexus impact + change detection**

Run: `mcp__gitnexus__detect_changes` and confirm only expected symbols/flows changed.

- [ ] **Step 4: In-routine reviewers (per house rule)**

Spawn in parallel on `git diff origin/main`: `code-reviewer` + `qa-tester`; add `security-auditor` (touches money/charge path — warranted here). Triage findings: fix real bugs before push; defer separate with a PR note. Then `release-manager` last on the committed state for GO/NO-GO.

- [ ] **Step 5: Push + PR**

```bash
git push origin feat/gh-1040-tax-exemption:feat/gh-1040-tax-exemption
git ls-remote origin feat/gh-1040-tax-exemption   # confirm remote SHA
gh pr create --base main --head feat/gh-1040-tax-exemption \
  --title "feat(billing): tax exemption for out-of-ZATCA-scope content (#1040)" \
  --body "Closes #1040. See docs/superpowers/specs/2026-06-13-tax-exemption-design.md. ..."
```

- [ ] **Step 6:** After merge, verify `origin/main` contains a sentinel (e.g. `gatewayChargeAmount`) before declaring done; run post-merge resync (`npx gitnexus analyze`).

---

## Self-review notes (coverage vs spec)

- §1 data model → Task 1. §2 pricing → Task 2; charge → Task 3; invoice mint → Task 6; ZATCA → Task 9. §3 settlement invariant → Tasks 7/8 (property tests). §4 admin/instructor UI → Task 12. §5 refunds → Task 13. Foreign-currency invoice (salvage #1038) → Task 10. Buyer breakdown UI → Task 11.
- Snapshot/TOCTOU: the order carries `taxExempt` (Tasks 4/5) and completion reads the snapshot, never the catalog (Tasks 7/8).
- Regression guards: non-exempt byte-identical (Task 2 Step 1, Task 3 Step 7).
- Out of scope (subscriptions, full #1038 SAR-mirror, historical re-mint, non-SAR PSP) — not touched.
- Counsel flag recorded in spec; not a code task.

---

## PLAN REVISION (post-code-discovery — supersedes Tasks 4–8 & adds Task 8b)

Reading the live completion/settlement/invoice code surfaced four facts the original
Tasks 4–8 under-specified. This section is authoritative where it conflicts.

**Facts:**

1. The invoice is minted in `course-enrollment-complete.orchestrator.ts` (courses) and
   **inline in** `event-registration-complete.handler.ts` (events) — not in the course
   completion handler. Invoice currency today = `command.payment.currency` (= "SAR");
   foreign currency lives only in an FX-anchor note.
2. `resolveInvoiceCharge` (`converted-invoice.helper.ts`) trips its under-capture branch
   when `amountPaid < displayPriceNumber(chargedSar)`. Exempt orders pay `chargedSar`
   verbatim → would falsely trip it. Exempt must bypass `resolveInvoiceCharge`.
3. `currency` + `chargedAmount` are snapshotted onto the order **only when a coupon
   applies** (the `couponData` cleared branch nulls them). Exempt orders must snapshot
   them **always**.
4. `record-settlement.ts` hard-codes `vatRate: 0.15`. Exempt must settle at `vatRate 0`.

**Task 4/5 (course/event checkout snapshot) — REVISED additions:**

- Read `<entity>.taxExempt` (findUnique returns it).
- Pass `{taxExempt: <entity>.taxExempt}` as the 4th arg to `computeChargeQuote`.
- Pass `taxExempt: <entity>.taxExempt` to `createPaymentIntent`.
- Build `const exemptData = <entity>.taxExempt ? {taxExempt: true, currency: <entity>.currency, chargedAmount: quote.grossPaidIncVat} : {taxExempt: false};`
  and spread it AFTER `...couponData` in both upsert branches (and the 100%-off path):
  `...couponData, ...exemptData, ...fxData`. (For exempt this guarantees currency +
  chargedAmount are persisted even with no coupon; for non-exempt it only adds
  `taxExempt: false`. The FX lock `...fxData` still carries chargedSar for settlement.)

**Task 6 (invoice mint handler) — REVISED:** add `taxExempt?`/`taxExemptReason?` to the
command; in `invoice.create` data set `currency: command.currency`, `taxRate: command.taxExempt ? 0 : 15`,
`taxExempt: command.taxExempt === true`, `taxExemptReason: command.taxExemptReason ?? null`,
and `payments.create.currency: command.currency`. (Lines already compute VAT per
`line.vatRate`; callers pass `vatRate 0` for exempt → `taxAmount` naturally 0.)

**Task 7 (course completion) — REVISED:** in `handleCourseEnrollmentComplete` select
`taxExempt` + `course.taxExemptReason`. Compute `const exempt = enrollment.taxExempt === true;`.

- chargeIntegrity: `expectedPaid: exempt ? lockedSar : displayPriceNumber(lockedSar)`.
- Branch the pending-invoice resolution:
    - exempt: `invoiceExVat = Number(enrollment.chargedAmount ?? enrollment.course.price)`;
      `invoiceCurrency = enrollment.currency ?? "SAR"`; `vatRate 0`; `fxAnchor = null`;
      `taxExemptReason = enrollment.course.taxExemptReason ?? null`. Do NOT call `resolveInvoiceCharge`.
    - non-exempt: existing `resolveInvoiceCharge` path; `invoiceCurrency = command.payment.currency`; `vatRate 15`; fxAnchor as today; reason null.
- Extend `PendingInvoiceContext` with `taxExempt`, `invoiceCurrency`, `taxExemptReason`.
- Orchestrator: `unitPriceExVat: pendingInvoice.invoiceExVat`, `vatRate: pendingInvoice.taxExempt ? 0 : 15`,
  `currency: pendingInvoice.invoiceCurrency`, `taxExempt: pendingInvoice.taxExempt`,
  `taxExemptReason: pendingInvoice.taxExemptReason`,
  `notes: pendingInvoice.taxExempt ? "Tax-exempt (out of ZATCA scope): <reason>" : buildInvoiceNotes(base, fxAnchor)`.

**Task 8 (event completion) — REVISED:** same as Task 7 but the event handler mints
inline (no orchestrator). Apply the same `exempt` branch to the `handleInvoiceCreate`
call already in that handler (currency, vatRate, taxExempt, reason, note; bypass
`resolveInvoiceCharge` for exempt).

**Task 8b (settlement writer) — NEW:** in `record-settlement.ts`, the order facts
(`resolveCourseFacts`/`resolveEventFacts` or equivalent) must read `taxExempt` from the
enrollment/registration row; when exempt, compute the breakdown with `vatRate 0`
(`vatAmount 0`, `netExVat = grossPaid`) instead of the hard-coded `VAT_RATE`. Subscriptions
unchanged. Property test: exempt order → `vatAmount 0`, `netExVat == grossPaid`;
non-exempt → unchanged 15% split.

**Property tests (Tasks 7/8/8b):** exempt order charges & settles exactly `p`
(invoice total == `p`, taxAmount 0, netExVat == `p`); non-exempt unchanged.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
