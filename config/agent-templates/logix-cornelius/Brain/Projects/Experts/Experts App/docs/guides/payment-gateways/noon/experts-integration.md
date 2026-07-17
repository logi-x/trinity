---
title: "Experts platform — Noon payment flow"
date: "2026-04-11"
tags: ["project/experts", "topic/guides", "topic/payments", "topic/noon", "tech/nextjs"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs/guides/guides-index|Guides index]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/payment-gateways-index|Payment gateways index]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/noon/guide|Noon integration guide]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/noon/redirect|Noon return URLs & status page]]

# Experts Noon Integration (How It Works)

This document explains the end‑to‑end payment flow for **Noon** in the Experts platform, including
checkout, return URL verification, and webhooks.

---

## 1) High‑Level Flow (Hosted Checkout)

1. **User clicks “Pay”** (Noon button) on a course page.
2. **Backend creates order (INITIATE)** and returns a Noon hosted checkout URL.
3. **User is redirected** to Noon’s hosted page.
4. **Noon redirects back** to our return URL (success page).
5. **Return page calls verify** (`/api/v1/courses/[id]/enroll/verify`) to check payment status.
6. **Noon sends webhooks** asynchronously (source of truth).
7. **Webhook completes enrollment** once payment is captured.

---

## 2) Key URLs in Experts

### Initiate (create payment)

```
POST /api/v1/courses/[id]/enroll
```

This calls the Noon gateway and returns `redirectUrl`.

### Return/Success Page

```
/en/courses/[id]/success?... (Noon redirects here)
```

The success page calls:

```
GET /api/v1/courses/[id]/enroll/verify
```

and can accept:

- `session_id` (Stripe)
- `orderId` (Noon)
- `merchantReference` (Noon)

### Webhook

```
POST /api/webhooks/noon
```

Receives signed JWT payload from Noon and updates internal state.

---

## 3) Noon INITIATE Payload (What We Send)

We send a compact payload that Noon accepts for hosted checkout:

- `order.reference` uses our helper:
  `EXPERTS + YYYYMMDDHHmmss + 2 letters`
- `order.name` trimmed to 50 characters
- `order.category` + `order.channel` set from env
- `items` array with a single line item

This reference is stored in DB as `providerRef` and used to match webhooks.

---

## 4) Return URL Verification (Why It Can Be “Pending”)

Noon may redirect before final capture.
Typical statuses:

- `3DS_RESULT_VERIFIED` → **Pending** (3DS done, capture not done)
- `CAPTURED` / `SUCCESS` → **Paid**

If pending, the success page shows “Payment Processing” and waits for webhook or
future verify checks.

---

## 5) Webhooks (Source of Truth)

Webhooks are authoritative. We:

1. Verify JWT signature
2. Parse event
3. Map Noon fields:
   - `merchantOrderRef` → `reference`
   - `orderStatus` (e.g. `3DS_RESULT_VERIFIED`)
4. Update enrollment/payment state

If a webhook event is **pending**, we store it but don’t complete enrollment.
When a **PAYMENT_SUCCESS** event arrives, we mark enrollment completed.

---

## 6) Why “Missing Reference” Happens

Noon’s webhook uses `merchantOrderRef`, not `order.reference`.
We now extract:

- `merchantOrderRef` → reference
- fallback to `order.reference`

---

## 7) Debug Checklist (When Something Fails)

- **403 / BadRequest** → payload mismatch (field length, invalid property)
- **3DS_RESULT_VERIFIED** → pending (not captured yet)
- **Missing reference** → webhook uses `merchantOrderRef`
- **403 + “Organization not exists”** → wrong business ID / environment / auth header

---

## 8) Where to Look in Code

**Initiate (Noon gateway):**

- `src/lib/payments/gateways/noon/noon.gateway.ts`

**Noon client + auth header:**

- `src/lib/payments/gateways/noon/noon.client.ts`

**Webhook parser:**

- `src/notifications/channels/webhook/providers/noon.provider.ts`

**Webhook handler:**

- `src/lib/payments/gateways/noon/noon.webhook.handler.ts`

**Verify route:**

- `app/api/v1/courses/[id]/enroll/verify/route.ts`

---

## 9) What’s Different from Stripe

- Stripe verification uses `session_id`
- Noon uses `orderId` / `merchantReference`
- Stripe has immediate success; Noon can return **pending** until capture

---

If you want this extended to **events** or **subscriptions**, the same flow applies with
their respective routes.
