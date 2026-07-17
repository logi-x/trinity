---
title: "lessons"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["tools"]
category: "tools"
source: "normalized"
source_id: "Tools/Fleet/lessons.md"
---
# Fleet lessons

Curated by telemetry (weekly). Caps: ≤15 lines/section, ≤120 total, one lesson per line.
Injected into every loop's context by ops/fleet/run-local.sh (all-loops + own section, first 40 lines).

## all-loops

- Re-emit EVERY `<!-- agent-fp/agent-class/collateral -->` marker on any `gh issue edit --body-file` — the edit replaces the whole body (evidence: contract §6)
- Collateral closes in PR bodies must be bare `Closes #N` lines — bold/backticks/links break the auto-close regex (evidence: #706)
- Raw SQL: verify column ownership against schema.prisma — `users` has no name column; display name is `profiles.full_name` (evidence: #947)
- Write issue/PR bodies to a temp file and pass `--body-file` — inline `--body` quoting breaks on backticks/newlines

## scout

- compose-v2 profile-gated services are invisible to `docker compose config` — that is proof opt-in works, not a finding (evidence: #865)
- Working-tree `docker/*/.env` files are gitignored deploy files — check `git ls-files` before flagging a committed secret (evidence: #865)
- zod `.url()` accepts `javascript:` scheme — flag href-rendered user URLs without a scheme regex as XSS (evidence: #909)

## rover

- Pair every adversarial/security fix with a happy-path test: enumerate every state that previously reached the changed code and succeeded (evidence: EXP-318)
- Deferred-path checks (verify/webhook/cron) must read signals snapshotted at initiation, never re-read mutable state at completion — TOCTOU (evidence: EXP-129)
- When fixing a route, fix its symmetric sibling (courses↔events↔subscriptions enroll/verify/webhook) in the same diff (evidence: EXP-129)
- Adding auth to a previously auth-less route breaks its success tests — add a happy-path session mock (evidence: #868)
- A new notify() key needs entries in BOTH email + chat registries plus a chat template, or tsc fails across notification.service.ts (evidence: #861)
- Index migrations: no CONCURRENTLY/INCLUDE — declare `@@index`, generate idempotent SQL via migrate diff, run db:check:drift (evidence: #860)
- Never run `npx prisma format` — it rewrites the whole 4.5k-line schema; hand-edit matching surrounding style (evidence: #857)
- When deleting a route/handler/wire-string, grep the VALUE (URLs, enum strings) not just the symbol — clients hardcode them (evidence: EXP-204)

## airlock

- Branch-staleness: files that landed on main after the PR branched show as regressions — diff against the merge-base before flagging (evidence: EXP-292 attempts)
- Squash-merge can land a stale head and drop a just-pushed commit — sentinel-verify origin/main content, never trust state=MERGED (evidence: #838)

## telemetry

- An append-only lessons file is the token problem reborn — evict before adding, always

## flight-director

- Prefer net-shrinking prompt edits; growth must be justified by a recurring bounce it prevents
