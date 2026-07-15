---
title: "EXP-299: POST /community/posts/{id}/comments has no rate limit"
date: "2026-06-03"
status: open
resolution: unknown
tags: [bug, community, rate-limit, dos, project/experts]
linear_url: "https://linear.app/experts/issue/EXP-299"
agent_fp: "af2656e7df89"
severity: high
area: api/community
file: "apps/experts-app/app/api/v1/community/posts/[id]/comments/route.ts"
symbol: POST
source: "generated"
source_id: "Raw/bugs/bug-exp-299-community-comments-post-no-rate-limit.md"
---

# EXP-299: POST /community/posts/{id}/comments — no rate limit

**Linear:** https://linear.app/experts/issue/EXP-299  
**FP:** `af2656e7df89` (R3)  
**Severity:** High  
**Filed:** 2026-06-03

## Summary

`POST /api/v1/community/posts/{id}/comments` has no rate-limit guard. An authenticated user can spam-create comments at machine speed — each write inserts a `Comment` row (~5 KB), fires a Redis feed event, runs activity helpers (transactions/notifications), and enqueues a BullMQ embed job.

## Repro

1. Authenticate as any valid user.
2. In a tight loop: `POST /api/v1/community/posts/<UUID>/comments` with `{"content": "<4999-char string>"}` — every request returns 201.
3. No 429 is ever returned.

## Impact

- DB exhaustion (Comment rows, activity rows, BullMQ jobs)
- Redis feed saturation
- `@mention` notification storm for mentioned users
- 100% reproducible

## Fix

Add `enforceCommentCreationRateLimit` (per-user sliding window, e.g. 30/min + 300/day) mirroring `enforcePostCreationRateLimit` added in PR #790 (EXP-281). Place immediately after auth guard, before any DB writes.

## Related

- EXP-281: Post creation rate limit (fixed PR #790) — same pattern
- EXP-303: Duplicate of this issue (same FP `af2656e7df89`, filed by concurrent scan, immediately closed)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
