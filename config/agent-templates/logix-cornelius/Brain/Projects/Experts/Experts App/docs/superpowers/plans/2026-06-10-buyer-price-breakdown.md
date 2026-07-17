---
title: "2026 06 10 buyer price breakdown"
date: "2026-06-10"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/plans/2026-06-10-buyer-price-breakdown.md"
---
# Buyer Price Breakdown + Coupon at Checkout + Currency Groundwork — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Buyer-facing price breakdown (list price / coupon / VAT / total) on paid course & event detail pages, real coupon application at checkout with TOCTOU-safe snapshots feeding settlement, and a `currency` column groundwork for future multi-currency.

**Architecture:** A pure pricing module (`src/lib/pricing/buyer-price-breakdown.ts`) is the single math source for both the client breakdown component and the server charge computation. A shared `<BuyerPriceBreakdown>` component (messages-prop pattern, like `CreatorPriceBreakdown`) renders in both detail sidebars. Coupon snapshots are written on the pending enrollment/registration at checkout initiation; completion, invoices, and settlement read the snapshot (scenario-A `priceOrder` inputs).

**Review amendment (2026-06-10):** Execute this plan with the review findings in `docs/superpowers/reviews/2026-06-10-buyer-price-event-refund-plan-review.md` applied. The original plan incorrectly said gateways pass `input.amount` through. Current Stripe/Noon/Tabby adapters charge `displayPriceNumber(input.amount)`, so checkout must send an ex-VAT gateway input while persisting VAT-inclusive buyer/invoice/settlement snapshots.

**Tech Stack:** Next.js 16 (App Router), Prisma 7 + PostgreSQL, zod, HeroUI v3, next-intl (en/ar/es), vitest (node env, `renderToStaticMarkup` for components).

**Spec:** `docs/superpowers/specs/2026-06-10-buyer-price-breakdown-design.md` (operator-approved).

**Working tree:** the isolated worktree `/home/logix/experts-price-breakdown`, branch `feat/buyer-price-breakdown`. All commands below run from `/home/logix/experts-price-breakdown/apps/experts-app` unless stated otherwise.

**House rules that bind every task:**

- Invoke `experts-constellation` skill before writing code and before committing (mandatory for experts-app).
- NEVER run `npx prisma format` (it rewrites the whole 4500-line schema). Hand-edit model blocks matching surrounding style.
- Run `pnpm experts:check` in a SEPARATE tool call before any commit; if FORMAT/LINT/TYPECHECK fails run `pnpm experts:check:fix` and re-check. Never batch check+commit in one shell invocation.
- Courses↔events are copy-paste siblings: every server-side change ships for both in the same logical unit.
- Tests need `DATABASE_URL=postgresql://localhost/experts_test` in the environment.
- No `git checkout`, no pushing, no PR creation inside tasks — the operator handles ship-out via experts-ship at the end.

**Corrected amount basis (binding for every task):**

1. `storedPriceExVat`: catalog `Course.price` / `Event.price`.
2. `listPriceIncVat`: `displayPriceNumber(storedPriceExVat)`.
3. `discountAmountIncVat`: coupon discount against `listPriceIncVat`.
4. `grossPaidIncVat`: buyer-visible/captured/invoice/settlement amount.
5. `gatewayInputAmountExVat`: `grossPaidIncVat / VAT_FACTOR`, passed to `createPaymentIntent` because gateways add VAT internally.

For stored price `400` and 20% coupon: `listPriceIncVat=460`, `discountAmountIncVat=92`, `gatewayInputAmountExVat=320`, `grossPaidIncVat=368`.

**Currency rule:** add schema/DTO/display groundwork only. Checkout rejects non-SAR and continues passing `"SAR"` to payment providers until payment, invoice, ZATCA, and settlement contracts are deliberately widened.

**Invariant:** `Payment captured gross == Invoice.totalAmount == enrollment/registration.amountPaid == OrderSettlement.grossPaid` for discounted paid purchases.

---

### Task 1: Pure pricing module

**Files:**

- Create: `src/lib/pricing/buyer-price-breakdown.ts`
- Test: `src/lib/pricing/__tests__/buyer-price-breakdown.test.ts`

- [ ] **Step 1: Write the failing test**

```ts
// src/lib/pricing/__tests__/buyer-price-breakdown.test.ts
import {describe, expect, it} from 'vitest'
import {computeBuyerBreakdown, computeChargeQuote, couponMatches, type BuyerCouponInput} from '@/lib/pricing/buyer-price-breakdown'

const percentCoupon: BuyerCouponInput = {
    couponEnabled: true,
    couponCode: 'SAVE20',
    couponDiscountType: 'percent',
    couponDiscountValue: 0.2 // unit fraction, matching priceOrder convention
}

const fixedCoupon: BuyerCouponInput = {
    couponEnabled: true,
    couponCode: 'FLAT50',
    couponDiscountType: 'fixed',
    couponDiscountValue: 50
}

const noCoupon: BuyerCouponInput = {
    couponEnabled: false,
    couponCode: null,
    couponDiscountType: null,
    couponDiscountValue: null
}

describe('couponMatches', () => {
    it('matches case-insensitively after trimming', () => {
        expect(couponMatches(percentCoupon, '  save20 ')).toBe(true)
    })
    it('rejects wrong code, disabled coupon, and missing applied code', () => {
        expect(couponMatches(percentCoupon, 'SAVE21')).toBe(false)
        expect(couponMatches({...percentCoupon, couponEnabled: false}, 'SAVE20')).toBe(false)
        expect(couponMatches(percentCoupon, null)).toBe(false)
        expect(couponMatches(noCoupon, 'SAVE20')).toBe(false)
    })
    it('rejects coupon rows with incomplete config', () => {
        expect(couponMatches({...percentCoupon, couponDiscountValue: null}, 'SAVE20')).toBe(false)
        expect(couponMatches({...percentCoupon, couponDiscountType: null}, 'SAVE20')).toBe(false)
    })
})

describe('computeBuyerBreakdown (VAT-inclusive buyer basis)', () => {
    it('no coupon: list = display price, gross = list, VAT extracted from gross', () => {
        const b = computeBuyerBreakdown(400, noCoupon, null)
        expect(b.storedPriceExVat).toBe(400)
        expect(b.listPriceIncVat).toBe(460) // 400 × 1.15
        expect(b.discountAmountIncVat).toBe(0)
        expect(b.grossPaidIncVat).toBe(460)
        expect(b.vatAmount).toBe(60) // 460 − 460/1.15
        expect(b.couponApplied).toBe(false)
    })
    it('percent coupon applies to the VAT-inclusive list price', () => {
        const b = computeBuyerBreakdown(400, percentCoupon, 'SAVE20')
        expect(b.listPriceIncVat).toBe(460)
        expect(b.discountAmountIncVat).toBe(92) // 20% of 460
        expect(b.grossPaidIncVat).toBe(368)
        expect(b.couponApplied).toBe(true)
    })
    it('fixed coupon subtracts the VAT-inclusive SAR amount, clamped to list price', () => {
        const b = computeBuyerBreakdown(400, fixedCoupon, 'FLAT50')
        expect(b.discountAmountIncVat).toBe(50)
        expect(b.grossPaidIncVat).toBe(410)
        const clamped = computeBuyerBreakdown(20, fixedCoupon, 'FLAT50')
        expect(clamped.discountAmountIncVat).toBe(23) // min(50, 20×1.15)
        expect(clamped.grossPaidIncVat).toBe(0)
    })
    it('unmatched code yields no discount', () => {
        const b = computeBuyerBreakdown(400, percentCoupon, 'WRONG')
        expect(b.discountAmountIncVat).toBe(0)
        expect(b.couponApplied).toBe(false)
    })
})

describe('computeChargeQuote', () => {
    it('returns null for an invalid code (never silently charges full price)', () => {
        expect(computeChargeQuote(400, percentCoupon, 'WRONG')).toBeNull()
        expect(computeChargeQuote(400, noCoupon, 'SAVE20')).toBeNull()
    })
    it('keeps gateway input ex-VAT while snapshots remain VAT-inclusive', () => {
        const q = computeChargeQuote(400, percentCoupon, 'save20')
        expect(q).toEqual({
            storedPriceExVat: 400,
            gatewayInputAmountExVat: 320,
            listPriceIncVat: 460,
            discountAmountIncVat: 92,
            grossPaidIncVat: 368,
            couponApplied: true
        })
    })
    it('fixed coupon clamps to the VAT-inclusive list price (100% discount → 0, never negative)', () => {
        const q = computeChargeQuote(30, fixedCoupon, 'FLAT50')
        expect(q).toEqual({
            storedPriceExVat: 30,
            gatewayInputAmountExVat: 0,
            listPriceIncVat: 34.5,
            discountAmountIncVat: 34.5,
            grossPaidIncVat: 0,
            couponApplied: true
        })
    })
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/pricing/__tests__/buyer-price-breakdown.test.ts`
Expected: FAIL — module `@/lib/pricing/buyer-price-breakdown` not found.

