---
title: "Incomplete payment — session resume vs reinitiate (Stripe, Tabby, Noon)"
date: "2026-04-11"
tags: ["project/experts", "topic/guides", "topic/payments", "topic/payment-gateways"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs/guides/guides-index|Guides index]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/payment-gateways-index|Payment gateways index]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/question|QUESTION — payload shapes]]

in Tabby/Noon docs, how incomplete payment should be handled ?

stripe (test) I did "Payment incomplete. Complete your payment to access the course.
"

does the same apply to Tabby/Noon ? Or do I need to reinitiate a new payment each time ?

Short answer: the UX message can be the same, but the mechanics are different.
With Stripe you usually resume the same intent/session. With Tabby and Noon, you generally re-initiate a new checkout after an incomplete attempt.

Here’s the clean, provider-accurate breakdown.

What “incomplete payment” means per provider
Stripe

Model: Intent/session–based, resumable
Typical causes: user closed tab, 3DS not finished, payment requires action

Stripe keeps a PaymentIntent / Checkout Session alive.

You can resume it by redirecting the user to the same session URL.

Statuses like requires_action, incomplete, open are expected.

Your message works perfectly:

“Payment incomplete. Complete your payment to access the course.”

Action:
✅ Reuse the same session → resume.

Tabby

Model: Authorization → Capture, non-resumable checkout sessions
Typical causes: user cancels, session expires, eligibility changes

A Tabby checkout session is single-use.

If it’s not completed, it will become expired, rejected, or stay authorized without capture.

There is no supported “resume checkout” flow.

Even if the order reference is the same, the session URL cannot be reused.

Action:
❌ Don’t reuse
✅ Create a new Tabby checkout session

UX text (recommended):

“Payment not completed. Please try again to access the course.”

Important:
If a payment reached authorized but not captured, you should not try to reuse it. Either capture (if appropriate) or let it expire and reinitiate.

Noon Payments

Model: Initiate → (Redirect) → Verify, single-use checkout
Typical causes: user closes browser, network issues, OTP not completed

Noon’s INITIATE creates a one-time checkout.

If the user doesn’t finish, the order is left in a non-final state (e.g., initiated, failed, or simply no success).

There is no resume URL.

Reusing the same order/session is not supported.

Action:
❌ Don’t reuse
✅ Initiate a new payment

UX text (recommended):

“Payment incomplete. Please retry to complete your purchase.”

The golden rule (important)

Only Stripe supports resuming an incomplete checkout.
Tabby and Noon require a fresh initiation every time.

What you should implement (provider-agnostic UX)

You can keep your same user-facing message across all gateways, but your backend behavior must differ.

UX (same everywhere)

“Payment incomplete. Complete your payment to access the course.”

Backend behavior (differs)
Provider Resume old session Reinitiate new payment
Stripe ✅ Yes ❌ No
Tabby ❌ No ✅ Yes
Noon ❌ No ✅ Yes
Recommended internal state machine (works for all 3)

Use your own payment state, not the gateway’s wording:

INITIATED
→ PENDING_USER_ACTION
→ PAID
→ FAILED
→ EXPIRED

Mapping examples

Stripe

incomplete → PENDING_USER_ACTION

resume allowed

Tabby

created → PENDING_USER_ACTION

expired/rejected → FAILED

must reinitiate

Noon

initiated → PENDING_USER_ACTION

no success webhook → EXPIRED

must reinitiate

Practical implementation pattern (clean)
On “Access course” click

Check internal payment state

If:

Stripe + resumable → redirect to same session

Tabby/Noon or expired → create new payment

Redirect user

Pseudocode
if (payment.provider === "stripe" && payment.canResume) {
redirect(payment.sessionUrl);
} else {
const newPayment = await createNewPayment(provider);
redirect(newPayment.redirectUrl);
}

One last critical warning (Tabby & Noon)

❗ Never allow two active authorizations for the same order

If Tabby is authorized but not captured:

Either capture it

Or let it expire

Do not start another charge until resolved

This avoids double holds / reconciliation pain.

Final verdict

✅ Your message text is fine for all providers

❌ Your Stripe behavior must NOT be copied to Tabby/Noon

🔁 Reinitiate for Tabby & Noon

▶️ Resume only for Stripe
