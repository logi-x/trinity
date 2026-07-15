---
title: "Experts Agent Digest — 30 May 2026"
date: "2026-05-30"
window_start: "2026-05-29T17:27:00Z"
window_end: "2026-05-30T23:59:59Z"
tags: ["digest", "project/experts", "agent", "2026-05"]
category: "digest"
source: "automation"
---

# Experts Agent Digest — 30 May 2026

**Window:** 2026-05-29T17:27:00Z → 2026-05-30T23:59:59Z
**Prior digest:** [[Raw/sources/2026-05-29-experts-agent-digest.md]]
**Branch:** `digest/2026-05-30` — PR #11

---

## Summary Table

| Metric | Count |
|--------|-------|
| New agent-fp issues | 18 |
| Other new issues | 5 |
| Resolved since yesterday | 16 |
| In Progress | 1 |
| Merged PRs | 15 |
| Needs human attention | 6 |

---

## Deployment Blocker

**EXP-220 — `ask_ai_conversations.deleted_at` column missing migration**

The `deleted_at` column is referenced in AI conversation query code but was never added via a Prisma migration. AI conversation continuation and history are broken. Any deploy that runs pending migrations will succeed structurally, but runtime queries will fail.

**Required action:** Add `prisma/migrations/<timestamp>_add_ask_ai_conversations_deleted_at/migration.sql` with `ALTER TABLE ask_ai_conversations ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP(3);`. Do not modify any already-applied migration.

---

## Merged PRs (15)

| PR | Title | Closes |
|----|-------|--------|
| #627 | fix: add APP_BASE_URL to cron-sidecar explicit environment block | EXP-175 |
| #629 | refactor: consolidate src/lib/auth.ts orphans into src/lib/auth/ package | EXP-200 |
| #630 | fix: resolve-storage-tier fallback when no active subscription | EXP-201 |
| #636 | chore: un-ignore src/lib for error-disclosure ESLint rule; fix ~44 lint errors | EXP-189 |
| #637 | fix: add take:N orderBy:desc pagination to getAskAiConversationForUser | EXP-205 |
| #638 | fix: replace error.message with opaque code in streamAskAiQuestion catch | EXP-207 |
| #639 | fix: replace broad no-restricted-syntax suppressions in embed services | EXP-203 |
| #640 | fix: add integration tests for resolve-storage-tier.ts | EXP-202 |
| #643 | fix: remove staging URL fallback from getBaseUrl() in src/lib/utils.ts (partial) | EXP-204 partial |
| #649 | fix: apply checkAskAiRateLimit in authorizeAskAiSession | EXP-206 partial |
| #654 | fix: re-derive admin role from DB in GET course handler | EXP-209 |
| #655 | fix: strip userId from liker objects in realtime likes-changed events | EXP-208 |
| #658 | refactor: introduce getDbCourseActor shared helper for DB-fresh course route auth | EXP-197, EXP-199 |
| #664 | fix: fix course-submit hardcoded approvalStatus=approved | EXP-214 |
| #665 | feat: establish src/lib/config/app-url.ts as canonical app origin resolver | EXP-204, EXP-216, EXP-217, EXP-218 |

---

## New Agent-FP Issues (18)

### Closed Same-Day (8)

| Issue | Title | Severity | Closed By |
|-------|-------|----------|-----------|
| EXP-204 | getBaseUrl() staging URL hardcoded fallback | High | PR #665 |
| EXP-205 | askAiConversation unbounded payload / no pagination | Medium | PR #637 |
| EXP-207 | SSE stream exposes Prisma errors via error.message | Medium | PR #638 |
| EXP-208 | likes channel exposes liker userId to anonymous callers | Medium | PR #655 |
| EXP-209 | GET course handler trusts JWT isAdmin without DB check | High | PR #654 |
| EXP-216 | getSitemapBaseUrl uses X-Forwarded-Host header | Medium | PR #665 |
| EXP-217 | es-auth layout hardcodes staging.experts.com.sa | Medium | PR #665 |
| EXP-218 | 14 metadata/modules files use staging URL fallback | Medium | PR #665 |

### Still Open (10)

| Issue | Title | Severity | Notes |
|-------|-------|----------|-------|
| EXP-206 | AI conversations missing rate limit | Medium | PR #649 partial — needs full per-route enforcement |
| EXP-210 | Publish route parses body before auth check | Medium | JWT staleness spinoff |
| EXP-211 | Modules list trusts JWT isAdmin | Medium | JWT staleness spinoff |
| EXP-212 | Lesson/quiz subroutes JWT staleness | Medium | JWT staleness spinoff — 4 routes |
| EXP-213 | Course-create trusts JWT isAdmin | Medium | JWT staleness spinoff |
| EXP-215 | share-utils getShareUrl() staging URL fallback | Medium | Missed by PR #665 sweep |
| EXP-219 | Remove redundant env vars from cron-sidecar compose | Low | In Progress |
| EXP-220 | **DEPLOYMENT BLOCKER:** deleted_at migration missing | High | AI conversation history broken |
| EXP-221 | AI conversation routes missing try/catch | Medium | Unhandled rejection risk |
| EXP-222 | AskAiSessionProvider loadConversation race condition | Medium | Client-side race on navigation |

---

## Other New Issues (5)

