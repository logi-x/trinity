---
title: "2026-05-31 Experts Agent Digest"
date: "2026-05-31"
tags: [agent, digest, project/experts]
category: "daily"
source: "automation"
source_id: "Raw/sources/2026-05-31-experts-agent-digest.md"
---

# Experts Agent Digest — 31 May 2026

**Window:** 2026-05-31T00:00:00Z → 2026-05-31T23:59:59Z  
**Prior digest:** [[Raw/sources/2026-05-30-experts-agent-digest.md]]

---

## Summary Table

| Metric | Count |
|--------|-------|
| New agent-fp issues (today) | 13 |
| Other new routine issues (today) | 6 |
| Resolved since yesterday | 19 |
| In Progress | 0 |
| Merged PRs | 17 |
| Needs human attention | 8 |

---

## New Today

Issues opened by routines (body contains `<!-- agent-fp:`):

| Issue | Title | FP | Severity | Status |
|-------|-------|-----|----------|--------|
| [EXP-226](https://linear.app/experts/issue/EXP-226) | [spinoff: EXP-213] course-create hardcodes `approvalStatus: "approved"` | `c44abea9d11a` (R5) | — | Backlog |
| [EXP-227](https://linear.app/experts/issue/EXP-227) | [infra] CI guard for Prisma schema↔migration drift | — | Medium | Done (same-day) |
| [EXP-228](https://linear.app/experts/issue/EXP-228) | [refactor] Ask AI button visibility: replace deny-list with allow-list | `cab2a2be679d` (R3) | Low | Done (same-day) |
| [EXP-229](https://linear.app/experts/issue/EXP-229) | [bug] Storage orphan-reaper has no environment isolation | `b5515fe4d993` (R3) | **Urgent** | Done (same-day) |
| [EXP-230](https://linear.app/experts/issue/EXP-230) | [bug] community-thumbnail & lesson-video uploads are PUT-first | `34d82d6b179c` (R3) | Medium | Done (same-day) |
| [EXP-231](https://linear.app/experts/issue/EXP-231) | [chore] Decommission the R2 orphan reaper | `010c9bb2c1f6` (R3) | Low | Done (same-day) |
| [EXP-232](https://linear.app/experts/issue/EXP-232) | [security] AI ask: client-supplied history injected verbatim when `conversationId` provided | `9a5c624e3966` (R3) | Medium | Backlog |
| [EXP-233](https://linear.app/experts/issue/EXP-233) | [security] BOLA: quiz DELETE uses global `isInstructor` without course-ownership check | `fafff305ee80` (R3) | **High** | Backlog |
| [EXP-239](https://linear.app/experts/issue/EXP-239) | Ask AI verify-then-persist non-atomic; soft-deleted conversations receive new messages | `638309d92b06` (R3) | Medium | Done (same-day) |
| [EXP-240](https://linear.app/experts/issue/EXP-240) | [spinoff: EXP-224] PUT /community/posts/[id] postUpdateBodySchema unguarded | `e89728f8ca7d` (R5) | Medium | Done (same-day) |
| [EXP-241](https://linear.app/experts/issue/EXP-241) | [bug] Community posts PUT uses JWT-derived `isAdmin` — revoked admin edits/pins any post | `f64b4f6e1ec5` (R3) | **High** | Backlog |
| [EXP-242](https://linear.app/experts/issue/EXP-242) | [bug] Community posts GET loads all posts without limit for popular/discussed sort — OOM DoS | `05d28729883a` (R3) | **High** | Backlog |
| [EXP-243](https://linear.app/experts/issue/EXP-243) | [security] Community posts GET: user-supplied limit uncapped on recent sort — unauthenticated DoS | `16a2b03d4ed4` (R3) | Medium | Backlog |
| [EXP-244](https://linear.app/experts/issue/EXP-244) | [security] Ask AI POST accepts unverified client-supplied history — fabricated assistant turns enable prompt injection | `9466e12a2635` (R3) | Medium | Backlog |

Other routine-authored issues (no agent-fp in visible body):

| Issue | Title | Severity | Status |
|-------|-------|----------|--------|
| [EXP-234](https://linear.app/experts/issue/EXP-234) | Instructor can re-submit an approved course, silently resetting admin approval | High | Backlog |
| [EXP-235](https://linear.app/experts/issue/EXP-235) | Admin can approve a rejected course directly, bypassing re-submission requirement | Medium | Backlog |
| [EXP-236](https://linear.app/experts/issue/EXP-236) | reject route parses request body before auth check and outside the try block | Medium | Backlog |
| [EXP-237](https://linear.app/experts/issue/EXP-237) | Ask AI accepts client-supplied history verbatim, enabling prompt context injection | Medium | Backlog |
| [EXP-238](https://linear.app/experts/issue/EXP-238) | Lesson video DELETE has no `userId` filter on attachment lookup | **High** | Backlog |

> Notes: EXP-237 and EXP-232/EXP-244 share the same root cause (`buildOpenAiMessages` passes client-supplied `history` verbatim) — three separate scanner hits on the same function within 12 hours. EXP-236 is the same body-parse-before-auth class as EXP-210 (resolved PR #678). EXP-241 is the JWT role-staleness class spreading to community domain routes.

---

## Repeated Pattern

| Pattern | Count (30d) | Current state |
|---------|------------|---------------|
| **JWT role-staleness** (session.user.isAdmin / JWT roles without DB re-derivation) | 16+ instances | EXP-241 is the first community-domain instance. Course routes have a canonical fix (`getDbCourseActor`); community routes lack one. The structural infrastructure fix remains deferred (2026-05-29 decision). Per-route patching is accepted interim posture. |
| **Unbounded `findMany` / missing `take:` bounds** | 5 instances (EXP-194, EXP-208, EXP-226, EXP-242, EXP-243) | EXP-242 (`take:undefined` for popular/discussed) and EXP-243 (user-supplied `limit` uncapped) both hit the same community posts GET handler same day — systemic gap confirmed. |
| **Client-supplied AI history verbatim injection** | 3 instances (EXP-232, EXP-237, EXP-244) | All three hit `buildOpenAiMessages` in `ask-ai-assistant.ts`. Three scanner hits within 12 hours. Fix should address all three together. |
| **Body-parse before auth guard** | 2 instances (EXP-210, EXP-236) | EXP-210 resolved (PR #678). EXP-236 filed same class 2 days later. A targeted ESLint rule (`request.json()` before `getServerSession`) is warranted. |

---

## Resolved Since Yesterday

| Issue | Resolved By | Notes |
|-------|-------------|-------|
| EXP-209 | PR #654 | JWT staleness — GET /courses/[id] |
| EXP-210 | PR #678 | Body-parse before auth in publish route |
| EXP-211 | PR #681 | Modules list trusts JWT `isAdmin` |
| EXP-212 | PR #684 | Lesson/quiz subroutes JWT staleness (4 routes) |
| EXP-213 | PR #678 | Course-create JWT staleness (attempt 2) |
| EXP-215 | (resolved) | share-utils `FALLBACK_BASE_URL` staging URL |
| EXP-220 | PR #679 | **DEPLOYMENT BLOCKER resolved** — `ask_ai_conversations.deleted_at` migration shipped |
| EXP-225 | PR #676 | Login UX whole-app remount regression |
| EXP-227 | PR #681 | CI Prisma migration-drift guard — opened and closed same day |
| EXP-228 | PR #685 | Ask AI deny-list refactor — opened and closed same day |
| EXP-229 | PR #687 | R2 orphan reaper env isolation — opened and closed same day |
| EXP-230 | PR #690 | Last PUT-first upload route — opened and closed same day |
| EXP-221 | PR #692 | AI conversation [id] route UUID guard + try/catch |
| EXP-206 | PR #694 | AI conversation management rate-limiting |
| EXP-222 | PR #695 | AskAiSessionProvider loadConversation stream/load race |
| EXP-231 | PR #691 | R2 orphan reaper decommissioned — opened and closed same day |
| EXP-239 | PR #705 | Ask AI verify-then-persist non-atomic — opened and closed same day |
| EXP-224 | PR #706 | Community posts POST input validation |
| EXP-240 | PR #706 | Community posts PUT validation bypass — opened and closed same day |

**19 resolved** this window. Yesterday's deployment blocker (EXP-220) resolved. The upload-ordering class (PUT-first) is fully closed — 5/5 routes converted.

---

## In-Flight Fixes

No issues remain in progress at end of window. All four issues that were in-flight at start of day (EXP-221, EXP-222, EXP-224, EXP-231) are resolved.

---

## Merged PRs

| PR | Title | Closes |
|----|-------|--------|
| #667 | chore(infra): remove redundant `NEXT_PUBLIC_SITE_URL`/`NEXT_SITE_URL` env vars | EXP-219 |
| #673 | fix(courses): set `approvalStatus` to `pending` on course submit | EXP-214 |
| #676 | fix(auth): stop whole-app remount on auth change breaking login UX | EXP-225 |
| #678 | fix(courses): DB-fresh role lookup on course-create route (attempt 2) | EXP-213 |
| #679 | fix(ai): ship `ask_ai_conversations.deleted_at` migration + fix `.gitignore` | EXP-220 |
| #681 | ci(prisma): migration-drift guard — shadow-DB `prisma migrate diff` in CI | EXP-227 |
| #682 | fix(agents): disable R9 + remove `allow_unrestricted_git_push` until EXP-158 ships | EXP-173 |
| #684 | fix(courses): DB-authoritative roles across all `[moduleId]` lesson/quiz sub-routes | EXP-212 |
| #685 | feat(ai): replace Ask AI route deny-list with layout-based allow-list | EXP-228 |
| #687 | fix(storage): fail-closed env-isolation gate on R2 orphan reaper | EXP-229 |
| #690 | fix(storage): community-thumbnail & lesson-video uploads pending-first | EXP-230 |
| #691 | chore(storage): decommission R2 orphan reaper + PUT-first guardrail | EXP-231 |
| #692 | fix(ai): harden AI conversation [id] route — UUID guard + try/catch | EXP-221 |
| #694 | fix(ai): rate-limit AI conversation management endpoints | EXP-206 |
| #695 | fix(ai): abort stream before loading a conversation | EXP-222 |
| #705 | fix(ai): re-check soft-delete in-tx before persisting Ask AI exchange | EXP-239 |
| #706 | fix(community): shared Zod schema for post create+update | EXP-224, EXP-240 |

**Semver: MINOR** — PR #685 (Ask AI allow-list, behaviour change for layouts) ships new user-facing behaviour. Remaining PRs are security/bug fixes and chores. Operator actions required before deploy: run `prisma migrate deploy` (PR #679); verify reaper cron removed from external schedulers (PR #691); confirm `NEXT_PUBLIC_SITE_URL`/`NEXT_SITE_URL` not referenced in nginx/traefik configs (PR #667); update CI workflow references to `migration-drift-scanner` (commit `45fceafc`).

---

## Migrations / Env / Infra Changes

**Database migration (PR #679 — EXP-220):**
Added `prisma/migrations/20260531000001_add_ask_ai_conversations_deleted_at/migration.sql`. Fixed `.gitignore`: blanket `*.sql` exclusion was silently swallowing Prisma migration SQL; scoped negation `prisma/migrations/**/*.sql` added so migration files can no longer be accidentally dropped.

**Environment variables (PR #667 — EXP-219):**
Removed `NEXT_PUBLIC_SITE_URL` and `NEXT_SITE_URL` from all compose files. Both held identical values to `NEXT_PUBLIC_APP_URL`.

**R2 orphan reaper decommissioned (PR #691 — EXP-231):**
The `reapR2Orphans` cron route, schedule, and feature flag are removed entirely. The pending-first upload invariant (PR #690, all 5 routes) replaces the reactive cleanup approach. Pre-existing orphans were cleaned by the reaper before decommission.

**R2 orphan reaper env gate (PR #687 — EXP-229):**
Added `APP_ENV` isolation check before decommission — ensured the reaper never ran cross-environment in the final cleanup pass.

**Agent configuration (PR #682 — EXP-173):**
Disabled R9 brain-auditor agent; removed `allow_unrestricted_git_push: true` from its definition. R9 cannot run until EXP-158 (brain pre-receive push guard) deploys.

**CI workflow fix (commit `45fceafc`):**
Updated `migration-drift` CI job runner from `code-version-reporter` to `migration-drift-scanner`. Corrects the tool reference added in PR #681.

---

## Architectural Notes

1. **AI ask input validation hardened by construction.** PR #706 closes EXP-224 (POST) and EXP-240 (PUT bypass) by introducing a shared Zod schema for community post create+update. This is the canonical pattern for ensuring PUT/PATCH handlers cannot re-introduce post-create bypasses: extract a shared schema and compose it in both handlers. EXP-241 (community JWT isAdmin) is the next open item for this file.

2. **Community domain: JWT staleness class now present.** EXP-241 (community posts PUT isAdmin from JWT) is the first confirmed instance in community routes. The `getDbCourseActor` helper is course-scoped. A `getDbCommunityActor` equivalent is needed to close EXP-241 and prevent recurrence. See new Decision-Log row (2026-05-31).

3. **AI conversation history injection — three simultaneous scanner hits.** EXP-232 (09:29Z), EXP-237 (09:34Z), and EXP-244 (21:39Z) all report `buildOpenAiMessages` passing client-supplied `history` verbatim to OpenAI. The fix for EXP-232 must simultaneously close EXP-237 and EXP-244 (same root cause). See new Decision-Log row (2026-05-31).

4. **Community posts GET: two unbounded query patterns, same handler.** EXP-242 (`take:undefined` for popular/discussed sort) and EXP-243 (user-supplied `limit` uncapped for recent sort) were both filed today from `app/api/v1/community/posts/route.ts`. Two issues in one day on one file signals a systemic unbounded-query gap. Both must be fixed together. See new Decision-Log row (2026-05-31).

5. **R2 orphan reaper decommissioned — reactive cleanup approach retired.** PR #691 removes the reaper entirely. The storage layer now relies on invariant enforcement at write time (pending-first), not compensating cleanup at scan time. Any new upload route must follow pending-first — enforced by code review and the storage-pending-reaper cron.

6. **Body-parse before auth: recurring pattern.** EXP-236 (reject route) is the second instance in 2 days after EXP-210 (publish route, resolved PR #678). A targeted ESLint rule (`request.json()` before `getServerSession` in route handlers) would eliminate recurrence at the class level. Not yet scheduled.

---

## Docs That Need Updating

| File | Required update |
|------|---------------|
| `apps/experts-app/prisma/` — migration guide or `CONTRIBUTING.md` | Document forward-only migration rule + new CI drift guard + `.gitignore` fix |
| `.env.example` / deployment docs | Add `APP_ENV` with description (required by R2 orphan reaper env gate, EXP-229) |
| `apps/experts-app/src/components/ai/AskAiAssistant.tsx` | Document allow-list opt-in pattern for layouts (EXP-228) |
| Brain `.claude/agents/` docs or `CLAUDE.md` | R9 disabled; note EXP-158 as re-enable prerequisite |
| Storage architecture docs | Note reaper decommission; pending-first is now sole orphan-prevention mechanism |
| Community routes / API docs | EXP-241 (JWT staleness PUT), EXP-242/243 (unbounded GET) open — mark as pending fix |

---

## Still Open

New today, still in Backlog:

| Issue | Title | Severity |
|-------|-------|----------|
| EXP-226 | course-create hardcodes `approvalStatus: "approved"` | — |
| EXP-232 | AI ask: client-supplied history injected verbatim (fix with EXP-237 + EXP-244) | Medium |
| EXP-233 | BOLA: quiz DELETE global `isInstructor` | **High** |
| EXP-234 | Instructor re-submit resets admin approval | **High** |
| EXP-235 | Admin approve rejected course directly | Medium |
| EXP-236 | reject route body-parse before auth | Medium |
| EXP-237 | Ask AI client history verbatim (same class as EXP-232/244) | Medium |
| EXP-238 | Lesson video DELETE no `userId` ownership check | **High** |
| EXP-241 | Community posts PUT JWT-derived `isAdmin` | **High** |
| EXP-242 | Community posts GET unbounded for popular/discussed sort | **High** |
| EXP-243 | Community posts GET user-supplied `limit` uncapped on recent sort | Medium |
| EXP-244 | Ask AI POST unverified client history (same class as EXP-232/237) | Medium |

Carried forward from prior days:

| Issue | Title | Severity | Since |
|-------|-------|----------|-------|
| EXP-223 | Unescaped post titles in AI learner context | Medium | 2026-05-28 |

---

## Needs Human Attention

Items appearing in 3+ consecutive digests still open, or new high-severity issues requiring immediate action:

| Item | In Digest Since | Priority | Action |
|------|-----------------|----------|--------|
| Traefik CSP header removal | 2026-05-22 (9 consecutive digests) | Medium | `curl -sI https://app.experts.com.sa/en \| grep -i content-security` |
| EXP-141 — R2 API token + Redis password committed in git history | 2026-05-26 (5 digests) | **Critical** | BFG/filter-repo history rewrite + token rotation outstanding |
| EXP-103 — 5 upload routes missing `enforceStorageQuota` guard | 2026-05-24 (6+ digests) | High | Depends on EXP-80 ledger; no PR open |
| EXP-127 — Advisory lock birthday collision at ~55k users | 2026-05-25 (5+ digests) | Medium | Pre-launch migration to 64-bit key |
| EXP-129 — Tabby webhook KSA geo-gate bypass | 2026-05-25 (5+ digests) | High | Enforce geo-restriction on verify/webhook paths |
| EXP-233 — BOLA: quiz DELETE *(new 2026-05-31)* | 2026-05-31 | **High / security** | Add `assertCourseWriteAccess` to quiz DELETE handler |
| EXP-238 — Lesson video DELETE cross-instructor deletion *(new 2026-05-31)* | 2026-05-31 | **High** | Add `userId` filter to attachment lookup in DELETE handler |
| EXP-241 — Community posts PUT JWT staleness *(new 2026-05-31)* | 2026-05-31 | **High** | Re-derive actor role from DB in PUT /community/posts/[id]; follow `getDbCourseActor` pattern |

---

## Changes vs Yesterday

| Metric | 2026-05-30 | 2026-05-31 | Delta |
|--------|-----------|-----------|-------|
| New agent-fp issues | 18 | 13 | — |
| Other routine issues | 5 | 6 | +1 |
| Resolved | 16 | 19 | +3 |
| Merged PRs | 15 | 17 | +2 |
| In Progress at EOD | 1 | 0 | -1 (all in-flight resolved) |
| Human attention items | 6 | 8 | +2 (EXP-241 community JWT; community GET DoS class) |

Key shifts: EXP-220 deployment blocker resolved. Upload-ordering class fully closed (5/5 routes). JWT staleness class expanded from course domain to community domain (EXP-241). AI history injection class confirmed with 3 scanner hits (EXP-232/237/244). Community posts GET has two separate unbounded query issues in the same handler (EXP-242/243).

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
