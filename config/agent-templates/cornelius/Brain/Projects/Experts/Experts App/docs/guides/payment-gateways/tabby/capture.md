---
title: "Tabby — authorization to capture flow"
date: "2026-04-11"
tags: ["project/experts", "topic/guides", "topic/payments", "topic/tabby", "tech/nextjs"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs/guides/guides-index|Guides index]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/payment-gateways-index|Payment gateways index]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/tabby/guide|Tabby integration guide]]
- [[Projects/Experts/Experts App/docs/guides/payment-gateways/tabby/full-test-checklist|Tabby QA checklist]]

Let’s walk through the correct Tabby authorization → capture flow, why captures: [] is expected, and how to fix it cleanly.

What this response really means

Your payload:

"status": "authorized",
"captures": [],
"closed_at": null

This means:

✅ Customer passed Tabby checks
✅ OTP + card verification succeeded
✅ Funds are authorized (reserved)
❌ Funds are NOT captured yet
❌ Money is NOT settled to you

In Tabby terms:

Authorization ≠ Payment completion

This is intentional.

Tabby payment lifecycle (important)

Tabby uses a 2-step model (very common in BNPL gateways):

CREATED → AUTHORIZED → CAPTURED → CLOSED

States explained
State Meaning
created Checkout session created
authorized Customer approved, funds reserved
captured Merchant confirmed the charge
closed Payment finalized & settled

You are currently here 👇
➡️ AUTHORIZED

Why captures: [] is correct

Because you haven’t told Tabby to capture yet.

Tabby never auto-captures.

This is by design so you can:

Verify inventory

Confirm enrollment

Avoid charging if something fails

Support delayed fulfillment

The missing step: CAPTURE

You must explicitly call Capture Payment API.

Correct capture flow (server-side only)
Step 1️⃣ Receive authorized signal

This usually happens via:

Webhook (recommended)

OR a server-side status check (less ideal)

Your webhook payload will say:

"status": "authorized"

Step 2️⃣ Call Capture API
Endpoint
POST <https://api.tabby.ai/api/v2/payments/{payment_id}/captures>

{payment_id} = "9ed359e8-2e7b-4532-9284-b4963aa6be08"

Step 3️⃣ Capture request (example)
async function captureTabbyPayment(paymentId: string, amount: number) {
const res = await fetch(
`https://api.tabby.ai/api/v2/payments/${paymentId}/captures`,
{
method: "POST",
headers: {
Authorization: `Bearer ${process.env.TABBY_SECRET_KEY}`,
"Content-Type": "application/json",
},
body: JSON.stringify({
amount: amount.toFixed(2), // "474.00"
}),
}
);

if (!res.ok) {
const err = await res.text();
throw new Error(`Tabby capture failed: ${err}`);
}

return res.json();
}

💡 Notes:

Amount must match or be ≤ authorized amount

You can do partial captures if supported by your account

In most cases, capture full amount immediately

What happens after capture

After a successful capture:

1️⃣ Capture response

You’ll see something like:

"captures": [
{
"id": "cap_123",
"amount": "474.00",
"created_at": "2026-02-07T11:27:10Z"
}
]

2️⃣ Status transitions

status → closed

closed_at → timestamp

3️⃣ Webhook fired

Tabby sends another webhook:

"status": "closed"

This is your final confirmation.

Correct webhook-driven logic (recommended)
DO NOT capture from frontend
DO NOT capture on redirect
DO capture from webhook
Ideal flow
Webhook: status=authorized
↓
Validate order exists & is valid
↓
Capture payment
↓
Grant access / enroll user
↓
Mark order as PAID

Why your current record looks “unfinished”

Your record:

"status": "authorized",
"captures": []

Means one of these is true:

You haven’t implemented capture yet ✅ (most likely)

Capture API call failed or wasn’t called

You’re testing and stopping after redirect

Nothing is broken.

Test-mode specifics (important)

In test mode:

OTP is usually 8888

Authorization always succeeds for test numbers

Capture still must be called

Settlement is simulated

So even in sandbox:

No capture = no closed payment

Where this fits in your architecture (clean way)

Given your earlier webhook channel design, do this:

In Tabby webhook handler
if (event.status === "authorized") {
await captureTabbyPayment(event.paymentId, event.amount);
}

In your domain service
onPaymentCaptured() {
enrollUser();
issueInvoice();
}

Keep capture infrastructure-level, not UI-level.

One more important rule (idempotency)

Tabby may:

Retry webhooks

Send multiple authorized events

So you must:

Check if already captured

Never double-capture

Example:

if (payment.captures.length === 0) {
capture();
}
