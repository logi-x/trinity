---
title: "2026 06 09 instructor settlement ledger 1 review"
date: "2026-06-09"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/reviews/2026-06-09-instructor-settlement-ledger-1-review.md"
---
Round 1 review:

**Blocking Issues**

- **Scope mismatch:** [Plan A](/home/logix/experts/docs/superpowers/plans/2026-06-09-instructor-settlement-ledger.md:11) is ledger-only for courses/events and defers payouts, balance view, creator/admin surfaces, subscriptions, and event/subscription clawback. But [the spec](/home/logix/experts/docs/superpowers/specs/2026-06-09-instructor-settlement-design.md:6) and issue #936 ask for settlement plus payout path. Either rename this as partial “ledger foundation, Refs #936” or expand it to include payout/balance/admin processing.
- **Settlement worker deployment is unresolved:** the plan says mirror ZATCA, but app worker guidance says deployed workers are pure compute/no Prisma. Settlement re-reads DB. Either make it a first-class DB-backed worker and update `package.json`, `tsup`, Docker/CI, docs, and ops, or use app-side internal routes/sweeps like storage janitor.
- **Idempotency race:** [record writer sample](/home/logix/experts/docs/superpowers/plans/2026-06-09-instructor-settlement-ledger.md:557) does `findUnique` then `create`. Concurrent webhook/reconciliation jobs can race into a unique violation. Add atomic upsert/create-conflict handling or catch Prisma `P2002` as success, plus a concurrent-call test.
- **Wrong event payable date:** plan references `event.endDate`, but `Event` has no such field. Use actual occurrence/schedule end data and define behavior for multi-occurrence events.
- **Wrong affiliate input:** [plan passes `{commissionAmount}`](/home/logix/experts/docs/superpowers/plans/2026-06-09-instructor-settlement-ledger.md:583), but `priceOrder` expects `{commissionType, commissionValue, fundedBy}`. Add a helper for fixed instructor-funded affiliate commission and test “netted once.”
- **Missing source IDs:** course/event completion contexts do not currently expose enrollment/registration row IDs, yet settlement keys need those IDs. Add a task to thread `enrollmentId` / `registrationId` through before enqueue wiring.
- **Delayed job after refund:** writer must require source status `completed`, not just `amountPaid != null`, or a queued settlement can create earnings after a refund.

**Important Amendments**

- Remove `onDelete: Cascade` from financial ledger relations; this is not immutable enough.
- Decide how to handle negative creator earnings when affiliate/discount exceeds instructor share.
- Snapshot contributor shares at sale time or prevent mutable revenue-share edits from changing settlement results after checkout.
- Rework reconciliation to query bounded candidates first, not load all settlements; add per-row failure counters.
- Add indexes for maturation/reporting: `CreatorEarning(status, payableAt)`, `CreatorEarning(settlementId)`, `OrderSettlement(status, sourceType, sourceId)`.
- Replace internal route skeleton placeholders with the actual `CRON_SECRET` guard pattern.
- Add migration preflight proving `contributor_earnings` is empty before replacing the stub.
- Add real verification gates: migration apply/drift, Prisma writer integration, cron auth tests, queue consume smoke, refund-after-queue test, and product/admin UAT.

**Recommendation**
Before implementation, revise the plan into either:

1. **Plan A ledger foundation only**, explicitly not closing #936, with operational reporting/stopgap and a separately written Plan B; or
2. **Full #936 one-shot**, adding `CreatorBalance`, payout method, creator request route, admin process route, basic reporting/surfaces, and launch/compliance gates.

The current plan is a useful foundation, but it has enough foot-guns that executing it as-is would likely create avoidable production and finance risks.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
