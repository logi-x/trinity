---
title: "2026 06 11 fleet redesign flight director design"
date: "2026-06-11"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/specs/2026-06-11-fleet-redesign-flight-director-design.md"
---
# Fleet Redesign: 5-Loop Topology + Flight Director

**Date:** 2026-06-11
**Status:** Approved design, pre-implementation
**Owner:** operator (ahmed) + main session
**Supersedes:** the 9-routine fleet under `.claude/loops/` (00-pulse … 08-overwatch)

## 1. Why

The agent fleet (formerly R1–R9, renamed to space-mission names in #971) works as a
closed maintenance loop — detect → fix → review → merge — but three problems forced
most of it off (`sentinel`, `radar`, `rover`, `airlock`, `overwatch` are
`enabled:false` today):

1. **Cost.** Cold orchestrator sessions run on a clock, not on events. Quiet days pay
   full price. Discovery context (git diff, board snapshot, dedup index) is gathered
   three times by three routines. Cheaper subagent models were tried; the floor was hit.
2. **No feedback component.** Per the loop-engineering frame (trigger / context /
   state / isolation / **feedback** / stop rules), the fleet has every component
   except feedback: when a loop fails repeatedly, humans diagnose and edit the
   prompts by hand. The system detects and recovers but never learns.
3. **Signal quality.** Noisy findings and gatekeeper bounces eroded trust, which is
   a co-equal reason the pipeline is off — not just spend.

This design consolidates 9 loops into 5 (matching discover → plan → execute →
verify → iterate), adds the missing memory and feedback components, and makes
quiet-day cost approach zero.

## 2. Decisions (locked during brainstorm)

| Decision                  | Choice                                                                                   |
| ------------------------- | ---------------------------------------------------------------------------------------- |
| Topology                  | Fewer, fatter loops — exactly 5                                                          |
| Pulse (permissions probe) | Deleted; survives as the shared zero-token `preflight.sh` gate                           |
| Telemetry                 | Repurposed: daily human digest → weekly fleet **memory** consolidator                    |
| Overwatch                 | Dissolved into airlock as an event-driven **fleet-config rubric** (no schedule)          |
| Flight-director authority | **Full self-merge for prompt edits** via airlock, compensated by hard stop rules         |
| Execution surface         | **Local-first** (WSL cron + runner); CCR mirror optional and deletable                   |
| Feature/intent lane       | Out of scope — separate brainstorm once the maintenance fleet is stable                  |
| Git hygiene               | Behavior changes = reviewed PRs on main; memory/measurement = brain or cache, never main |

## 3. Topology

| #   | Loop                | Phase          | Absorbs                    | Cadence           | Preflight early-exit              |
| --- | ------------------- | -------------- | -------------------------- | ----------------- | --------------------------------- |
| 1   | **scout**           | Discover       | sentinel + radar + salvage | Daily             | no commits since last-scanned SHA |
| 2   | **rover**           | Plan + Execute | — (unchanged core)         | Daily             | no fix-ready issues               |
| 3   | **airlock**         | Verify         | overwatch (as rubric)      | 3×/day (every 8h) | no open `agent-generated` PRs     |
| 4   | **telemetry**       | Memory         | replaces daily digest      | Weekly            | no new run logs/verdicts          |
| 5   | **flight-director** | Iterate        | observatory                | Weekly            | — (its job is the look-back)      |

Notes:

- **Rover carries Plan + Execute.** Its prompt already plans then implements; a
  separate plan loop would add a cold-session handoff for no quality gain.
- **scout** runs one orchestrator that gathers context once (diff window, board
  snapshot, dedup index), then runs the security / correctness / completeness walks
  as parallel subagents feeding one shared dedup + filing pass. This kills the
  triple-paid discovery context, the largest avoidable cost.
- **Maker≠checker seams preserved:** rover/airlock stay separate cold sessions;
  flight-director (fleet editor) is checked by airlock's fleet-config rubric
  (fleet checker). These two seams are non-negotiable.

## 4. Flight-director

### Inputs

1. Airlock verdicts — `gatekeeper-verdict: BLOCK/PASS` comments, clustered by
   authoring loop and failure class.
2. Run outcomes — `.cache/experts-routines/logs/*` (failures, timeouts, early-exit ratio).
3. Cost feed — `.cache/experts-routines/costs.jsonl` (new; see §6).
4. `~/brain/fleet/lessons.md` — curated facts from telemetry.
5. Board state — inherited observatory duties.

### One run, three jobs, strict order

1. **Board hygiene** (acting, not report-only): close verified-stale agent-filed
   issues, fix labels, merge duplicates. Human-filed issues remain report-only.
2. **Fleet performance review:** per-loop scorecard — bounce rate, cost per useful
   outcome (per merged fix / per confirmed finding), early-exit ratio. One page to
   `~/brain/fleet/`.
3. **At most ONE improvement PR** — highest-leverage prompt/skill edit justified by
   a recurring pattern (≥2 occurrences). PR body must cite evidence (bounce/run
   links) and state the scorecard metric it expects to improve.

### Stop rules (load-bearing, given self-merge)

- **File allowlist:** `.claude/loops/*.prompt.md`, `.claude/skills/experts-*/SKILL.md`,
  `ops/fleet/contracts/*.md`. Never: its own `05-flight-director.*`, loop configs
  (`*.json`), `.github/**`, `.claude/agents/**`, runner/dispatch scripts.
  Enforced 3×: its prompt, airlock's rubric, and a CI path-guard job failing any
  `agent-generated` PR that touches outside the allowlist.
- **Rate limit:** one improvement PR per cycle, hard. Surplus findings go to
  lessons for next cycle.
- **Shrink bias:** prompt-growing edits must justify growth in the PR body;
  net-shrinking preferred; per-file token ceiling ≈ current size. (A self-editing
  loop's default failure mode is monotonic prompt growth.)
- **Auto-revert:** each FD PR records its target metric. Next cycle, if that loop's
  bounce rate or cost worsened, FD's one PR is the revert.
- **Two-strike escalation:** two self-reverts in the same area → third change in
  that area requires a human label (same mechanism as `routine-enable-approved`).

### Merge path

FD PRs flow through the normal pipeline: airlock reviews cold under the
fleet-config rubric (ex-overwatch checklist: tool-grant creep, guardrail deletion,
enable-flips, prompt-injection seams) and merges on PASS in a later run. FD never
merges its own PR. The verdict-run/merge-run delay is the human interception window.
Existing CI label gates (`routine-enable-approved`, `tool-grant-approved`) remain
the human backstop for the dangerous categories.

## 5. Telemetry (memory loop)

**Artifact:** `~/brain/fleet/lessons.md` — capped at ≤15 lines/section,
≤120 lines total; sections: `all-loops`, `scout`, `rover`, `airlock`,
`flight-director`.

**Sources (trust order):** airlock verdict comments → run logs → main-session
memory notes (the ~15 routine-relevant feedback notes seed the file) → brain
session notes.

**Discipline = curation, not collection:** per cycle, add ≤3 lessons; at section
cap, evict or merge — keep lessons that demonstrably stopped a recurring bounce,
drop ones that never fired.

**Write path:** direct commit/push to brain (telemetry already has brain push
access). No PRs on main for memory churn.

**Read-side brake:** the runner injects lessons into each loop's context at prompt
assembly and **hard-truncates to the cap** — a bloated file cannot bloat any
loop's context. The brake sits where the token cost lives.

**Human digest** continues as a one-page by-product into brain each cycle.

## 6. Cost plumbing & triggers

- **Cost capture (ships first):** runner parses the CLI's usage output and appends
  `{ts, loop, slot, model, input_tokens, output_tokens, cache_read, duration,
outcome}` to `.cache/experts-routines/costs.jsonl`. ~10 lines; no behavior change.
- **Preflight gates:** cron cadence stays, but `ops/fleet/preflight.sh` runs
  before any Claude session starts — zero tokens. Checks per loop as in §3.
  Quiet-day fleet cost ≈ a few `gh`/`git` calls.
- **Model policy unchanged:** orchestrators Sonnet, subagents per existing
  overrides. Savings come from not running, not from cheaper models (that lever is
  exhausted).

## 7. Repo layout & local/CCR isolation

```
.claude/loops/                  # WHAT — prompts only (like skills/, agents/)
  01-scout.prompt.md … 05-flight-director.prompt.md
  README.md                     # one-page index

ops/fleet/                      # HOW (local) — the only thing cron touches
  run-local.sh  pool-dispatch.sh  setup-worktrees.sh  crontab.txt  preflight.sh
  contracts/
    github-issues-contract.md  dedup-protocol.md

ops/fleet/ccr/                  # cloud mirror — optional, deletable as a unit
  *.trigger.json  index.json  sync.ts
```

**Isolation contract:**

- Prompts reference only `.claude/loops/` + `ops/fleet/contracts/` — pure "what."
- Local runner reads prompts + contracts, injects lessons from `~/brain`
  (truncated). Never reads `ops/fleet/ccr/`.
- CCR sync is a _consumer_ of the canonical prompts (inlines them into trigger
  configs via `sync.ts`) — never a second source of truth.
- Disabling remote = flip/delete `ops/fleet/ccr/`; local cron doesn't notice.

## 8. Git hygiene rule

**If it changes behavior → reviewed PR on main** (FD prompt edits, ≤1/week,
evidence-linked — auditable history for a self-modifying system).
**If it's memory or measurement → brain or cache** (lessons, scorecards, digests
→ `~/brain/fleet/`; costs/logs → `.cache/`, never committed).

## 9. Migration path (each step ships independently)

1. **Cost capture** in the current runner — start accumulating data now.
2. **Repo restructure** — `git mv` to §7 layout; update crontab paths; delete pulse.
   No prompt content changes.
3. **Merge discovery → scout** — the main prompt-engineering work; old
   sentinel/radar/salvage prompts are raw material.
4. **Preflight gates** — then re-enable scout/rover/airlock on new cadences
   (pipeline back to life, cheap on quiet days).
5. **Telemetry rewrite** — digest → memory consolidator; seed lessons.md from
   main-session memory notes; runner starts injecting lessons.
6. **Flight-director** — new prompt + airlock fleet-config rubric + CI path-guard.
   **Report-only for its first two cycles** (scorecard, no PR), then self-merge
   unlocks.

## 10. Verification & success criteria

- Per-step gates: `bash -n`, JSON parse, prose-link resolution; path-guard tested
  with a deliberate out-of-allowlist agent PR (must fail CI).
- After ~1 month, read off FD's own scorecard:
    - quiet-day cost ≈ preflight-only (cents);
    - bounce rate trending down (lessons file earning its keep);
    - zero allowlist escapes;
    - operator touches the fleet only at label gates + weekly scorecard.
- Kill switch unchanged: comment out the crontab; no daemon, no state to unwind.

## 11. Out of scope

- Feature/intent lane (spec→decompose→dispatch loop) — separate brainstorm later;
  FD's scorecard data will inform it.
- CCR re-enablement mechanics beyond keeping `ops/fleet/ccr/` syncable.
- Renaming on-disk worktree slot paths (`~/experts-wt/r3-slot*`) — operational,
  untouched.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
