---
title: "2026-06-07 Experts — Decision-Blocked Five + agent/skill/worktree cleanup"
date: "2026-06-07"
tags: [project/experts, agent, backlog, session, payments, realtime, ci, db, tooling]
category: "daily"
source: "session"
source_id: "Raw/sources/2026-06-07-experts-decision-blocked-five.md"
---

# Experts — Decision-Blocked Five + tooling cleanup

Follow-on to [[Raw/sources/2026-06-06-experts-close-the-rest]]. The operator supplied the five decisions
that the previous "close the rest" sweep was blocked on, then asked to ship them through the full pipeline
in a loop. Also handled a `.claude/` agent/skill/worktree cleanup.

## Outcome — board fully cleared

All five shipped via the full pipeline (commit → PR → CI watched green → squash-merge → sentinel-verify on
`origin/main` → branch prune → GH mirror close → Linear Done). **CI passed first try on every PR.** After:
Linear Todo / Backlog / In Progress / In Review all **empty**.

| PR   | Issue   | Change                                                                                                                                |
| ---- | ------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| #877 | EXP-283 | `.github/dependabot.yml` — docker ecosystem × (3 Dockerfile dirs + prod/staging compose), **weekly, grouped**                         |
| #878 | EXP-203 | `extractDiagnosticMessage()` in `@/lib/errors/api-error`; **both** inline `no-restricted-syntax` suppressions removed                 |
| #879 | EXP-262 | per-user WS cap `MAX_WS_PER_USER=10` (atomic INCR→check→rollback) + WS JWT TTL **24h→1h**                                             |
| #880 | EXP-83  | `VALIDATE CONSTRAINT course_isfree_price_consistency` migration (prod sweep = 0 violating rows)                                       |
| #881 | EXP-305 | Tabby geo-block moved **before** capture → `closeTabbyPayment` voids the authorization; already-captured race → manual-refund alert   |

## The five decisions (operator)

- **EXP-305:** before-capture **void only, no auto-refund** → [[Wiki/Concepts/Payments]].
- **EXP-262:** cap **10**/user, TTL **1h** → [[Wiki/Concepts/WebSockets]].
- **EXP-83:** prod sweep = **zero rows** → ship the VALIDATE migration.
- **EXP-283:** **weekly, grouped** into one PR → [[Wiki/Concepts/GitHub Actions]].
- **EXP-203:** **shared helper** `extractDiagnosticMessage()` allowlisted once.

## Key findings / gotchas

- **EXP-305 — "no ledger to reverse."** The verify routes never capture (capture is **webhook-only**), and an
  invoice/ZATCA is created only on completion — which never runs for a blocked purchase. So a geo-blocked buyer
  has **no invoice/payment record to reverse**; the right fix is void-before-capture, not a refund/ledger entry.
  Surfaced this to the operator before writing money code; they chose void-only.
- **EXP-203 — a bare `return err.message` trips no EXP-189 selector.** The guard's selectors are scoped to
  `NextResponse.json` sinks and to `VariableDeclarator[id.name=/message|errMsg.../]`. A helper that does
  `if (err instanceof Error) return err.message;` outside any response sink matches **none** of them → the two
  call-site suppressions could be **removed entirely**, not just consolidated. Better than the issue's ask.
- **EXP-262 — `incrWsConnectionCount` already returns the post-incr count**, so the cap is the canonical
  race-safe INCR→check→rollback with zero helper changes; `closeAll()` already decrements on close = the rollback.
- **EXP-83 — CHECK constraints are drift-invisible.** No `schema.prisma` change; `VALIDATE CONSTRAINT` doesn't
  alter the modelled schema, so `db:check:drift` stays clean ("No difference detected"), confirmed locally + in CI.
- **`.github/`-only PRs trigger no app CI** (path-filtered `experts-app.yml`) → #877 was MERGEABLE/CLEAN with
  0 checks → merged directly. Same class as docs-only PRs. → [[Wiki/Concepts/GitHub Actions]].
- **Pipeline discipline held:** staged only the unit's files each time (the `gitnexus-cli/SKILL.md` reindex
  artifact in the tree is **not** mine — never staged it); verified each change is actually on `origin/main`
  with a sentinel grep, not just PR=MERGED.

## Tooling cleanup (decision; execution partial)

- Created **one** Experts-specific `.claude/agents/browser-agent.md` (Claude Code `.md` agent → agent-browser
  skill + Playwright MCP, RTL/HeroUI-v3/payments-flow aware), replacing the ruflo `browser/browser-agent.yaml`.
- **Decision:** drop the ruflo/claude-flow agent subdirs (`consensus/core/sparc/swarm/testing` + `browser`) and
  the ruflo skill pack; keep native `Workflow`/`Agent` orchestration + bespoke Experts agents + **gitnexus**
  (the only genuine repo-grounded code-intel). `agentdb-vector-search` etc. contradict the real **pgvector**
  stack (`src/lib/ai/*`). → [[Decision-Log]].
- **Execution state:** 17 ruflo skills already deleted (uncommitted by a concurrent process); the 6 agent subdirs
  + 13 ruflo skill dirs are flagged for removal but **not yet committed**.
- **Worktrees:** removed all 9 stale worktrees (exp-197/198/199, r3-slot1–4, close-the-rest,
  synthetic-frolicking-goblet) after verifying each was clean and its content already on `main`.

## Process notes

- Worked in the main tree (session configured to work in place). Branch-per-unit, push explicit `branch:branch`,
  `gh pr checks --watch` (backgrounded for the longer CI runs).
- GH mirrors (#779/#634/#741/#403/#809) all auto-closed by the `Closes EXP-NNN` trailers; Linear flipped via MCP.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