- [ ] **Step 3: Write the implementation**

```ts
// src/lib/pricing/buyer-price-breakdown.ts
/**
 * Buyer-facing price math, shared by the detail-page breakdown component and
 * the enroll/register charge computation. Single source of truth.
 *
 * Two bases, intentionally different (operator decision, see GitHub issue
 * filed in Task 12 — update this reference with the real number):
 * - DISPLAY basis (computeBuyerBreakdown): price × VAT_FACTOR, matching the
 *   page's existing `SaudiRiyal type="display"` convention.
 * - CHARGE basis (computeChargeAmount): Number(price) verbatim, matching what
 *   createPaymentIntent has always charged (and what settlement treats as
 *   VAT-inclusive gross).
 */
import {clampPercentFraction} from '@/lib/number/percent-fraction'
import {displayPriceNumber, vatFromIncl} from '@/lib/utils'

export interface BuyerCouponInput {
    couponEnabled: boolean
    couponCode: string | null
    couponDiscountType: 'percent' | 'fixed' | null
    couponDiscountValue: number | null
}

export interface BuyerBreakdown {
    storedPriceExVat: number
    listPriceIncVat: number
    discountAmountIncVat: number
    vatAmount: number
    grossPaidIncVat: number
    couponApplied: boolean
}

export interface ChargeQuote {
    storedPriceExVat: number
    gatewayInputAmountExVat: number
    listPriceIncVat: number
    discountAmountIncVat: number
    grossPaidIncVat: number
    couponApplied: boolean
}

function round2(value: number): number {
    return Math.round(value * 100) / 100
}

function normalizeCouponCode(code: string): string {
    return code.trim().toLowerCase()
}

export function couponMatches(coupon: BuyerCouponInput, appliedCode: string | null | undefined): boolean {
    if (!coupon.couponEnabled || !coupon.couponCode || !coupon.couponDiscountType || coupon.couponDiscountValue == null) {
        return false
    }
    if (!appliedCode || !appliedCode.trim()) return false
    return normalizeCouponCode(coupon.couponCode) === normalizeCouponCode(appliedCode)
}

function discountFor(basis: number, coupon: BuyerCouponInput): number {
    if (coupon.couponDiscountType === 'percent') {
        return round2(basis * clampPercentFraction(coupon.couponDiscountValue ?? 0))
    }
    return round2(Math.min(coupon.couponDiscountValue ?? 0, basis))
}

export function computeBuyerBreakdown(price: number, coupon: BuyerCouponInput, appliedCode?: string | null): BuyerBreakdown {
    const listPrice = displayPriceNumber(price)
    const couponApplied = couponMatches(coupon, appliedCode)
    const discountAmount = couponApplied ? discountFor(listPrice, coupon) : 0
    const total = Math.max(0, round2(listPrice - discountAmount))
    return {listPrice, discountAmount, vatAmount: vatFromIncl(total), total, couponApplied}
}

/** Returns null when the code does not match an enabled, fully-configured coupon. */
export function computeChargeQuote(price: number, coupon: BuyerCouponInput, appliedCode?: string | null): ChargeQuote | null {
    // Implementation should match the checked-in source; gateways add VAT internally.
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/pricing/__tests__/buyer-price-breakdown.test.ts`
Expected: PASS (all tests). If the `vatFromIncl(460)` expectation is off by a cent, fix the TEST to the helper's actual rounding (the helper is canon), not the helper.

- [ ] **Step 5: Commit**

```bash
git add src/lib/pricing/buyer-price-breakdown.ts src/lib/pricing/__tests__/buyer-price-breakdown.test.ts
git commit -m "feat(pricing): pure buyer price-breakdown + charge-quote math"
```

---

### Task 2: Schema — currency column + coupon snapshot columns + migration

**Files:**

- Modify: `prisma/schema.prisma` (Course ~line 340, Event ~line 862, CourseEnrollment ~line 757, EventRegistration ~line 1088)
- Create: `prisma/migrations/<timestamp>_buyer_breakdown_currency_coupon_snapshot/migration.sql`

- [ ] **Step 1: Hand-edit the four model blocks** (match surrounding alignment/style exactly; do NOT run `prisma format`)

In `model Course`, directly after the `price` line (line 340):

```prisma
    price                     Decimal                       @default(0) @db.Decimal(10, 2)
    currency                  String                        @default("SAR") @db.VarChar(10)
```

In `model Event`, directly after its `price` line (line 862):

```prisma
    price                     Decimal             @default(0) @db.Decimal(10, 2)
    currency                  String              @default("SAR") @db.VarChar(10)
```

(`VarChar(10)` matches the existing `currency` convention on `Invoice` and `CoursePriceVersion`/`EventPriceVersion`.)

In `model CourseEnrollment`, after `billingCountryCode` (line 757):

```prisma
    billingCountryCode String?                @map("billing_country_code") @db.VarChar(2)
    couponCode         String?                @map("coupon_code") @db.VarChar(64)
    couponDiscount     Decimal?               @map("coupon_discount") @db.Decimal(10, 2)
    couponListPrice    Decimal?               @map("coupon_list_price") @db.Decimal(10, 2)
```

In `model EventRegistration`, after its `billingCountryCode` (line 1088):

```prisma
    billingCountryCode String?                 @map("billing_country_code") @db.VarChar(2)
    couponCode         String?                 @map("coupon_code") @db.VarChar(64)
    couponDiscount     Decimal?                @map("coupon_discount") @db.Decimal(10, 2)
    couponListPrice    Decimal?                @map("coupon_list_price") @db.Decimal(10, 2)
```

- [ ] **Step 2: Generate the migration SQL DB-free** (house pattern from EXP-149: `migrate diff --from-schema <old> --to-schema <new> --script`)

```bash
git show HEAD:apps/experts-app/prisma/schema.prisma > /tmp/schema-old.prisma
mkdir -p prisma/migrations/$(date +%Y%m%d%H%M%S)_buyer_breakdown_currency_coupon_snapshot
npx prisma migrate diff --from-schema /tmp/schema-old.prisma --to-schema prisma/schema.prisma --script > prisma/migrations/<the-dir-you-just-made>/migration.sql
```

