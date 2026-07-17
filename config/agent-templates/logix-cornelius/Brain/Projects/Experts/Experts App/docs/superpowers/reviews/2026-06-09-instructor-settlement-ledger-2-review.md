---
title: "2026 06 09 instructor settlement ledger 2 review"
date: "2026-06-09"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/reviews/2026-06-09-instructor-settlement-ledger-2-review.md"
---
Verdict: not yet a safe one-shot. One revision pass needed.

The design (four-layer model, affiliate-mirror, status-guarded writes, idempotency-by-unique-key) is sound. But the plans contain 4 confirmed factual errors (code that references fields/shapes that don't exist) and 1 make-or-break architecture question that, executed as-written, produce a worker that crashes on
first job, settlements keyed to undefined, and silently wrong money math. None are deep — all are fixable in the plan docs before execution.

---

🔴 BLOCKING — confirmed facts (verified against the live codebase)

These were ground-truthed against prisma/schema.prisma and price-order.ts. They are not judgment calls:

┌─────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────────┐
│ # │ Defect │ Evidence │ Fix │
├─────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ B1 │ priceOrder affiliate input is wrong. Both plans pass affiliate: {commissionAmount}. The real AffiliateMetadata is {commissionType, commissionValue, fundedBy} │ Fails TYPECHECK; if bypassed, instructorEarning→NaN→Postgres │ Pass {commissionType:"fixed", commissionValue: amount, │
│ │ (price-order.ts:24-29). No commissionAmount field exists. │ rejects the row. Affiliate not netted. │ fundedBy:"INSTRUCTOR"} via a small adapter + a "netted once" test. │
├─────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ B2 │ Event.endDate does not exist. Plan A calls calculateEventPayableDate(event.endDate ?? new Date()). Event end lives on EventOccurrence.endsAt. The ?? new Date() │ schema.prisma Event model (no endDate); end is per-occurrence. │ Resolve end from last non-cancelled EventOccurrence.endsAt; warn if │
│ │ makes it a silent wrong-date — earnings mature immediately, collapsing the event refund window. │ │ none. Or drop events from Plan A. │
├─────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ B3 │ completionResult.pendingInvoice.enrollmentId does not exist. PendingInvoiceContext exposes only {businessEntityId, courseTitle, coursePrice, courseId}. The │ course-enrollment-complete.handler.ts │ Thread enrollmentId/registrationId out of the handlers (a │
│ │ settlement sourceId would be undefined → jobId settlement_course_undefined → all course settlements collide into one job. Same for event registrationId. │ │ prerequisite task — can't be worked around at the call site). │
├─────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ B4 │ Subscription has no amountPaid/currency column. Plan B's resolveSubscriptionFacts reads subscription.amountPaid; amount only exists on the command, not the row. A │ schema.prisma Subscription model │ Source gross from the Invoice, or pass amountPaid in the job payload. │
│ │ DB-re-resolving worker can't recover the gross → grossPaid<=0 skips every subscription. │ │ │
└─────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────┴───────────────────────────────────────────────────────────────────────┘

---

🔴 BLOCKING — the architecture make-or-break

B5 — Worker deployment topology is self-contradictory. tsup.config.ts explicitly bundles workers as "framework-free: NO Prisma, NO DB client" (the ZATCA worker is pure-compute, fed a snapshot). But this design's settlement worker re-reads the DB to resolve facts. As specified, the worker bundle excludes Prisma →
crashes on the first prisma.courseEnrollment.findUnique(). Spec §11 itself is split-brained: it says "BullMQ worker re-resolving from DB (storage-janitor precedent)" and "crons are internal routes wrapping pure functions."

Pick one before coding Phase 4 (architecture-reviewer's recommendation, which I share):

- Option C (simplest): drop the worker entirely. Make the settlement write an internal cron-sweep route (storage-janitor pattern, which the spec already adopts for the other two crons). The reconciliation sweep is the delivery mechanism. One fewer process, no bundling fight.
- Option A: snapshot pattern (thread facts into the job like ZATCA) — keeps the queue, no infra change, but more API-side threading.
- Option B: make it a first-class DB-backed worker (update tsup/package.json/Docker/CI/docs) — heaviest.

    ***

    🟠 BLOCKING/IMPORTANT — logic foot-guns (multi-agent consensus; several already flagged in round-1 and not applied)

- B6 — Settlement written after a refund. Writer gates on amountPaid != null, not status. A job queued before a refund but run after it creates live earnings on a refunded order; clawback already ran and matched nothing. Add status === 'refunded'/'cancelled' guard to all three resolvers. (round-1 flagged; still
  present)
- B7 — onDelete: Cascade on the financial ledger. Deleting an OrderSettlement silently destroys its earning audit trail. Change to onDelete: Restrict. (round-1 flagged; still present)
- B8 — Idempotency race. findUnique→create with no P2002 catch; concurrent worker + reconcile sweep race the unique index → job fails & retries 8×. Catch P2002 as success (or upsert). (round-1 flagged; still present)
- B9 — Reconciliation sweep loads the entire settlements table into memory every tick (the take only bounds candidates). OOM time-bomb. Use a bounded NOT EXISTS anti-join. (round-1 flagged; still present)
- I1 — Failed payout strands earnings forever. On CreatorPayout→failed, payoutId is never cleared, so those approved lines satisfy neither payable (payout_id IS NULL) nor paid — invisible to the balance view permanently. Clear payoutId in the failed-transaction; also extend the "one pending" guard to cover
  processing.
- I2 — Clawback keyed by (buyerUserId, itemType, itemId), not the settlement/source row. A buyer who refunds → re-enrolls → refunds again claws the wrong (already-paid) earnings. Key clawback on settlement: {sourceType, sourceId}.
- I3 — Negative instructorEarning unhandled. A high affiliate commission (live today) can exceed the 80% instructor share → negative earning lines. Guard: if instructorEarning <= 0, write platform-only settlement, zero lines, observe a warning.
- I4 — Missing indexes for the maturation hot path: @@index([status, payableAt]) and @@index([settlementId]). (round-1 flagged; still present)
- I5 — Cron route auth is a placeholder (const guard = /_..._/ null → endpoint is open). Wire the real storage-janitor pattern verbatim: getEnvOrSecret("CRON_SECRET","cron_secret") + timingSafeCompareCronSecret.

    ***

    🟡 Worth fixing in the plan text (lower risk)

- Role enum mismatch: "secondary" isn't a real value — it's co_instructor/contributor (InstructorRole) / co_host/speaker/guest (HostRole). Tests use a synthetic value; real role column will hold the enum strings.
- Two-PR seam: defer payoutId column to Plan B (add column+relation together) so Plan A doesn't leave a dangling column the drift gate flags. Or accept it with a documented migration comment.
- CreatorBalance view is drift-gate sensitive — hand-author SQL to match the schema view block exactly; mirror AffiliateBalance's Decimal convention.
- Stopgap visibility (PM): Plan A accrues earnings nobody can see/pay until Plan B. Add a tiny GET /internal/settlement/stats (counts + totals by status) so the ledger isn't dark, and commit to a ≤2-week gap between the PRs (or ship as one).
- Document the unknowns: the 100 SAR threshold origin; subscription renewal collision risk (does a renewal create a new Subscription row or update? — affects the idempotency key); event-clawback deferral needs explicit operator sign-off (event refunds will silently not claw back).
- One false alarm to dismiss: the architecture-reviewer worried Commission.userId might be the affiliate, not the buyer — the live refund handler queries commission … where userId: enrollment.userId, confirming userId = buyer. The plan's query is fine.

    ***

    Recommendation

    This is close — the bones are good and the affiliate-mirror keeps risk low. But it should not go to one-shot execution until B1–B9 are folded into the plan docs and B5 (worker topology) is decided. Round-1 already caught ~half of these and they weren't applied, so a verification-after-revision step matters.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
