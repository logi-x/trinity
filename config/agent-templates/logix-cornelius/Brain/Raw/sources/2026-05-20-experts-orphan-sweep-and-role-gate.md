---
title: Experts — Orphan-Attachment Sweep + Role-Gate Cleanup + Cron-Sidecar Pivot (20 May 2026)
date: 2026-05-20
tags: [project/experts-app, session, storage, janitor, workers, refactor, cron, architecture, project/experts]
related:
  - "[[Raw/sources/2026-05-19-experts-post-refactor-bug-fixes.md]]"
  - "[[Raw/sources/2026-05-15-experts-security-incident-sweep-session]]"
  - "[[Wiki/Concepts/Prisma]]"
---

# Orphan-Attachment Sweep + Role-Gate Cleanup

Followup to the AI code review on PR #334 / #336 — the two architectural findings deferred from `#336` (review items **#6** role-gating duplication and **#8** file-orphan cleanup) and the deployment gap they exposed in the storage janitor.

Branch: `fix/orphan-attachment-sweep-and-role-gate-20260520`. PR **#337**.

## What shipped

| Commit | Scope |
|---|---|
| `9cd12c2d` | **#6** — drop redundant session-role pre-filter on lesson-asset handlers; rely solely on `assertCourseWriteAccess` |
| `9a24959c` | **#8** — orphan-attachment sweep + cron-triggered deployment pivot |

## #6 — role-gating: layered → single gate

The three lesson-asset handlers (create / delete / list) had a two-layer pattern:

1. JWT `isInstructor`/`isAdmin` pre-filter (cheap, no DB).
2. `assertCourseWriteAccess` guard (authoritative — `CourseInstructor` table lookup).

Layer 1 was defensive but introduced a drift risk: a user with a `CourseInstructor` row but no `instructor` string in their JWT roles would be wrongly blocked. The guard already handles the admin bypass and is O(1) on the indexed `(courseId, userId)` lookup, so the saved roundtrip is negligible.

Removed layer 1 from all three handlers + their route files + their tests. Replaced the three "neither instructor nor admin" tests with "course-access guard rejects" tests — same outcome from the user's perspective, but tests the real gate.

## #8 — file-orphan sweep + the deployment gap discovery

Investigated the existing `storage-janitor.worker.ts` (added 2026-05-13 as part of incident #5) and discovered **it has never been deployed in staging or production**. Why:

- `Dockerfile.worker` installs from `package.worker.json`, which explicitly excludes Prisma. The other workers (pdf, zatca, ai) are pure-compute on Redis/BullMQ — they don't read the DB.
- The storage janitor needs DB access by design (it deletes File / Attachment rows).
- So the worker would crash at runtime on Prisma import.
- And there was no `experts-stg-storage-janitor-worker` compose service anyway.

So both the pending-file sweep AND any new orphan sweep would have been dead code in prod under the original "add a worker docker service" plan.

The fix aligns with the **cron-sidecar pattern** documented in Decision-Log 2026-04-27: scheduled jobs hit internal API routes from `experts-stg-cron` (Alpine + crond + curl). Every other scheduled job in the platform (embedding sync, recommendation refresh, knowledge sync, payment reconciliation) uses this lane.

Restructure:

- **`storage-janitor.sweeps.ts`** (NEW) — pure sweep functions, no BullMQ Worker instantiation. Safe to import from anywhere.
- **`storage-janitor.worker.ts`** (slimmed) — thin BullMQ wrapper, re-exports the pure functions for backwards compatibility with existing tests.
- **`/api/v1/internal/storage-janitor/sweep/route.ts`** (NEW) — POST endpoint, CRON_SECRET bearer auth.
- **`/api/v1/internal/storage-janitor/orphan-sweep/route.ts`** (NEW) — same shape.
- **`docker/staging/docker-compose.yml`** — two new cron entries: `*/5 * * * *` for the pending sweep, `0 */6 * * *` for the orphan sweep.

The BullMQ worker is kept for `pnpm all` local-dev convenience — same code path, runs scheduled jobs through Redis instead of cron.

### Orphan-sweep design notes

Targets: `Attachment` rows with all 5 course-scope back-relations empty (`courseAssets`, `courseModuleAssets`, `courseLessonAssets`, `courseExamQuestionAssets`, `courseQuizQuestionAssets`).

Conservative-on-File: only deletes the File when **all** of:

- File.status = ready
- File has no transcripts (lesson video subtitles)
- File has no captions
- File has only this one Attachment (`attachments: { every: { id: orphan.id, ... } }`)

Otherwise leaves the Attachment alone (better to leak than break a referenced media object — File can be shared with transcripts/captions).

Age threshold: 24h (`STORAGE_JANITOR_ORPHAN_THRESHOLD_HOURS`). Long enough that edit flows briefly orphaning an attachment (delete-then-recreate-with-new-role) have time to re-attach before the sweep claims it.

Compare-and-delete atomicity: the orphan-condition `where` clause is repeated inside `deleteMany`. A concurrent attach-to-new-scope between the read and write matches 0 rows and is skipped cleanly. Same pattern as the existing pending-file sweep.

Delete sequence: R2 object first (errors swallowed — may already be gone), then `prisma.file.deleteMany` with the compare clause (Attachment cascades via the FK `onDelete: Cascade`).

## Patterns worth keeping

### Side-effect-free vs. side-effect-ful module split

When a worker module instantiates a BullMQ Worker at top level, importing it anywhere — including a Next.js API route — spins up a Redis subscriber and registers event handlers in that process. Bad. Split into:

- `<name>.sweeps.ts` — pure functions, no top-level side effects.
- `<name>.worker.ts` — thin wrapper that imports from `.sweeps.ts` and binds to BullMQ.

Tests and API routes import from `.sweeps.ts`; only the worker startup imports `.worker.ts`. Documented in the file headers.

### "Is the worker actually running in prod?"

Before adding code to a worker, audit:

1. `package.json` scripts (`worker:<name>`)
2. `apps/.../workers/<name>/start-*` and tsup entry list
3. `docker/<env>/docker-compose.yml` — service definitions
4. `docker-compose.yml` cron sidecar — alternative invocation path

The storage janitor only had (1) and the start script (`pnpm all` for local dev) — it was *never* deployed. Easy to miss because the BullMQ scheduling code looks like a complete worker. A worker without a compose service or cron entry is just a local script.

## Pre-existing CSP test failure (NOT caused by this branch)

While running gates I hit `__tests__/csp-environment.test.ts > connect-src does NOT contain any ws://localhost or ws://private-IP source`. Investigation: `proxy.ts` was modified in the working tree (NOT by me — user-WIP) to add `ws://127.0.0.1:3026/3027` and `ws://200.22.50.145:3026/3027` to the base CSP policy. Those should only be in `DEV_ONLY_CSP_ADDITIONS`. Tests against clean main pass; the test correctly flags the regression.

Did not include the proxy.ts change in this PR — left it as working-tree WIP for separate handling. Same for `package.json` (added `--skip-agents-md` to `gitnexus:analyze`) and the 4 other docker-compose files that had mirrored cron entries from a prior local edit.

## Pending

- [ ] Push #337 (done) → review + merge
- [ ] Out-of-band: deploy the new cron entries to staging
- [ ] Post-deploy: smoke test the two new cron invocations
- [ ] Out-of-band: mirror cron entries to the other 4 compose files (data/, production/, secondary staging) — separate ops PR
- [ ] Out-of-band: resolve the working-tree CSP regression in proxy.ts (move the dev WS endpoints out of the base policy)
- [ ] `npx gitnexus analyze` after merge — index stale

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