Then hand-edit the generated SQL to be idempotent (`ADD COLUMN IF NOT EXISTS`). Expected content (verify the diff output matches; table/schema prefixes come from the generator):

```sql
ALTER TABLE "public"."courses" ADD COLUMN IF NOT EXISTS "currency" VARCHAR(10) NOT NULL DEFAULT 'SAR';
ALTER TABLE "public"."events" ADD COLUMN IF NOT EXISTS "currency" VARCHAR(10) NOT NULL DEFAULT 'SAR';
ALTER TABLE "public"."course_enrollments" ADD COLUMN IF NOT EXISTS "coupon_code" VARCHAR(64);
ALTER TABLE "public"."course_enrollments" ADD COLUMN IF NOT EXISTS "coupon_discount" DECIMAL(10,2);
ALTER TABLE "public"."course_enrollments" ADD COLUMN IF NOT EXISTS "coupon_list_price" DECIMAL(10,2);
ALTER TABLE "public"."event_registrations" ADD COLUMN IF NOT EXISTS "coupon_code" VARCHAR(64);
ALTER TABLE "public"."event_registrations" ADD COLUMN IF NOT EXISTS "coupon_discount" DECIMAL(10,2);
ALTER TABLE "public"."event_registrations" ADD COLUMN IF NOT EXISTS "coupon_list_price" DECIMAL(10,2);
```

- [ ] **Step 3: Regenerate the client and run the drift gate**

```bash
npx prisma generate
pnpm db:check:drift
```

Expected: generate succeeds; drift gate reports schema ↔ migrations parity. If drift fails, the migration SQL doesn't match the schema edit — reconcile before continuing.

- [ ] **Step 4: Commit**

```bash
git add prisma/schema.prisma prisma/migrations/
git commit -m "feat(schema): currency on Course/Event + coupon snapshot on enrollments/registrations"
```

---

### Task 3: Thread `currency` through DTOs and mappers

**Files:**

- Modify: `src/lib/courses/catalog/dto/course.dto.ts` (~line 163, next to `price`)
- Modify: `src/lib/courses/catalog/mappers/course.mapper.ts`
- Modify: `src/lib/events/dto/event.dto.ts` (~line 176, next to `price`)
- Modify: `src/lib/events/mappers/event.mapper.ts`
- Test: extend `src/lib/courses/catalog/mappers/__tests__/course.mapper.test.ts`

- [ ] **Step 1: Add the failing assertion** — in the existing course mapper test, find the test that asserts `price` on the mapped DTO and add alongside it:

```ts
expect(dto.currency).toBe('SAR')
```

If the test fixture course object now fails typecheck for a missing `currency` field, add `currency: "SAR"` to the fixture.

- [ ] **Step 2: Run to verify it fails**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/courses/catalog/mappers/__tests__/course.mapper.test.ts`
Expected: FAIL — `currency` undefined on DTO.

- [ ] **Step 3: Implement** — in `course.dto.ts` add directly under `price: number;`:

```ts
price: number
currency: string
```

In `course.mapper.ts`, in the object literal where `price: Number(course.price)` (or equivalent) is emitted, add:

```ts
  currency: course.currency,
```

Mirror both edits in `event.dto.ts` / `event.mapper.ts` (`currency: event.currency`). If the events mapper has its own test with a fixture, add `currency: "SAR"` there too.

- [ ] **Step 4: Run mapper tests + targeted typecheck**

```bash
DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/courses/catalog/mappers src/lib/events/mappers
pnpm typecheck:touched -- src/lib/courses/catalog/dto/course.dto.ts src/lib/courses/catalog/mappers/course.mapper.ts src/lib/events/dto/event.dto.ts src/lib/events/mappers/event.mapper.ts
```

Expected: PASS. (Watch for events-local duplicate DTO definitions — the shared-DTO lesson: if a second `EventDTO`-ish type exists in `src/lib/events/registrations/dto/`, leave it alone; only the canonical DTO gains `currency`.)

- [ ] **Step 5: Commit**

```bash
git add src/lib/courses/catalog/dto/course.dto.ts src/lib/courses/catalog/mappers/ src/lib/events/dto/event.dto.ts src/lib/events/mappers/
git commit -m "feat(dto): expose currency on CourseDTO/EventDTO"
```

---

### Task 4: i18n keys (en/ar/es)

**Files:**

- Modify: `src/i18n/messages/en/pricing.json`
- Modify: `src/i18n/messages/ar/pricing.json`
- Modify: `src/i18n/messages/es/pricing.json`

The `pricing` namespace is already registered in `src/i18n/request.ts` — no wiring change needed.

- [ ] **Step 1: Add a top-level `"breakdown"` object** as a sibling of the existing `"common"` key in each locale file.

`en/pricing.json`:

```json
"breakdown": {
  "title": "Price breakdown",
  "listPrice": "Price",
  "coupon": "Coupon {code}",
  "vat": "VAT ({rate}%)",
  "total": "Total",
  "couponLabel": "Have a coupon?",
  "couponPlaceholder": "Enter coupon code",
  "apply": "Apply",
  "remove": "Remove",
  "invalidCoupon": "This coupon code is not valid"
}
```

`ar/pricing.json`:

```json
"breakdown": {
  "title": "تفاصيل السعر",
  "listPrice": "السعر",
  "coupon": "قسيمة {code}",
  "vat": "ضريبة القيمة المضافة ({rate}٪)",
  "total": "الإجمالي",
  "couponLabel": "هل لديك قسيمة خصم؟",
  "couponPlaceholder": "أدخل رمز القسيمة",
  "apply": "تطبيق",
  "remove": "إزالة",
  "invalidCoupon": "رمز القسيمة غير صالح"
}
```

`es/pricing.json`:

```json
"breakdown": {
  "title": "Desglose del precio",
  "listPrice": "Precio",
  "coupon": "Cupón {code}",
  "vat": "IVA ({rate}%)",
  "total": "Total",
  "couponLabel": "¿Tienes un cupón?",
  "couponPlaceholder": "Introduce el código del cupón",
  "apply": "Aplicar",
  "remove": "Quitar",
  "invalidCoupon": "Este código de cupón no es válido"
}
```

- [ ] **Step 2: Validate JSON parses**

Run: `node -e "['en','ar','es'].forEach(l => JSON.parse(require('fs').readFileSync('src/i18n/messages/'+l+'/pricing.json','utf8')))"`
Expected: silent success.

- [ ] **Step 3: Commit**

```bash
git add src/i18n/messages/en/pricing.json src/i18n/messages/ar/pricing.json src/i18n/messages/es/pricing.json
git commit -m "feat(i18n): pricing.breakdown buyer-facing keys (en/ar/es)"
```

---

### Task 5: `MoneyAmount` + `BuyerPriceBreakdown` components

**Files:**

- Create: `src/lib/pricing/components/money-amount.tsx`
- Create: `src/lib/pricing/components/buyer-price-breakdown.tsx`
- Test: `src/lib/pricing/components/__tests__/buyer-price-breakdown.test.tsx`

- [ ] **Step 1: Write the failing component test** (node-env `renderToStaticMarkup` + string asserts — house convention; NO testing-library, no DOM events. Interactive behavior is covered by the Task 1 pure functions.)

```tsx
// src/lib/pricing/components/__tests__/buyer-price-breakdown.test.tsx
import {describe, expect, it} from 'vitest'
import {renderToStaticMarkup} from 'react-dom/server'
import {BuyerPriceBreakdown} from '@/lib/pricing/components/buyer-price-breakdown'
import type {BuyerCouponInput} from '@/lib/pricing/buyer-price-breakdown'

