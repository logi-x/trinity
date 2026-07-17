---
title: "EXP-276 — Exam reset POST does not validate examId belongs to courseId — BOLA cross-course attempt deletion"
date: "2026-06-02"
status: open
resolution: unknown
tags: [bug, security, courses, bola, authorization, project/experts]
linear: "https://linear.app/experts/issue/EXP-276/bug-exam-reset-post-does-not-validate-examid-belongs-to-courseid-bola"
fingerprint: "4c24416c67be"
---

## Summary

`app/api/v1/creator/courses/[courseId]/exams/[examId]/reset/route.ts` — the POST handler calls `assertCourseWriteAccess({courseId: COURSE_A_UUID, userId: attacker})` (passes for Course A instructor) but never verifies that `examId` belongs to Course A. An instructor of Course A can reset exam attempts for any exam on any course by supplying a foreign `examId` in the URL.

## Root cause

`apps/experts-app/app/api/v1/creator/courses/[id]/exams/[examId]/reset/route.ts/POST` — missing `prisma.exam.findUnique({ where: { id: examId, courseId } })` ownership check before the reset operation.

Fix: add an `examId → courseId` membership check (same pattern as module/lesson routes) that returns 404 on mismatch.

## Agent fingerprint

`<!-- agent-fp: 4c24416c67be -->`

## Status

`open` — Backlog (High). BOLA class, same pattern as EXP-233 (quiz DELETE BOLA, resolved).

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
