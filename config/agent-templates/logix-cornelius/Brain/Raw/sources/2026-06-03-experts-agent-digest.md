---
title: "2026-06-03 Experts Agent Digest"
date: "2026-06-03"
tags: [agent, digest, project/experts]
category: "daily"
source: "automation"
source_id: "Raw/sources/2026-06-03-experts-agent-digest.md"
---

# Experts Agent Digest — 03 June 2026

**Window:** 2026-06-02T00:00:00Z → 2026-06-03T23:59:59Z  
**Prior digest:** [[Raw/sources/2026-06-02-experts-agent-digest.md]]  
**Updated:** 2026-06-03T21:35Z (late-day R3 batch added — EXP-299–304 + PRs #799/#800/#801)

---

## Summary Table

| Metric | Count |
|--------|-------|
| New agent-fp issues (today) | 11 |
| Resolved since yesterday | 11 |
| In-flight fixes (PR open / In Review) | 3 |
| Merged PRs | 7 |
| Needs human attention | 8 |

---

## New Today

### Morning batch (EXP-291 cluster follow-ups, 09:00–09:30Z)

Issues opened by routines (body contains `<!-- agent-fp:`):

| Issue | Title | FP | Severity | Status |
|-------|-------|-----|----------| ------|
| [EXP-293](https://linear.app/experts/issue/EXP-293) | [security] auth()/getUserPermissions() before try bypasses safeErrorJson — 37-handler class + lint rule | `a5301e354c25` (R3) | Medium | **In Review** |
| [EXP-294](https://linear.app/experts/issue/EXP-294) | [security] Community comment & post author email exposed to unauthenticated callers (PII) | `62b3ed0583aa` (R3) | Medium | Backlog |
| [EXP-295](https://linear.app/experts/issue/EXP-295) | [bug] owner can delete admin-locked post — moderation lock not enforced in DELETE | `4443149a35c8` (R3) | **High** | Backlog |
| [EXP-296](https://linear.app/experts/issue/EXP-296) | [bug] TOCTOU race in PUT /posts/[id] allows non-admin to bypass moderation lock | `b0b5f560f31a` (R3) | Medium | Backlog |
| [EXP-297](https://linear.app/experts/issue/EXP-297) | [bug] TOCTOU in thumbnail upload bypasses moderation lock, orphans R2 assets with permanent quota charge | `1537707518d5` (R3) | Medium | Backlog |
| [EXP-298](https://linear.app/experts/issue/EXP-298) | [security] GET /posts/{id}/comments has no post visibility check — moderated-post comments exposed | `c4214ca6efed` (R3) | Medium | Backlog |

> All 6 are follow-ups from the EXP-291 community hardening cluster (PRs #790, #792, #794). EXP-295/296/297 are direct TOCTOU/lock-gap follow-ups to the new `adminLockedAt` moderation lock (migration `20260603000000_post_admin_locked_at`).

### Evening batch (R3 post-moderation-lock review, 21:20–21:35Z)

| Issue | Title | FP | Severity | Status |
|-------|-------|-----|----------|--------|
| [EXP-299](https://linear.app/experts/issue/EXP-299) | [bug] POST /community/posts/{id}/comments has no rate limit — authenticated spam exhausts DB, notifications, BullMQ | `af2656e7df89` (R3) | **High** | Backlog |
| [EXP-300](https://linear.app/experts/issue/EXP-300) | [bug] POST /internal/upload community case ignores adminLockedAt — moderation lock bypassed via gallery upload | `3d41f56d651f` (R3) | **High** | Backlog |
| [EXP-301](https://linear.app/experts/issue/EXP-301) | [bug] GET /posts/{id}/comments silently truncates beyond 200 — no hasMore signal, oldest comments permanently inaccessible | `00ccd3cef33a` (R3) | Medium | Backlog |
| [EXP-302](https://linear.app/experts/issue/EXP-302) | [bug] exam reset POST non-atomic — concurrent student submission in gap window silently corrupts in-flight exam data | `f9ce9ef4c26c` (R3) | Medium | Backlog |
| [EXP-304](https://linear.app/experts/issue/EXP-304) | [security] Residual git option injection after EXP-279 fix — git fetch missing `--` separator | `e2fb255d8f59` (R3) | Medium | Backlog |

> EXP-303 opened concurrently as a duplicate of EXP-299 (same FP `af2656e7df89`) and immediately closed Duplicate.  
> EXP-299/EXP-300 extend the moderation-lock coverage gap found in EXP-295: comment spam and gallery uploads bypass the same lock.  
> EXP-302 was found while reviewing the EXP-276 fix (PR #801).  
> EXP-304 is a follow-up to EXP-279: the `env:` indirection fix in PR #799 still leaves a `git fetch` call without a `--` separator — a branch named `--upload-pack=cmd` can inject into git's own argv parser (GitHub may block leading-`--` branch names at push time, but the guard is not guaranteed).

---

## Repeated Pattern

From `Raw/agent-state/findings-index.md` — files/symbols appearing 3+ times in last 30 days:

| Pattern | Occurrences (30d) | State |
|---------|------------------|-------|
| `apps/experts-app/app/api/v1/community/posts/[id]/route.ts` | **11 issues** (EXP-241✓, EXP-253✓, EXP-254✓, EXP-277✓, EXP-280✓, EXP-287✓, EXP-288✓, EXP-295 open, EXP-296 open) | Most prior issues resolved today. Two TOCTOU follow-ups remain from new moderation lock. |
| `apps/experts-app/app/api/v1/community/posts/[id]/comments/route.ts` | **7 issues** (EXP-288✓, EXP-289✓, EXP-290✓, EXP-294 open, EXP-298 open, EXP-299 open, EXP-301 open) | GET+POST hardened morning; rate-limit + visibility + pagination still open. |
| `apps/experts-app/src/lib/courses/catalog/handlers/course-submit.handler.ts` | **3 issues** (EXP-234✓, EXP-278 open, EXP-285 folded→EXP-278) | EXP-278 must be fixed atomically with transaction per 2026-06-02 decision. |
| `apps/experts-app/src/lib/ai/ask/ask-ai-assistant.ts` | **4 issues** (EXP-223 open, EXP-232 open, EXP-239✓, EXP-252 open) | Prompt-injection + AskAiDomainError + TOCTOU — all open. |
| **Community API domain (total)** | **20 issues** (EXP-242–304 range) | EXP-291 cluster Done; moderation lock + PII + rate-limit layer is next focus. |
| **`safeErrorJson` bypass class** | EXP-287✓ (seed) → EXP-293 (class: 37 handlers, In Review) → PR #800 (first handler fixed) | EXP-293 In Review. Reject-route fixed by PR #800; lint rule still needed. |
| **`.github/workflows/experts-app.yml` injection class** | EXP-261✓ → EXP-279✓ → EXP-304 (residual `git fetch` argv) | EXP-279 fixed (PR #799); EXP-304 is residual. |

---

## Resolved Since Yesterday

Issues whose Linear status flipped to Done/resolved in the last 24h (11 total):

| Issue | Title | Resolved By | Merged |
|-------|-------|-------------|--------|
| [EXP-291](https://linear.app/experts/issue/EXP-291) | [cluster] Community posts & comments API hardening (umbrella) | PRs #790, #792, #794 | 2026-06-03T09:13Z |
| [EXP-290](https://linear.app/experts/issue/EXP-290) | Comments POST no input validation — unbounded content blobs | PR #794 | 2026-06-03T09:09Z |
| [EXP-289](https://linear.app/experts/issue/EXP-289) | Comments GET unbounded findMany with no cache read — OOM DoS | PR #794 | 2026-06-03T09:09Z |
| [EXP-288](https://linear.app/experts/issue/EXP-288) | Post detail GET unbounded comment fetch OOM DoS | PR #792 | 2026-06-03T07:03Z |
| [EXP-287](https://linear.app/experts/issue/EXP-287) | GET /community/posts/[id] auth() moved outside try block | PR #792 | 2026-06-03T07:03Z |
| [EXP-280](https://linear.app/experts/issue/EXP-280) | Community PUT allows owner to reverse admin unpublish | PR #792 | 2026-06-03T07:03Z |
| [EXP-277](https://linear.app/experts/issue/EXP-277) | Community DELETE has no admin bypass — moderation blocked | PR #792 | 2026-06-03T07:03Z |
| [EXP-286](https://linear.app/experts/issue/EXP-286) | Community posts GET popular/discussed totalPosts incoherent | PR #790 | 2026-06-03T04:45Z |
| [EXP-281](https://linear.app/experts/issue/EXP-281) | Community post creation POST has no rate limit | PR #790 | 2026-06-03T04:45Z |
| [EXP-279](https://linear.app/experts/issue/EXP-279) | GitHub Actions workflow injection via `${{ github.base_ref }}` in migration-immutability | PR #799 | 2026-06-03T09:41Z |
| [EXP-276](https://linear.app/experts/issue/EXP-276) | Exam reset POST no examId→courseId ownership check — BOLA | PR #801 | 2026-06-03T19:35Z |

---

## In-Flight Fixes

| Issue | Title | Status | Since |
|-------|-------|--------|-------|
| [EXP-293](https://linear.app/experts/issue/EXP-293) | auth()/getUserPermissions() before try — 37-handler class + lint rule | **In Review** | 2026-06-03T21:08Z |
| [EXP-120](https://linear.app/experts/issue/EXP-120) | CRON_SECRET timing-safe compare skips check when secret undefined | In Review | carried |
| [EXP-133](https://linear.app/experts/issue/EXP-133) | CRON_AUTH_TOKEN timing-safe compare skips check on undefined | In Review | carried |

---

## Merged PRs

| PR | Title | Closes | Merged |
|----|-------|--------|--------|
| [#789](https://github.com/logi-x/experts/pull/789) | docs(courses): TODO on intentional create-time auto-approve | — (EXP-292 tracking open) | 2026-06-02T23:17Z |
| [#790](https://github.com/logi-x/experts/pull/790) | fix(community): rate-limit post creation + coherent pagination (EXP-281, EXP-286) | EXP-281, EXP-286 | 2026-06-03T04:45Z |
| [#792](https://github.com/logi-x/experts/pull/792) | fix(community): admin moderation + OOM/error hardening on post detail (EXP-277, EXP-280, EXP-287, EXP-288) | EXP-277, EXP-280, EXP-287, EXP-288 | 2026-06-03T07:03Z |
| [#794](https://github.com/logi-x/experts/pull/794) | fix(community): bound + cache-guard comments GET, validate comments POST (EXP-289, EXP-290) | EXP-289, EXP-290 | 2026-06-03T09:09Z |
| [#799](https://github.com/logi-x/experts/pull/799) | fix(ci): prevent workflow injection in migration-immutability job (EXP-279) | EXP-279 | 2026-06-03T09:41Z |
| [#800](https://github.com/logi-x/experts/pull/800) | fix(courses): gate reject-route body parse + auth behind try (EXP-236 / EXP-293 class) | EXP-236 | 2026-06-03T10:00Z |
| [#801](https://github.com/logi-x/experts/pull/801) | fix(creator): validate examId belongs to course before reset (EXP-276) | EXP-276 | 2026-06-03T19:35Z |

Direct commits (routines-agent, no PR):

| SHA | Message | Time |
|-----|---------|------|
| `9857e6e` | fix(email): update email header logo URL to new CDN link | 2026-06-03T07:09Z |
| `bd86dc4` | docs(gitnexus): update SKILL.md PostToolUse hook auto-analyze behavior | 2026-06-03T09:19Z |
| `0bda549` | chore(deps): update graphql and node-releases in pnpm-lock.yaml | 2026-06-03T09:44Z |
| `746b544` | docs(gitnexus): clarify analyze hook behavior and staleness detection | 2026-06-02T22:24Z |
| `609dc5b` | docs(agents,claude): update GitNexus index info (22165 symbols / 40626 relationships) | 2026-06-02T20:22Z |

**Semver: PATCH** — all changes are security/bug fixes, API hardening, CI hardening, and docs updates. No new user-facing features.

---

## Migrations / Env / Infra Changes

**New migration (PR #792):**  
`prisma/migrations/20260603000000_post_admin_locked_at/migration.sql` — adds `adminLockedAt DateTime?` (nullable timestamp) to the `Post` model. Backs the new admin content governance lock: admin unpublish stamps the field, non-admin writes rejected while stamped, admin re-publish clears it.

**CI hardening (PR #799):**  
`.github/workflows/experts-app.yml` migration-immutability job: `${{ github.base_ref }}`, `${{ github.event.before }}`, and `${{ github.event_name }}` moved to `env:` block variables, preventing shell-metacharacter injection from branch names. EXP-304 filed as a residual: the `git fetch` call in the same step still lacks a `--` separator.

No env or Docker/infra changes today.

---

## Architectural Notes

### 1. Post moderation lock — write-coverage gap growing (EXP-295–300)

PR #792 introduced `adminLockedAt` moderation lock on POST.isPublished writes. In-routine security-auditor found incomplete coverage. Five open issues:

- **EXP-295 (High)**: `DELETE` has no lock check — owner deletes a moderated post in 1 request, 100% reproducible.
- **EXP-296 (Medium)**: `PUT` lock check is TOCTOU-vulnerable (~65% race success in 10 concurrent requests).
- **EXP-297 (Medium)**: Thumbnail `POST` has a 50–200ms race window during `arrayBuffer()`+hash; orphans R2 assets with permanent quota charge.
- **EXP-298 (Medium)**: Comments `GET` has no parent-post visibility check; moderated-post thread exposed to unauthenticated callers.
- **EXP-300 (High)**: Internal upload community case has no `adminLockedAt` check — gallery upload bypasses moderation lock entirely.

Fix pattern: `prisma.post.update({ where: { id, adminLockedAt: null }, data: ... })` pushes the predicate into the DB WHERE clause (atomic conditional update). See Decision-Log 2026-06-03 entry.

### 2. EXP-293 class: first handler fixed by PR #800

PR #800 (`fix(courses): gate reject-route body parse + auth behind try`) fixed the courses reject-route as the first of 37 handlers in the EXP-293 class. Pattern corrected: `auth()` and `request.json()` were called before the outermost `try` block; a throw from either bypassed `safeErrorJson`. New funnel inside try: `auth → 401 gate → DB isAdmin → 403 gate → body parse → schema parse`. EXP-293 moved to In Review at 21:08Z; the lint rule (`no-auth-before-try`) and the remaining 36 handlers are the deliverable.

### 3. EXP-279 fixed; EXP-304 residual found immediately

PR #799 moved `${{ github.base_ref }}` etc. into `env:` blocks, closing the RCE vector. R3 scanner found EXP-304: the same step's `git fetch ... $GH_BASE_REF` still lacks a `--` separator. A branch named `--upload-pack=cmd` passes through shell quoting intact but is then parsed by git's own argv parser. Fix: `git fetch --no-tags origin -- "$GH_BASE_REF"`. GitHub may block leading-`--` branch names at push, but this is not a guaranteed hard guard.

### 4. EXP-276 BOLA closed (PR #801)

Exam reset POST now includes `prisma.exam.findUnique({ where: { id: examId, courseId } })` ownership guard, mirroring the sibling GET/DELETE handlers. Closes the cross-course BOLA gap where an instructor could reset another course's exam by crafting the URL. EXP-302 filed simultaneously: the two-step delete (answers then attempts) is non-atomic and vulnerable to mid-gap student submission.

### 5. Rate-limit architecture converging

Three PRs this day establish a per-resource rate-limit tier:
- **Posts POST** (PR #790): `enforcePostCreationRateLimit` — 10/min + 100/day sliding window
- **Comments POST** (EXP-299 open): same pattern needed — `enforceCommentCreationRateLimit`
- **Uploads** (existing): `enforceUploadRateLimit`

The shared pattern (`Redis INCR + TTL sliding window + 429 + Retry-After`) should be extracted into a generic `enforceRateLimit(key, windowSec, maxCount)` helper.

---

## Docs That Need Updating

| File | Required Update |
|------|----------------|
| `apps/experts-app/app/api/v1/community/posts/[id]/route.ts` | EXP-295: add `adminLockedAt` guard in DELETE; EXP-296: wrap PUT lock check atomically |
| `apps/experts-app/app/api/v1/community/posts/[id]/thumbnail/route.ts` | EXP-297: move lock check inside DB transaction (post-hash, not pre-arrayBuffer) |
| `apps/experts-app/app/api/v1/community/posts/[id]/comments/route.ts` | EXP-298: add parent post visibility check + cache invalidation on unpublish; EXP-299: add rate limit; EXP-301: add hasMore/totalCount to GET response |
| `apps/experts-app/app/api/v1/internal/upload/route.ts` | EXP-300: add `adminLockedAt` check in community upload case |
| `apps/experts-app/src/lib/community/` | EXP-294: strip `author.email` from GET payloads and Redis `CommentData`/`PostData` types |
| 37 route handlers (safeErrorJson-audit.md list) | EXP-293: move `auth()`/`getUserPermissions()` inside try; add `no-auth-before-try` ESLint rule |
| `.github/workflows/experts-app.yml` migration-immutability job | EXP-304: add `--` separator to `git fetch` call |
| `apps/experts-app/app/api/v1/creator/courses/[id]/exams/[examId]/reset/route.ts` | EXP-302: wrap two-step delete in `prisma.$transaction` |

---

## Still Open

New today, remaining in Backlog:

| Issue | Title | Severity |
|-------|-------|----------|
| EXP-294 | Community author email PII exposed to unauthenticated callers | Medium |
| EXP-295 | Owner can DELETE admin-locked post — moderation lock incomplete | **High** |
| EXP-296 | TOCTOU race in PUT allows non-admin to bypass moderation lock | Medium |
| EXP-297 | TOCTOU in thumbnail upload — moderation lock bypass + R2 orphan | Medium |
| EXP-298 | GET /posts/{id}/comments has no post visibility check | Medium |
| EXP-299 | POST /comments no rate limit — comment spam exhausts DB/BullMQ | **High** |
| EXP-300 | Internal upload community case ignores adminLockedAt | **High** |
| EXP-301 | GET /posts/{id}/comments silent truncation — no hasMore signal | Medium |
| EXP-302 | Exam reset POST non-atomic — concurrent student submission corrupts data | Medium |
| EXP-304 | Residual git option injection: `git fetch` missing `--` separator | Medium |

EXP-293 is now In Review.

Carried forward (selected high-severity open issues):

| Issue | Title | Severity | Since |
|-------|-------|----------|-------|
| EXP-278 | handleCourseSubmit missing "pending" guard — double-submit | **High** | 2026-06-02 |
| EXP-275 | R2 no automated backup/replication | **High** | 2026-06-02 |
| EXP-274 | Container memory limits + Postgres tuning | **High** | 2026-06-02 |
| EXP-252 | persistAskAiExchange TOCTOU (FOR UPDATE missing) | **High** | 2026-06-01 |
| EXP-262 | No per-user WebSocket connection cap | Medium | 2026-06-01 |
| EXP-223 | AI prompt injection via community post context | Medium | 2026-05-28 |
| EXP-140 | ZATCA invoice no retry on transient errors | **High** | 2026-05-22 |
| EXP-142 | ZATCA invoice XML injection (unescaped chars) | **High** | 2026-05-22 |
| EXP-129 | Tabby KSA geo-gate bypass on verify + webhook | **High** | 2026-05-22 |
| EXP-120 | CRON_SECRET timing-safe compare skips check (in review) | **High** | 2026-05-22 |
| EXP-133 | CRON_AUTH_TOKEN timing-safe compare skips check (in review) | **High** | 2026-05-22 |

---

## Needs Human Attention

Items appearing in 3+ consecutive digests still open, or new high items requiring immediate action:

| Item | In Digest Since | Priority | Action Required |
|------|----------------|----------|-----------------|
| Traefik `headers.contentSecurityPolicy` removal | 2026-05-22 (**14 consecutive digests**) | Medium | **Critically overdue** — `curl -sI https://app.experts.com.sa/en \| grep -i content-security` |
| [EXP-141](https://linear.app/experts/issue/EXP-141) R2 API token + Redis password in git history | 2026-05-26 (9 digests) | **Critical** | BFG/filter-repo history rewrite + token rotation still outstanding |
| [EXP-103](https://linear.app/experts/issue/EXP-103) 5 upload routes missing enforceStorageQuota | 2026-05-24 (11 digests) | High | Depends on EXP-80 ledger; no PR open |
| [EXP-129](https://linear.app/experts/issue/EXP-129) Tabby webhook KSA geo-gate bypass | 2026-05-25 (10 digests) | High | Enforce geo-restriction on verify + webhook paths |
| [EXP-127](https://linear.app/experts/issue/EXP-127) Advisory lock birthday collision at ~55k users | 2026-05-25 (10 digests) | Medium | Pre-launch migration to 64-bit key |
| [EXP-223](https://linear.app/experts/issue/EXP-223) AI prompt injection via community post context | 2026-05-28 (7 digests) | Medium | XML-tag separation still needed after newline guard (PR #706) |
| [EXP-295](https://linear.app/experts/issue/EXP-295) Owner can DELETE admin-locked post | Today | **High** | Immediate: 1-line atomic guard in DELETE handler; moderation fully defeated without it |
| [EXP-304](https://linear.app/experts/issue/EXP-304) Residual git option injection in CI | Today | Medium | Add `--` separator to `git fetch` in migration-immutability job |

---

## Source References

- Commits on `logi-x/experts main` today: PRs #789–#801 range + 5 direct routines-agent commits
- Linear issues filed today: EXP-293–304 (11 unique; EXP-303 closed duplicate)
- Linear issues resolved today: EXP-277, EXP-279, EXP-280, EXP-281, EXP-286, EXP-287, EXP-288, EXP-289, EXP-290, EXP-291, EXP-276 (11 total)
- Prior digest: [[Raw/sources/2026-06-02-experts-agent-digest.md]]
- Findings index: [[Raw/agent-state/findings-index.md]] (read-only)

---

_Generated by automated digest routine. Updated 21:35Z with late-day R3 batch (EXP-299–304). EXP-291 community hardening cluster completed (3 file-scoped PRs, 9 issues resolved). EXP-279 (CI injection) + EXP-276 (exam reset BOLA) both resolved in afternoon. New moderation-lock coverage gaps (EXP-295–300) are immediate follow-ups to the adminLockedAt schema addition. EXP-293 (37-handler auth-before-try class) moved In Review; first handler fixed by PR #800. Two Decision-Log entries added (adminLockedAt atomic writes, auth-before-try lint rule)._

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