const messages = {
    title: 'Price breakdown',
    listPrice: 'Price',
    coupon: 'Coupon {code}',
    vat: 'VAT (15%)',
    total: 'Total',
    couponLabel: 'Have a coupon?',
    couponPlaceholder: 'Enter coupon code',
    apply: 'Apply',
    remove: 'Remove',
    invalidCoupon: 'This coupon code is not valid'
}

const coupon: BuyerCouponInput = {
    couponEnabled: true,
    couponCode: 'SAVE20',
    couponDiscountType: 'percent',
    couponDiscountValue: 0.2
}

const noCoupon: BuyerCouponInput = {
    couponEnabled: false,
    couponCode: null,
    couponDiscountType: null,
    couponDiscountValue: null
}

function render(props: Partial<Parameters<typeof BuyerPriceBreakdown>[0]> = {}) {
    return renderToStaticMarkup(
        <BuyerPriceBreakdown
            price={400}
            currency="SAR"
            isFree={false}
            coupon={noCoupon}
            appliedCouponCode={null}
            onApplyCoupon={() => {}}
            messages={messages}
            {...props}
        />
    )
}

describe('BuyerPriceBreakdown', () => {
    it('renders nothing for free items', () => {
        expect(render({isFree: true})).toBe('')
        expect(render({price: 0})).toBe('')
    })

    it('renders list price, VAT and total on the display basis', () => {
        const html = render()
        expect(html).toContain('Price breakdown')
        expect(html).toContain('460.00') // list = total, 400 × 1.15
        expect(html).toContain('60.00') // VAT extracted
        expect(html).toContain('Total')
    })

    it('shows the coupon row and discounted total when a code is applied', () => {
        const html = render({coupon, appliedCouponCode: 'SAVE20'})
        expect(html).toContain('SAVE20')
        expect(html).toContain('92.00') // 20% of 460
        expect(html).toContain('368.00')
    })

    it('offers the coupon input only when the item has an enabled coupon', () => {
        expect(render()).not.toContain('Have a coupon?')
        expect(render({coupon})).toContain('Have a coupon?')
    })

    it('renders non-SAR currencies through Intl, not the riyal glyph', () => {
        const html = render({currency: 'USD'})
        expect(html).toContain('$')
    })
})
```

- [ ] **Step 2: Run to verify it fails**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/pricing/components/__tests__/buyer-price-breakdown.test.tsx`
Expected: FAIL — components not found.

- [ ] **Step 3: Implement `MoneyAmount`** (the multi-currency seam)

```tsx
// src/lib/pricing/components/money-amount.tsx
import {SaudiRiyal} from '@/components/ui/saudi-riyal'

/**
 * Currency-aware money renderer. SAR keeps the existing riyal-glyph component;
 * any future currency renders through Intl. `amount` is a FINAL display value —
 * no VAT math happens here (callers pass already-computed breakdown numbers),
 * hence SaudiRiyal type="format".
 */
export function MoneyAmount({amount, currency, className}: {amount: number; currency: string; className?: string}) {
    if (currency === 'SAR') {
        return <SaudiRiyal value={amount} size="sm" type="format" className={className} />
    }
    return (
        <span dir="ltr" className={className}>
            {new Intl.NumberFormat('en', {style: 'currency', currency}).format(amount)}
        </span>
    )
}
```

- [ ] **Step 4: Implement `BuyerPriceBreakdown`**

```tsx
// src/lib/pricing/components/buyer-price-breakdown.tsx
'use client'

import {useState} from 'react'
import {BadgePercent, Receipt} from 'lucide-react'
import {Button, Input} from '@heroui/react'
import {computeBuyerBreakdown, couponMatches, type BuyerCouponInput} from '@/lib/pricing/buyer-price-breakdown'
import {MoneyAmount} from '@/lib/pricing/components/money-amount'

export type BuyerPriceBreakdownMessages = {
    title: string
    listPrice: string
    coupon: string // contains {code}
    vat: string // pre-interpolated by the caller (rate baked in)
    total: string
    couponLabel: string
    couponPlaceholder: string
    apply: string
    remove: string
    invalidCoupon: string
}

type BuyerPriceBreakdownProps = {
    price: number
    currency: string
    isFree: boolean
    coupon: BuyerCouponInput
    appliedCouponCode: string | null
    onApplyCoupon: (code: string | null) => void
    messages: BuyerPriceBreakdownMessages
}

function Row({
    label,
    amount,
    currency,
    negative = false,
    emphasis = false
}: {
    label: string
    amount: number
    currency: string
    negative?: boolean
    emphasis?: boolean
}) {
    return (
        <div className="flex items-center justify-between gap-3 text-sm">
            <span className={emphasis ? 'font-semibold' : 'text-muted-foreground'}>{label}</span>
            <span className={negative ? 'text-emerald-600' : emphasis ? 'font-semibold' : 'text-muted-foreground'}>
                {negative ? <span dir="ltr">-</span> : null}
                <MoneyAmount amount={amount} currency={currency} />
            </span>
        </div>
    )
}

export function BuyerPriceBreakdown({
    price,
    currency,
    isFree,
    coupon,
    appliedCouponCode,
    onApplyCoupon,
    messages
}: BuyerPriceBreakdownProps) {
    const [draftCode, setDraftCode] = useState('')
    const [invalid, setInvalid] = useState(false)

    if (isFree || price <= 0) return null

    const breakdown = computeBuyerBreakdown(price, coupon, appliedCouponCode)
    const couponOffered = coupon.couponEnabled && Boolean(coupon.couponCode)

    const handleApply = () => {
        if (couponMatches(coupon, draftCode)) {
            setInvalid(false)
            onApplyCoupon(draftCode.trim())
        } else {
            setInvalid(true)
        }
    }

    return (
        <div className="border-border/60 space-y-3 rounded-2xl border border-dashed bg-white p-3">
            <div className="flex items-center gap-2">
                <Receipt className="text-muted-foreground h-4 w-4" />
                <p className="text-sm font-medium">{messages.title}</p>
            </div>

            <div className="space-y-2" aria-live="polite">
                <Row label={messages.listPrice} amount={breakdown.listPrice} currency={currency} />
                {breakdown.couponApplied && appliedCouponCode ? (
                    <Row
                        label={messages.coupon.replace('{code}', appliedCouponCode.trim().toUpperCase())}
                        amount={breakdown.discountAmount}
                        currency={currency}
                        negative
                    />
                ) : null}
                <Row label={messages.vat} amount={breakdown.vatAmount} currency={currency} />
                <div className="border-border/50 border-t pt-2">
                    <Row label={messages.total} amount={breakdown.total} currency={currency} emphasis />
                </div>
            </div>

            {couponOffered &&
                (breakdown.couponApplied ? (
                    <Button
                        variant="ghost"
                        size="sm"
                        type="button"
                        className="text-muted-foreground w-full text-xs"
                        onClick={() => {
                            setDraftCode('')
                            onApplyCoupon(null)
                        }}
                    >
                        <BadgePercent className="h-3 w-3 ltr:mr-1 rtl:ml-1" />
                        {messages.remove}
                    </Button>
                ) : (
                    <div className="space-y-1">
                        <label htmlFor="buyer-coupon-code" className="text-muted-foreground text-xs">
                            {messages.couponLabel}
                        </label>
                        <div className="flex items-center gap-2">
                            <Input
                                id="buyer-coupon-code"
                                value={draftCode}
                                onChange={(e) => {
                                    setDraftCode(e.target.value)
                                    setInvalid(false)
                                }}
                                placeholder={messages.couponPlaceholder}
                                className="h-9 flex-1 text-sm"
                            />
                            <Button size="sm" variant="outline" type="button" onClick={handleApply} isDisabled={!draftCode.trim()}>
                                {messages.apply}
                            </Button>
                        </div>
                        {invalid && (
                            <p className="text-danger text-xs" role="alert">
                                {messages.invalidCoupon}
                            </p>
                        )}
                    </div>
                ))}
        </div>
    )
}
```

