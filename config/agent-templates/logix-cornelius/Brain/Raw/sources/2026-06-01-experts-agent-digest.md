---
title: "2026-06-01 Experts Agent Digest"
date: "2026-06-01"
tags: [agent, digest, project/experts]
category: "daily"
source: "automation"
source_id: "Raw/sources/2026-06-01-experts-agent-digest.md"
---

# Experts Agent Digest — 01 June 2026

**Window:** 2026-06-01T00:00:00Z → 2026-06-01T23:59:59Z  
**Prior digest:** [[Raw/sources/2026-05-31-experts-agent-digest.md]]

---

## Summary Table

| Metric | Count |
|--------|-------|
| New agent-fp issues (today) | 17 |
| Resolved since yesterday | 9 |
| In-flight fixes (PR open / in review) | 3 |
| Merged PRs | 10 |
| Needs human attention | 8 |

---

## New Today

Issues opened by routines (body contains `<!-- agent-fp:`):

| Issue | Title | FP | Severity | Status |
|-------|-------|-----|----------|---------|
| [EXP-245](https://linear.app/experts/issue/EXP-245) | [bug] Upload route masks DB connection errors as 403 Forbidden | `4a1c9e7d2b8f` (R3) | **High** | Done (same-day) |
| [EXP-246](https://linear.app/experts/issue/EXP-246) | [infra] Postgres has no persistent data volume in any env — container recreate wipes the database | `7c2e5a91d4f0` (R3) | **Urgent** | Done (same-day) |
| [EXP-247](https://linear.app/experts/issue/EXP-247) | [db] storage_alerts UNIQUE(userId) never reached prod — migration edited in place + add CI immutability guard | `9f3b6c1e80a2` (R3) | **High** | Done (same-day) |
| [EXP-248](https://linear.app/experts/issue/EXP-248) | [db] snake_case storage_alerts.userId → user_id (lone unmapped userId column) | `c41d8e2b7a90` (R3) | **Low** | Done (same-day) |
| [EXP-250](https://linear.app/experts/issue/EXP-250) | [completeness] R2_API_TOKEN env defined but no caller reads it | `b509d8df0101` (R7) | **Low** | Todo |
| [EXP-251](https://linear.app/experts/issue/EXP-251) | [bug] pg18 volume-path flip + deleted migration guide — production data loss on next deploy | `f1b51da1e291` (R3) | **Critical** | Backlog |
| [EXP-252](https://linear.app/experts/issue/EXP-252) | [bug] persistAskAiExchange soft-delete re-check has no FOR UPDATE lock — TOCTOU race | `5f9fdc5505e8` (R3) | **High** | Backlog |
| [EXP-253](https://linear.app/experts/issue/EXP-253) | [bug] community posts DELETE handler missing UUID guard — Prisma P2023 → 500 | `2e356038195a` (R3) | **High** | Backlog |
| [EXP-254](https://linear.app/experts/issue/EXP-254) | [security] GET /community/posts/[id] returns draft posts — missing isPublished filter | `edb9dfa6147f` (R3) | **High** | Backlog |
| [EXP-256](https://linear.app/experts/issue/EXP-256) | [bug] Migration 000000 raw DELETE references hardcoded "userId" column — fails if column pre-renamed | `a255a6272d63` (R3) | **Medium** | Backlog |
| [EXP-257](https://linear.app/experts/issue/EXP-257) | [spinoff: EXP-242] Community posts GET: totalPages incoherent for in-memory sorts beyond 500-post cap | `287cf4064d7b` (R3) | **High** | Backlog |
| [EXP-258](https://linear.app/experts/issue/EXP-258) | [spinoff: EXP-242] Community posts GET: unbounded search string allows large ILIKE pattern DoS | `43a31eb41924` (R3) | **High** | Backlog |
| [EXP-259](https://linear.app/experts/issue/EXP-259) | [spinoff: EXP-242] Community posts GET: unknown sort value silently returns undefined-order results | `9cdb1de81b76` (R3) | **High** | Backlog |
| [EXP-260](https://linear.app/experts/issue/EXP-260) | [security] realtime container has no memory limit — WebSocket exhaustion causes host OOM | `a8c3c745818c` (R3) | **Medium** | Backlog |
| [EXP-261](https://linear.app/experts/issue/EXP-261) | [security] migration-immutability CI guard bypassed by direct push to main | `72edaca4cf46` (R3) | **Medium** | Backlog |
| [EXP-262](https://linear.app/experts/issue/EXP-262) | [security] no per-user WebSocket connection cap — authenticated Redis exhaustion DoS | `b5781cc27ee7` (R3) | **Medium** | Backlog |
| [EXP-263](https://linear.app/experts/issue/EXP-263) | [spinoff: EXP-242] totalPages uncapped for in-memory sorts — clients receive unreachable page numbers | `5aba1482` (R5) | **High** | Backlog |

> Note: EXP-249 (pg18 tracking issue, no agent-fp) and EXP-255 (uid 1001 vs 1000 incident report, no agent-fp) were also created today but are not agent-fp issues.  
> Note: EXP-257 and EXP-263 address the same root cause (totalPages miscalculation) from R3 and R5 scanner passes respectively; fix together.

---

## Repeated Pattern

From `Raw/agent-state/findings-index.md` — files/symbols appearing 3+ times in last 30 days:

| Pattern | Occurrences (30d) | State |
|---------|------------------|-------|
| `apps/experts-app/app/api/v1/community/posts/route.ts` | **6 open issues** (EXP-242, 243, 257, 258, 259, 263) | EXP-242 in-review PR #738; 5 spinoffs in Backlog. Highest-density open-issue file in the codebase. |
| **JWT role-staleness** (`session.user.isAdmin` without DB re-derivation) | 15+ instances | EXP-241 (community PUT) still open. Structural fix deferred (Decision-Log 2026-05-29). Community domain now affected alongside courses and events. |
| **Cron secret timing-unsafe compare** (plain `!==` instead of `timingSafeEqual`) | 8 issues (EXP-111, 112, 114, 115, 116, 119, 120, 133) | EXP-120 + EXP-133 in-review; 6 others open. |
| **Docker container no resource limits** (`mem_limit`/`cpus` missing) | 3 issues (EXP-141 Next.js app, EXP-177 Postgres, EXP-260 realtime) | All open; EXP-260 new today. |
| **`persistAskAiExchange` / `ask-ai-assistant.ts`** | 4 issues (EXP-232, 237, 244, 252) | All open; EXP-252 new today adds a TOCTOU race on top of the verbatim-history class. |

---

## Resolved Since Yesterday

| Issue | Resolved By | Notes |
|-------|-------------|-------|
| [EXP-233](https://linear.app/experts/issue/EXP-233) | PR #729 | BOLA: quiz DELETE global isInstructor (filed 2026-05-31) |
| [EXP-234](https://linear.app/experts/issue/EXP-234) | PR #732 | Instructor re-submits approved course resets admin approval (filed 2026-05-31) |
| [EXP-238](https://linear.app/experts/issue/EXP-238) | PR #733 | Lesson video DELETE no userId filter on attachment lookup (filed 2026-05-31) |
| [EXP-245](https://linear.app/experts/issue/EXP-245) | PR #712 | Upload masks DB connection errors as 403 — same-day open+close |
| [EXP-246](https://linear.app/experts/issue/EXP-246) | PR #715 | Postgres no persistent data volume in any env — same-day open+close |
| [EXP-247](https://linear.app/experts/issue/EXP-247) | PR #717 | storage_alerts UNIQUE never reached prod + CI immutability guard — same-day open+close |
| [EXP-248](https://linear.app/experts/issue/EXP-248) | PR #719 | snake_case storage_alerts.userId → user_id — same-day open+close |
| [EXP-249](https://linear.app/experts/issue/EXP-249) | PR #724 | pg18 + parent volume mount tracking issue — same-day open+close |
| [EXP-255](https://linear.app/experts/issue/EXP-255) | PR #731 | realtime uid 1001 vs 1000 Docker secrets mismatch — same-day open+close |

**9 resolved** this window. Six were same-day open+close cycles. EXP-233/234/238 were filed yesterday and resolved today by merged PRs.

---

## In-Flight Fixes

| Issue | Title | PR | Status |
|-------|-------|----|--------|
| [EXP-242](https://linear.app/experts/issue/EXP-242) | community GET unbounded findMany popular/discussed | PR #738 | In Review — awaiting gatekeeper |
| [EXP-120](https://linear.app/experts/issue/EXP-120) | CRON_SECRET timing-safe compare skips check when secret is undefined | — | In Review |
| [EXP-133](https://linear.app/experts/issue/EXP-133) | CRON_AUTH_TOKEN timing-safe compare skips check on undefined | — | In Review |

---

## Merged PRs

| PR | Title | Closes | Merged |
|----|-------|--------|--------|
| [#712](https://github.com/logi-x/experts/pull/712) | fix(upload): stop masking DB connection errors as 403 Forbidden | EXP-245 | 02:44Z |
| [#714](https://github.com/logi-x/experts/pull/714) | chore(staging): pin postgres to pg16 (match prod) + digest-pin redis/alpine | — | 02:44Z |
| [#715](https://github.com/logi-x/experts/pull/715) | fix(infra): add persistent data volume to Postgres in all envs | EXP-246 | 02:44Z |
| [#717](https://github.com/logi-x/experts/pull/717) | fix(db): converge storage_alerts UNIQUE(userId) + CI migration-immutability guard | EXP-247 | 04:58Z |
| [#719](https://github.com/logi-x/experts/pull/719) | fix(db): snake_case storage_alerts.userId → user_id (additive follow-up to #717) | EXP-248 | 07:14Z |
| [#724](https://github.com/logi-x/experts/pull/724) | infra(docker): pg18 + parent volume mount across all envs (prod pg16→pg18 bump) | EXP-249 | 08:01Z |
| [#729](https://github.com/logi-x/experts/pull/729) | fix(courses): add assertCourseWriteAccess to quiz DELETE handler | EXP-233 | 19:36Z |
| [#731](https://github.com/logi-x/experts/pull/731) | fix(realtime): run as node uid 1000 so it can read Docker secrets (EXP-255) | EXP-255 | 21:01Z |
| [#732](https://github.com/logi-x/experts/pull/732) | fix(courses): guard against re-submission of approved courses | EXP-234 | 21:39Z |
| [#733](https://github.com/logi-x/experts/pull/733) | fix(courses): scope lesson video DELETE attachment lookup to requesting user | EXP-238 | 21:39Z |

**Semver: PATCH** — all PRs are security/bug fixes or infra corrections; no new user-facing behaviour.  
Operator actions required before next deploy:
1. **EXP-251 BLOCKER**: Verify Postgres volume path after PR #724 — take `pg_dump` before any `docker compose up`.
2. Confirm migration `20260601000000_storage_alerts_enforce_unique_user` applies cleanly (EXP-256: raw SQL uses `"userId"` but column renamed to `user_id` by PR #719).

---

## Migrations / Env / Infra Changes

**New migration landed today:**  
`prisma/migrations/20260601000000_storage_alerts_enforce_unique_user/migration.sql` — adds `UNIQUE(userId)` constraint on `storage_alerts`. ⚠️ EXP-256: the raw SQL `DELETE` in this migration hardcodes `"userId"` (Prisma model field name); the column is simultaneously being renamed to `user_id` (snake_case) by PR #719. Environments applying in a specific order may fail with column-not-found.

**Persistent Postgres volumes (PRs #715, #724):**  
PR #715 added named Docker volumes for Postgres in all three environments (production, staging, dev). Postgres PGDATA was previously in the container's ephemeral writable layer — any container recreate or image pull would destroy data.  
PR #724 then upgraded all envs from pg16 to pg18 and changed the volume mount path from `/var/lib/postgresql/data` to `/var/lib/postgresql`. ⚠️ EXP-251: this path change means Postgres will initialise a fresh empty cluster on first start, silently discarding all data in the old volume. `POSTGRES-VOLUME-MIGRATION.md` was also deleted.

**Staging version alignment (PR #714):**  
Pinned staging Postgres to `pg16` to match production (staging was floating on a mutable tag). Digest-pinned `redis:7.2-alpine` in staging.

**Realtime service UID fix (PR #731):**  
Changed `experts-realtime` container user from `realtime` (uid 1001) to `node` (uid 1000). Docker bind-mounted secrets are owned by uid 1000; uid 1001 was silently falling back to `redis://127.0.0.1:6379`, causing staging WebSocket/presence degradation.

---

## Architectural Notes

### 1. community/posts/route.ts: 6 open issues — highest-density file in codebase

`apps/experts-app/app/api/v1/community/posts/route.ts` generated 4 new spinoffs today (EXP-257, EXP-258, EXP-259, EXP-263) on top of the existing EXP-242 (in-review PR #738) and EXP-243. Six distinct open issues against one endpoint in < 24h:
- `take:undefined` for popular/discussed sort (EXP-242, in-review)
- user-supplied `limit` uncapped on recent sort (EXP-243)
- `totalPages` incoherent for in-memory sorts (EXP-257 + EXP-263, two scanner hits)
- unbounded `search` ILIKE DoS (EXP-258)
- missing `sort` enum validation (EXP-259)

All five remaining spinoffs should be bundled with PR #738 before merge.

### 2. pg18 volume-path regression (EXP-251) — production data-loss risk

PR #724 introduced a two-part regression: (1) volume mount path changed from `/var/lib/postgresql/data` to `/var/lib/postgresql`, causing Postgres to initialise a fresh empty cluster inside the mounted volume; (2) `POSTGRES-VOLUME-MIGRATION.md` deleted, removing the operator runbook. This is the third critical infra regression in 30 days (after EXP-101 public DB ports, EXP-175 missing cron APP_BASE_URL). EXP-251 calls for blocking the deploy and taking a verified `pg_dump` before any container recreate.

### 3. Dual migration CI guard now fully deployed (PRs #681 + #717)

- **Layer 1 (PR #681)**: shadow-DB drift check — `prisma migrate diff` exits 1 on schema↔migration drift (EXP-220 class)
- **Layer 2 (PR #717)**: immutability check — fails any PR that modifies, renames, or deletes an applied migration file (EXP-169/EXP-247 class)

Caveat: EXP-261 (new today) flags that Layer 2 only runs on `pull_request` events, not on `push` to main. Direct commits bypass it entirely.

### 4. WebSocket resource governance gap (EXP-260, EXP-262)

Two security issues filed today against `apps/experts-realtime/`:
- **EXP-262**: No per-user WS connection cap. `incrWsConnectionCount` in `presence-redis.ts` tracks connections but the `server.ts` upgrade handler never enforces a ceiling. Combined with a 24h WS JWT TTL, an authenticated user can exhaust Redis connection pool slots for all users.
- **EXP-260**: No `mem_limit` or `cpus` on any realtime container compose definition. Unauthenticated WS flood can OOM the host, taking down co-located services.

These define a missing resource-governance layer for the realtime service. See new Decision-Log row.

### 5. Upload error semantics corrected (PR #712)

Upload routes now return `503 Service Unavailable + Retry-After: 5` on Prisma transient connection errors (P1001/P1002/P1008/P1017) rather than silently returning 403 Forbidden. Corrects a semantic confusion that made DB outages appear as permission errors to clients and in monitoring.

---

## Docs That Need Updating

| File | Required update |
|------|----------------|
| `POSTGRES-VOLUME-MIGRATION.md` (deleted in PR #724) | Restore or replace with pg16→pg18 upgrade guide including volume-path migration steps |
| `apps/experts-app/prisma/CONTRIBUTING.md` or migration guide | Add rule: raw SQL in migrations must use physical DB column names (`user_id`), not Prisma model field names (`userId`). Reference EXP-256. |
| `docker/production/docker-compose.yml` comments | Document volume-path convention; reference EXP-251 |
| `apps/experts-realtime/` README | Document per-user WS connection cap (EXP-262) and `mem_limit`/`cpus` requirement (EXP-260) |
| Brain `Action-Tracker.md` | EXP-256–263 rows added this digest |

---

## Still Open

New today, remaining in Backlog:

| Issue | Title | Severity |
|-------|-------|----------|
| EXP-250 | R2_API_TOKEN env defined but never read | Low |
| EXP-251 | pg18 volume-path flip — data loss on next deploy | **Critical** |
| EXP-252 | persistAskAiExchange TOCTOU — messages written to deleted conversations | **High** |
| EXP-253 | community DELETE missing UUID guard — Prisma P2023 → 500 | **High** |
| EXP-254 | GET /community/posts/[id] returns draft posts to unauthenticated callers | **High** |
| EXP-256 | migration raw DELETE hardcoded "userId" — fails if column pre-renamed | Medium |
| EXP-257 | totalPages incoherent for in-memory sorts (spinoff EXP-242) | **High** |
| EXP-258 | unbounded search ILIKE DoS (spinoff EXP-242) | **High** |
| EXP-259 | unknown sort returns undefined-order results (spinoff EXP-242) | **High** |
| EXP-260 | realtime container no memory limit | Medium |
| EXP-261 | CI immutability guard bypassed by direct push to main | Medium |
| EXP-262 | no per-user WebSocket connection cap | Medium |
| EXP-263 | totalPages uncapped for in-memory sorts, duplicate EXP-257 (spinoff EXP-242) | Medium |

Carried forward (selected high-severity):

| Issue | Title | Severity | Since |
|-------|-------|----------|-------|
| EXP-241 | community posts PUT JWT isAdmin staleness | **High** | 2026-05-31 |
| EXP-242 | community GET unbounded findMany (+ 4 spinoffs) | **High** | 2026-05-31 |
| EXP-223 | prompt injection via community post context in AI | Medium | 2026-05-28 |
| EXP-208 | realtime sync Section 3 unbounded userPosts/userComments | **High** | 2026-05-21 |
| EXP-141 | R2 API token + Redis password in git history | **Critical** | 2026-05-26 |

---

## Needs Human Attention

Items in 3+ consecutive digests still open, or new critical/urgent issues:

| Item | In Digest Since | Priority | Action Required |
|------|----------------|----------|-----------------|
| Traefik `headers.contentSecurityPolicy` removal | 2026-05-22 (11 consecutive digests) | Medium | **OVERDUE** (due 2026-06-01). `curl -sI https://app.experts.com.sa/en \| grep -i content-security` |
| [EXP-251](https://linear.app/experts/issue/EXP-251) pg18 volume-path flip | New today | **Critical** | Block next prod deploy; take `pg_dump`; revert/fix volume path before `docker compose up` |
| [EXP-141](https://linear.app/experts/issue/EXP-141) R2 API token + Redis password in git history | 2026-05-26 (6 digests) | **Critical** | BFG/filter-repo history rewrite + token rotation still outstanding |
| [EXP-103](https://linear.app/experts/issue/EXP-103) 5 upload routes missing `enforceStorageQuota` | 2026-05-24 (8 digests) | High | Depends on EXP-80 ledger; no PR open |
| [EXP-129](https://linear.app/experts/issue/EXP-129) Tabby webhook KSA geo-gate bypass | 2026-05-25 (7 digests) | High | Enforce geo-restriction on verify + webhook paths |
| [EXP-127](https://linear.app/experts/issue/EXP-127) advisory lock birthday collision at ~55k users | 2026-05-25 (7 digests) | Medium | Pre-launch migration to 64-bit key |
| [EXP-241](https://linear.app/experts/issue/EXP-241) community PUT JWT staleness | 2026-05-31 (2 digests) | **High** | Re-derive actor from DB; implement `getDbCommunityActor` helper |
| [EXP-242](https://linear.app/experts/issue/EXP-242) community GET unbounded (+ 4 spinoffs) | 2026-05-31 (2 digests) | **High** | PR #738 in review; bundle spinoffs EXP-257/258/259/263 before merge |

---

## Source References

- Commits on `logi-x/experts main` today: PRs #712, #714, #715, #717, #719, #724, #729, #731, #732, #733
- Linear issues filed today: EXP-245–263 (17 agent-fp; EXP-249 and EXP-255 non-agent-fp)
- Linear issues resolved today: EXP-233, EXP-234, EXP-238, EXP-245–249, EXP-255 (9 total)
- Prior digest: [[Raw/sources/2026-05-31-experts-agent-digest.md]]
- Findings index: [[Raw/agent-state/findings-index.md]] (read-only)

---

_Generated by automated digest routine (full end-of-day pass; supersedes morning partial). Community posts GET endpoint has 6 open findings — highest-density file. EXP-251 (pg18 volume-path flip) is a production data-loss risk requiring immediate operator attention before next deploy._

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
