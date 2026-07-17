---
title: "Processing Fees"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "topic/processing-fees", "processing-fee"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Processing Fees.md"
---

# Processing Fees

Processing fees are the gateway and platform charges attached to purchases in Experts, especially where card fees, revenue share, affiliate commissions, and instructor payouts all meet.

## Context in Experts

This topic is part of the [[Wiki/Concepts/Payments]] model. It matters because pricing on the storefront is not the same thing as net revenue after gateway costs, platform cuts, refunds, and payout timing.

## What it affects

- Final customer charge breakdown
- Instructor net earnings
- Platform margin
- Affiliate commission math
- Refund handling and reversals

## Design considerations

- Fee treatment should be explicit and auditable
- Fee logic must stay consistent across Stripe, Noon, and other providers
- Revenue share rules should not hide true gateway cost

## Implementation notes

- 2026-04-14: Creator event pricing was aligned with creator course pricing in `apps/experts-app`. Event create/edit pricing now follows the same guardrails: paid pricing requires a positive amount, affiliate promotion and coupon controls only unlock once the price exceeds `MINIMUM_ALLOWED_AFFILIATE_COMMISSION_AMOUNT`, and dropping below that threshold clears affiliate/coupon state to avoid hidden invalid pricing combinations.

## In the vault

The payments page treats processing fees as a dedicated subtopic rather than a small implementation detail, which suggests recurring business and product decisions around fee visibility and settlement.

## Related

- [[Wiki/Concepts/Payments]]
- [[Wiki/Concepts/Noon Payments]]
- [[Wiki/Concepts/Affiliate System]]
- [[Decision-Log]]
