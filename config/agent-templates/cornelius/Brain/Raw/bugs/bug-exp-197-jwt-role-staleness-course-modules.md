---
title: "EXP-197: JWT role-staleness on course curriculum module routes — revoked admin bypass"
linear_id: "EXP-197"
agent_fp: "4beadfc873f2"
date: "2026-05-29"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, auth, courses, project/experts]
category: "bug"
source: "automation"
---

# EXP-197: JWT role-staleness on course curriculum module routes

**Linear:** [EXP-197](https://linear.app/experts/issue/EXP-197) | **Fingerprint:** `4beadfc873f2`

## Summary
The course curriculum module routes (POST create, PUT update, DELETE delete) read `isAdmin` from the JWT session claim rather than querying the database. A user whose admin role was revoked retains write access to curriculum modules in any course until their JWT expires (up to 30 days).

## Location
- `apps/experts-app/app/api/v1/courses/[id]/modules/route.ts` — POST handler
- `apps/experts-app/src/lib/courses/curriculum/modules/handlers/course-module-create.handler.ts`
- `apps/experts-app/src/lib/courses/curriculum/modules/handlers/course-module-update.handler.ts`
- `apps/experts-app/src/lib/courses/curriculum/modules/handlers/course-module-delete.handler.ts`

## Related
EXP-69, 78, 84, 85, 88, 89, 90, 91 (same class — JWT role-staleness), EXP-198, EXP-199 (same PR surface)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
