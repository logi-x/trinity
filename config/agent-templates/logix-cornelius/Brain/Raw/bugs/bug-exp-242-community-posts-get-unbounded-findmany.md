---
title: "EXP-242: Community posts GET loads all posts without limit for popular/discussed sort — unauthenticated OOM DoS"
date: "2026-05-31"
status: open
resolution: unknown
tags: [bug, dos, unbounded-query, community, performance, project/experts]
---

## Summary

`GET /api/v1/community/posts` passes `take: undefined` to Prisma when `sort` is `popular` or `discussed`. Prisma issues an unbounded `findMany` loading all published posts with nested author+profile relations into memory. No authentication is required. Concurrent unauthenticated requests can exhaust application memory.

## File

`apps/experts-app/app/api/v1/community/posts/route.ts` — `GET` handler

## Repro

```
GET /api/v1/community/posts?sort=popular
```

No authentication. Returns all posts. For amplified DoS, issue 20 concurrent requests.

## Agent Fingerprint

`05d28729883a` (R3)

## Linear

https://linear.app/experts/issue/EXP-242

## Fix

Add `take: MAX_POSTS_PAGE_SIZE` (e.g. 20) for popular/discussed sort paths. Fix in the same PR as EXP-243 (same handler, adjacent code path). See Decision-Log 2026-05-31 for the list endpoint bounds decision.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
