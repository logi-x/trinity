---
title: "EXP-236: reject route parses request body before auth check and outside the try block"
linear_id: "EXP-236"
agent_fp: "auto"
date: "2026-05-31"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, courses, project/experts]
category: "bug"
source: "automation"
---

# EXP-236: reject route body-parse before auth

**Linear:** [EXP-236](https://linear.app/experts/issue/EXP-236) | **Status:** Backlog  
**Same class as:** EXP-210 (publish route, resolved PR #678)

## Summary
In `app/api/v1/courses/[id]/reject/route.ts`, `request.json()` is called before the `try` block and before auth is checked. A body parse error from an unauthenticated request is not caught by the route error handler.

## File
`apps/experts-app/app/api/v1/courses/[id]/reject/route.ts` — `POST`

## Repro
1. Send `POST /api/v1/courses/{id}/reject` without authentication, with a malformed JSON body.
2. The parse error propagates uncaught, returning a 500 instead of a 401/400.

## Fix
Move `request.json()` inside the `try` block and after the auth guard, consistent with the EXP-210 fix on the publish route.

## Related
- EXP-210 (publish route body-parse before auth, resolved PR #678)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
