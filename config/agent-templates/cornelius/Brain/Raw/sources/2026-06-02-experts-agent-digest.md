---
title: "2026-06-02 Experts Agent Digest"
date: "2026-06-02"
tags: [agent, digest, project/experts]
category: "daily"
source: "automation"
source_id: "Raw/sources/2026-06-02-experts-agent-digest.md"
---

# Experts Agent Digest — 02 June 2026

**Window:** 2026-06-02T00:00:00Z → 2026-06-02T23:59:59Z  
**Prior digest:** [[Raw/sources/2026-06-01-experts-agent-digest.md]]

---

## Summary Table

| Metric | Count |
|--------|-------|
| New agent-fp issues (today) | 18 |
| Resolved since yesterday | 20 |
| In-flight fixes (PR open / in review) | 2 |
| Merged PRs | 23 |
| Needs human attention | 8 |

---

## New Today

Issues opened by routines (body contains `<!-- agent-fp:`):

| Issue | Title | FP | Severity | Status |
|-------|-------|-----|----------|--------|
| [EXP-273](https://linear.app/experts/issue/EXP-273) | [bug] Release workflow has no force_build_realtime input | `7d65c8b1dd47` (R3) | Medium | Done (same-day via PR #761) |
| [EXP-274](https://linear.app/experts/issue/EXP-274) | [infra] Add container memory limits + Postgres memory tuning | `c3483b4cd2e6` (R3) | **High** | Backlog |
| [EXP-275](https://linear.app/experts/issue/EXP-275) | [infra] R2 has no automated backup/replication — unrecoverable deletion | `dad0348c3622` (R3) | **High** | Backlog |
| [EXP-276](https://linear.app/experts/issue/EXP-276) | [bug] exam reset POST no examId→courseId ownership check — BOLA | `4c24416c67be` (R3) | **High** | Backlog |
| [EXP-277](https://linear.app/experts/issue/EXP-277) | [bug] community posts DELETE has no admin bypass — moderation blocked | `300e6e064c43` (R3) | **High** | Backlog |
| [EXP-278](https://linear.app/experts/issue/EXP-278) | [bug] handleCourseSubmit missing "pending" guard — double-submit while under review | `7a77f4e88d1c` (R3) | **High** | Backlog |
| [EXP-279](https://linear.app/experts/issue/EXP-279) | [security] GitHub Actions workflow injection via `${{ github.base_ref }}` in migration-immutability | `612635d18b4f` (R3) | **High** | Backlog |
| [EXP-280](https://linear.app/experts/issue/EXP-280) | [security] Community post PUT allows owner to reverse admin unpublish | `10787fbfd313` (R3) | Medium | Backlog |
| [EXP-281](https://linear.app/experts/issue/EXP-281) | [security] Community post creation POST has no rate limit — authenticated DoS | `25ef3eed3a78` (R3) | Medium | Backlog |
| [EXP-282](https://linear.app/experts/issue/EXP-282) | [security] Production cron + all container base images floating — supply-chain risk | `bcd1d1b0ba51` (R3) | Medium | Done (same-day via PR #777) |
| [EXP-283](https://linear.app/experts/issue/EXP-283) | [devops] Add Docker digest-update automation (Dependabot) | `2925412d3273` (R3) | Low | Backlog |
| [EXP-284](https://linear.app/experts/issue/EXP-284) | [bug] assertCourseWriteAccess admin bypass — any admin can force-submit any instructor's course | `20ca5e858867` (R3) | **High** | Backlog |
| [EXP-285](https://linear.app/experts/issue/EXP-285) | [bug] handleCourseSubmit read+write not atomic — TOCTOU dormant until EXP-278 fix | `4cbf93d87242` (R3) | Medium | Backlog |
| [EXP-286](https://linear.app/experts/issue/EXP-286) | [bug] community posts GET popular/discussed: totalPosts reflects full DB count but only 500 navigable | `07a618296c89` (R3) | Medium | Backlog |
| [EXP-287](https://linear.app/experts/issue/EXP-287) | [bug] GET /community/posts/[id] — auth() moved outside try block, unhandled exception bypasses safeErrorJson | `2f672f5b4d96` (R3) | Medium | Backlog |
| [EXP-288](https://linear.app/experts/issue/EXP-288) | [security] Community post detail GET — unbounded comment fetch OOM DoS | `47a8e3572d1a` (R3) | Medium | Backlog |
| [EXP-289](https://linear.app/experts/issue/EXP-289) | [security] Community comments GET — unbounded findMany, no cache read — unauthenticated OOM DoS | `d1b9205afee9` (R3) | Medium | Backlog |
| [EXP-290](https://linear.app/experts/issue/EXP-290) | [security] Community comments POST — no input validation allows unbounded content blobs | `f0979bbccfad` (R3) | Medium | Backlog |

> Note: EXP-273 and EXP-282 opened and resolved same-day.
> Note: EXP-283 is a devops follow-up to EXP-282 (Dependabot automation); deliberately not in the R3 auto-fix lane.

---

## Repeated Pattern

From `Raw/agent-state/findings-index.md` — files/symbols appearing 3+ times in last 30 days:

| Pattern | Occurrences (30d) | State |
|---------|------------------|-------|
| `apps/experts-app/app/api/v1/community/posts/[id]/route.ts` | 6 issues (EXP-241✓, EXP-253✓, EXP-254✓, EXP-277 open, EXP-280 open, EXP-287 open) | Three open issues remain post-sweep; moderation bypass, owner-unpublish-reversal, auth-outside-try |
| `apps/experts-app/app/api/v1/community/posts/route.ts` | 7 issues (EXP-242✓, EXP-243✓, EXP-257✓, EXP-258✓, EXP-259✓, EXP-281 open, EXP-286 open) | EXP-286 (totalPosts incoherent) is a regression from the EXP-242 fix; EXP-281 (rate limit) still open |
| `apps/experts-app/app/api/v1/community/posts/[id]/comments/route.ts` | 3 issues today (EXP-288, EXP-289, EXP-290 — all open) | NEW: comments layer enters scope; first R3 scan of this endpoint |
| `apps/experts-app/src/lib/ai/ask/ask-ai-assistant.ts` | 3 issues (EXP-223 open, EXP-232 open, EXP-252 open) | Prompt injection + AskAiDomainError + TOCTOU — all open |
| **JWT role-staleness class** | 15+ instances total in 30d | **Fully resolved today** via PRs #756+#757 (4 gatekeeper attempts). All three tiers covered |
| **Docker container no resource limits** | 3 issues (EXP-141 app, EXP-177 postgres, EXP-274 new) | EXP-274 subsumes EXP-260 (realtime, duplicate) |
| **BOLA / cross-resource ownership** | 3 issues (EXP-233✓, EXP-238✓, EXP-276 open) + EXP-284 (admin bypass variant) | EXP-284 (assertCourseWriteAccess admin bypass) is a distinct but related class |
| **handleCourseSubmit** | 3 issues (EXP-234✓, EXP-278 open, EXP-285 open) | EXP-278 (missing pending guard) + EXP-285 (TOCTOU race) must be fixed atomically in one `$transaction` |

---

## Resolved Since Yesterday

Issues whose Linear status flipped to Done/resolved after the 2026-06-01 digest (20 total):

| Issue | Title | Resolved By | Merged |
|-------|-------|-------------|--------|
| [EXP-241](https://linear.app/experts/issue/EXP-241) | JWT role-staleness sweep (Tier 1 API + Tier 2 helpers + lint) | PR #756 | 2026-06-01T23:10Z |
| [EXP-264](https://linear.app/experts/issue/EXP-264) | Fix stale isAdmin in GET /api/me | PR #756 | 2026-06-01T23:10Z |
| [EXP-268](https://linear.app/experts/issue/EXP-268) | Fail-closed error handling in getDbCourseActor | PR #756 | 2026-06-01T23:10Z |
| [EXP-271](https://linear.app/experts/issue/EXP-271) | Fail-closed test for _lib/course-route-actor | PR #756 | 2026-06-01T23:10Z |
| [EXP-265](https://linear.app/experts/issue/EXP-265) | Extend jwtRoleSelectors ESLint to non-route app/api helpers | PR #757 | 2026-06-01T23:36Z |
| [EXP-267](https://linear.app/experts/issue/EXP-267) | Add jwtRoleSelectors lint rule to app/**/page.tsx and layout.tsx | PR #757 | 2026-06-01T23:36Z |
| [EXP-270](https://linear.app/experts/issue/EXP-270) | Fix JWT isAdmin gate on GET /invoices/[id]/preview RSC | PR #757 | 2026-06-01T23:36Z |
| [EXP-272](https://linear.app/experts/issue/EXP-272) | Replace console.error with logger.error in getUserPermissions | PR #757 | 2026-06-01T23:36Z |
| [EXP-266](https://linear.app/experts/issue/EXP-266) | Consolidate duplicate getDbCourseActor into canonical export | PR #758 | 2026-06-02T01:08Z |
| [EXP-273](https://linear.app/experts/issue/EXP-273) | Release workflow no force_build_realtime input | PR #761 | 2026-06-02T04:06Z |
| [EXP-250](https://linear.app/experts/issue/EXP-250) | Remove dead R2_API_TOKEN from .env.example | PR #764 | 2026-06-02T05:27Z |
| [EXP-261](https://linear.app/experts/issue/EXP-261) | migration-immutability CI guard also guards direct push to main | PR #766 | 2026-06-02T06:22Z |
| [EXP-242](https://linear.app/experts/issue/EXP-242) | Community posts GET unbounded findMany for popular/discussed | PR #768 | 2026-06-02T07:07Z |
| [EXP-243](https://linear.app/experts/issue/EXP-243) | Community posts GET uncapped user-supplied limit | PR #768 (collateral) | 2026-06-02T07:07Z |
| [EXP-257](https://linear.app/experts/issue/EXP-257) | Community posts GET totalPages incoherent for in-memory sorts | PR #768 (collateral) | 2026-06-02T07:07Z |
| [EXP-258](https://linear.app/experts/issue/EXP-258) | Community posts GET unbounded search ILIKE DoS | PR #768 (collateral) | 2026-06-02T07:07Z |
| [EXP-259](https://linear.app/experts/issue/EXP-259) | Community posts GET unknown sort value | PR #768 (collateral) | 2026-06-02T07:07Z |
| [EXP-253](https://linear.app/experts/issue/EXP-253) | Community posts DELETE missing UUID guard | PR #769 | 2026-06-02T07:08Z |
| [EXP-254](https://linear.app/experts/issue/EXP-254) | GET /community/posts/[id] returns draft posts | PR #769 (collateral) | 2026-06-02T07:08Z |
| [EXP-282](https://linear.app/experts/issue/EXP-282) | All container base images floating — supply-chain risk (full fleet sweep) | PR #777 | 2026-06-02T12:30Z |

Also canceled/duplicated today: EXP-256 (wontfix/by-design), EXP-260 (duplicate of EXP-274), EXP-263 (duplicate of EXP-257), EXP-269 (duplicate of EXP-270).

---

## In-Flight Fixes

| Issue | Title | Status |
|-------|-------|--------|
| [EXP-120](https://linear.app/experts/issue/EXP-120) | CRON_SECRET timing-safe compare skips check when secret undefined | In Review |
| [EXP-133](https://linear.app/experts/issue/EXP-133) | CRON_AUTH_TOKEN timing-safe compare skips check on undefined | In Review |

---

## Merged PRs

| PR | Title | Closes | Merged |
|----|-------|--------|--------|
| [#756](https://github.com/logi-x/experts/pull/756) | fix(security): DB-fresh role gates + fail-closed actor + lint guard (EXP-241) [attempt 4] | EXP-241, EXP-264, EXP-268, EXP-271 | 2026-06-01T23:10Z |
| [#757](https://github.com/logi-x/experts/pull/757) | fix(security): DB-fresh role gates in RSC + extend lint to app/** (EXP-267/265/270/272) | EXP-265, EXP-267, EXP-270, EXP-272 | 2026-06-01T23:36Z |
| [#758](https://github.com/logi-x/experts/pull/758) | refactor(courses): consolidate duplicate getDbCourseActor (EXP-266) | EXP-266 | 2026-06-02T01:08Z |
| [#759](https://github.com/logi-x/experts/pull/759) | chore(routines): unify dedup fingerprint recipe across issue-filing routines | — | 2026-06-02T02:02Z |
| [#761](https://github.com/logi-x/experts/pull/761) | ci(release): add force_build_realtime input (EXP-273) | EXP-273 | 2026-06-02T04:06Z |
| [#762](https://github.com/logi-x/experts/pull/762) | docs(routines): Rule 4 — status transitions + post-merge re-index | — | 2026-06-02T04:16Z |
| [#763](https://github.com/logi-x/experts/pull/763) | chore(g,routines): Rule 4 post-merge uses ./g --clean + protected-branch guard | — | 2026-06-02T04:23Z |
| [#764](https://github.com/logi-x/experts/pull/764) | chore(env): remove dead R2_API_TOKEN from .env.example (EXP-250) | EXP-250 | 2026-06-02T05:27Z |
| [#766](https://github.com/logi-x/experts/pull/766) | ci(migration-immutability): also guard direct pushes to main (EXP-261) | EXP-261 | 2026-06-02T06:22Z |
| [#768](https://github.com/logi-x/experts/pull/768) | fix(community): harden posts list GET — bound fetch, clamp inputs, validate sort (EXP-242) | EXP-242, EXP-243, EXP-257, EXP-258, EXP-259 | 2026-06-02T07:07Z |
| [#769](https://github.com/logi-x/experts/pull/769) | fix(community): guard post-id DELETE + close draft disclosure on GET (EXP-253, EXP-254) | EXP-253, EXP-254 | 2026-06-02T07:08Z |
| [#777](https://github.com/logi-x/experts/pull/777) | chore(docker,ci): unify Node 26.3.0 + digest-pin all base images (EXP-282) | EXP-282 | 2026-06-02T12:30Z |
| [#778](https://github.com/logi-x/experts/pull/778) | Fix/global cleanup (pnpm 11.5.1 + deps update + seed avatar URL fix) | — | 2026-06-02T21:11Z |
| [#733](https://github.com/logi-x/experts/pull/733) | fix(courses): scope lesson video DELETE attachment lookup to requesting user (EXP-238) | EXP-238 | 2026-06-01T21:39Z |
| [#732](https://github.com/logi-x/experts/pull/732) | fix(courses): guard against re-submission of approved courses (EXP-234) | EXP-234 | 2026-06-01T21:39Z |
| [#731](https://github.com/logi-x/experts/pull/731) | fix(realtime): run as node uid 1000 so it can read Docker secrets (EXP-255) | EXP-255 | 2026-06-01T21:01Z |
| [#729](https://github.com/logi-x/experts/pull/729) | fix(courses): add assertCourseWriteAccess to quiz DELETE handler (EXP-233) | EXP-233 | 2026-06-01T19:36Z |
| [#724](https://github.com/logi-x/experts/pull/724) | infra(docker): pg18 + parent volume mount across all envs (EXP-249) | EXP-249 | 2026-06-01T08:01Z |
| [#719](https://github.com/logi-x/experts/pull/719) | fix(db): snake_case storage_alerts.userId → user_id (EXP-248) | EXP-248 | 2026-06-01T07:14Z |
| [#717](https://github.com/logi-x/experts/pull/717) | fix(db): converge storage_alerts UNIQUE(userId) + CI migration-immutability guard (EXP-247) | EXP-247 | 2026-06-01T04:58Z |
| [#715](https://github.com/logi-x/experts/pull/715) | fix(infra): add persistent data volume to Postgres in all envs (EXP-246) | EXP-246 | 2026-06-01T02:44Z |
| [#714](https://github.com/logi-x/experts/pull/714) | chore(staging): pin postgres to pg16 (match prod) + digest-pin redis/alpine | — | 2026-06-01T02:44Z |
| [#712](https://github.com/logi-x/experts/pull/712) | fix(upload): stop masking DB connection errors as 403 Forbidden | — | 2026-06-01T02:44Z |

**Semver: PATCH** — all changes are security/bug fixes, refactors, CI improvements, infra corrections, or dependency updates. No new user-facing features.

Operator follow-ups required:
1. Revoke `R2_API_TOKEN` at Cloudflare (EXP-250 — credential may be a live management-plane token)
2. EXP-279: Fix `.github/workflows/experts-app.yml` migration-immutability job to use `env:` block instead of direct `${{ github.base_ref }}` interpolation before next PR triggers the job

---

## Migrations / Env / Infra Changes

- **`.github/workflows/experts-app.yml`** (PR #766): `migration-immutability` job now triggers on `push` to protected branches when migration files change. Diff base branches correctly between PR and push events.
- **`.env.example`** (PR #764): `R2_API_TOKEN` removed. Operator should revoke the live Cloudflare management-plane token if provisioned.
- **Dockerfile + docker-compose (PR #777)**: Full container-fleet Node version pump to 26.3.0; all base images digest-pinned. App/worker: `node:26.3.0-bookworm-slim@sha256:79723b41…`; prisma/realtime: `node:26.3.0-alpine3.23@sha256:144769ec…`; prod cron: `alpine:3.23.4@sha256:5b10f432…`. `.nvmrc` 24→26; CI `setup-node` 24→26; `engines.node >=26.0.0` across root/app/prisma/realtime.
- **`package.json` / `pnpm-lock.yaml` (PR #778)**: pnpm 11.5.0→11.5.1; ESLint, lint-staged, TypeScript-ESLint updates; AWS SDK 3.1059.0 across app + worker; seed avatar URLs updated to new CDN links.
- **No new Prisma migrations today.**

---

## Architectural Notes

### 1. JWT role-staleness class fully closed — 4 gatekeeper attempts

The EXP-241 sweep (started 2026-05-31) completed after 4 gatekeeper attempts across PRs #756, #757:
- **Tier 1** (API route handlers, 10 course routes + 11 other routes): `getDbCourseActor` and `getUserPermissions()`
- **Tier 2** (server helpers not behind proxy gate): `assert-learn-page-access`, `get-public-user-profile`, `/api/me`
- **Tier 3** (RSC layouts/pages): 18 admin/console layouts, invoice preview page
- **ESLint guard**: `jwtRoleSelectors` now covers `app/api/**/route.ts`, `src/lib/**`, and `app/**/*.ts(x)` — the full surface

Largest single security remediation in the project history (~30 route files, ~18 layouts, 4 PRs). The per-route DB patching posture established 2026-05-29 is now complete at the class level.

### 2. EXP-279: GH Actions injection vector introduced same day as EXP-261 fix

PR #766 (fixing EXP-261 — migration-immutability direct-push bypass) introduced `${{ github.base_ref }}` directly in a `run:` shell step without env var indirection. Any PR from a branch whose name contains shell metacharacters (`'`, `;`, `|`, `$()`) can inject arbitrary commands into the CI runner. Must be fixed before the next PR triggers the migration-immutability job. **Decision-Log entry added (2026-06-02).**

### 3. assertCourseWriteAccess admin bypass (EXP-284) — write-gate vulnerability

`assertCourseWriteAccess` short-circuits at `if (isAdmin) return {ok: true}` before querying `courseInstructor`. Any admin can force-submit any instructor's course. This is distinct from the JWT staleness class: the DB IS queried for `isAdmin` (via `getDbCourseActor`), but the ownership check is bypassed entirely. **Decision-Log entry added.** Architecture implication: write-gating helpers must perform the resource ownership DB query regardless of the caller's role level; admin-bypass is not a blanket exemption from ownership verification on write operations.

### 4. EXP-278 + EXP-285 must be fixed atomically

EXP-278 (missing `approvalStatus !== "pending"` guard) and EXP-285 (non-atomic read+write TOCTOU race) share `handleCourseSubmit`. Fixing EXP-278 alone narrows the guard but does not close the race window: two concurrent submissions can both pass the new guard if their reads interleave before either write. Both fixes must land in a single `$transaction` (select + update wrapped atomically). Any PR fixing only EXP-278 without the transaction wrapper should be blocked.

### 5. Community domain API now at 5 sub-areas — R3 expanding to comments layer

R3 has now generated findings across 5 distinct community API sub-areas:
1. **Posts list** `posts/route.ts` — 7 issues, mostly resolved
2. **Post detail** `posts/[id]/route.ts` — 6 issues, 3 open
3. **Post create/update/delete** — 3 open (EXP-277, EXP-280, EXP-281)
4. **Post comments list** `posts/[id]/comments/route.ts GET` — EXP-289 new today
5. **Post comments create** `posts/[id]/comments/route.ts POST` — EXP-290 new today

EXP-288 (unbounded comment fetch inside post detail GET) straddles areas 2 and 4. Pattern: each layer fix surfaces the next. The comments endpoint has not previously been touched by security remediation.

### 6. Fingerprint dedup recipe canonicalized (PR #759)

All three issue-filing routines (R01, R02, R07) now use `sha1(file:symbol:finding_class)` with severity and routine-of-origin excluded from the salt. Near-match linking replaces fork-and-file. Cross-type findings-index scan prevents cross-routine duplicates.

### 7. Node 26.3.0 + supply-chain hardening complete (PR #777)

Full container fleet uniformly on Node 26.3.0 with immutable digest pins. No floating base image tags remain in `apps/` or `docker/`. EXP-283 (Dependabot) ensures these pins don't decay — devops decision needed on cadence and grouping.

---

## Docs That Need Updating

| File | Required Update |
|------|----------------|
| `POSTGRES-VOLUME-MIGRATION.md` (deleted by PR #724) | Restore or replace with pg16→pg18 upgrade guide including volume-path migration steps |
| `.github/workflows/experts-app.yml` `migration-immutability` job | Fix `${{ github.base_ref }}` shell interpolation (EXP-279) — use `env:` block indirection |
| `apps/experts-realtime/` README | Document per-user WS cap requirement (EXP-262) and mem_limit/cpus requirement (EXP-274) |
| `apps/experts-app/prisma/` migration guide | Raw SQL in migrations must reference physical DB column names (snake_case as `@map()`), not Prisma camelCase field names |
| `docker/production/docker-compose.yml` | Add `mem_limit` + `memswap_limit` + `shm_size` to postgres and realtime services (EXP-274) |
| `apps/experts-app/app/api/v1/community/posts/[id]/comments/route.ts` | Harden: GET needs `take:` cap + `Cache-Control`; POST needs Zod validation + content length cap; rate limit per EXP-288/289/290 |
| `apps/experts-app/src/lib/courses/catalog/guards/course-access.guard.ts` | Fix assertCourseWriteAccess admin bypass: perform `courseInstructor` DB check even when `isAdmin` (EXP-284) |

---

## Still Open

New today, remaining in Backlog:

| Issue | Title | Severity |
|-------|-------|----------|
| EXP-274 | Container memory limits + Postgres tuning | **High** |
| EXP-275 | R2 no automated backup/replication | **High** |
| EXP-276 | Exam reset BOLA (no examId→courseId ownership check) | **High** |
| EXP-277 | Community DELETE no admin bypass — moderation blocked | **High** |
| EXP-278 | Course submit double-submit guard missing | **High** |
| EXP-279 | GH Actions workflow injection via `${{ github.base_ref }}` | **High** |
| EXP-280 | Community PUT owner can reverse admin unpublish | Medium |
| EXP-281 | Community POST no rate limit — authenticated DoS | Medium |
| EXP-283 | No Docker digest-update automation (Dependabot) | Low |
| EXP-284 | assertCourseWriteAccess admin bypass — any admin force-submits any course | **High** |
| EXP-285 | handleCourseSubmit TOCTOU race (dormant until EXP-278 fix lands) | Medium |
| EXP-286 | Community posts GET popular/discussed: totalPosts incoherent vs navigable range | Medium |
| EXP-287 | GET /community/posts/[id]: auth() outside try block bypasses safeErrorJson | Medium |
| EXP-288 | Community post detail GET: unbounded comment fetch OOM DoS | Medium |
| EXP-289 | Community comments GET: unbounded findMany unauthenticated OOM DoS | Medium |
| EXP-290 | Community comments POST: no input validation — unbounded content blobs | Medium |

Carried forward (selected high-severity open issues):

| Issue | Title | Severity | Since |
|-------|-------|----------|-------|
| EXP-252 | persistAskAiExchange TOCTOU race (FOR UPDATE missing) | **High** | 2026-06-01 |
| EXP-262 | No per-user WebSocket connection cap | Medium | 2026-06-01 |
| EXP-223 | AI prompt injection via community post context | Medium | 2026-05-28 |
| EXP-226 | Course catalog GET no take bound for non-recent sort | **High** | 2026-05-28 |
| EXP-232 | Ask AI non-streaming path AskAiDomainError unhandled | **High** | 2026-05-29 |
| EXP-120 | CRON_SECRET timing-safe compare skips check (in review) | **High** | 2026-05-22 |
| EXP-133 | CRON_AUTH_TOKEN timing-safe compare skips check (in review) | **High** | 2026-05-22 |
| EXP-140 | ZATCA invoice submission no retry on transient errors | **High** | 2026-05-22 |
| EXP-142 | ZATCA invoice XML special-char escaping (XML injection) | **High** | 2026-05-22 |
| EXP-129 | Tabby KSA geo-gate bypass on verify + webhook | **High** | 2026-05-22 |

---

## Needs Human Attention

Items appearing in 3+ consecutive digests still open, or new critical/high items:

| Item | In Digest Since | Priority | Action Required |
|------|----------------|----------|-----------------|
| Traefik `headers.contentSecurityPolicy` removal | 2026-05-22 (**12 consecutive digests**) | Medium | **Severely overdue** (due 2026-06-01). `curl -sI https://app.experts.com.sa/en \| grep -i content-security` |
| [EXP-141](https://linear.app/experts/issue/EXP-141) R2 API token + Redis password in git history | 2026-05-26 (7 digests) | **Critical** | BFG/filter-repo + token rotation still outstanding |
| [EXP-103](https://linear.app/experts/issue/EXP-103) 5 upload routes missing `enforceStorageQuota` | 2026-05-24 (9 digests) | High | Depends on EXP-80 ledger; no PR open |
| [EXP-129](https://linear.app/experts/issue/EXP-129) Tabby webhook KSA geo-gate bypass | 2026-05-25 (8 digests) | High | Enforce restriction on verify + webhook paths |
| [EXP-127](https://linear.app/experts/issue/EXP-127) Advisory lock birthday collision at ~55k users | 2026-05-25 (8 digests) | Medium | Pre-launch migration to 64-bit key |
| [EXP-223](https://linear.app/experts/issue/EXP-223) AI prompt injection via community posts | 2026-05-28 (5 digests) | Medium | XML-tag separation still needed after newline guard |
| [EXP-279](https://linear.app/experts/issue/EXP-279) GH Actions shell injection in migration-immutability | Today | **High** | Fix `${{ github.base_ref }}` before next PR triggers the CI job |
| [EXP-275](https://linear.app/experts/issue/EXP-275) R2 no backup/replication — ZATCA legal exposure | Today | **High** | Implement rclone copy + PITR prefixes; operator required for off-provider retention |

---

## Source References

- Commits on `logi-x/experts main` today: 21 (PRs #756–#778 range + direct commit `85a6d8d` GitNexus docs)
- Linear issues filed today: EXP-273–290 (18 agent-fp issues)
- Linear issues resolved today: EXP-241, 242, 243, 250, 253, 254, 257, 258, 259, 261, 264, 265, 266, 267, 268, 270, 271, 272, 273, 282 (20 total)
- Prior digest: [[Raw/sources/2026-06-01-experts-agent-digest.md]]
- Findings index: [[Raw/agent-state/findings-index.md]] (read-only)

---

_Updated by automated digest routine (end-of-day pass; supersedes earlier partial). 18 new issues total including assertCourseWriteAccess admin bypass (EXP-284, High) and community comments layer expansion (EXP-288–290). JWT role-staleness class fully closed after 4 gatekeeper attempts. Node 26.3.0 + full container digest-pin complete. Community domain now spans 5 sub-areas with 13 issues filed today._

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
