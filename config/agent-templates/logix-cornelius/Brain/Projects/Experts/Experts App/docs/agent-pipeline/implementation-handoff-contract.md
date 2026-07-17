---
title: "implementation handoff contract"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/agent-pipeline/implementation-handoff-contract.md"
---
# Implementation Handoff Contract

**Outcome:** a triaged finding can be handed to an agent/subagent (or a human) for implementation without ambiguity.
(EXP-45)

A finding is "ready for implementation" only when it carries everything an implementer needs to start without
re-investigating. This is the contract between **triage** and **implementation** (R3 `03-fix-bugs`, or a human PR).

## Raw findings are forbidden in this lane

A raw finding (just symptom + evidence) is not an implementation task. Triage must enrich it into a handoff before it can
move to `Todo` for R3 or be assigned to a human. An issue in the implementation lane that lacks the handoff fields below
must be sent back to triage, not guessed at.

## Required handoff fields

| Field                                   | What it pins down                                                                                                                                                            |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Source finding**                      | Link to the originating finding/issue (and its fingerprint), so the fix can be validated against the original report.                                                        |
| **Scope of change**                     | The specific behavior to change — stated as an outcome, not a vague area.                                                                                                    |
| **Non-goals**                           | What is explicitly out of scope (prevents scope creep and keeps the diff reviewable).                                                                                        |
| **Expected patch behavior**             | What the code should do after the change (the new contract, the new status codes, the new value).                                                                            |
| **Files / modules likely involved**     | If known — the concrete files, and any **symmetric sibling** files that must change in the same diff (e.g. course/event/subscription verify routes).                         |
| **Validation command / check**          | The exact command(s) that prove it: `pnpm experts:check`, `pnpm --dir apps/experts-app typecheck:touched -- <files>`, the vitest path, `pnpm db:check:drift` for migrations. |
| **Rollback / migration risk**           | Whether the change is reversible; for DB work, the migration ordering and drift implications; for infra, what takes effect on next deploy.                                   |
| **Required reviewer / validation gate** | Which gate must pass — the R5 gatekeeper, a specific specialist lens (payments, security, realtime), and/or CI.                                                              |

## Ownership & handoff rules

- **One owner at a time.** When R3 (or a person) picks up an issue, move it to `In Progress`. Do not leave it `Todo`
  while being worked, or two workers may collide.
- **Disjoint files fan out; shared files bundle.** Before dispatching a cluster, map issues → files. Same-file issues are
  **one** bundled PR (a per-issue worktree pool would collide); only fan out across disjoint files.
- **Branch before the PR.** Name the branch for the issue (`feature/exp-NNN-…` or `fix/exp-NNN-…`) before opening the PR;
  renaming a branch after the PR exists closes the PR.
- **Atomic, behavior-named commits.** End agent commit messages with the `Co-Authored-By` trailer used by the routines.
- **PR body links the issue** and lists any collateral issue ids as **plain text** (`EXP-240`, not `**EXP-240**` or a
  link) so the auto-close regex matches.
- **Carry the markers forward:** keep the finding's `` `<!-- agent-fp: <hash> -->` `` reachable, and for R3-auto-fixable
  work ensure `label=bug` + `status=Todo` are set.
- **Out-of-scope discoveries** become new findings (via the [intake contract](./intake-contract.md)) or spinoffs — never
  silently folded into an unrelated diff.

## Already-resolved short-circuit

If, on reading the current code, the implementer finds the finding is **already fixed on `main`** (common for spinoffs),
do not fabricate a change. Close the issue as already-resolved with on-`main` evidence (file:line), close the GitHub
mirror, and skip the PR. This is a valid implementation outcome.

## Example handoff

```
Source:   EXP-309 (`<!-- agent-fp: f83653187ae8 -->`)
Scope:    require an authenticated owner before any Tabby-verify state mutation
Non-goals: do not touch Stripe/Noon branches or the webhook (server-to-server, no session)
Expected: 401 when no session; 403 when session.user.id !== enrollment.userId; legit owner still 200
Files:    courses/[id]/enroll/verify/route.ts AND sibling events/[id]/register/verify/route.ts
Validation: pnpm --dir apps/experts-app exec vitest run <both route tests>; typecheck:touched -- <files>
Rollback: pure logic add, reversible; no migration
Gate:     R5 gatekeeper + CI Verify; security lens
```

## Acceptance criteria (this document)

- [x] Implementation issue template (handoff fields) is documented.
- [x] Raw findings are forbidden in this lane.
- [x] Ownership and handoff rules are clear.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
