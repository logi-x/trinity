---
title: "EXP-254: GET /community/posts/[id] returns draft posts — missing isPublished filter allows unauthenticated draft disclosure"
linear_id: "EXP-254"
agent_fp: "edb9dfa6147f"
date: "2026-06-01"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, security, community, project/experts]
category: "bug"
source: "automation"
---

# EXP-254: Community GET /posts/[id] returns draft posts to unauthenticated callers

**Linear:** [EXP-254](https://linear.app/experts/issue/EXP-254/security-get-community-posts-id-returns-draft-posts-missing-ispublished) | **Status:** Backlog

## Summary

The `GET /api/v1/community/posts/[id]` route returns a post regardless of its `isPublished` status. An unauthenticated (or any authenticated) caller who knows a post's UUID can retrieve a post that the author has not yet published. The list endpoint (`GET /api/v1/community/posts`) correctly filters to `isPublished: true` for unauthenticated callers, but the detail endpoint does not.

## File

`apps/experts-app/app/api/v1/community/posts/[id]/route.ts` — `GET` handler, Prisma `findUnique` call

## Repro

```bash
curl https://<host>/api/v1/community/posts/<draft-post-uuid>
# Returns full post data including unpublished draft content
```

## Fix

Add `isPublished: true` to the Prisma `findUnique` (or `findFirst`) `where` clause in the GET handler, OR add an ownership check so the post is only returned to the author when `isPublished: false`.

## Related

- EXP-242 — community posts GET unbounded for popular/discussed sort
- EXP-253 — Community posts DELETE missing UUID guard

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
