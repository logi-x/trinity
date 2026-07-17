---
title: "Instructor settlement system (#936) shipped in two flag-gated PRs: Plan A #961 (courses earnings ledger) + Plan B #962 ("
date: "2026-06-09"
decision: "Instructor settlement system (#936) shipped in two flag-gated PRs: Plan A #961 (courses earnings ledger) + Plan B #962 (payouts, surfaces, platform-only subscriptions). Four-layer model: OrderSettleme"
stakeholders: "Logix, Payments"
review_by: "2026-09-09"
source: "[[Raw/sources/2026-06-07-experts-decision-blocked-five]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Instructor settlement system (#936) shipped in two flag-gated PRs: Plan A #961 (courses earnings ledger) + Plan B #962 (payouts, surfaces, platform-only subscriptions). Four-layer model: OrderSettlement (financial truth, unique on sourceType+sourceId) → CreatorEarning lines → CreatorPayout (manual admin execution) → creator_balances SQL view (payable = approved ∧ payout_id IS NULL). Everything inert behind `SETTLEMENT_LEDGER_ENABLED` (default off); go-live = deploy → wire cron reconcile/mature routes → flip flag. Events and subscription renewals explicitly out of scope (D-9 / follow-on).

**Rationale:** Money-correctness invariants locked in by the review panel: payout-request eligible earnings are `SELECT … FOR UPDATE` inside the tx with amount = Σ of linked rows (double-spend impossible); admin process uses #956 status-guarded updateMany (pending/processing → terminal, 409 on count=0, failed unlinks non-terminal earnings); refund clawback cancels in-flight payouts but unlinks ONLY payouts the guarded cancel actually cancelled (refund-vs-complete race can't return paid earnings to payable); subscription settlement keys gross on the earliest PAID invoice. VAT-registered creators must not be paid until self-billing exists (admin warning, spec §12).

**Stakeholders:** Logix, Payments

**Source:** [[Raw/sources/2026-06-07-experts-decision-blocked-five]]
