Next enhancements

1. morning_digest.py scans memory, not the Action-Tracker

The current digest reads Claude Code memory files for date mentions. The Action-Tracker is the canonical source — but nothing scans it. The digest
should parse Action-Tracker.md directly: surface all Open rows where Priority is Critical or High, plus any row where Deadline ≤ today.

Low effort, high daily value.

---

2. Decision-Log has no staleness signal

Decisions from November 2025 may already be superseded. No way to know without reading them all. Add a review_by field to each Decision-Log row —
then the lint workflow (or audit_index.py) can flag overdue reviews.

| Date | Decision | Rationale | Owner | Review By |

---

3. No convention for closing completed actions

The Action-Tracker has Status: Completed rows but they'll accumulate and pollute the active view. Define a convention — move completed rows to a ##
Archived section at the bottom, or to a separate Action-Tracker-Archive.md. Right now the tracker will just grow unbounded.

---

4. coverage_report.py — conversation health

781 conversation files exist but there's no visibility into which ones are properly tagged vs. raw imports. A script that reports:

- % of conversations with tags in frontmatter
- % with at least one `WikiLink` to an entity
- Oldest 10 untagged files

This tells you where the knowledge graph is thin.

---

5. Missing "Close an Action" workflow in CLAUDE.md

There are workflows for Ingest, Query, and Lint — but nothing for:

- Marking an action complete + noting what was done
- Logging a decision as implemented
- Archiving a completed meeting's actions

These are the natural outputs of working sessions and they're currently unguided, which means they don't happen consistently.

---

6. status field is inconsistent across project entities

Confirmed on Experts.md, but HoWA, Logix ETF, MCP Core, N8N Core, Visora, Beyound likely don't have it yet. The add_project_status.py tool exists —
has it been run against all of them?

---

Priority order

┌─────┬─────────────────────────────────────────────────────┬────────┬────────┐
│ # │ Enhancement │ Effort │ Impact │
├─────┼─────────────────────────────────────────────────────┼────────┼────────┤
│ 1 │ Upgrade morning_digest.py to scan Action-Tracker.md │ Low │ High │
├─────┼─────────────────────────────────────────────────────┼────────┼────────┤
│ 2 │ Add review_by to Decision-Log + lint check │ Low │ High │
├─────┼─────────────────────────────────────────────────────┼────────┼────────┤
│ 3 │ Define completed-action archiving convention │ Low │ Medium │
├─────┼─────────────────────────────────────────────────────┼────────┼────────┤
│ 4 │ Add "Close an Action" workflow to CLAUDE.md │ Low │ Medium │
├─────┼─────────────────────────────────────────────────────┼────────┼────────┤
│ 5 │ coverage_report.py for conversations │ Medium │ Medium │
├─────┼─────────────────────────────────────────────────────┼────────┼────────┤
│ 6 │ Verify status field across all project entities │ Low │ Low │
└─────┴─────────────────────────────────────────────────────┴────────┴────────┘

Want me to start with #1 (the digest upgrade) or tackle these in order?

---

Completed so far

Wave 1 (original lint report)
All 7 items done — index fixed, stubs filled, duplicates merged, audit script, Priority column, meeting template.

Wave 2 (this session)
All 6 items done — morning digest, stale decisions, archive convention, Close an Action workflow, coverage report, status field verified.

Plus one carry-over: updated field missing from all 11 project entity files (schema says it should be there, it isn't yet).

---

Next wave options

Wave 3 — Knowledge flow (close the gaps the tooling just exposed)

┌─────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬────────┬────────┐
│ # │ Item │ Effort │ Impact │
├─────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼────────┤
│ 1 │ Add updated field to 11 project entities │ Low │ Low │
├─────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼────────┤
│ 2 │ Tag → entity link enrichment — script that reads existing tags (project/experts, topic/payments) and adds the matching `WikiLink` to conversation files — closes the 453-file gap │ Medium │ High │
├─────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼────────┤
│ 3 │ morning_digest: add explicit "Pending Ingests" queue — files in Raw/sources/ older than 24h that haven't been ingested yet (currently digest only shows last 24h) │ Low │ Medium │
├─────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼────────┤
│ 4 │ Session close note tool — \_tools/reports/session_close.py that scaffolds a structured note into Raw/sources/ at end of a work session │ Low │ Medium │
└─────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────┴────────┘

Wave 4 — Meeting intelligence

┌─────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬────────┬────────┐
│ # │ Item │ Effort │ Impact │
├─────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼────────┤
│ 5 │ Meeting → tracker extraction helper — after ingesting a meeting note, script suggests Action-Tracker and Decision-Log rows from the text │ Medium │ High │
├─────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼────────┤
│ 6 │ Weekly review script — shows pages touched that week (from Log.md), actions closed, decisions reviewed, coverage delta │ Medium │ Medium │
└─────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────┴────────┘

Wave 5 — Graph & navigation

┌─────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────┬────────┬────────┐
│ # │ Item │ Effort │ Impact │
├─────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼────────┤
│ 7 │ Project snapshot automation — project_snapshot.py generates a dated status page for any project on demand │ Medium │ Medium │
├─────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼────────┤
│ 8 │ Orphan detection in audit_index.py — pages with no inbound WikiLinks │ Low │ Medium │
├─────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼────────┤
│ 9 │ Other project repos (HoWA, ETF, etc.) — same CLAUDE.md/AGENTS.md wiring we did for experts-app │ Low │ Medium │
└─────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────┴────────┘

---

My recommendation for Wave 3

Start with 2 → 3 → 4 in that order:

- #2 tag enrichment closes the biggest structural gap (453 files, ~58% of the vault) — and the coverage report now makes it measurable
- #3 pending ingests makes the morning digest complete — right now files sit in Raw/sources/ silently
- #4 session close tool closes the loop on the knowledge flow we designed today — without it, the capture ritual is still manual and easy to skip

Plus #1 is 5 minutes of work, we can do it right now if you want.

Which of these do you want to tackle?
