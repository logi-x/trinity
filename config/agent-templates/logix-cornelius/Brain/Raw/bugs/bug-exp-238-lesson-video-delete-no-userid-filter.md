---
title: "EXP-238: Lesson video DELETE has no userId filter on attachment lookup, allowing co-instructor cross-deletion"
linear_id: "EXP-238"
agent_fp: "auto"
date: "2026-05-31"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, security, courses, idor, project/experts]
category: "bug"
source: "automation"
---

# EXP-238: Lesson video DELETE missing ownership check

**Linear:** [EXP-238](https://linear.app/experts/issue/EXP-238) | **Status:** Backlog

## Summary
The `DELETE` handler for lesson videos fetches the media attachment with no `userId` filter. `assertCourseWriteAccess` only checks that the caller has course write access — it does not verify attachment ownership. Any co-instructor on the same course can delete another instructor's lesson video, destroying both the DB records and the R2 object.

## File
`apps/experts-app/app/api/v1/courses/[id]/modules/[moduleId]/lessons/[lessonId]/video/route.ts` — `DELETE`

## Repro
1. Instructor A and Instructor B are both co-instructors on the same course.
2. Instructor A uploads a lesson video (creates `Attachment` row with `userId = A`).
3. Instructor B sends DELETE to the video route — attachment lookup has no `userId: B` filter.
4. Instructor B successfully deletes Instructor A's video.

## Fix
Add `userId: session.user.id` filter to the attachment `findFirst` query in the DELETE handler to enforce ownership.

## Related
- EXP-212 (JWT staleness on lesson/quiz subroutes, resolved PR #684)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
