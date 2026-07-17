---
title: "966 Event Settlement Refunds Shipped"
date: "2026-06-11"
tags: [session-log, project/experts]
category: "session-log"
---

# Session: #966 Event Settlement & Refunds shipped (PR #1003)

- **Date:** 2026-06-11
- **Type:** implementation session (subagent-driven execution of a superpowers plan)
- **Outcome:** merged to main (squash 06515d77), sentinel-verified; issue #966 auto-closed

## What shipped
Lifts the D-9 event exclusion: event refund flow (attendee request POST/GET + UI, admin approve/reject shared + event process handler with credit note/ZATCA/clawback), settlement writer `"event"` branch with coupon-snapshot parity (#998 rebase), shared clawback extraction (`src/lib/settlement/clawback-settlement.ts`), reconcile 3-way fair-budget sweep, affiliate holdUntil = max(+3d, eventStart), E-6 refunded-row re-purchase block, polymorphic `refund_requests` (sourceType + registrationId FK + hand-added CHECK constraint), admin queue discriminated DTO/UI (en/ar/es).

## Decisions / gotchas worth keeping
- **Refund-process race fix is now the house pattern:** atomic CAS claim on `refundRequest.status` as the first tx statement + credit-note reuse-or-create INSIDE the tx; loser gets 409. Applied to BOTH event and course handlers in the same diff (sibling rule).
- Eligibility time gates evaluate at `requestedAt` (EXP-129 snapshot rule); state gates re-check current reality.
- `resolveEventStart/End` (event-refund-policy.ts) are the canonical occurrence resolvers — fetch occurrences unfiltered, let the policy exclude cancelled rows; the completion handler's occurrence select now filters `isCancelled: false` (cancelled-first rows used to poison the affiliate holdUntil anchor and invoice occurrenceId).
- Admin refunds query: `publishingStatus` filter must be scoped to the course OR-arm or event rows silently vanish (§7 trap).
- Worktree tooling: lint-staged resolves a different prettier config than the `pnpm format` gate (run prettier with `--config ../../prettier.config.js` explicitly); `experts:test`/`experts:check` only exist at repo root; experts_test DB needs `prisma migrate deploy` with TEST_DATABASE_URL credentials (default user → P1010).

## Open actions
- #1004 — affiliate attribution writes escape callers' interactive transactions (global prisma client); Tier-1 = move call outside the tx.
- Regenerate `src/i18n/extracted.csv` (stale pre-#973 48-hour refund copy).
- Named follow-ons from the spec: #965 subscription refunds, re-purchase-after-refund (new-row model), bulk event-cancel refunds, refund lifecycle notifications.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
