---
title: "2026 06 10 event settlement refunds 2 review"
date: "2026-06-10"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/reviews/2026-06-10-event-settlement-refunds-2-review.md"
---
# Spec review round 2 — six-agent panel on the #966 Events-phase spec

**Date:** 2026-06-10
**Panel:** workflow-orchestrator, concept-architect, code-reviewer, architecture-reviewer, product-manager, Explore (codebase sweep)
**Caveat:** mid-run, the working tree moved off the docs branch (an agent checked out main and the docs branch got swept by branch cleanup), so the panel reviewed **issue #966 + the codebase without the v2 spec text**. Findings were therefore triaged by the orchestrator against v2: items v2 already covered are marked as such; genuinely new items were verified against code before adoption.

## Adopted into v3 (verified against code)

1. **Re-purchase after refund recycles the registration id** (workflow F-1, verified at `event-register.handler.ts` — only `completed` blocks; upsert on `(eventId, userId)`): second purchase hits the settlement unique `("event", registrationId)` and the host earns nothing; `commissionAlreadyAttributed` (no status filter) blocks re-attribution. → **E-6: block re-registration of `refunded` registrations**; re-purchase model is a named follow-on. Operator-confirmed.
2. **Slow-admin trap / TOCTOU direction** (workflow F-7): the course process handler re-checks `withinRefundWindow` at process time; with the event 48h-before-start hard deadline, a timely request could expire in the admin queue. → **snapshot-at-request rule** (§4): time gates evaluated against `requestedAt`, state gates against now. Matches the EXP-129 house pattern.
3. **Rejected-request lockout** (PM A-2): one-request-ever per registration locks attendees out after a rejection inside a hard deadline. Operator decided **strict course parity anyway (E-7)** — risk accepted, documented.
4. **No attendee-facing refund UI exists for courses** (PM B-1): "full parity" would ship events API-only. Operator decided **minimal attendee UI ships in this phase (E-8)**.
5. **Admin queue `publishingStatus` relation filter would silently hide event rows; triage badge counts all `requested` rows** (code-reviewer M-7) → explicit trap notes in §7.
6. **Notifications: course refund flow sends none** (concept B-4; registries verified empty of refund keys) → deliberate-deferral statement + named follow-on (§4, §8).
7. **`HostRole` primary is `"host"`, not `"primary"`** (code-reviewer M-5) → made loud in §6 (wrong role ⇒ every single-host event fires the fallback warn); writer test asserts no-warn on single host.
8. **Occurrence select must fetch `endsAt`** (code-reviewer M-3: completion handler selects `startsAt` only) → §6 note.
9. **`payableAt` staleness on occurrence reschedule** (workflow F-3) → §2.1: snapshot-immutable, edge documented.
10. **Attribution mechanics for the holdUntil fix** (workflow F-4): `handleAffiliateAttribution` input lacks event start → thread optional `eventStartsAt` with DB fallback; `referral.expiresAt` explicitly unchanged (§5.1).
11. **Legal discretionary clauses** (PM A-4/A-5): "attended/accessed" denial and platform-credit option are admin discretion in v1, documented (§4, §8).
12. **Migration mechanics**: explicit `DROP NOT NULL`; cross-schema FK precedent named (§3.1).
13. **Cron sidecar gap re-flagged** (Explore): reconcile/mature/stats routes still unwired in `docker/production/docker-compose.yml` — folded into the D-8 go-live note (§6); seeder event branch added to sequencing.
14. **Bulk-refund re-evaluation trigger** (PM B-2) → §8.

## Already covered by v2 (panel couldn't see the file)

ZATCA credit note parity; occurrence-based start/end + zero-occurrence rules; reconcile third anti-join + SettlementSourceType widening; shared clawback signature/transaction shape incl. payout-cancel re-read; commission clawback keying `(userId,"event",eventId)`; admin route dispatch by sourceType; neutral discriminated query/DTO move; inverse Prisma relation + db:generate; `refunded` terminal status; cleanup widening; seat-count behavior; en/ar legal-copy consistency; E-1 window∧48h AND-logic.

## Rejected / corrected

- **"Nullable @unique breaks uniqueness / needs partial unique"** (architecture-reviewer): Postgres treats NULLs as distinct; two nullable `@unique` FK columns give exactly the intended per-source one-request invariant under E-7. No partial index needed.
- **"Refund window should open after the event ends"** (architecture-reviewer): contradicts the published Refund Policy (48h-before-start rule); E-1 stands.
- **"Event branch missing from completion handler / spec mismatch"** (Explore): not a gap — that IS this phase's deliverable (D-9 exclusion being lifted).
- **#969 (legal-docs-curator)**: treated this spec's superseded v1 rule as shipped code truth. Nothing is shipped; E-1 conforms code to the published copy. Closed as invalid.

**Verdict after triage:** v3 adopted all verified must-fixes; spec re-approved by operator (E-1..E-8).

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
