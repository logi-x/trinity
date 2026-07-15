---
title: "EXP-253: community posts DELETE handler missing UUID guard — Prisma P2023 on malformed id returns 500"
linear_id: "EXP-253"
agent_fp: "2e356038195a"
date: "2026-06-01"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, api, community, project/experts]
category: "bug"
source: "automation"
---

# EXP-253: Community posts DELETE missing UUID guard

**Linear:** [EXP-253](https://linear.app/experts/issue/EXP-253/bug-community-posts-delete-handler-missing-uuid-guard-prisma-p2023-on) | **Status:** Backlog

## Summary
The GET and PUT handlers in `app/api/v1/community/posts/[id]/route.ts` both guard with `routeParamsWithIdSchema.safeParse({id})` and return HTTP 400 for malformed IDs. The DELETE handler is missing this guard: a malformed (non-UUID) `id` reaches Prisma and throws `PrismaClientValidationError` (P2023), returning an unhandled 500.

## File
`apps/experts-app/app/api/v1/community/posts/[id]/route.ts` — `DELETE` handler

## Repro
```bash
curl -X DELETE https://<host>/api/v1/community/posts/not-a-uuid \
  -H "Cookie: <session>"
# Returns HTTP 500 instead of HTTP 400
```

## Fix
Add `routeParamsWithIdSchema.safeParse({id})` guard at the top of the DELETE handler, matching the existing GET and PUT guard pattern.

## Related
- EXP-221 — AI conversation routes missing UUID guard (resolved PR #692)
- EXP-254 — community GET /[id] draft disclosure

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
