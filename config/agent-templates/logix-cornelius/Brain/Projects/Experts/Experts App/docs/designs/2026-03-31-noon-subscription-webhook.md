---
title: "Noon Subscription Webhook Handler — outcome"
date: "2026-03-31"
tags: ["project/experts", "topic/noon-subscription-webhook", "outcome"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

# Noon Subscription Webhook Handler

**Outcome:** Noon recurring-billing events (renewal, payment failure, cancellation) now update Subscription DB records instead of falling through the webhook handler as unmatched references.

## What shipped
- Subscription lifecycle handling added to the Noon webhook handler: a `prisma.subscription.findFirst` lookup (`provider: "noon"`) runs before the existing enrollment failed-cancel path so subscription billing events are intercepted rather than silently consumed.
- Three outcome branches for a matched subscription:
  - Success → `handleSubscriptionRenew` with 30-day period advancement; emits `noon.webhook.subscription.renewed`; result `subscription_renewed`.
  - Failed + cancellation signal → `handleSubscriptionCancel`; result `subscription_canceled`.
  - Failed + no cancellation signal → sets `subscription.status = "paused"`; result `subscription_payment_failed`.
- `NoonWebhookResult.target` widened from `"course" | "event"` to include `"subscription"`.

## Key decisions
- Cancellation detected via raw Noon fields (`CANCEL` substring in `event.raw.type` / `orderStatus` / `order.status`), not `event.status`, because `cancelled`/`canceled` are not members of the `WebhookEventStatus` union.
- 30-day period advancement used as a safe default since Noon does not return period dates natively (plan-interval derivation deferred to phase 13).
- `provider: "stripe"` dummy literal passed to `RenewSubscriptionCommand` because it was typed `"stripe"` only (provider widening deferred to phase 13).

## Key files
- `apps/experts-app/src/lib/payments/gateways/noon/noon.webhook.handler.ts`

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
