---
title: "affiliate v2"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/affiliate-v2"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  Q: I don't think these are good, as I think there's a better alternative and they're prone to errors totalEarnings Decimal @default(0) @map("total_earnings") @db.Decimal(10, 2) pendingEarnings Decimal @default(0) @map("pending_earnings") @db.Decimal(10, 2) paidEarnings Decimal @default(0) @map("paid_earnings") @db.Decimal(10, 2) don't you agree, or am I wrong ?

A: You’re not wrong at all — in fact, I strongly agree with you 👍
Those fields are a liability, not a convenience, in a serious financial system.

Your instinct here is exactly what senior fintech / accounting systems follow.

Short answer

✅ Yes, they’re error-prone and should not be authoritative
❌ They should never be the source of truth

At best, they are cached projections.
At worst, they silently desync and destroy trust.

Why these fields are dangerous
1️⃣ They violate single source of truth

You already have:

Commission

AffiliatePayout

Those already encode all monetary reality.

Storing:

totalEarnings

pendingEarnings

paidEarnings

means you now have two truths:

The ledger (commissions / payouts)

The summary (affiliate totals)

Eventually, they will disagree.

2️⃣ Race conditions are inevitable

Examples:

Two commissions approved concurrently

Payout job retries

Manual admin adjustments

Partial payouts

Refunds after payout creation

All it takes is one failed transaction or one missing lock and your totals drift.

You can “try” to fix this with:

Transactions

Row locks

Background reconciliation jobs

…but now you’re fighting your own schema.

3️⃣ Refunds & reversals destroy naive counters

Consider:

Commission approved

Affiliate sees balance

Refund happens

Commission cancelled

Which number do you decrement?
What if payout already exists?

Ledger-based systems handle this naturally.
Counters don’t.

What mature systems do instead (Stripe, Shopify, AdSense)

They follow ledger-first accounting:

💡 All balances are derived, never stored.

The correct mental model
Source of truth

Commission rows = credits

AffiliatePayout rows = debits

Everything else is a view.

How to replace those fields cleanly
1️⃣ Remove these from Affiliate
// ❌ remove
totalEarnings
pendingEarnings
paidEarnings

2️⃣ Derive balances via queries (or materialized views)
Pending balance
SUM(commission_amount)
WHERE affiliate_id = ?
AND status = 'pending'

Approved / payable balance
SUM(commission_amount)
WHERE affiliate_id = ?
AND status = 'approved'
AND payout_id IS NULL

Paid balance
SUM(commission_amount)
WHERE affiliate_id = ?
AND status = 'paid'

“But isn’t this expensive?”

Great question — this is where people get confused.

Reality

Affiliates don’t have millions of rows

Aggregates on indexed columns are fast

PostgreSQL handles this extremely well

And if you do need speed…

The only acceptable optimization
Materialized View (read-only cache)
CREATE MATERIALIZED VIEW affiliate_balances AS
SELECT
affiliate_id,
SUM(CASE WHEN status = 'pending' THEN commission_amount ELSE 0 END) AS pending,
SUM(CASE WHEN status = 'approved' AND payout_id IS NULL THEN commission_amount ELSE 0 END) AS payable,
SUM(CASE WHEN status = 'paid' THEN commission_amount ELSE 0 END) AS paid
FROM billing.commissions
GROUP BY affiliate_id;

Refresh on schedule or event

Never manually mutated

Always reproducible

✅ This is safe
❌ Counters in Affiliate are not

When counters are acceptable (rare)

Only if all are true:

Read-only mirror

Rebuilt regularly

Never manually adjusted

Never used for payments

Even then, I’d still prefer a view.

Verdict (very clear)

You are 100% right.

Those fields:

❌ add risk

❌ add reconciliation complexity

❌ add hidden bugs

Removing them:

✅ simplifies logic

✅ guarantees correctness

✅ aligns with real accounting systems

✅ scales safely
