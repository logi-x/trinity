---
title: '2026-06-06 Experts — Backlog Close-out ("close the rest")'
date: "2026-06-06"
tags: [project/experts, agent, backlog, session, payments, security, ci, realtime]
category: "daily"
source: "session"
source_id: "Raw/sources/2026-06-06-experts-close-the-rest.md"
---

# Experts — Backlog Close-out ("close the rest")

Operator directive: **"close the rest"** of the Experts Linear backlog, isolated in a worktree to avoid colliding with
the other scheduled agents. Worked the full remaining board (Todo empty at start; ~17 open Backlog issues).

## Outcome

**14 issues resolved.** 4 merged PRs + 4 already-resolved closes + 6 governance docs. Remaining 5 are all
decision-blocked (see [[Action-Tracker]]).

### Merged PRs

| PR   | Issues                     | Change                                                                                                                                                      |
| ---- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| #868 | EXP-309, EXP-308           | Tabby verify routes: `auth()` + `userId` ownership before completion side-effects (401/403); currency no-op → `*.tabby_currency_mismatch` observe + SAR pin |
| #869 | EXP-108                    | Subscription checkout: optional `locale` + `es`-aware `Accept-Language` derivation → Spanish Tabby message reachable                                        |
| #870 | EXP-306                    | Removed dead `src/components/ui/sonner.tsx` (zero importers; app uses the `sonner` package directly)                                                        |
| #871 | EXP-42, 43, 44, 45, 46, 47 | `docs/agent-pipeline/` — finding intake contract, vuln + bug templates, handoff contract, validation checklist, runbooks                                    |

### Closed as already-resolved on `main` (verified, no PR)

- **EXP-307** — subscriptions verify has no Tabby branch by design; `resolveSubscriptionProvider` coerces `tabby`→`stripe`; invariant already documented in-route.
- **EXP-313 / EXP-314** — event host + course instructor email already routed through `mapUserToDTO` (email:null) / `userPublicSelect` by the EXP-294 sweep.
- **EXP-323** — `course-edit.guard.ts` already selects `adminLockedAt` and both edit asserts call `isCourseAdminLocked` (EXP-292 parent fix).

## Key gotchas (also filed to topics)

- **R5 spinoffs are usually already-fixed** by their parent PR's broader sweep. Read current code, not the stale issue
  text — 4 of 5 spinoffs this session were close-as-already-resolved; only **EXP-309 (unauth Tabby-verify completion)**
  was a genuinely-open security hole. → [[Wiki/Concepts/Payments]], memory `feedback-r5-spinoffs-often-already-fixed`.
- **Docs-only PRs don't trigger the path-filtered `experts-app.yml`** → "no checks reported", `mergeable CLEAN`, empty
  `statusCheckRollup`; merge directly. → [[Wiki/Concepts/GitHub Actions]].
- **git arg-injection** needs `--` before the refspec; quoting doesn't stop git's option parser (EXP-304). And
  `set -a; . bake-env` over-exports every credential — use a subshell (EXP-176). → [[Wiki/Concepts/GitHub Actions]].
- Worktree env quirk: full `tsc` exits 2 with **0 `error TS` lines** (gitignored generated Prisma client) — compare
  error counts with/without a change to prove neutrality; rely on `typecheck:touched` + CI for the real gate.
- Adding `auth()` to a previously-auth-less route 401s its existing success tests → add a default owning-session mock.

## Decisions

- Governance docs home = **`docs/agent-pipeline/`** (operator choice over Linear descriptions). → [[Decision-Log]].
- Stale R5 spinoffs → close-as-already-resolved-on-`main` with file:line evidence, not re-implemented. → [[Decision-Log]].

## Open (decision-blocked) — see [[Action-Tracker]]

EXP-305 (Tabby refund policy), EXP-262 (WS connection cap value), EXP-83 (prod data sweep), EXP-283 (Dependabot
cadence), EXP-203 (eslint suppression pattern).

## Process notes

- Worked entirely in the `close-the-rest` git worktree (own `node_modules`); `origin/main` advanced under the run twice
  (#867 + others) — the fresh-from-`origin/main` worktree absorbed it with zero conflicts. Each code PR locally verified
  (vitest + prettier + `typecheck:touched`) before push; all passed CI first try.
- Related prior session: [[Raw/sources/2026-06-03-experts-agent-digest]].

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
