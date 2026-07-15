---
title: "EXP-298 — GET /posts/{id}/comments has no post visibility check — moderated-post comments exposed"
date: "2026-06-03"
updated: "2026-06-03"
tags: ["security", "community", "api", "visibility", "moderation", project/experts]
category: "bug"
source: "agent-scan"
source_id: "Raw/bugs/bug-exp-298-comments-no-post-visibility-check.md"
status: open
resolution: unknown
---

# EXP-298 — GET /posts/{id}/comments has no post visibility check — moderated-post comments exposed

**Linear:** https://linear.app/experts/issue/EXP-298
**FP:** `c4214ca6efed`
**Severity:** Medium
**Status:** open
**Filed:** 2026-06-03
**Routine:** R3

## File / Symbol

`apps/experts-app/app/api/v1/community/posts/[id]/comments/route.ts` — `GET` handler

## Repro

1. Admin unpublishes a harmful post via `PUT /api/v1/community/posts/{POST_ID}` with `{ "isPublished": false }`.
2. Unauthenticated attacker sends `GET /api/v1/community/posts/{POST_ID}/comments`.
3. Comments endpoint returns the full comment thread with no check that the parent post is published or accessible.
4. Additionally: if a warm Redis cache was written before the admin unpublish, the cache is not invalidated → comments served from cache for up to 300s after the post is hidden.

## Root Cause

The post-detail `GET` route (`posts/[id]/route.ts`) was fixed by EXP-254 to enforce `isPublished` visibility. The comments `GET` route (`posts/[id]/comments/route.ts`) was hardened by EXP-289 (bounded fetch + cache read guard) but never received an equivalent parent-post visibility check.

Secondary: `POST /api/v1/community/posts/{id}/comments` also lacks a check that the parent post is published before creating a comment (folded FP `c78d703bcc3e`).

## Fix

Add a parent post lookup at the top of the comments GET handler:
```ts
const post = await prisma.post.findUnique({ where: { id: postId }, select: { isPublished: true, userId: true, adminLockedAt: true } });
if (!post) return 404;
if (!post.isPublished && session?.user?.id !== post.userId && !isAdmin) return 404;
```
Also invalidate the comments Redis cache key when admin unpublishes a post (in the PUT handler). Mirror the same check in the POST comments handler.

## Agent Fingerprint

`<!-- agent-fp: c4214ca6efed -->`

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
