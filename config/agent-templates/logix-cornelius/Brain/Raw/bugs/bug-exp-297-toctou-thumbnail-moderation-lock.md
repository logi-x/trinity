---
title: "EXP-297 — TOCTOU in thumbnail upload bypasses moderation lock, orphans R2 assets"
date: "2026-06-03"
updated: "2026-06-03"
tags: ["bug", "community", "api", "toctou", "moderation", "storage", "r2", "quota", project/experts]
category: "bug"
source: "agent-scan"
source_id: "Raw/bugs/bug-exp-297-toctou-thumbnail-moderation-lock.md"
status: open
resolution: unknown
---

# EXP-297 — TOCTOU in thumbnail upload bypasses moderation lock, orphans R2 assets with permanent quota charge

**Linear:** https://linear.app/experts/issue/EXP-297
**FP:** `1537707518d5`
**Severity:** Medium
**Status:** open
**Filed:** 2026-06-03
**Routine:** R3

## File / Symbol

`apps/experts-app/app/api/v1/community/posts/[id]/thumbnail/route.ts` — `POST` handler

## Repro

1. Admin sends `PUT /api/v1/community/posts/POST_ID` with `{ "isPublished": false }` → stamps `adminLockedAt` — do not await.
2. Owner concurrently uploads a large thumbnail via `POST /api/v1/community/posts/POST_ID/thumbnail` with a 10 MB image.
3. Thumbnail route's `findUnique` (~line 69) reads `adminLockedAt = null` before the admin write lands → passes the lock check.
4. During the 50–200 ms spent on `arrayBuffer()` + content-hash computation, admin write lands and stamps `adminLockedAt`.
5. Route continues: uploads to R2 (asset at `status=ready`), writes `File` row, associates with post.
6. New R2 asset is now permanently quota-charged and janitor-unclaimable (status=ready with no pending→ready lifecycle; orphan reaper won't touch it).

## Root Cause

The thumbnail route follows pending-first upload pattern (correct) but reads `adminLockedAt` via `findUnique` before the expensive `arrayBuffer()` call. The 50–200 ms buffer processing window is the TOCTOU gap.

## Fix

Move the moderation lock check to after `arrayBuffer()` and hash computation are complete (immediately before the R2 PUT), or use an atomic conditional DB operation. If post is locked at that point, abort before the R2 write and return 403. This eliminates both the lock bypass and the R2 orphan creation.

## Agent Fingerprint

`<!-- agent-fp: 1537707518d5 -->`

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
