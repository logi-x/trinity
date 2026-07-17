---
title: "readme"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/agent-pipeline/readme.md"
---
# Agent Finding Pipeline

This directory defines the **contract** that automated agents and subagents follow when they file, triage, implement, and
close findings on the Experts Linear board. It exists so that a finding produced by a scheduled routine (or an ad-hoc
agent run) is immediately triageable, safely implementable, and provably done — without a human having to reverse-engineer
what the agent meant.

## Why this exists

The repo runs scheduled agent routines (`.claude/routines/`) that scan the codebase and the board:

| Routine                               | Role                                      | Cadence (Asia/Riyadh) |
| ------------------------------------- | ----------------------------------------- | --------------------- |
| `01-scan-vulnerabilities` (R1)        | Files **vulnerability** findings          | daily ~09:20          |
| `02-find-critical-bugs` (R2)          | Files **bug** findings                    | daily ~09:00          |
| `03-fix-bugs` (R3)                    | Implements `bug` + `Todo` findings as PRs | daily ~10:00          |
| `04-docs-digest` (R4)                 | Summarizes recent activity                | daily ~09:40          |
| `05-gatekeeper` (R5)                  | Reviews agent PRs before merge            | hourly                |
| `07-codebase-completeness-audit` (R7) | Files **completeness** findings           | Mon/Thu               |
| `08-linear-board-audit` (R8)          | Detects duplicates / drift / conflicts    | Mon                   |
| `09-routines-audit` (R9)              | Audits agents/routines for security drift | Tue                   |

R1/R2/R7 **produce** findings; R3 **consumes** them; R5 **gates** the resulting PRs. A finding that does not conform to the
intake contract cannot flow cleanly through that pipeline — it stalls in triage, gets misrouted, or merges without
evidence. These documents make each handoff unambiguous.

## The documents

1. [`intake-contract.md`](./intake-contract.md) — the universal contract every agent-created finding must satisfy, plus
   routing rules (which finding goes to which template/lane). **Raw notes are not findings.**
2. [`vulnerability-finding-template.md`](./vulnerability-finding-template.md) — the template for security findings
   (R1), including severity → Linear priority mapping.
3. [`bug-finding-template.md`](./bug-finding-template.md) — the template for bug findings (R2), including priority mapping
   and duplicate detection.
4. [`implementation-handoff-contract.md`](./implementation-handoff-contract.md) — what a triaged finding must carry
   before it is handed to an implementing agent (R3) or a human.
5. [`validation-evidence-checklist.md`](./validation-evidence-checklist.md) — the evidence required before any finding may
   move to **Done**. Separate paths for security vs. bug fixes.
6. [`runbooks.md`](./runbooks.md) — operating runbooks for each stage (intake, triage, security handling, bug handling,
   handoff, validation/closure, escalation, status/comment conventions).

## Lifecycle at a glance

```
 produce            triage              implement           validate            close
[R1/R2/R7]  ──▶  [intake contract] ──▶ [handoff contract] ──▶ [evidence ──▶ Done]
 finding         + template            R3 / human PR          checklist]   (+ close GH mirror)
                 + routing                                    R5 gatekeeper
```

## Linear conventions referenced throughout

- **Team:** Experts. **Workflow states:** `Backlog` → `Recourses` (parked/holding) → `Todo` → `In Progress` →
  `In Review` → `Done`; plus `Duplicate` and `Canceled` as terminal states.
- **Priority:** `1` Urgent · `2` High · `3` Medium · `4` Low · `0` None.
- **Labels:** `bug`, `security`, `completeness`.
- **GitHub mirror:** every Linear issue has a mirrored GitHub issue; the two-way sync means closing one side without the
  other gets reopened — always close **both**.
- **Fingerprint:** each agent-filed finding carries an inline-coded dedup marker `` `<!-- agent-fp: <hash> -->` `` in its
  body so re-scans and the board audit can detect duplicates.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
