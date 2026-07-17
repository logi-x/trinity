---
title: "EXP-257: Community posts GET totalPages incoherent for in-memory sorts beyond 500-post cap"
date: "2026-06-01"
status: open
resolution: unknown
tags: [bug, api, community, pagination, project/experts]
linear: "https://linear.app/experts/issue/EXP-257/spinoff-exp-242-community-posts-get-totalpages-incoherent-for-in"
fingerprint: "287cf4064d7b"
---

## Summary

For `popular` and `discussed` sorts in `GET /api/v1/community/posts`, `totalPosts` comes from a full `prisma.post.count()` query while the actual data is sliced to a 500-post in-memory cap. The response reports `totalPages: Math.ceil(totalPosts / limit)` — advertising page numbers for posts that will never be returned. Clients navigating to those pages receive empty results.

## Location

`apps/experts-app/app/api/v1/community/posts/route.ts:88` — `totalPages: Math.ceil(totalPosts / limit)`  
Spinoff of EXP-242. Duplicate root cause addressed by EXP-263 (R5 scan).

## Repro Steps

1. Create > 500 posts.
2. `GET /api/v1/community/posts?sort=popular&limit=20` — `totalPages` reports `Math.ceil(total_db_count / 20)` instead of `Math.ceil(500 / 20) = 25`.
3. Navigate to page 26+ — empty result.

## Agent Fingerprint

`287cf4064d7b` (R3)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
