---
title: "EXP-243: Community posts GET user-supplied limit uncapped on recent sort — unauthenticated DoS"
date: "2026-05-31"
status: open
resolution: unknown
tags: [bug, security, dos, unbounded-query, community, project/experts]
---

## Summary

For `sort=recent`, `GET /api/v1/community/posts` parses the caller-supplied `limit` query parameter and passes it directly as `take:` with no upper-bound clamp. An unauthenticated caller can set `limit=1000000` and cause Prisma to load arbitrarily many rows. Combined with EXP-242 (same handler, popular/discussed path), the community posts GET handler has no safe query bounds on any sort path.

## File

`apps/experts-app/app/api/v1/community/posts/route.ts` — `GET` handler

## Repro

```
GET /api/v1/community/posts?sort=recent&limit=100000
```

No authentication required.

## Agent Fingerprint

`16a2b03d4ed4` (R3)

## Linear

https://linear.app/experts/issue/EXP-243

## Fix

Clamp `limit` to a server-side maximum: `const safeTake = Math.min(parseInt(limit) || 20, 50)`. Fix in the same PR as EXP-242. See Decision-Log 2026-05-31 for the list endpoint bounds decision.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
