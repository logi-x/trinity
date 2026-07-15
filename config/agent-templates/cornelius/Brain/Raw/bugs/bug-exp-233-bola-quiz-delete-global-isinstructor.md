---
title: "EXP-233: [security] BOLA: quiz DELETE uses global isInstructor without course-ownership check"
linear_id: "EXP-233"
agent_fp: "fafff305ee80"
date: "2026-05-31"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, security, courses, bola, project/experts]
category: "bug"
source: "automation"
---

# EXP-233: BOLA — quiz DELETE missing course-ownership check

**Linear:** [EXP-233](https://linear.app/experts/issue/EXP-233) | **Status:** Backlog

## Summary
The EXP-212 fix hardened lesson and quiz routes with `getDbCourseActor()` for all verbs, but the `DELETE` verb on `quizzes/[quizId]` was missed. It checks only the **platform-level** `actor.isInstructor` flag — any instructor on the platform can delete any course's quiz, regardless of course ownership.

This is a Broken Object Level Authorization (BOLA) vulnerability.

## File
`apps/experts-app/app/api/v1/courses/[id]/modules/[moduleId]/quizzes/[quizId]/route.ts` — `DELETE` handler

## Repro
1. Authenticate as Instructor A.
2. Obtain the `quizId` of a quiz belonging to Instructor B's course.
3. Send `DELETE /api/v1/courses/{b-course-id}/modules/{moduleId}/quizzes/{quizId}`.
4. Quiz is deleted — no course-ownership check occurs.

## Fix
Add `getDbCourseActor(courseId, userId)` call and assert course-write access before processing DELETE, consistent with the EXP-212 fix on other verbs.

## Related
- EXP-212 (JWT staleness on lesson/quiz subroutes, resolved PR #684 — DELETE was missed)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
