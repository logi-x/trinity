---
title: "Monetization Pipeline"
date: "2026-06-08"
updated: "2026-06-08"
tags: ["entity", "topic", "topic/monetization", "topic/payments", "topic/affiliates"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Monetization Pipeline.md"
---

# Monetization Pipeline — State Map (as of 2026-06-08)

The end-to-end "how money is made and split" picture for the Experts LMS, assembled from a focused
read-only investigation (6 agents, two independent passes) against `origin/main` on 2026-06-08.
Companion to [[Payments]] (gateway/invoice mechanics), [[Affiliate System]], and [[Affiliates]].

> **Headline:** the creator monetization-and-settlement layer is **largely unimplemented in code** —
> several half-wired pipelines that never connect to real money movement. The affiliate side is the
> only part that actually runs. This is **half-built, not a regression.** Now tracked on the board
> (GitHub issues #935 / #936 / #937 / #916) instead of lurking.

## What actually happens on a paid sale (course / event / subscription — all identical)

```
Buyer pays FULL list price ─► payment intent = Number(price)   [no discount, ever]
  course-enroll.handler.ts:134 · event-register.handler.ts:154 · subscription-checkout.handler.ts:95
   ▼ on success the completion orchestrator writes:
     • enrollment/registration row (status=completed, amountPaid = full gross)
     • activity tracking
     • buyer invoice + ZATCA (single line, full price + 15% VAT)
     • affiliate Commission — ONLY if a referral — = amountPaid × rate  [computed on GROSS]
   ▼ …and nothing else. No ledger. No platform fee. No instructor earning. No instructor payout.
```

## The four structural gaps

| # | Gap | Status in code | GitHub |
| - | --- | -------------- | ------ |
| 1 | **Discounts/coupons non-functional end-to-end** | Two disconnected half-built systems: inline `couponEnabled/couponCode/...` columns on Course/Event (written at create, **never read at checkout**, only drive a 7-day price-edit cooldown + creator preview) **and** a standalone `Coupon` table (`schema.prisma:1250`, **zero write paths**, legacy "never re-wired"). No buyer-facing promo field. Every charge is full list price. | [#935](https://github.com/logi-x/experts/issues/935) `backlog` |
| 2 | **No instructor/creator settlement or payout** | The gross→VAT→2.5%-gateway→80/20-split math (`price-order.ts` + `settlement-config.ts`) is imported by **only 3 React components** (2 creator pricing forms + `/admin/processing-fee-calculator`) — preview only, zero server importers. `revenue.service.ts` validates `revenueShare` sums + payout *timing* but computes **no amounts**. `ContributorEarning` is a dead stub (fields/relations commented out, never written). Only **affiliate** payouts exist. Platform collects 100%; instructor liabilities tracked nowhere. | [#936](https://github.com/logi-x/experts/issues/936) `backlog` |
| 3 | **Discount UI gated behind affiliate-promotion toggle** | Client complaint: can't create a discount unless "promote" is on. Confirmed — but it's **UI-only** (JSX render conditions in the two pricing-section forms; server schemas/routes treat coupon & promotion as independent). Symptom of #1: unlocking it would expose a discount that does nothing. | [#937](https://github.com/logi-x/experts/issues/937) `backlog`, blocked-by #935 |
| 4 | **Affiliate commission never clawed back on refund** | The one *working* money pipeline still leaks: refunds never cancel/reverse commission. Only forward writes exist (create + admin approve/pay). Confirmed **identical across course / event / subscription**. `cancelled` status exists in the DTO but is never assigned. | [#916](https://github.com/logi-x/experts/issues/916) `security` (Tier-1 shippable; Tier-2 paid-commission = decision) |

## Recommended directions (defaults, not decisions — pending operator call)

- **#935:** consolidate on the inline-column model, **delete/repurpose the orphaned `Coupon` table**, build a buyer-facing promo field + checkout redemption (subtract from `amount` at the three intent sites); hide the discount UI until then. Funding model = decide *with* #936.
- **#936:** promote `priceOrder` to a **shared server lib** (one source of truth for preview + settlement), write a **per-sale earnings ledger** at completion (resurrect/replace `ContributorEarning`: gross/VAT/gateway/platform-share/instructor-net/`payableAt`), build instructor payouts **mirroring the affiliate system**. Confirm whether instructors are paid manually today (operator input).
- **#937:** blocked-by #935. If redemption ships → decouple (gate coupon on `price > 0`, FE-only, **both** course + event forms). If deferred → **hide** the toggle. Never unlock a no-op.
- **#916:** Tier-1 (cancel `pending`/`approved` commission on refund + guard maturation) is shippable now across all three handlers; the new instructor ledger (#936) should mirror this clawback fix from day one.

## Key code coordinates

- Charge amount (full price): `course-enroll.handler.ts:134`, `event-register.handler.ts:154`, `subscription-checkout.handler.ts:95`
- Affiliate commission (gross × rate): `src/lib/affiliate/helpers/affiliate.helper.ts:186` (create at `:209`)
- Preview-only split math: `src/lib/orders/price-order.ts`, `src/lib/pricing/settlement-config.ts` (`DEFAULT_INSTRUCTOR_SPLIT_FRACTION = 0.8`, `DEFAULT_GATEWAY_FEE_FRACTION = 0.025`, `MINIMUM_ALLOWED_AFFILIATE_COMMISSION_AMOUNT = 119.99`)
- Revenue (validation/timing only): `src/modules/revenue/revenue.service.ts`
- Dead stub: `ContributorEarning` `prisma/schema.prisma:1927-1941`
- Discount UI gating: `course-pricing-section.tsx:350-353`, `event-pricing-section.tsx:267-269`
- Orphan coupon reader (always 0): `published-price-policy.ts:50` (`detectActivePromotion`)

## Funding model (intended, per `priceOrder` — only relevant once settlement exists)

`FundedByCoupon = "INSTRUCTOR"` and `FundedByAffiliate = "INSTRUCTOR"` are hardcoded: the **instructor
absorbs 100% of every discount and affiliate commission**, with splits taken on the post-discount net.
There is **no** platform-funded or promotion-funded discount concept implemented.

## Related

- [[Payments]] · [[Affiliate System]] · [[Affiliates]] · [[Noon Payments]]
- Filed via the `experts-beacon` skill + `_github-issues-contract.md` (R1/R2 routine parity for ad-hoc findings).
