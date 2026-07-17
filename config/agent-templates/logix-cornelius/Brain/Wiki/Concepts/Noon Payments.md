---
title: "Noon Payments"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "topic/noon-payments"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Noon Payments.md"
---

# Noon Payments

Noon is the regional payment gateway used in Experts for Saudi Arabia and wider MENA payment coverage where local card behavior matters more than a global-only provider setup.

## Context in Experts

[[Wiki/Concepts/Payments]] identifies Noon as the regional gateway alongside Stripe and Tabby. In practice, Noon belongs to the commerce and webhook layer of Experts App.

## Where it fits

- Payment session creation for regional checkouts
- Webhook handling after provider-side status changes
- Invoice confirmation before downstream billing actions
- Localized gateway coverage for Saudi users

## Why it matters

Experts is a Saudi-focused platform, so Noon is not just an optional add-on. It is part of making the billing stack region-appropriate in currency, payment methods, and operational expectations.

## Adjacent concerns

- [[Wiki/Concepts/Processing Fees]] for gateway cost treatment
- [[Wiki/Concepts/ZATCA]] once invoices become compliance artifacts
- Refund and payout rules from the broader payments workflow

## Related

- [[Wiki/Concepts/Payments]]
- [[Wiki/Concepts/Processing Fees]]
- [[Wiki/Concepts/ZATCA]]
