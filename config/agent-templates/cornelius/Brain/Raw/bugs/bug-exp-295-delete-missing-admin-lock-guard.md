---
title: "EXP-295 — owner can delete admin-locked post — moderation lock not enforced in DELETE"
date: "2026-06-03"
updated: "2026-06-03"
tags: ["bug", "community", "api", "moderation", "security", project/experts]
category: "bug"
source: "agent-scan"
source_id: "Raw/bugs/bug-exp-295-delete-missing-admin-lock-guard.md"
status: open
resolution: unknown
---

# EXP-295 — Owner can delete admin-locked post — moderation lock not enforced in DELETE

**Linear:** https://linear.app/experts/issue/EXP-295
**FP:** `4443149a35c8`
**Severity:** High
**Status:** open
**Filed:** 2026-06-03
**Routine:** R3

## File / Symbol

`apps/experts-app/app/api/v1/community/posts/[id]/route.ts` — `DELETE` handler (~line: findUnique + owner check)

## Repro

1. Admin sends `PUT /api/v1/community/posts/{POST_ID}` with `{ "isPublished": false }` → stamps `adminLockedAt`.
2. Post owner immediately sends `DELETE /api/v1/community/posts/{POST_ID}`.
3. DELETE handler queries `prisma.post.findUnique({ where: {id}, select: {userId: true} })` — `adminLockedAt` not selected, not checked.
4. Ownership check `post.userId === session.user.id` passes → post is deleted, defeating the moderation lock.

No concurrency required. 100% reproducible.

## Root Cause

PR #792 (EXP-280) added `adminLockedAt` logic to the `PUT` handler only. The `DELETE` handler was not updated to check the lock. The admin bypass (DB-fresh `getUserPermissions`) was added for moderation deletion (EXP-277), but the reverse (preventing owner deletion of locked content) was missed.

## Fix

In the DELETE handler, after the `findUnique` that loads `userId`, also select `adminLockedAt`. Add guard: if `post.adminLockedAt !== null && !isAdmin`, return 403 "Content has been administratively restricted". Admin bypass for GDPR/moderation deletion should remain.

## Agent Fingerprint

`<!-- agent-fp: 4443149a35c8 -->`

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
