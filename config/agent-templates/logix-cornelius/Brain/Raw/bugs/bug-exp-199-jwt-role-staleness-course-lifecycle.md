---
title: "EXP-199: JWT role-staleness on course lifecycle routes — revoked admin can delete/archive/clone/publish"
linear_id: "EXP-199"
agent_fp: "ebb296405be7"
date: "2026-05-29"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, security, auth, courses, project/experts]
category: "bug"
source: "automation"
---

# EXP-199: JWT role-staleness on course lifecycle routes

**Linear:** [EXP-199](https://linear.app/experts/issue/EXP-199) | **Fingerprint:** `ebb296405be7`

## Summary
Four course lifecycle routes read `isAdmin` from the JWT session claim rather than the database: DELETE, POST archive, POST clone, POST publish. A revoked admin's stale JWT bypasses `assertCourseWriteAccess` on all four routes, allowing them to delete, archive, clone, or publish any course (cross-account for admin; own courses for revoked instructor).

## Location
- `apps/experts-app/app/api/v1/courses/[id]/route.ts:102–103` — DELETE
- `apps/experts-app/app/api/v1/courses/[id]/archive/route.ts:20–21` — POST archive
- `apps/experts-app/app/api/v1/courses/[id]/clone/route.ts:21–22` — POST clone
- `apps/experts-app/app/api/v1/courses/[id]/publish/route.ts` — POST publish

## Related
EXP-69, 78, 84, 85, 88, 89, 90, 91 (same class), EXP-197, EXP-198 (same PR surface from PR #619)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