Note: if `@heroui/react` `Input` has a different prop surface (e.g. `onValueChange` instead of `onChange`), check an existing in-tree usage (`rg -n "<Input" src/lib --type tsx | head`) and match it.

- [ ] **Step 5: Run to verify it passes**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/pricing/components/__tests__/buyer-price-breakdown.test.tsx`
Expected: PASS. If the HeroUI `Input` pulls client-only context that breaks static render, swap it for a plain `<input>` styled with the same classes as nearby kit inputs — note the deviation in the commit body.

- [ ] **Step 6: Commit**

```bash
git add src/lib/pricing/components/money-amount.tsx src/lib/pricing/components/buyer-price-breakdown.tsx src/lib/pricing/components/__tests__/buyer-price-breakdown.test.tsx
git commit -m "feat(pricing): buyer-facing MoneyAmount + BuyerPriceBreakdown components"
```

---

### Task 6: Wire breakdown into the COURSE detail page (sidebar + mobile bar + enroll body)

**Files:**

- Modify: `src/lib/courses/detail/use-course-detail.ts` (~lines 230-330)
- Modify: `src/lib/courses/detail/course-detail-page.tsx`
- Modify: `src/lib/courses/detail/sections/course-detail-sidebar.tsx`
- Modify: `src/lib/courses/detail/sections/course-detail-mobile-bar.tsx`

- [ ] **Step 1: Hook state + request body** — in `use-course-detail.ts`:

Add state next to `enrollingProvider`:

```ts
const [appliedCouponCode, setAppliedCouponCode] = useState<string | null>(null)
```

In `handleEnroll`'s `JSON.stringify({...})` body (line ~246), add after `provider,`:

```ts
            ...(appliedCouponCode ? {couponCode: appliedCouponCode} : {}),
```

Add `appliedCouponCode` to the `useCallback` dependency array, and export `appliedCouponCode` + `setAppliedCouponCode` from the hook's return object (next to `handleEnroll`).

- [ ] **Step 2: Sidebar** — in `course-detail-sidebar.tsx`:

Add to `CourseDetailSidebarProps`:

```ts
  appliedCouponCode: string | null;
  onApplyCoupon: (code: string | null) => void;
```

Destructure both in the component. Add imports:

```ts
import {useTranslations} from 'next-intl' // already imported — just add the second hook call below
import {BuyerPriceBreakdown} from '@/lib/pricing/components/buyer-price-breakdown'
import {computeBuyerBreakdown} from '@/lib/pricing/buyer-price-breakdown'
import {VAT_RATE} from '@/lib/utils'
```

Inside the component body (after `const t = useTranslations("courses.detail");`):

```ts
const tb = useTranslations('pricing.breakdown')
const buyerCoupon = {
    couponEnabled: course.couponEnabled,
    couponCode: course.couponCode,
    couponDiscountType: course.couponDiscountType,
    couponDiscountValue: course.couponDiscountValue
}
const buyerBreakdown = computeBuyerBreakdown(Number(course.price), buyerCoupon, appliedCouponCode)
const breakdownMessages = {
    title: tb('title'),
    listPrice: tb('listPrice'),
    coupon: tb('coupon', {code: '{code}'}),
    vat: tb('vat', {rate: Math.round(VAT_RATE * 100)}),
    total: tb('total'),
    couponLabel: tb('couponLabel'),
    couponPlaceholder: tb('couponPlaceholder'),
    apply: tb('apply'),
    remove: tb('remove'),
    invalidCoupon: tb('invalidCoupon')
}
```

(The `coupon` message keeps its `{code}` placeholder — the component interpolates the actual code via `.replace`, so pass it through next-intl with a literal `{code}` value.)

At the TOP of `renderPaidPaymentOptions()`'s returned `<div className="space-y-2">` (so the breakdown appears above the pay buttons in all three branches that render payment options):

```tsx
<BuyerPriceBreakdown
    price={Number(course.price)}
    currency={course.currency}
    isFree={course.isFree}
    coupon={buyerCoupon}
    appliedCouponCode={appliedCouponCode}
    onApplyCoupon={onApplyCoupon}
    messages={breakdownMessages}
/>
```

Then make the pay buttons agree with the breakdown total: replace BOTH `<SaudiRiyal value={Number(course.price)} size="sm" className="h-4 w-4" type="display" />` occurrences (noon button line ~149 and stripe button line ~179) with:

```tsx
<SaudiRiyal value={buyerBreakdown.total} size="sm" className="h-4 w-4" type="format" />
```

(`buyerBreakdown.total` equals the old `displayPrice` when no coupon is applied — zero visual change for the no-coupon case. Leave the `TabbyPromo amount` untouched.)

- [ ] **Step 3: Page plumbing** — in `course-detail-page.tsx`, destructure `appliedCouponCode` and `setAppliedCouponCode` from the `useCourseDetail(...)` result and pass to BOTH `<CourseDetailSidebar ... />` and `<CourseDetailMobileBar ... />`:

```tsx
appliedCouponCode = {appliedCouponCode}
onApplyCoupon = {setAppliedCouponCode}
```

- [ ] **Step 4: Mobile bar** — `course-detail-mobile-bar.tsx` has the same shape (props type + `renderPaidPaymentOptions`-style block with `SaudiRiyal ... type="display"` at lines ~314 and ~423). Apply the SAME edits as Step 2: add the two props, compute `buyerCoupon`/`buyerBreakdown`/`breakdownMessages` identically, render `<BuyerPriceBreakdown ...messages={breakdownMessages} />` above its payment buttons, and switch its `type="display"` SaudiRiyal occurrences to `value={buyerBreakdown.total} type="format"`.

- [ ] **Step 5: Verify**

```bash
pnpm typecheck:touched -- src/lib/courses/detail/use-course-detail.ts src/lib/courses/detail/course-detail-page.tsx src/lib/courses/detail/sections/course-detail-sidebar.tsx src/lib/courses/detail/sections/course-detail-mobile-bar.tsx
DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/courses/detail
```

Expected: clean typecheck; existing detail tests still green (new props may need adding to any test fixtures rendering the sidebar — add `appliedCouponCode={null} onApplyCoupon={() => {}}`).

- [ ] **Step 6: Commit**

```bash
git add src/lib/courses/detail/
git commit -m "feat(courses): buyer price breakdown + coupon entry on course detail"
```

---

### Task 7: Wire breakdown into the EVENT detail page

**Files:**

- Modify: `src/lib/events/detail/use-event-detail.ts` (`handleRegister` body ~line 215)
- Modify: `src/lib/events/detail/event-detail-page.tsx`
- Modify: `src/lib/events/detail/sections/event-detail-sidebar.tsx`
- Modify: `src/lib/events/detail/sections/event-detail-mobile-bar.tsx` (if present; check `ls src/lib/events/detail/sections/`)

- [ ] **Step 1: Repeat Task 6 one-for-one for events** — same hook state (`appliedCouponCode` in `use-event-detail.ts`, spread `...(appliedCouponCode ? {couponCode: appliedCouponCode} : {})` into the register fetch body), same sidebar edits (`t = useTranslations("events.detail")` already exists; add `tb = useTranslations("pricing.breakdown")`, `buyerCoupon` from `event.coupon*` fields, `buyerBreakdown` from `Number(event.price)`, render `<BuyerPriceBreakdown price={Number(event.price)} currency={event.currency} isFree={event.isFree} ... />` at the top of its `renderPaidPaymentOptions()`, switch its `type="display"` SaudiRiyal occurrences (~lines 167-172 and the stripe button) to `value={buyerBreakdown.total} type="format"`), same page plumbing.

- [ ] **Step 2: Verify**

```bash
pnpm typecheck:touched -- src/lib/events/detail/use-event-detail.ts src/lib/events/detail/event-detail-page.tsx src/lib/events/detail/sections/event-detail-sidebar.tsx
DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/events/detail
```

Expected: clean.

- [ ] **Step 3: Commit**

```bash
git add src/lib/events/detail/
git commit -m "feat(events): buyer price breakdown + coupon entry on event detail"
```

---

### Task 8: Coupon at checkout — COURSE enroll (schema, command, handler, route)

**Files:**

- Modify: `src/lib/courses/enrollments/commands/course-enroll.schema.ts`
- Modify: `src/lib/courses/enrollments/commands/course-enroll.command.ts`
- Modify: `src/lib/courses/enrollments/handlers/course-enroll.handler.ts`
- Modify: `app/api/v1/courses/[id]/enroll/route.ts`
- Test: `src/lib/courses/enrollments/handlers/__tests__/course-enroll.handler.test.ts` (extend; if absent, the enroll tests live in `app/api/v1/courses/[id]/enroll/__tests__/` — extend there)

- [ ] **Step 1: Write the failing handler tests.** Locate the existing enroll handler/route test file (it mocks `@/lib/prisma` and `createPaymentIntent`). Add, following its existing mock fixtures (a paid course fixture with `price: 400`):

```ts
const couponCourse = {
    // ...spread the existing paid-course fixture...
    couponEnabled: true,
    couponCode: 'SAVE20',
    couponDiscountType: 'percent',
    couponDiscountValue: 0.2
}

