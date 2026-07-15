---
title: "2026-05-28 Experts Agent Digest"
date: "2026-05-28"
tags: [agent, digest, project/experts]
category: "daily"
source: "automation"
source_id: "Raw/sources/2026-05-28-experts-agent-digest.md"
---

# 2026-05-28 Experts Agent Digest

Window: 2026-05-27T00:00:00Z → 2026-05-28T23:59:59Z.

---

## New today

Issues created with agent fingerprints (`<!-- agent-fp:`) in the last 24h:

| # | Title | Status | Severity | FP | Created |
|---|-------|--------|----------|----|------|
| [EXP-145](https://linear.app/experts/issue/EXP-145) | [completeness] 4 routes recorded wrong bucket (R2_BUCKET_STATIC) while uploadPublicAsset() writes to R2_BUCKET_USER_UPLOADS | **Done** | High | `a833e0781a` | 2026-05-27 |
| [EXP-146](https://linear.app/experts/issue/EXP-146) | [bug] storage-janitor sweeps hardcode R2_BUCKET_USER_UPLOADS — ignore File.bucket | Backlog | Medium | `4f5c6023b9` | 2026-05-27 |
| [EXP-147](https://linear.app/experts/issue/EXP-147) | [bug] deleteFromR2 hardcodes R2_BUCKET_STATIC — wrong bucket for user-upload cover cleanup | Backlog | Medium | `33154b3f57` | 2026-05-27 |
| [EXP-150](https://linear.app/experts/issue/EXP-150) | [security] Gatekeeper collateral-close allows silent issue closure via PR magic words | Backlog | Medium | `c0773ce1e8` | 2026-05-27 |
| [EXP-151](https://linear.app/experts/issue/EXP-151) | [security] Routines 07/08 grant Bash+WebFetch to autonomous cron agents reading adversary-controlled content | Backlog | Medium | `9ad9431817` | 2026-05-27 |
| [EXP-152](https://linear.app/experts/issue/EXP-152) | [security] CRON_SECRET exposed in cron sidecar process arguments via curl -H Authorization | **Done** | Medium | `a672576f84` | 2026-05-27 |
| [EXP-153](https://linear.app/experts/issue/EXP-153) | [security] Stack trace unconditionally exposed in POST /notifications/read 500 response | **Done** | Medium | `4de176194b` | 2026-05-27 |
| [EXP-154](https://linear.app/experts/issue/EXP-154) | [security] Stack trace unconditionally exposed in POST+DELETE /follow 500 responses | **Done** | Medium | `b3683e1f8c` | 2026-05-27 |
| [EXP-155](https://linear.app/experts/issue/EXP-155) | [security] Stack trace AND error.message unconditionally exposed in GET+POST /content/views 500 responses | **Done** | Medium | `934996db87` | 2026-05-27 |
| [EXP-163](https://linear.app/experts/issue/EXP-163) | [spinoff: EXP-155] error.message unconditionally exposed in content-views stats route | Backlog | — | `d9f0b99eef` | 2026-05-28 |
| [EXP-164](https://linear.app/experts/issue/EXP-164) | [spinoff: EXP-155] error.message unconditionally exposed in content-views track route | Backlog | — | `d86d455719` | 2026-05-28 |
| [EXP-165](https://linear.app/experts/issue/EXP-165) | [spinoff: EXP-155] error.message unconditionally exposed in content-views batch route | Backlog | — | `f8bca258fd` | 2026-05-28 |
| [EXP-166](https://linear.app/experts/issue/EXP-166) | [spinoff: EXP-116] commissions/approve-pending route exposes raw error.message in 500 responses | Backlog | — | `c19c55c239` | 2026-05-28 |
| [EXP-167](https://linear.app/experts/issue/EXP-167) | [spinoff: EXP-152] Redis healthcheck exposes REDIS_PASSWORD in process arguments via redis-cli -a | **Done** | Medium | `4c90b482dd` | 2026-05-28 |
| [EXP-168](https://linear.app/experts/issue/EXP-168) | [security][sweep] Move all runtime secrets to Docker secrets — class-level fix following EXP-167 | **Done** | High | — | 2026-05-28 |
| [EXP-169](https://linear.app/experts/issue/EXP-169) | [bug] Prisma migration checksum drift blocks prisma migrate deploy on any env with EXP-118 applied | **Done** | High | `28f8a04400` | 2026-05-28 |
| [EXP-170](https://linear.app/experts/issue/EXP-170) | [bug] quizzes/attempts/submit leaks raw error.message in production via safeErrorJson publicMessage parameter | Backlog | Medium | `55d3c00efd` | 2026-05-28 |
| [EXP-171](https://linear.app/experts/issue/EXP-171) | [security] Unauthenticated diagnostic endpoint exposes Share table schema and sample record | Backlog | Medium | `7f7d070769` | 2026-05-28 |
| [EXP-173](https://linear.app/experts/issue/EXP-173) | [security] R9 routine has allow_unrestricted_git_push on brain without deployed server-side guard | Backlog | High | `b153a42096` | 2026-05-28 |
| [EXP-174](https://linear.app/experts/issue/EXP-174) | [security] IDOR in realtime sync endpoint — arbitrary post activity accessible via user-supplied channels | Backlog | Medium | `8ae9786514` | 2026-05-28 |
| [EXP-175](https://linear.app/experts/issue/EXP-175) | [bug] cron sidecar lost APP_BASE_URL after PR #566 removed env_file — all 8 cron tasks silently failing | Backlog | High | `468ada456745` | 2026-05-28 |
| [EXP-176](https://linear.app/experts/issue/EXP-176) | [security] CI set -a exports all bake-env credentials when EXPERTS_APP_DATABASE_URL absent | Backlog | Medium | `9ed3e9c5ca1e` | 2026-05-28 |
| [EXP-177](https://linear.app/experts/issue/EXP-177) | [bug] pgvector:pg16 mutable undigested image tag in production postgres service | Backlog | Medium | `7274890de478` | 2026-05-28 |

**23 new** agent-fp issues this window (EXP-172 cancelled as duplicate of EXP-170). 9 resolved same-day (EXP-145, EXP-152, EXP-153, EXP-154, EXP-155, EXP-167, EXP-116 from prior wave + EXP-168 via PR #577, EXP-169 operator-restored). 14 remain open.

---

## Repeated pattern

Findings appearing 3+ times in the last 30 days (from `Raw/agent-state/findings-index.md`):

| Pattern | Count | Linear IDs | Current state |
|---------|-------|------------|--------------|
| CRON_SECRET timing-unsafe / fail-open on cron routes | 7 | EXP-111, EXP-112, EXP-114, EXP-115, EXP-116, EXP-119, EXP-133 | 5 resolved today; EXP-133 in-review; fully closed as a class with PR #565 |
| Error disclosure (stack trace / error.message in 500 responses) | 8 | EXP-132, EXP-153, EXP-154, EXP-155, EXP-163, EXP-164, EXP-165, EXP-166 | EXP-132/153/154/155 resolved; class eliminated by PR #557 ESLint rule; EXP-163/164/165/166 remain as pre-existing spinoffs |
| R2 storage bucket mismatch (write path ≠ URL origin) | 4 | EXP-134, EXP-145, EXP-146, EXP-147 | EXP-145 resolved (PR #529); EXP-134, EXP-146, EXP-147 still open |
| Prompt injection via Bash grants in agent/routine definitions | 3 | EXP-143, EXP-151, EXP-173 | All open; EXP-143 (agents), EXP-151 (routines 07/08), EXP-173 (R9) |

---

## Resolved since yesterday

Linear issues flipped to Done / resolved in the last 24h:

| # | Title | Merged via | Resolved at |
|---|-------|-----------|------------|
| EXP-114 | storage-janitor/sweep CRON_SECRET plain !== (stale-skip) | already fixed PR #513 | 2026-05-28 (stale-closed) |
| EXP-115 | ai/embeddings/sync CRON_SECRET plain !== (stale-skip) | already fixed PR #522 | 2026-05-28 (stale-closed) |
| EXP-116 | admin cron routes fail-open when CRON_SECRET unset | PR #565 | 2026-05-28T04:24Z |
| EXP-145 | 4 routes recorded wrong bucket in File.bucket | PR #529 | 2026-05-27 |
| EXP-152 | CRON_SECRET exposed in cron sidecar process args | PR #566 | 2026-05-28T04:24Z |
| EXP-153 | Stack trace in notifications/read 500 response | PR #551 | 2026-05-28T00:58Z |
| EXP-154 | Stack trace in follow/unfollow 500 responses | PR #552 | 2026-05-28T00:58Z |
| EXP-155 | Stack trace + error.message in content-views 500 responses | PR #556 | 2026-05-28T00:58Z |
| EXP-158 | brain-agent-push-guard documentation | PR #549 | 2026-05-27T23:49Z |
| EXP-159 | Tool-grant CI alert + label gate workflow | PR #548 | 2026-05-27T23:46Z |
| EXP-160 | R7/R8 enable-gate CI workflow | PR #546 | 2026-05-27 |
| EXP-162 | R9 routines-auditor subagent | PR #547 | 2026-05-27T23:43Z |
| EXP-167 | Redis healthcheck password argv exposure | PR #568 | 2026-05-28T06:13Z |
| EXP-168 | Docker secrets sweep — all runtime secrets moved to Docker secrets | PR #577 | 2026-05-28T20:20Z |
| EXP-169 | Prisma migration checksum drift — deployment blocker | operator-restored original migration files | 2026-05-28 |

15 resolved this window. EXP-114 and EXP-115 were stale-closed (underlying code fixed earlier by PRs #513 and #522 respectively).

---

## In-flight fixes

Agent-opened issues currently In Progress or In Review:

| # | Title | Opened | Status |
|---|-------|--------|-------|
| EXP-120 | Missing auth unit tests for cron routes | 2026-05-25 | In Review (targeted verification: 15 tests passed via PR #513) |
| EXP-133 | orphan-sweep CRON_SECRET timing-unsafe + fail-open | 2026-05-26 | In Review (resolved by PR #513; Linear moved to In Review) |

---

## Merged PRs

29 PRs merged in window 2026-05-27T00:00:00Z → 2026-05-28T23:59:59Z:

| PR | Title | Linear | Merged |
|----|-------|--------|-------|
| [#513](https://github.com/logi-x/experts/pull/513) | fix(storage): timing-safe CRON_SECRET on sweep+orphan routes [attempt 2] | EXP-112, EXP-133 | 2026-05-27 |
| [#517](https://github.com/logi-x/experts/pull/517) | fix(storage): storage alerts use real tier quotas | EXP-117 | 2026-05-27 |
| [#518](https://github.com/logi-x/experts/pull/518) | fix(storage): reapR2Orphans pagination cursor | EXP-125 | 2026-05-27 |
| [#519](https://github.com/logi-x/experts/pull/519) | fix(storage): admin storage metrics LIMIT clause | EXP-126 | 2026-05-27 |
| [#522](https://github.com/logi-x/experts/pull/522) | fix(auth): CRON_SECRET timing-safe length-leak [attempt 3] | EXP-119 | 2026-05-27 |
| [#523](https://github.com/logi-x/experts/pull/523) | fix(storage): StorageAlert serializable tx + @unique | EXP-118 | 2026-05-27 |
| [#525](https://github.com/logi-x/experts/pull/525) | fix(storage): video DELETE DB-first before R2 | EXP-131 | 2026-05-27 |
| [#526](https://github.com/logi-x/experts/pull/526) | fix(storage): video upload+delete ledger asymmetry | EXP-130 | 2026-05-27 |
| [#529](https://github.com/logi-x/experts/pull/529) | fix(storage): 4 routes wrong bucket in File.bucket | EXP-145 | 2026-05-27 |
| [#538](https://github.com/logi-x/experts/pull/538) | fix(api): stack trace guard in video route 500 responses | EXP-132 | 2026-05-27 |
| [#546](https://github.com/logi-x/experts/pull/546) | ci(routines): R7/R8 enable-gate workflow | EXP-160 | 2026-05-27 |
| [#547](https://github.com/logi-x/experts/pull/547) | feat(routines): R9 routines-auditor subagent | EXP-162 | 2026-05-27T23:43Z |
| [#548](https://github.com/logi-x/experts/pull/548) | ci(agents): tool-grant alert + label gate workflow | EXP-159 | 2026-05-27T23:46Z |
| [#549](https://github.com/logi-x/experts/pull/549) | docs(security): brain-agent-push-guard reference | EXP-158 | 2026-05-27T23:49Z |
| [#550](https://github.com/logi-x/experts/pull/550) | feat(routines): set agent identity before brain commit | EXP-158 followup | 2026-05-28T00:23Z |
| [#551](https://github.com/logi-x/experts/pull/551) | fix(api): guard stack trace in notifications/read | EXP-153 | 2026-05-28T00:58Z |
| [#552](https://github.com/logi-x/experts/pull/552) | fix(api): guard stack trace in follow/unfollow route | EXP-154 | 2026-05-28T00:58Z |
| [#556](https://github.com/logi-x/experts/pull/556) | fix(api): guard stack trace + error.message in content-views | EXP-155 | 2026-05-28T00:58Z |
| [#557](https://github.com/logi-x/experts/pull/557) | feat(api): safeErrorJson helper + ESLint no-error-stack rule | EXP-132/153/154/155 class fix | 2026-05-28T01:14Z |
| [#558](https://github.com/logi-x/experts/pull/558) | fix(errors): safeErrorJson evaluates APP_ENV per-call | regression fix | 2026-05-28T01:25Z |
| [#559](https://github.com/logi-x/experts/pull/559) | chore(routines): R1 cost reduction — Haiku flip + context hygiene | — | 2026-05-28T02:01Z |
| [#560](https://github.com/logi-x/experts/pull/560) | chore(routines): R2 cost reduction — brain-first dedup | — | 2026-05-28T02:10Z |
| [#561](https://github.com/logi-x/experts/pull/561) | chore(routines): R5 cost reduction — frequency drop 24→3/day | — | 2026-05-28T02:21Z |
| [#562](https://github.com/logi-x/experts/pull/562) | chore(routines): R3/R4/R6 context hygiene | — | 2026-05-28T02:32Z |
| [#563](https://github.com/logi-x/experts/pull/563) | chore(routines): R7/R8/R9 cost reduction + repo↔cloud reconciliation | — | 2026-05-28T03:50Z |
| [#565](https://github.com/logi-x/experts/pull/565) | fix(auth): admin cron routes fail-closed when CRON_SECRET unset | EXP-116 | 2026-05-28T04:24Z |
| [#566](https://github.com/logi-x/experts/pull/566) | fix(docker): hide CRON_SECRET from cron sidecar process args | EXP-152 | 2026-05-28T04:24Z |
| [#568](https://github.com/logi-x/experts/pull/568) | fix(docker): avoid redis password argv exposure in healthcheck | EXP-167 | 2026-05-28T06:13Z |
| [#577](https://github.com/logi-x/experts/pull/577) | fix(docker): move all runtime secrets to Docker secrets — prod + staging | EXP-168 | 2026-05-28T20:20Z |

**Semver signal: PATCH.** All merges are security hardening, bug fixes, infra hardening, and internal tooling. No new user-facing API surface, no breaking schema changes in the primary app. The `safeErrorJson` helper (PR #557) is internal-only. PR #577 completes the Docker secrets migration class.

**Migration note:** PR #523 adds a `@unique` constraint for `StorageAlert`. Run `prisma migrate deploy` before starting the service. Verify `CRON_SECRET` is set before deploying PRs #565/566/568/577 — all now fail-closed. PRs #566/568/577 require container restarts after deploying the new Docker secrets configuration.

---

## Migrations / env / infra changes

- **No new Prisma schema migrations in this window** beyond PR #523 (StorageAlert @unique, merged 2026-05-27).
- **Docker Compose** — four hardening changes: (1) PR #568: Redis healthcheck uses `REDISCLI_AUTH` env var, no `-a` arg; startup no longer passes `--requirepass` on argv. (2) PR #566: CRON_SECRET written to `/run/curl-auth.conf` at startup (mode 0600) and referenced via `--config`; never appears in curl process args. (3) PR #565: admin cron routes fail-closed when `CRON_SECRET` unset. (4) PR #577: all remaining runtime secrets (database credentials, Redis password) moved to Docker secrets (tmpfs-mounted); `env_file: .env` fully removed from all production and staging services.
- **`.github/workflows/`** — two new workflows added: `tool-grant-alert.yml` (EXP-159, PR #548), `routine-enable-gate.yml` (EXP-160, PR #546).
- **`.claude/agents/`** — R1-R9 model flips: `architecture-reviewer`, `dependency-auditor`, `codebase-completeness-auditor`, `linear-board-auditor`, `routines-auditor` → Haiku. New `routines-auditor.md` added (EXP-162). `security-auditor.md` WebSearch cap added.
- **`.claude/routines/`** — R1-R9 context hygiene + cost reduction. R5 frequency: 24/day → 3/day. New `09-routines-audit.{json,prompt.md}` added. R3 cron aligned: `0 7 * * *` → `0 10/12 * * *`.
- **pnpm** — `--frozen-lockfile` removed from install commands; `.env` file copying logic added for Prisma `db:generate` in CI.

---

## Architectural notes

1. **`safeErrorJson` eliminates error.stack disclosure class by construction** (PR #557): An ESLint `no-restricted-syntax` rule scoped to `app/api/**/route.{ts,tsx}` now blocks `(error|err|e).stack` at CI. Eight routes swept. The bug class (EXP-132, EXP-153, EXP-154, EXP-155 and their spinoffs) is now structurally unrepresentable. New `src/lib/errors/api-error.ts` is a load-bearing module; must be treated as such in dependency review. **Decision-Log row added.**

2. **Gatekeeper (R5) frequency reduced 8×** (PR #561): From 24/day to 3/day. Average merge latency increases from ~30min to ~4hr. `gatekeeper-merge-now` label retained for human-bypass. **~85% cost reduction.** Decision-Log row added.

3. **Tool-grant CI gate** (PR #548, EXP-159): PRs touching `.claude/agents/**` or `.claude/routines/*.json` now block CI until human-applied `tool-grant-approved` label is present. This is the structural enforcement for the agent-Bash-grant invariant from 2026-05-26 Decision-Log. **Decision-Log row added.**

4. **R9 routines-auditor — meta-routine with unresolved push risk** (PR #547, EXP-173): New routine audits agent definitions for 6 security drift rules. Agent scoped to read-only (no Bash/Write/Edit/WebFetch). However, R9 was added with `allow_unrestricted_git_push: true` on brain before a server-side guard is deployed — the R9 PR itself was flagged as EXP-173 by a concurrent R3 run. **EXP-158 (brain-agent-push-guard) was closed as documentation only**; actual enforcement lives in a brain-side workflow that must be operator-deployed.

5. **EXP-169 resolved via operator restore** (2026-05-28): Commit `02266b32` squashed two already-applied migrations in-place. Any environment that ran EXP-118 would fail `prisma migrate deploy` with P3005/P3006 checksum drift. Operator restored original migration file contents. **Applied migrations must never be mutated in-place — Decision-Log row added.**

---

## Docs that need updating

- **brain storage architecture** — EXP-134, EXP-146, EXP-147 still open. Any existing storage architecture doc describing R2 write paths may be stale post-EXP-77 split.
- **`.claude/agents/` security guide** — EXP-143, EXP-151, EXP-173 all open. Once resolved, the agent definitions guide should document the read-only Bash constraint and the new tool-grant CI gate.
- **ZATCA configuration** — EXP-140/EXP-142 open. Brain vault ZATCA setup guide should note the DEBUG_ZATCA guard requirement and APP_ENV production guard for force-fail flags.
- **Prisma migration workflow** — EXP-169 resolved but guide should document that applied migrations must never be squashed or mutated in-place; only additive migrations are safe.

---

## Still open

Open agent-filed issues not addressed today:

| # | Title | Severity | Age | Status |
|---|-------|----------|-----|-------|
| EXP-122 | Stale reservation opens quota-bypass window | Medium | 3d | open |
| EXP-124 | Storage reservation DELETE lacks user_id ownership check | Medium | 3d | open |
| EXP-127 | hashtext() advisory lock int32 birthday collision at ~55k users | Medium | 3d | open |
| EXP-129 | Tabby verify/webhook paths bypass KSA geo-restriction | High | 3d | open |
| EXP-134 | R2_BUCKET_STATIC write target misaligned with R2_USER_UPLOADS_PUBLIC_URL | High | 2d | open |
| EXP-135 | R2_BUCKET_CERTIFICATIONS missing from .env.example | High | 2d | open |
| EXP-140 | ZATCA debug event name mismatch — gov API responses via DEBUG=true | Medium | 2d | open |
| EXP-141 | R2 + Redis credentials committed in plaintext to git history | **Critical** | 2d | open — rotate immediately |
| EXP-142 | ZATCA_FORCE flags lack APP_ENV!=production guard | Medium | 2d | open |
| EXP-143 | .claude/agents Bash grant — indirect prompt injection path | Medium | 2d | open |
| EXP-146 | storage-janitor sweeps hardcode R2_BUCKET_USER_UPLOADS, ignore File.bucket | Medium | 1d | open |
| EXP-147 | deleteFromR2 hardcodes R2_BUCKET_STATIC — wrong bucket for cover cleanup | Medium | 1d | open |
| EXP-150 | Gatekeeper collateral-close allows silent Linear issue closure | Medium | 1d | open |
| EXP-151 | Routines 07/08 grant Bash+WebFetch to autonomous agents | Medium | 1d | open |
| EXP-163 | content-views stats error.message exposed | — | <1d | Backlog |
| EXP-164 | content-views track error.message exposed | — | <1d | Backlog |
| EXP-165 | content-views batch error.message exposed | — | <1d | Backlog |
| EXP-166 | commissions route error.message exposed | — | <1d | Backlog |
| EXP-170 | quiz submit error.message via safeErrorJson publicMessage | Medium | <1d | Backlog |
| EXP-171 | Unauthenticated diagnostic endpoint (Share table) | Medium | <1d | Backlog |
| EXP-173 | R9 allow_unrestricted_git_push on brain without server-side guard | High | <1d | Backlog |
| EXP-174 | IDOR in realtime sync endpoint | Medium | <1d | Backlog |
| EXP-175 | cron sidecar lost APP_BASE_URL — all 8 cron tasks silently failing | **High** | <1d | Backlog |
| EXP-176 | CI set -a exports all bake-env credentials | Medium | <1d | Backlog |
| EXP-177 | pgvector:pg16 mutable undigested image tag in production postgres | Medium | <1d | Backlog |

---

## Needs human attention

Items appearing in 3+ consecutive digests still open/in-review, plus critical/blocked escalations:

1. **Traefik CSP removal — 8th consecutive digest.** `proxy.ts` is the sole authoritative CSP source since 2026-05-22 (Decision-Log 2026-05-22). Traefik `headers.contentSecurityPolicy` must be removed as the capstone step. No PR open. Due 2026-06-01. Action-Tracker row from 2026-05-22 remains Open.

2. **EXP-141 — CRITICAL: credentials in git history (2nd digest).** `docker/workers/docker-compose.yml` was deleted but R2 API token, R2 secret key, and Redis password remain in the git object store. Must rotate immediately regardless of EXP-141 fix status.

3. **EXP-103 — 4th consecutive digest** (2026-05-24, 25, 26, 28). 5 upload routes still bypass `enforceStorageQuota`. End-to-end quota enforcement is incomplete.

4. **EXP-83 — 5th consecutive digest** (2026-05-23, 24, 25, 26, 28). `course_assets` VALIDATE constraint (NULL `attachment_id` + NULL `url` rows allowed). No PR open.

5. **EXP-127 — 3rd digest** (2026-05-25, 26, 28). hashtext() advisory lock birthday collision at ~55k users. Storage ledger correctness at scale depends on fixing this.

6. **EXP-129 — 3rd digest** (2026-05-25, 26, 28). Tabby `verify`/`webhook` bypass KSA geo-restriction. Forged payment completions from non-KSA origins still possible.

7. **EXP-175 — URGENT: all cron tasks silently failing (new today).** PR #566 removed `env_file: .env` from the cron sidecar without migrating `APP_BASE_URL` to the explicit `environment:` block. All 8 cron tasks that call internal routes silently fail (curl target evaluates to a malformed URL). Must patch in `docker/production/docker-compose.yml` and `docker/staging/docker-compose.yml`. Due 2026-05-29.

---

## Subagent outputs

### release-manager

**Semver recommendation: PATCH.** 29 merged PRs — all security hardening, bug fixes, infra hardening, and internal tooling. No new user-facing API surface, no breaking schema changes in the primary app. The `safeErrorJson` helper (PR #557) is internal-only.

**Migration notes:** (1) PR #523 adds `@unique` on StorageAlert — `prisma migrate deploy` required before service start. (2) PRs #565/566/568/577 require container restarts. (3) `CRON_SECRET` must be set in all environments — all admin and internal cron routes now fail-closed if unset.

**Branch hygiene:** 14 of 28 PRs merged on 2026-05-27 in a burst (backlog clearance). PRs #551/552/556 merged at same timestamp — confirm CI ran independently. PR #558 (regression) follows PR #557 by 11 minutes; treat as single logical unit in release notes.

**Next MINOR candidates:** EXP-103 close (quota enforced on all upload routes); any new public API endpoint.

### architecture-reviewer

Four new Decision-Log rows warranted. See "Architectural notes" section above.

Key concerns: (1) `safeErrorJson` is now a load-bearing module. (2) EXP-173 (R9 push grant without server-side guard) is the most urgent open item — the tool-grant CI gate does not retroactively protect already-merged agent configs. (3) EXP-175 is the most urgent operational item — all cron tasks failing since PR #566 deploy. (4) Storage bucket mismatch (EXP-146/147) still relies on implicit coupling.

---

## Statistics

| Metric | Count |
|--------|------|
| New agent-fp issues | 23 (22 new + 1 cancelled duplicate EXP-172) |
| Resolved same-day (new) | 9 (EXP-145, EXP-152, EXP-153, EXP-154, EXP-155, EXP-167, EXP-116 + EXP-168, EXP-169) |
| Carry-forward resolved this window | 6 (EXP-114 stale, EXP-115 stale, EXP-158, EXP-159, EXP-160, EXP-162) |
| **Total resolved this window** | **15** |
| In-flight (In Review / Todo) | 2 (EXP-120, EXP-133) |
| **Merged PRs** | **29** |
| New Decision-Log rows | 4 |
| **Needs human attention** | **7** (Traefik CSP, EXP-141, EXP-103, EXP-83, EXP-127, EXP-129, EXP-175) |

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
