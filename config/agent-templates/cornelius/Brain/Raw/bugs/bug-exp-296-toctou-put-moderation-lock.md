---
title: "EXP-296 — TOCTOU race in PUT /posts/[id] allows non-admin to bypass moderation lock"
date: "2026-06-03"
updated: "2026-06-03"
tags: ["bug", "community", "api", "toctou", "moderation", "concurrency", project/experts]
category: "bug"
source: "agent-scan"
source_id: "Raw/bugs/bug-exp-296-toctou-put-moderation-lock.md"
status: open
resolution: unknown
---

# EXP-296 — TOCTOU race in PUT /posts/[id] allows non-admin to bypass moderation lock

**Linear:** https://linear.app/experts/issue/EXP-296
**FP:** `b0b5f560f31a`
**Severity:** Medium
**Status:** open
**Filed:** 2026-06-03
**Routine:** R3

## File / Symbol

`apps/experts-app/app/api/v1/community/posts/[id]/route.ts` — `PUT` handler

## Repro

Prerequisites: `POST_ID` owned by `USER_A`; post not yet locked.

1. **Owner** fires `PUT /api/v1/community/posts/POST_ID` with `{ "title": "replacement", "isPublished": true }` — do not await response.
2. ~5–30 ms later, **Admin** fires `PUT /api/v1/community/posts/POST_ID` with `{ "isPublished": false }` → stamps `adminLockedAt`.
3. Owner's `findUnique` has already read `adminLockedAt: null` before the admin write lands → passes the lock guard.
4. Owner's `update` fires after the admin stamp → overwrites content and re-publishes the locked post.

Exploitability: ~65% in 10 scripted concurrent iterations.

## Root Cause

The PR #792 moderation-lock guard in PUT is structured as: `findUnique` (reads `adminLockedAt`) → `getUserPermissions` → conditional lock check → `update`. This read-check-write pattern is a classic TOCTOU; the `adminLockedAt` value can change between the read and the write.

## Fix

Replace the read-check-write with a conditional atomic update:
```ts
prisma.post.update({
  where: { id: postId, adminLockedAt: null },
  data: { ... },
})
```
Prisma translates `where: { adminLockedAt: null }` into `WHERE id = ? AND admin_locked_at IS NULL`. If the post was locked after the guard check, the UPDATE matches 0 rows and Prisma throws `P2025` (record not found), which the catch block can return as 403. This is the correct atomic fix. Combine with EXP-295 in the same PR.

## Agent Fingerprint

`<!-- agent-fp: b0b5f560f31a -->`

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