it('charges the discounted amount and snapshots the coupon when a valid code is supplied', async () => {
    // arrange: course.findUnique resolves couponCourse
    // act: invoke with {...baseCommand, couponCode: "save20"}
    expect(createPaymentIntentMock).toHaveBeenCalledWith(
        expect.objectContaining({amount: 320}) // 400 − 20%
    )
    expect(enrollmentUpsertMock).toHaveBeenCalledWith(
        expect.objectContaining({
            update: expect.objectContaining({
                couponCode: 'save20',
                couponDiscount: 80,
                couponListPrice: 400
            })
        })
    )
})

it('rejects an invalid code with 400 INVALID_COUPON and creates no payment intent', async () => {
    // act: invoke with {...baseCommand, couponCode: "WRONG"} against couponCourse
    const result = await handleCourseEnroll(command)
    expect(result).toEqual(expect.objectContaining({status: 400, code: 'INVALID_COUPON'}))
    expect(createPaymentIntentMock).not.toHaveBeenCalled()
})

it('routes a 100%-discount coupon through the free-completion path', async () => {
    // arrange: fixed coupon covering the full price (couponDiscountType: "fixed", couponDiscountValue: 400)
    // expect: upsert with status "completed", amountPaid 0, coupon snapshot present; no payment intent
})

it('clears a stale coupon snapshot when re-attempting without a code', async () => {
    // act: invoke with NO couponCode against couponCourse
    expect(enrollmentUpsertMock).toHaveBeenCalledWith(
        expect.objectContaining({
            update: expect.objectContaining({
                couponCode: null,
                couponDiscount: null,
                couponListPrice: null
            })
        })
    )
    expect(createPaymentIntentMock).toHaveBeenCalledWith(expect.objectContaining({amount: 400}))
})
```

Adapt mock variable names to the file's existing conventions (read it first). The crucial assertions are the four behaviors; keep the existing happy-path tests untouched.

- [ ] **Step 2: Run to verify the new tests fail**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run <that test file>`
Expected: new tests FAIL; pre-existing tests still PASS.

- [ ] **Step 3: Schema + command.** In `course-enroll.schema.ts` add after `provider`:

```ts
  couponCode: z.string().trim().min(1).max(64).optional(),
```

