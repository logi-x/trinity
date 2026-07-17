---
title: "EXP-300: POST /internal/upload community case ignores adminLockedAt"
date: "2026-06-03"
status: open
resolution: unknown
tags: [bug, community, moderation, upload, security, project/experts]
linear_url: "https://linear.app/experts/issue/EXP-300"
agent_fp: "3d41f56d651f"
severity: high
area: api/community
file: "apps/experts-app/app/api/v1/internal/upload/route.ts"
symbol: POST
source: "generated"
source_id: "Raw/bugs/bug-exp-300-upload-community-ignores-admin-lock.md"
---

# EXP-300: Internal upload — community case ignores adminLockedAt

**Linear:** https://linear.app/experts/issue/EXP-300  
**FP:** `3d41f56d651f` (R3)  
**Severity:** High  
**Filed:** 2026-06-03

## Summary

The `/api/v1/internal/upload` route's `entityType: "community"` case does not check `Post.adminLockedAt`. An admin moderation action (stamping `adminLockedAt` via PUT) is bypassed entirely by the owner uploading a gallery image.

## Repro

1. Admin `PUT /api/v1/community/posts/<POST_UUID>` with `{"isPublished": false}` — stamps `adminLockedAt`.
2. Post owner calls `POST /api/v1/internal/upload` with `entityType: "community"` and `entityId: <POST_UUID>` and a gallery image.
3. Upload succeeds — no 403 returned despite the moderation lock.

## Impact

Moderation lock (introduced in PR #792, migration `20260603000000_post_admin_locked_at`) is bypassed via gallery upload. Post owner can add new gallery images to a suppressed post, effectively mutating its content while locked.

## Fix

In the community upload case, after fetching the post, check:
```ts
if (post.adminLockedAt !== null && !perms.isAdmin) {
  return safeErrorJson(new DomainError(403, "Content has been administratively restricted"));
}
```

## Related

- EXP-295: DELETE handler also missing adminLockedAt guard
- EXP-296: PUT TOCTOU race on moderation lock
- EXP-297: Thumbnail POST TOCTOU on moderation lock
- PR #792: Introduced adminLockedAt (incomplete coverage)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
