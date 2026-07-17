---
title: "EXP-76 — Course progress POST: lesson-to-course ownership check skipped for completed=false — cross-course completion counter inflation"
date: "2026-05-22"
status: open
resolution: unknown
tags: [bug, security, authorization, business-logic, courses, project/experts]
linear: "https://linear.app/experts/issue/EXP-76/bug-course-progress-post-lesson-to-course-ownership-check-skipped-for"
fingerprint: "226fb913256a"
---

## Summary

`POST /api/v1/courses/[id]/progress` verifies lesson-to-course ownership only when `completed=true`. When `completed=false`, the route skips the ownership check, allowing an attacker to submit progress records for lessons from a different course. This inflates the completion counter for the target course, potentially triggering false course completion and certificate eligibility.

## Repro

1. Enroll (status `completed`) in Course A (lessons A1, A2, A3) and Course B (lessons B1, B2, B3).
2. Call `POST /api/v1/courses/courseB-id/progress` with `{ "lessonId": "<A1>", "completed": false }`.
3. The request succeeds — A1 is counted as a progress record against Course B.
4. Repeat for A2, A3 to inflate Course B's completion counter.
5. Then call with `completed=true` for B1, B2, B3 to trigger false completion.

## Impact

Cross-course phantom completion records; false course completion status; certificate bypass.

## Agent fingerprint

`<!-- agent-fp: 226fb913256a -->`

## Status

`open` — Todo as of 2026-05-22.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
