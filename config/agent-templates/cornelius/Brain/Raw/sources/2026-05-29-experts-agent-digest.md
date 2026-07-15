---
title: "2026-05-29 Experts Agent Digest"
date: "2026-05-29"
tags: [agent, digest, project/experts]
category: "daily"
source: "automation"
source_id: "Raw/sources/2026-05-29-experts-agent-digest.md"
---

# 2026-05-29 Experts Agent Digest

Window: 2026-05-28T00:00:00Z → 2026-05-29T23:59:59Z.

---

## New today

Issues created with agent fingerprints (`<!-- agent-fp:`) in the last 24h:

| # | Title | Status | Severity | FP | Created |
|---|-------|--------|----------|----|--------|
| [EXP-183](https://linear.app/experts/issue/EXP-183) | [spinoff: EXP-170] course-exams submit route leaks raw error.message | **Done** | Medium | `21719349276427` | 2026-05-29T01:41Z |
| [EXP-184](https://linear.app/experts/issue/EXP-184) | [spinoff: EXP-170] admin/commissions/[id]/approve leaks raw error.message | **Done** | Medium | `2d9086d77592` | 2026-05-29T01:41Z |
| [EXP-185](https://linear.app/experts/issue/EXP-185) | [spinoff: EXP-170] auth/native/register leaks DB constraint details on dup email | **Done** | Medium | `471dcdaf05d1` | 2026-05-29T01:42Z |
| [EXP-186](https://linear.app/experts/issue/EXP-186) | [spinoff: EXP-170] console/health route leaks raw DB and Redis connection strings | **Done** | Medium | `7270e1172f0d` | 2026-05-29T02:47Z |
| [EXP-187](https://linear.app/experts/issue/EXP-187) | [spinoff: EXP-170] ESLint sink rule misses two-step pattern | **Done** | Low | `5f40cac28e45` | 2026-05-29T02:47Z |
| [EXP-188](https://linear.app/experts/issue/EXP-188) | [spinoff: EXP-170] ESLint sink rule bypassed for src/lib/** | **Cancelled** | Low | `5f549d4217a8` | 2026-05-29T02:47Z |
| [EXP-192](https://linear.app/experts/issue/EXP-192) | [spinoff: EXP-174] Add take: bound to Section 2 post query in realtime sync | **Done** | Low | `3c5002d2354f` | 2026-05-29T04:09Z |
| [EXP-193](https://linear.app/experts/issue/EXP-193) | [spinoff: EXP-174] Fix channel isolation — events for unsubscribed post channels | **Done** | Medium | `f77e9e808a26` | 2026-05-29T04:09Z |
| [EXP-194](https://linear.app/experts/issue/EXP-194) | [bug] Section 3 unbounded userPosts/userComments in realtime sync — hot-path DoS | Backlog | **High** | `7e6cad1a8d0d` | 2026-05-29T09:23Z |
| [EXP-195](https://linear.app/experts/issue/EXP-195) | [bug] Liker userId exposed in realtime sync polling events for public posts | Backlog | Medium | `c84fb6ebe85f` | 2026-05-29T09:23Z |
| [EXP-196](https://linear.app/experts/issue/EXP-196) | [bug] manageCurriculum button inverted — active courses locked out, archived editable | Backlog | **High** | `e9bb508fbffa` | 2026-05-29T21:13Z |
| [EXP-197](https://linear.app/experts/issue/EXP-197) | [security] JWT role-staleness on course curriculum module routes — revoked admin bypass | Backlog | Medium | `4beadfc873f2` | 2026-05-29T21:30Z |
| [EXP-198](https://linear.app/experts/issue/EXP-198) | [security] JWT role-staleness on creator event detail GET — revoked admin reads private data | Backlog | Medium | `5a05720d6738` | 2026-05-29T21:32Z |
| [EXP-199](https://linear.app/experts/issue/EXP-199) | [security] JWT role-staleness on course lifecycle routes — revoked admin can delete/archive/clone/publish | Backlog | **High** | `ebb296405be7` | 2026-05-29T21:32Z |

**14 new** agent-fp issues this window (EXP-183–188, 192–199). EXP-188 cancelled as duplicate of EXP-189. 8 resolved same-day. 6 remain open (EXP-194, 195, 196, 197, 198, 199).

Additionally, the following were filed by routines with manual fingerprints (not `<!-- agent-fp:` stamped in Linear body): EXP-178 (orphan-reaper CDN guard — **resolved** PR #582), EXP-179 (profile cover UX — **resolved** PR #585), EXP-180 (profile cover 404 — **resolved** PR #587), EXP-181 (build break — **resolved** PR #589), EXP-182 (30+ error.message routes — **resolved** PR #604), EXP-189 (ESLint src/lib gap — **open**), EXP-190 (Prisma migrate DATABASE_URL — **resolved** PR #606), EXP-191 (realtime sync rate limiting — **open**).

---

## Repeated pattern

Findings appearing 3+ times in the last 30 days (from `Raw/agent-state/findings-index.md`):

| Pattern | Count (30d) | Current state |
|---------|------------|---------------|
| JWT role-staleness (read roles from JWT, not DB) | 11 | EXP-69, 78, 84, 85, 88, 89, 90, 91 (all resolved pre-2026-05-26); **EXP-197, 198, 199 opened today** on new course lifecycle surface — root cause structurally unaddressed |
| Error disclosure (`error.message` / `error.stack` in 500 responses) | 15 issues over 4 days | **CLOSED AS A CLASS** — PR #604 swept 100 files / 134 sites; DomainError + safeErrorJson + two ESLint selectors. KNOWN GAP: `src/lib/**` still globally ESLint-ignored (EXP-189 open) |
| CRON_SECRET timing-unsafe / fail-open on cron routes | 7 | **CLOSED AS A CLASS** — PRs #478, #513, #522, #565 resolved all 7 |
| R2 storage bucket mismatch (write path ≠ URL origin) | 5 | EXP-145/146/147/148 resolved; **EXP-134 still open** (upload-public-asset write bucket misaligned) |
| Realtime sync DoS / IDOR / PII / over-delivery | 6 | EXP-174, 192, 193 resolved; **EXP-191, 194, 195 open** on same route file |
| Prompt injection via Bash/WebFetch grants in agent configs | 3 | EXP-143, 151, 173 — all open, no PR filed |

---

## Resolved since yesterday

Linear issues that flipped to Done in this window:

| # | Title | Merged via | Resolved at |
|---|-------|-----------|------------|
| EXP-146 | storage-janitor sweeps hardcode R2_BUCKET_USER_UPLOADS | PR #593 | 2026-05-29T00:18Z |
| EXP-147 | deleteFromR2 hardcodes R2_BUCKET_STATIC for cover cleanup | Already fixed PR #505 | 2026-05-29 (verified + closed Done) |
| EXP-148 | checkStorage false-ok when R2 upload buckets unset | PR #591 | 2026-05-29T00:22Z |
| EXP-170 | quiz submit error.message via safeErrorJson publicMessage | PR #604 (attempt 3) | 2026-05-29T03:07Z |
| EXP-171 | Unauthenticated share/test diagnostic endpoint | PR #607 (route deleted) | 2026-05-29T03:54Z |
| EXP-174 | IDOR in realtime sync — arbitrary post activity via user-supplied channels | PR #612 | 2026-05-29T04:21Z |
| EXP-175 | Cron sidecar missing APP_BASE_URL — all 8 cron tasks silently failing | PRs #590 + #592 | 2026-05-29T00:16Z |
| EXP-178 | Storage orphan-reaper can delete static CDN assets | PR #582 | 2026-05-28T22:45Z |
| EXP-179 | Profile cover: no live update, inconsistent buttons, wrong crop | PR #585 | 2026-05-28T23:42Z |
| EXP-180 | Profile default cover 404s from files.experts.com.sa | PR #587 | 2026-05-28T23:58Z |
| EXP-181 | App image build fails — module-level OpenAI client throws at build | PR #589 | 2026-05-29T00:10Z |
| EXP-182 | ~30 routes return `{error: error.message}` as public error field | Absorbed into PR #604 | 2026-05-29T03:07Z |
| EXP-183 | [spinoff EXP-170] course-exams submit leaks error.message | PR #604 | 2026-05-29T03:07Z |
| EXP-184 | [spinoff EXP-170] admin commissions approve individual leaks error.message | PR #604 | 2026-05-29T03:07Z |
| EXP-185 | [spinoff EXP-170] auth/native/register leaks P2002 DB constraint details | PR #604 | 2026-05-29T03:07Z |
| EXP-186 | [spinoff EXP-170] console/health route leaks DB and Redis connection strings | PR #604 | 2026-05-29T03:07Z |
| EXP-187 | [spinoff EXP-170] ESLint sink rule missed two-step const message pattern | PR #604 | 2026-05-29T03:11Z |
| EXP-190 | Prisma migrate container can't resolve DATABASE_URL from Docker secret | PR #606 | 2026-05-29T03:54Z |
| EXP-192 | [spinoff EXP-174] Section 2 post query unbounded in realtime sync | PR #613 | 2026-05-29T04:42Z |
| EXP-193 | [spinoff EXP-174] Channel isolation over-delivery in realtime sync | PR #614 | 2026-05-29T04:48Z |

**20 resolved** this window. Two bug classes fully closed: error-disclosure (PR #604) and CRON_SECRET timing-unsafe (PRs #478/513/522/565).

---

## In-flight fixes

Agent-opened issues currently In Progress or In Review:

| # | Title | Opened | Status |
|---|-------|--------|--------|
| EXP-120 | Missing auth unit tests for cron routes | 2026-05-25 | In Review (15 auth tests passed via PR #513) |
| EXP-133 | orphan-sweep CRON_SECRET timing-unsafe + fail-open | 2026-05-26 | In Review (resolved by PR #513; Linear moved to In Review) |

---

## Merged PRs

18 PRs merged in window 2026-05-28T00:00:00Z → 2026-05-29T23:59:59Z (incremental from 2026-05-28 digest cutoff after PR #577):

| PR | Title | Linear | Merged |
|----|-------|--------|--------|
| [#582](https://github.com/logi-x/experts/pull/582) | fix(storage): guard orphan-reaper against deleting static CDN assets | EXP-178 | 2026-05-28T22:44Z |
| [#583](https://github.com/logi-x/experts/pull/583) | chore(eslint): forbid direct process.env access to secret-backed vars | EXP-168 | 2026-05-28T22:45Z |
| [#585](https://github.com/logi-x/experts/pull/585) | fix(profile): live cover update, consistent buttons, 4:1 banner | EXP-179 | 2026-05-28T23:42Z |
| [#587](https://github.com/logi-x/experts/pull/587) | fix(profile): fall back to static brand cover for non-upload coverPhoto | EXP-180 | 2026-05-28T23:57Z |
| [#589](https://github.com/logi-x/experts/pull/589) | fix(ai): lazy OpenAI client — next build doesn't need OPENAI_SECRET | EXP-181 | 2026-05-29T00:10Z |
| [#590](https://github.com/logi-x/experts/pull/590) | fix(docker): restore APP_BASE_URL for cron sidecar so scheduled jobs run | EXP-175 | 2026-05-29T00:14Z |
| [#591](https://github.com/logi-x/experts/pull/591) | fix(health): flag missing R2 upload buckets in checkStorage | EXP-148 | 2026-05-29T00:22Z |
| [#592](https://github.com/logi-x/experts/pull/592) | fix(docker): restore APP_BASE_URL for dev cron sidecar | EXP-175 | 2026-05-29T00:27Z |
| [#593](https://github.com/logi-x/experts/pull/593) | fix(storage): route janitor sweep deletes by File.bucket | EXP-146 | 2026-05-29T00:29Z |
| [#604](https://github.com/logi-x/experts/pull/604) | fix(api): full error-disclosure sweep — DomainError + safeErrorJson + ESLint (attempt 3) | EXP-170, 182–187 | 2026-05-29T03:07Z |
| [#606](https://github.com/logi-x/experts/pull/606) | fix(prisma): hydrate DATABASE_URL from Docker secret in migrate container | EXP-190 | 2026-05-29T03:54Z |
| [#607](https://github.com/logi-x/experts/pull/607) | fix(security): remove unauthenticated share/test diagnostic endpoint | EXP-171 | 2026-05-29T03:54Z |
| [#612](https://github.com/logi-x/experts/pull/612) | fix(security): realtime sync IDOR + channel-cap + ReDoS guard | EXP-174 | 2026-05-29T04:21Z |
| [#613](https://github.com/logi-x/experts/pull/613) | fix(realtime): bound Section 2 post query take:50 in sync route | EXP-192 | 2026-05-29T04:42Z |
| [#614](https://github.com/logi-x/experts/pull/614) | fix(realtime): strict channel isolation for post like events | EXP-193 | 2026-05-29T04:47Z |
| [#617](https://github.com/logi-x/experts/pull/617) | chore(dependencies): update package versions and pnpm to 11.5.0 | — | 2026-05-29T16:35Z |
| [#618](https://github.com/logi-x/experts/pull/618) | feat(courses): implement archive and delete dialogs in CourseOverviewPage | — | 2026-05-29T16:38Z |
| [#619](https://github.com/logi-x/experts/pull/619) | Fix/all alert dialogs — clone, publish, delete + CreatePostFAB + EditCoursePage | — ⚠️ introduced EXP-196 | 2026-05-29T17:27Z |

**Semver recommendation: MINOR.** PR #618 adds new course archive/delete lifecycle dialogs (user-facing feature). PR #617 bumps pnpm to 11.5.0. Remaining PRs are security fixes and bug fixes. **⚠️ WARNING**: PR #619 introduced EXP-196 (inverted ternary, primary creator workflow broken). Prioritise hotfix before next deploy.

**Operator actions required:**
1. Restart cron containers after deploy; run one-off `payments/reconcile/batch` catch-up for the ~4h EXP-175 silent-failure window.
2. Rebuild prisma image so `migrate deploy` resolves DATABASE_URL from Docker secret (PR #606).
3. pnpm pinned to `11.5.0` — update CI, Docker build images, developer envs (PR #617).
4. Verify no `cdn.experts.com.sa/assets/*` objects were deleted by the pre-fix orphan-reaper; restore from backup if needed (PR #582).
5. PR #607 deleted the diagnostic route `GET /content/share/test` — update any runbooks referencing it to use `psql` table-check instead.

---

## Migrations / env / infra changes

- **No new Prisma schema migrations** in this window.
- **Prisma migrate container** — PR #606: `apps/experts-prisma/prisma.config.ts` hydrates `DATABASE_URL` from `DATABASE_URL_FILE` env or `/run/secrets/database_url`. Required for `prisma migrate deploy` in CI/production after EXP-168.
- **Docker Compose** — PRs #590/#592: `APP_BASE_URL` restored to cron sidecar explicit `environment:` blocks (production, staging, dev) after EXP-175 regression.
- **ESLint** — PR #583: `no-restricted-syntax` bans direct `process.env.<SECRET_VAR>` reads in `apps/experts-app/**`.
- **pnpm 11.5.0** — PR #617. Lock file updated; pin in CI and build images.
- **Diagnostic route removed** — PR #607 deleted `app/api/v1/content/share/test/route.ts` entirely.

---

## Architectural notes

1. **Error disclosure class fully resolved by construction; known gap in `src/lib/**`** (PR #604, EXP-189). `safeErrorJson` is now the sole permitted 500-response serializer across 100 route files / 134 sites. Two ESLint selectors enforce recurrence in `app/api/**/route.{ts,tsx}`. `src/lib/**` remains globally ESLint-ignored — ~44 pre-existing violations would surface if the ignore is removed. Until EXP-189 closes, the boundary is incomplete at the lib layer.

2. **Realtime sync IDOR resolved; security model established; three spinoffs remain open** (PR #612). `authorizedPostIds` gate (isPublished OR owner), `MAX_CHANNELS=20` cap, UUID-shape guard, `take:500` bound, strict `isChannelRequested` at both emit sites. Anonymous callers may subscribe to published-post channels by design. **Open**: EXP-191 (rate limiting), EXP-194 (Section 3 DoS amplifier at lines ~281/288), EXP-195 (liker userId in public-post events). This file has generated 6 Linear issues in one day and is a decomposition candidate.

3. **JWT role-staleness class is not architecturally addressed — every new route surface is a fresh exposure** (EXP-197, 198, 199). PR #619 added course lifecycle and curriculum UI actions; R3 immediately filed three new JWT staleness issues on the new surface. 11 instances total in 30 days. A middleware-level DB role-resolution layer is the indicated structural fix; per-route patching continues in the meantime. Decision-Log row added.

4. **PR #619 regression: EXP-196 is High severity and blocks the primary creator workflow** (merged 2026-05-29T17:27Z). The `manageCurriculum` ternary inversion locks all active courses out of the curriculum editor. The gatekeeper security review does not cover UI-layer changes, and this gap is now demonstrably costly (one PR: one logic bug + three JWT staleness exposures). Decision-Log row added.

5. **Realtime sync channel authorization is the new canonical model for multi-channel auth** (PR #612). The `authorizedPostIds` gate pattern (isPublished OR ownership check before any post-scoped query, strict `isChannelRequested` at emit sites, `MAX_CHANNELS` cap) should be the reference implementation for any future realtime subscription feature. Decision-Log row added.

---

## Docs that need updating

- **Error handling guide** — `DomainError` + `safeErrorJson` now canonical (PR #604); guide should document when to throw `DomainError` vs. return a generic 500, and note the `src/lib/**` ESLint gap (EXP-189).
- **Realtime sync endpoint docs** — new auth model (MAX_CHANNELS=20, `authorizedPostIds`, UUID guard, strict `isChannelRequested`) documented; EXP-191/194/195 still open.
- **Docker secrets deployment runbook** — `runtime-secrets.ts` pattern and Prisma migrate container hydration (PR #606) are new; operator runbook needs updating.
- **Course lifecycle API** — new archive/clone/publish/delete endpoints documented (PR #619); EXP-196/197/198/199 still open — note until fixed.
- **Storage architecture** — EXP-134 open (upload-public-asset bucket mismatch); existing R2 write-path docs may be stale post-EXP-77.

---

## Still open

Open agent-filed issues not addressed today:

| # | Title | Severity | Age | Status |
|---|-------|----------|-----|--------|
| EXP-122 | Stale reservation opens 15m–24h quota-bypass window | Medium | 4d | open |
| EXP-124 | Storage reservation DELETE lacks user_id ownership check | Medium | 4d | open |
| EXP-127 | hashtext() advisory lock int32 birthday collision at ~55k users | Medium | 4d | open |
| EXP-129 | Tabby verify/webhook paths bypass KSA geo-restriction | High | 4d | open |
| EXP-134 | R2_BUCKET_STATIC write target misaligned with R2_USER_UPLOADS_PUBLIC_URL | High | 3d | open |
| EXP-135 | R2_BUCKET_CERTIFICATIONS missing from .env.example | High | 3d | open |
| EXP-140 | ZATCA debug event not scoped to DEBUG_ZATCA | Medium | 3d | open |
| EXP-141 | R2 + Redis credentials committed in plaintext to git history | **Critical** | 3d | open — rotate immediately |
| EXP-142 | ZATCA_FORCE flags lack APP_ENV!=production guard | Medium | 3d | open |
| EXP-143 | .claude/agents Bash grant — indirect prompt injection path | Medium | 3d | open |
| EXP-150 | Gatekeeper collateral-close allows silent Linear issue closure | Medium | 2d | open |
| EXP-151 | Routines 07/08 grant Bash+WebFetch to autonomous agents | Medium | 2d | open |
| EXP-173 | R9 allow_unrestricted_git_push on brain without server-side guard | High | 1d | open |
| EXP-176 | CI set -a exports all bake-env credentials | Medium | 1d | open |
| EXP-177 | pgvector:pg16 mutable undigested image tag in production | Medium | 1d | open |
| EXP-189 | src/lib/** globally ESLint-ignored — sink rule can't fire | Medium | <1d | Todo |
| EXP-191 | No rate limiting on realtime sync polling endpoint | Medium | <1d | Todo |
| EXP-194 | Section 3 unbounded DoS amplifier in realtime sync | **High** | <1d | Backlog |
| EXP-195 | Liker userId exposed in realtime polling for public posts | Medium | <1d | Backlog |
| EXP-196 | manageCurriculum button inverted — active courses locked out | **High** | <1d | Backlog |
| EXP-197 | JWT role-staleness on course curriculum module routes | Medium | <1d | Backlog |
| EXP-198 | JWT role-staleness on creator event detail GET | Medium | <1d | Backlog |
| EXP-199 | JWT role-staleness on course lifecycle routes | **High** | <1d | Backlog |

---

## Needs human attention

Items appearing in 3+ consecutive digests still open/in-review, plus critical/high escalations:

1. **Traefik CSP removal — 9th consecutive digest.** `proxy.ts` is the sole authoritative CSP source since 2026-05-22 (Decision-Log). Traefik `headers.contentSecurityPolicy` must be removed. No PR open. Due 2026-06-01.

2. **EXP-141 — CRITICAL: credentials in git history (3rd consecutive digest).** `docker/workers/docker-compose.yml` was deleted from the working tree but R2 API token, R2 secret key, and Redis password remain permanently in the git object store. **Rotate credentials immediately.** Consider BFG/filter-repo history rewrite.

3. **EXP-103 — 5th consecutive digest** (2026-05-24, 25, 26, 28, 29). 5 upload routes still bypass `enforceStorageQuota`. End-to-end quota enforcement incomplete.

4. **EXP-83 — 6th consecutive digest** (2026-05-23, 24, 25, 26, 28, 29). `course_assets` NULL `attachment_id` + NULL `url` rows allowed at the DB level. No PR open.

5. **EXP-127 — 4th consecutive digest** (2026-05-25, 26, 28, 29). `hashtext()` advisory lock int32 birthday collision at ~55k users. Storage ledger correctness at scale depends on this.

6. **EXP-129 — 4th consecutive digest** (2026-05-25, 26, 28, 29). Tabby `verify`/`webhook` bypass KSA geo-restriction. Forged payment completions from non-KSA origins still possible.

7. **EXP-196 — NEW HIGH: primary creator workflow broken (regression from PR #619, merged today).** `manageCurriculum` ternary inverted: all active courses locked out of curriculum editor, archived courses show live curriculum link. Hotfix required before next deploy.

---

## Statistics

| Metric | Count |
|--------|-------|
| New agent-fp issues (stamped in Linear body) | 14 (EXP-183–188, 192–199) |
| New routine-filed issues (manual FP, not stamped) | 8 (EXP-178–182, 189–191) |
| Resolved same-day (of new stamped) | 8 (EXP-183–187 via PR #604; EXP-192–193 via PRs #613/#614; EXP-188 cancelled) |
| Resolved same-day (of manual-FP) | 6 (EXP-178–182, 190) |
| **Total resolved this window** | **20** |
| In-flight (In Review) | 2 (EXP-120, EXP-133) |
| **Merged PRs** | **18** |
| New Decision-Log rows | 3 |
| **Needs human attention** | **7** (Traefik CSP, EXP-141, EXP-103, EXP-83, EXP-127, EXP-129, EXP-196) |

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