In `course-enroll.command.ts` add `couponCode?: string;` to the command type (match the file's style).

- [ ] **Step 4: Handler.** In `course-enroll.handler.ts`:

Imports:

```ts
import {computeChargeAmount, type ChargeQuote} from '@/lib/pricing/buyer-price-breakdown'
```

Destructure `couponCode` from `command` (line 10). After the `existing?.status === "completed"` early-return (line 76) and BEFORE the free-course branch, insert:

```ts
// Coupon-at-checkout: validate the buyer-supplied code against the course's
// coupon config. Reject loudly — never fall back to charging full price for
// a code the buyer believes is applied.
let chargeQuote: ChargeQuote | null = null
if (couponCode && !course.isFree && Number(course.price) > 0) {
    chargeQuote = computeChargeAmount(
        Number(course.price),
        {
            couponEnabled: course.couponEnabled,
            couponCode: course.couponCode,
            couponDiscountType: (course.couponDiscountType as 'percent' | 'fixed' | null) ?? null,
            couponDiscountValue: course.couponDiscountValue == null ? null : Number(course.couponDiscountValue)
        },
        couponCode
    )
    if (!chargeQuote) {
        observe(
            'course.enrollment.invalid_coupon',
            {requestId, userId, courseId: course.id},
            {level: 'warn', dedupeKey: `course.enrollment.invalid_coupon:${course.id}:${userId}`}
        )
        return {error: 'Invalid coupon code', status: 400 as const, code: 'INVALID_COUPON' as const}
    }
}

const couponSnapshot = chargeQuote
    ? {
          couponCode: couponCode!,
          couponDiscount: chargeQuote.discountAmount,
          couponListPrice: chargeQuote.listPrice
      }
    : {couponCode: null, couponDiscount: null, couponListPrice: null}
```

In the FREE COURSE branch keep behavior unchanged (a free course ignores coupons — the `!course.isFree` guard above means `chargeQuote` is null there).

After the free branch, add the 100%-discount path (before the `// PAID COURSE` success URL block):

```ts
// 100%-discount coupon: nothing to charge — complete immediately through the
// same shape as the free path, keeping the coupon snapshot for audit.
if (chargeQuote && chargeQuote.chargeAmount === 0) {
    const enrollment = await prisma.courseEnrollment.upsert({
        where: {userId_courseId: {courseId: course.id, userId}},
        update: {status: 'completed', amountPaid: 0, ...couponSnapshot},
        create: {
            courseId: course.id,
            userId,
            provider: 'free',
            status: 'completed',
            amountPaid: 0,
            ...couponSnapshot
        }
    })

    await activityHelpers.trackCourseEnrolled(userId, course.id, course.title)

    const fullEnrollment = await prisma.courseEnrollment.findFirst({
        where: {id: enrollment.id},
        include: enrollmentInclude
    })

    observe(
        'course.enrollment.completed.coupon_full_discount',
        {requestId, userId, courseId: course.id, enrollmentId: enrollment.id},
        {
            level: 'info',
            dedupeKey: `course.enrollment.completed.coupon_full_discount:${course.id}:${userId}`
        }
    )

    return {free: true, enrollment: fullEnrollment ? mapEnrollmentToDTO(fullEnrollment) : null}
}
```

In the PAID COURSE `createPaymentIntent` call change `amount`:

```ts
    amount: chargeQuote ? chargeQuote.chargeAmount : Number(course.price),
```

and `currency: "SAR"` → `currency: course.currency,`.

In the pending upsert (line ~164) spread the snapshot into BOTH `update` and `create` (refresh-on-every-attempt, same rationale as `billingCountryCode`):

```ts
    update: {
      status: "pending",
      provider: payment.provider,
      providerRef: payment.reference,
      billingCountryCode: billingCountryCode ?? null,
      ...couponSnapshot,
    },
    create: {
      userId,
      courseId: course.id,
      status: "pending",
      provider: payment.provider,
      providerRef: payment.reference,
      billingCountryCode: billingCountryCode ?? null,
      ...couponSnapshot,
    },
```

In the `course.enrollment.redirected` observe payload change `amount: Number(course.price)` → `amount: chargeQuote ? chargeQuote.chargeAmount : Number(course.price)` and `currency: "SAR"` → `currency: course.currency`.

- [ ] **Step 5: Route.** In `app/api/v1/courses/[id]/enroll/route.ts`, find where `handleCourseEnroll`'s result is mapped to the error response (`result.error` / `result.status`) and include the optional code:

```ts
return NextResponse.json({error: result.error, ...('code' in result && result.code ? {code: result.code} : {})}, {status: result.status})
```

(Adapt to the file's exact result-handling shape — read it; the schema parse already picks up `couponCode` because the route does `CourseEnrollSchema.parse(await request.json())` and the command construction must pass `couponCode: input.couponCode` through.)

Client-side: in `use-course-detail.ts` `handleEnroll`, surface the rejection — extend the existing `!res.ok` alert branch:

```ts
alert(
    data.code === 'TABBY_KSA_ONLY'
        ? t('tabbyKsaOnly')
        : data.code === 'INVALID_COUPON'
          ? tb('invalidCoupon')
          : data.error || t('failedToStartEnrollment')
)
```

(`tb` = `useTranslations("pricing.breakdown")` added to the hook; include it in the callback deps.)

- [ ] **Step 6: Run the new tests + the FULL existing enroll suites (happy-path regression guard)**

```bash
DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/courses/enrollments app/api/v1/courses
```

Expected: ALL pass — pre-existing no-coupon tests must be untouched and green (coupon logic only activates when `couponCode` is present in the request).

- [ ] **Step 7: Commit**

```bash
git add src/lib/courses/enrollments/ app/api/v1/courses/[id]/enroll/route.ts src/lib/courses/detail/use-course-detail.ts
git commit -m "feat(courses): apply coupon at checkout with snapshot on enrollment (INVALID_COUPON 400)"
```

---

### Task 9: Coupon at checkout — EVENT register (symmetric sibling)

**Files:**

- Modify: `src/lib/events/commands/event-register.schema.ts`
- Modify: `src/lib/events/commands/event-register.command.ts`
- Modify: `src/lib/events/handlers/event-register.handler.ts`
- Modify: `app/api/v1/events/[id]/register/route.ts`
- Modify: `src/lib/events/detail/use-event-detail.ts` (INVALID_COUPON alert, mirroring Task 8 Step 5)
- Test: the existing event-register handler/route test file (find via `rg -ln "handleEventRegister" --glob "*test*"`)

- [ ] **Step 1: Repeat Task 8 one-for-one for events.** Same failing tests first (charge 320 on SAVE20, INVALID_COUPON 400 + no intent, 100%-discount → completed `amountPaid: 0` with snapshot, stale-snapshot cleared on no-code retry). Then: `couponCode: z.string().trim().min(1).max(64).optional()` in `EventRegisterSchema`; `couponCode?: string` on `EventRegisterCommand`; identical `chargeQuote`/`couponSnapshot` logic in `handleEventRegister` after the `existing?.status === "completed"` check (line ~101), using `event.*` coupon fields and observe keys `event.registration.invalid_coupon` / `event.registration.completed.coupon_full_discount`; `amount: chargeQuote ? chargeQuote.chargeAmount : Number(event.price)` and `currency: event.currency` in `createPaymentIntent`; snapshot spread into the `eventRegistration.upsert` update+create (line ~178); route passes `couponCode` through and surfaces `code` in the error JSON. Note: events return errors via `DomainError` in places — keep the `{error, status, code}` return shape consistent with how the existing "already registered" 400 flows back.

- [ ] **Step 2: Run the new tests + the FULL existing register/verify suites**

```bash
DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/events app/api/v1/events
```

Expected: all green.

- [ ] **Step 3: Commit**

```bash
git add src/lib/events/ app/api/v1/events/[id]/register/route.ts
git commit -m "feat(events): apply coupon at checkout with snapshot on registration (INVALID_COUPON 400)"
```

---

### Task 10: Settlement reads the coupon snapshot (courses only — events are excluded from settlement v1 by D-9)

**Files:**

- Modify: `src/lib/settlement/record-settlement.ts` (`resolveCourseFacts` lines 32-53, `priceOrder` call lines 103-109)
- Test: `src/lib/settlement/__tests__/record-settlement.test.ts` (extend)

- [ ] **Step 1: Write the failing test.** In the existing settlement test file, following its mock conventions (it mocks `prisma.courseEnrollment.findUnique` etc.), add:

```ts
it('passes the checkout coupon snapshot to priceOrder as scenario-A inputs', async () => {
    // arrange: enrollment mock gains couponCode "SAVE20", couponDiscount 80, couponListPrice 400,
    //          amountPaid 320 (the discounted gross)
    // act: recordOrderSettlement({sourceType: "course", sourceId: ...})
    // assert on the created orderSettlement row:
    expect(orderSettlementCreateMock).toHaveBeenCalledWith(
        expect.objectContaining({
            data: expect.objectContaining({
                grossPaid: 320,
                discountInstructorCost: 80 // instructor funds the discount (scenario A)
            })
        })
    )
})

it('settles exactly as before when no coupon snapshot exists', async () => {
    // arrange: enrollment with null coupon fields, amountPaid 400
    // assert discountInstructorCost: 0 and grossPaid: 400 — byte-identical to today
})
```

- [ ] **Step 2: Run to verify it fails**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/settlement/__tests__/record-settlement.test.ts`
Expected: new tests FAIL (discountInstructorCost currently always 0), existing tests PASS.

- [ ] **Step 3: Implement.** In `record-settlement.ts`:

Extend `OrderFacts`:

```ts
type OrderFacts = {
    buyerUserId: string
    itemId: string
    itemTitle: string
    grossPaid: number
    payableAt: Date
    contributors: ContributorRow[]
    primaryRole: string
    couponDiscount: number | null
    couponListPrice: number | null
}
```

In `resolveCourseFacts`'s return object add:

```ts
    couponDiscount: e.couponDiscount == null ? null : Number(e.couponDiscount),
    couponListPrice: e.couponListPrice == null ? null : Number(e.couponListPrice),
```

Replace the `priceOrder` call (lines 103-109) with:

```ts
const couponApplied = facts.couponDiscount != null && facts.couponDiscount > 0
const breakdown = priceOrder({
    grossPaid: facts.grossPaid,
    vatRate: VAT_RATE,
    instructorSplitFraction: DEFAULT_INSTRUCTOR_SPLIT_FRACTION,
    gatewayFeeFraction: DEFAULT_GATEWAY_FEE_FRACTION,
    affiliate: toInstructorFundedAffiliate(commission ? Number(commission.commissionAmount) : 0),
    // Scenario A: discount happened at checkout — gross paid is already the
    // discounted amount; the snapshot (written at initiation, TOCTOU-safe)
    // carries the discount and original list price for the ledger.
    coupon: couponApplied
        ? {
              discountType: 'fixed' as const,
              discountValue: facts.couponDiscount!,
              fundedBy: 'INSTRUCTOR' as const
          }
        : null,
    checkoutDiscountAmount: couponApplied ? facts.couponDiscount! : undefined,
    listPriceIncVatInput: couponApplied ? (facts.couponListPrice ?? undefined) : undefined
})
```

(The `orderSettlement.create` already persists `discountInstructorCost: breakdown.discountCostInstructor` — no change needed there.)

- [ ] **Step 4: Run the FULL settlement suite**

Run: `DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/settlement`
Expected: all green, including the pre-existing no-coupon cases.

- [ ] **Step 5: Commit**

```bash
git add src/lib/settlement/
git commit -m "feat(settlement): course settlements consume the checkout coupon snapshot (scenario A)"
```

---

### Task 11: Multi-currency plan document

**Files:**

- Create: `docs/superpowers/specs/2026-06-10-multi-currency-plan.md` (repo root `docs/`, not apps/)

- [ ] **Step 1: Write the doc** with exactly these sections (each 1-3 paragraphs, grounded in the code as it exists after Tasks 2-3):

1. **Current state** — SAR-only; `currency` columns now exist on Course/Event (default `"SAR"`), threaded into DTOs and `createPaymentIntent`; `MoneyAmount` renders non-SAR via `Intl.NumberFormat`; ZATCA invoices, settlement ledger, and Tabby/Noon are SAR-pinned.
2. **Two pricing models compared** — (a) price-per-currency (creator sets explicit prices per enabled currency; no FX risk, more creator work) vs (b) FX-at-display (one base price + daily rates; less creator work, rate-staleness and rounding risk, charge-vs-display drift). Recommend (a) for paid content, noting the existing `CoursePriceVersion`/`EventPriceVersion` audit tables would need a per-currency dimension.
3. **PSP support matrix** — Stripe: full multi-currency (first non-SAR rollout candidate); Noon: SAR/AED-centric, verify per-merchant config; Tabby: KSA/SAR only (already geo-gated via `billingCountryCode` snapshot) — non-SAR checkout must hide Tabby.
4. **ZATCA constraint** — KSA tax invoices must be SAR; a non-SAR charge needs a stored FX rate + SAR-converted amounts on the Invoice row at completion time (snapshot, never recomputed).
5. **Settlement/ledger implications** — `OrderSettlement.currency` exists but everything assumes SAR; either settle in charge currency with per-currency payout pools, or convert to SAR at a snapshotted rate. Recommend convert-at-completion with rate stored on the settlement row.
6. **Phased rollout** — Phase 0 (done in this PR): currency column + display seam. Phase 1: Stripe-only USD for courses, ZATCA FX snapshot, hide Tabby/Noon for non-SAR. Phase 2: per-currency creator pricing UI. Phase 3: events + payouts in non-SAR.
7. **Open questions for the operator** — who sets FX rates (manual admin vs provider API); rounding policy; whether subscriptions ever go multi-currency.

- [ ] **Step 2: Commit**

```bash
git add docs/superpowers/specs/2026-06-10-multi-currency-plan.md
git commit -m "docs(pricing): multi-currency rollout plan (phase 0 shipped as currency groundwork)"
```

---

### Task 12: File the VAT display/charge discrepancy issue + cross-reference in code

- [ ] **Step 1: Invoke the `experts-beacon` skill** (Skill tool) with this verified finding:

> **Title:** `[bug] Detail pages display price ×1.15 while checkout charges the stored price verbatim`
> **Evidence:** `src/lib/courses/detail/sections/course-detail-sidebar.tsx` renders `SaudiRiyal type="display"` → `displayPrice()` → `price × VAT_FACTOR`; `src/lib/courses/enrollments/handlers/course-enroll.handler.ts:134` charges `Number(course.price)`; all gateways pass `input.amount` through (`stripe.gateway.ts` `toMinorUnits(n(input.amount))`). Creator form (`CreatorPriceBreakdown`: buyerPays = entered price) and settlement (`priceOrder` extracts VAT from grossPaid) both treat stored price as VAT-INCLUSIVE — the ×1.15 display is the outlier. A buyer sees 460.00 SAR and is charged 400.00 SAR. Same for events.
> **Operator decision (2026-06-10):** buyer-facing breakdown intentionally matches the DISPLAY basis for now; fixing the divergence is this issue's scope. Labels: `bug`. Note in body: NOT R3-auto-fixable (pricing-semantics product decision required: either displays drop ×1.15, or checkout charges ×1.15).

Follow the beacon skill's fingerprint/marker/dedup steps exactly.

- [ ] **Step 2: Update the code comment** in `src/lib/pricing/buyer-price-breakdown.ts` (Task 1 left "see GitHub issue filed in Task 12") with the real issue number, e.g. `see #NNN`.

- [ ] **Step 3: Commit**

```bash
git add src/lib/pricing/buyer-price-breakdown.ts
git commit -m "docs(pricing): link display/charge divergence comment to filed issue"
```

---

### Task 13: Full gate + review panel

- [ ] **Step 1: Full check** (separate tool call from any commit):

```bash
pnpm experts:check
```

If FORMAT/LINT/TYPECHECK fail: `pnpm experts:check:fix`, then re-run `pnpm experts:check`. Fix remaining failures by hand.

- [ ] **Step 2: Full test run for the touched domains + drift gate:**

```bash
DATABASE_URL=postgresql://localhost/experts_test pnpm vitest run src/lib/pricing src/lib/courses src/lib/events src/lib/settlement app/api/v1/courses app/api/v1/events
pnpm db:check:drift
```

Expected: all green.

- [ ] **Step 3: Review panel before any push** (house rule): spawn `code-reviewer` + `qa-tester` agents in parallel on `git diff origin/main`, triage findings — fix real bugs before ship-out, defer cosmetic ones with a PR note. (`security-auditor` not required — no security label — but the coupon path touches payments; if either reviewer flags an authz/value-tampering concern, add a security-auditor pass.)

- [ ] **Step 4: Stop.** Do NOT push or open a PR — report status to the operator, who ships via the experts-ship lifecycle (issue, PR with `Closes #N`, gatekeeper hand-off).

---

## Self-review notes (already applied)

- **Spec coverage:** §1 module→Task 1; §2 component→Tasks 4-7; §3 coupon checkout→Tasks 8-9 (snapshot, INVALID_COUPON, 100%-discount, happy-path guard); §4 currency→Tasks 2-3 + the `currency:` swaps in Tasks 8-9; §5 plan doc→Task 11; issue filing→Task 12; §7 tests→inside each task; gate→Task 13.
- **Verify/webhook paths need NO change:** completion reads `amountPaid` from the GATEWAY (`verification.amountPaid`, Noon `order.amount`, Tabby `payment.amount`), so a discounted charge flows through automatically; settlement reads `enrollment.amountPaid` + the new snapshot columns. Confirmed against `app/api/v1/courses/[id]/enroll/verify/route.ts` and `record-settlement.ts`.
- **Known accepted quirks:** display-vs-charge divergence (operator decision, Task 12); `TabbyPromo` still shows the undiscounted charge amount (cosmetic, BNPL preview only); events settlement untouched (D-9).

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
