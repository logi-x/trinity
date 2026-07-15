---
title: "Payments"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "topic/payments"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Payments.md"
---

# Payments — Integration Patterns

Payment processing across the Experts LMS: subscriptions, course enrollments, event registrations.

## Providers

| Gateway    | Region              | Use case                       |
| ---------- | ------------------- | ------------------------------ |
| **Stripe** | Global              | Primary — cards, subscriptions |
| **Noon**   | Saudi Arabia / MENA | Regional — local card schemes  |
| **Tabby**  | Saudi Arabia / UAE  | Buy-now-pay-later              |

## Code Paths (relative to `apps/experts-app/`)

| Path                   | Role                                                   |
| ---------------------- | ------------------------------------------------------ |
| `src/lib/payments/`    | Gateway clients and shared utilities                   |
| `src/modules/billing/` | Domain logic — invoices, subscriptions, payouts, ZATCA |
| `app/api/v1/commerce/` | Payment API routes (initiate, verify, status)          |
| `app/api/webhooks/`    | Stripe, Noon, Tabby webhook receivers                  |

## Billing Flow

```
User initiates payment (course / event / subscription)
  └─ API route: app/api/v1/commerce/
       └─ billing handler: creates pending invoice + lines
            └─ gateway: Stripe / Noon / Tabby — payment session
                 └─ Webhook received (async): app/api/webhooks/
                      └─ invoice confirmed → enqueueInvoiceZatca()
                           └─ ZATCA pipeline (see [[Wiki/Concepts/ZATCA]])
```

## Subscription Plans

Subscriptions are the prerequisite for publishing content — no instructor can publish a course/event without an active plan. Agreed in the Nov 2025 client review.

Plans gate:

- Content publishing (instructor)
- Enrollment limits or features (learner)
- Payout eligibility

## Refund Model

Refunds are intentionally not frictionless — controlled exceptions, not a happy path.

### Courses (self-paced)

| Condition                                | Refundable |
| ---------------------------------------- | ---------- |
| Within X days (e.g. 7) AND progress ≤ Y% | Yes        |
| Certificate issued                       | No         |
| Course completed                         | No         |

### Events

| Condition                                        | Refundable |
| ------------------------------------------------ | ---------- |
| Event not started AND within cancellation window | Yes        |
| Event started or attended                        | No         |
| Recording delivered                              | No         |
| No-show                                          | No         |

**Key decisions (Nov 2025):**

- Refund policy is **per-course/event**, set by the instructor at creation
- Instructor dashboard has **no self-serve refund button** — all refunds go through admin (prevents fake-course fraud)
- Instructor payouts on the **15th of each month**

## Webhooks

Each gateway has its own webhook receiver. Webhook handlers:

- Verify signature before processing
- Are idempotent — safe to replay
- Transition invoice status and trigger downstream (ZATCA enqueue, notification)

## Processing Fees

See [[Wiki/Concepts/Processing Fees]] for the commission and fee model.

## Decisions

- 2026-05-24: Tabby checkout eligibility is enforced from the trusted Cloudflare `CF-IPCountry` request header only. Tabby is allowed only for `SA`; missing or non-`SA` country fails closed with Noon/card options left available. Do not use saved address, profile nationality, or client-provided country as the enforcement source.
- 2026-06-06: **Tabby completion (verify) routes require auth + ownership.** `courses/[id]/enroll/verify` and `events/[id]/register/verify` previously located the pending enrollment/registration solely by the Tabby `providerRef`/`payment_id` with no `auth()` — anyone holding another user's `payment_id` could drive their enrollment to completion. Now they call `auth()` and assert `session.user.id === userId` before any side-effect (401/403). Stripe/Noon branches and the server-to-server webhook are intentionally exempt. (EXP-309 / PR #868.)
- 2026-06-06: Tabby (KSA) settles only in **SAR**; completion records pin `"SAR"`. The old `resolvedCurrency === "SAR" ? "SAR" : "SAR"` (and the webhook's private `ensureSar`) are no-ops — a non-SAR value from the Tabby API is now surfaced via an `observe()` warning (`*.tabby_currency_mismatch`) instead of being silently masked. (EXP-308 / PR #868.)
- 2026-06-06: Subscription checkout accepts an optional `locale` (`ar`/`en`/`es`) and derives `es` from `Accept-Language`, so `tabbyKsaOnlyMessage`'s Spanish branch is reachable (was always English). Enroll/register stay `ar`/`en`. (EXP-108 / PR #869.)
- 2026-06-06: **Tabby geo-block is now enforced BEFORE capture (void-only, no auto-refund).** EXP-305 / PR #881. EXP-129 only re-checked geo at completion — which ran in the webhook _after_ `captureTabbyPayment`, leaving non-SA buyers paid-but-not-enrolled. The geo gate moved into the authorized-capture branch (`resolveTabbyGeoBlock` reads the checkout country snapshot): if blocked and still only authorized → `closeTabbyPayment` cancels the authorization so **funds are never captured**; if a capture already exists (race) → **no auto-refund**, an `error`-level `observe` (`remediation: manual_refund_required`) fires so an operator drives the existing admin **RefundRequest** flow. EXP-129's completion-time check is kept as defense-in-depth. **Product decision: void-only, no automated refund.** Note: there is **no ledger/invoice to reverse** — the verify routes never capture (webhook-only) and an invoice/ZATCA is created only on completion, which never runs for a blocked purchase. New client fn: `closeTabbyPayment` (Tabby "close" = cancel authorization).

## Related

- [[Wiki/Concepts/ZATCA]]
- [[Wiki/Concepts/Noon Payments]]
- [[Wiki/Concepts/Processing Fees]]
- [[Wiki/Concepts/Affiliate System]]
- [[Projects/Experts/Experts App/docs/guides/refund]]
- [[Projects/Experts/Experts App/docs/reference/flows]]