| Issue | Title | Severity | Status |
|-------|-------|----------|--------|
| EXP-200 | auth.ts + auth-context.tsx + auth-utils.ts orphans in src/lib/ | Medium | Closed — PR #629 |
| EXP-201 | resolve-storage-tier.ts throws when no active subscription | Medium | Closed — PR #630 |
| EXP-202 | resolve-storage-tier.ts missing integration tests | Medium | Closed — PR #640 |
| EXP-203 | no-restricted-syntax suppressions in embed/embedding-sync services | Low | Closed — PR #639 |
| EXP-219 | Remove redundant NEXT_PUBLIC_APP_URL from cron-sidecar compose | Low | In Progress |

---

## Resolved Since Yesterday (16)

| Issue | Resolved By |
|-------|-------------|
| EXP-189 | PR #636 (un-ignore src/lib for error-disclosure ESLint rule) |
| EXP-197 | PR #658 (getDbCourseActor shared helper) |
| EXP-199 | PR #658 (getDbCourseActor shared helper) |
| EXP-200 | PR #629 (auth package consolidation) |
| EXP-201 | PR #630 (storage-tier fallback fix) |
| EXP-202 | PR #640 (integration tests) |
| EXP-203 | PR #639 (ESLint suppression cleanup) |
| EXP-204 | PR #665 (canonical app-URL — class closed) |
| EXP-205 | PR #637 (AI conversation pagination) |
| EXP-207 | PR #638 (SSE error opaque code) |
| EXP-208 | PR #655 (strip liker userId) |
| EXP-209 | PR #654 (DB-fresh role check in GET course) |
| EXP-214 | PR #664 (fix hardcoded approvalStatus) |
| EXP-216 | PR #665 (canonical app-URL sweep) |
| EXP-217 | PR #665 (canonical app-URL sweep) |
| EXP-218 | PR #665 (canonical app-URL sweep) |

---

## Repeated Pattern: JWT Role-Staleness

**14 total instances filed in 30 days; 8 new spinoffs today (EXP-209–215 from PR #619).**

PR #619 (course lifecycle expansion) merged at 2026-05-29T17:27Z — the start of today's window — and immediately produced 8 new staleness instances. PR #658 resolved EXP-197/199 via the `getDbCourseActor` shared helper, which is now the canonical pattern for course route auth. Open spinoffs: EXP-210, 211, 212, 213, 215.

Infrastructure-level fix (middleware-layer DB role resolution) remains deferred — see 2026-05-29 decision log entry. Per-route patching continues as the accepted interim posture.

---

## Architectural Class Closed: Canonical App URL (PR #665)

`src/lib/config/app-url.ts` is now the single source of truth for the app's public origin. Closed 4 issues (EXP-204, 216, 217, 218).

- `getAppBaseUrl()` — throws in production if `NEXT_PUBLIC_APP_URL` absent (fail-closed)
- `getPublicBaseUrl()` — returns `undefined` in SSG/build contexts (safe for SEO meta)
- ESLint rule bans `staging.experts.com.sa` literal in `app/**` and `src/lib/**`

PR #643 (attempt 1) used an `APP_BASE_URL` fallback env var; PR #665 rejected that — any fallback permits misconfigured builds to mint broken internal Docker URLs silently. Throwing at first request surfaces the misconfiguration immediately.

EXP-215 (`share-utils` staging fallback) was missed by this sweep and remains open.

---

## Architectural Signal: getDbCourseActor Canonical Pattern (PR #658)

PR #658 introduced `getDbCourseActor(courseId, userId)` as the shared helper for DB-fresh role lookup on course routes. All new course routes must use this helper rather than inline DB queries or JWT claims. Existing routes patched in prior days (EXP-197, EXP-199) consolidated onto this helper.

---

## Error-Disclosure Class: Fully Closed

PR #604 (ESLint sink + `safeErrorJson` sweep) and PR #636 (un-ignore `src/lib/**`) together close all known instances of `error.message` reaching production responses. ESLint `no-restricted-syntax` rule now fires on `src/lib/**` — the known gap from EXP-189 is resolved.

---

## Needs Human Attention (6)

| Item | Reason | Priority |
|------|--------|----------|
| Traefik CSP header removal | 7 consecutive digests — confirm removed: `curl -sI https://app.experts.com.sa/en \| grep -i content-security` | Medium |
| EXP-141 | R2 token + Redis password committed in git history; BFG rewrite outstanding | Critical |
| EXP-103 | 5 upload routes not yet on `enforceStorageQuota` guard | High |
| EXP-83 | VALIDATE constraint on `course_assets` table | Low |
| EXP-127 | Advisory lock key birthday collision at ~55k users | Medium |
| EXP-129 | Tabby webhook geo-gate bypass | High |

**EXP-220** (DEPLOYMENT BLOCKER) is listed separately above — requires a migration before next deploy.

---

## Changes vs Yesterday's Digest

| Metric | 2026-05-29 | 2026-05-30 | Delta |
|--------|-----------|-----------|-------|
| New agent-fp issues | 14 | 18 | +4 (JWT staleness spinoffs from PR #619) |
| Resolved | 20 | 16 | —  |
| Merged PRs | 18 | 15 | — |
| Human attention items | 7 | 6 | -1 (EXP-196 closed) |

EXP-196 (manageCurriculum ternary inverted, High) confirmed resolved — was filed and closed within the prior window.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
