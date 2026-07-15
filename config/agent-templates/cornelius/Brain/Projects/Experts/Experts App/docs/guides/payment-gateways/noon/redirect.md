---
title: "Noon — return URLs vs payment status page (vs Tabby)"
date: "2026-04-11"
tags: ["project/experts", "topic/guides", "topic/payments", "topic/noon", "tech/nextjs"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs/guides/guides-index|Guides index]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/payment-gateways-index|Payment gateways index]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/noon/guide|Noon integration guide]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/noon/experts-integration|Experts Noon flow]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/tabby/guide|Tabby guide]]

since Tabby has a better return url, we need to manually redirect noon to payment status page first to check then redirect to corresponding success/cancelled/failed

or is there a better approach according to noon docs ? and how should payment status check ?

Great question — and you’re thinking about exactly the right pain point with Noon vs Tabby.

Short answer up front:

Yes, your idea (always landing on a “payment status / checking” page first) is not only valid for Noon — it’s actually the recommended and safest approach.
Noon does not guarantee reliable success/cancel semantics via return URLs the way Tabby does.

Let’s break it down cleanly and map it to what Noon expects vs what works in production.

How Noon return URLs actually work (reality vs expectation)

According to Noon Payments docs and real-world behavior:

Noon return URLs are:

✅ UX-only

❌ Not authoritative

❌ Not strongly typed (success ≠ paid)

❌ Not guaranteed to be hit

Noon’s redirect happens when:

The user finishes (or exits) the hosted page

BUT before settlement is guaranteed

AND sometimes before final state is available

So unlike Tabby:

Noon does not reliably differentiate success / cancelled / failed via URLs

You must verify server-side every time

Comparison: Tabby vs Noon (important distinction)
Tabby

Separate success, cancel, failure URLs

Stronger semantics

payment_id is explicit

Still: webhook is source of truth, but redirect is useful

Noon

Often a single return URL

Minimal or inconsistent query params

Redirect ≠ payment completed

Docs explicitly emphasize Get Order verification

👉 This is why Noon integrations that rely on return URL alone eventually break.

The BEST approach for Noon (recommended)

Your instinct is correct — and here’s the clean pattern:

✅ Always redirect Noon users to a neutral status page first

Never redirect directly to:

/payment/success

/payment/failed

/payment/cancelled

Instead:

Noon → /payment/status?provider=noon&orderRef=XYZ

This page does one thing only:

Ask your backend: “What is the payment state?”

Correct Noon payment flow (production-safe)

1. User pays on Noon hosted page
2. Noon redirects to YOUR return URL (neutral)
3. Status page loads
4. Backend calls Noon Get Order API
5. Backend checks internal DB (webhook may already have fired)
6. Frontend redirects accordingly

How payment status should be checked (very important)
❌ What NOT to do

Don’t trust URL params

Don’t trust frontend timing

Don’t assume redirect = success

✅ What TO do (priority order)
1️⃣ Your database (authoritative)

If you have webhooks (you should):

Check internal payment record

This is the source of truth

2️⃣ Noon Get Order API (fallback / confirmation)

If DB is not final yet:

Call Noon’s Get Order endpoint

Interpret the result

Noon status interpretation (practical mapping)

From Noon API responses, you’ll typically see:

Order status

Transactions list (SALE / AUTH / CAPTURE)

Transaction status

Treat payment as PAID only if:

There is a transaction with:

type: SALE or CAPTURE

status: SUCCESS

Anything else is not paid.

Example: Payment status decision logic
function resolveNoonPaymentState(order) {
const tx = order.transactions?.[0];

if (!tx) return "pending";

if (
(tx.type === "SALE" || tx.type === "CAPTURE") &&
tx.status === "SUCCESS"
) {
return "success";
}

if (tx.status === "FAILED") {
return "failed";
}

return "pending";
}

UX flow on /payment/status
Status page logic

- Show “Checking payment status…”
- Call /api/payments/status?orderRef=XYZ
- Backend:
  - Check DB
  - If not final → call Noon Get Order
  - Update DB if needed
- Return normalized status
- Frontend redirects:
  - success → /payment/success
  - failed → /payment/failed
  - pending → show spinner + poll OR show message

Why this is BETTER than trying to mimic Tabby

Trying to force Noon into:

success / cancel / failed

…will eventually cause:

“User paid but got failure page”

“User cancelled but payment went through”

Support tickets 😅

Your status-first approach avoids all of that.

What Noon docs implicitly expect you to do

Noon docs repeatedly emphasize:

Server-side verification

Get Order API

Webhooks for finality

They do not promise:

Reliable redirect semantics

Resume flows

Deterministic URL outcomes

So your approach is actually more correct than trying to mirror Tabby.

Unified approach (works for Stripe, Tabby, Noon)

Here’s the nice part 👇
You can standardize this for all providers:

/payment/status?paymentId=...

Provider Redirect usefulness Final authority
Stripe High Webhook / Intent
Tabby Medium Webhook
Noon Low Webhook + Get Order

But the UI flow stays the same.

Final recommendation (clear)
✅ For Noon

Single return URL

Always land on status page

Always verify backend-side

Redirect after verification

❌ Don’t rely on:

URL params

Redirect timing

Frontend-only logic
