---
title: "EXP-302: Exam reset POST non-atomic — concurrent student submission corrupts data"
date: "2026-06-03"
status: open
resolution: unknown
tags: [bug, courses, exams, race-condition, data-integrity, project/experts]
linear_url: "https://linear.app/experts/issue/EXP-302"
agent_fp: "f9ce9ef4c26c"
severity: medium
area: courses/exams
file: "apps/experts-app/app/api/v1/creator/courses/[id]/exams/[examId]/reset/route.ts"
symbol: POST
source: "generated"
source_id: "Raw/bugs/bug-exp-302-exam-reset-non-atomic.md"
---

# EXP-302: Exam reset POST — non-atomic two-step delete

**Linear:** https://linear.app/experts/issue/EXP-302  
**FP:** `f9ce9ef4c26c` (R3)  
**Severity:** Medium  
**Filed:** 2026-06-03

## Summary

The exam reset handler performs two sequential non-transactional deletes:
```ts
await prisma.courseExamAnswer.deleteMany({ where: { attempt: { examId, userId } } }); // Delete 1
await prisma.courseExamAttempt.deleteMany({ where: { examId, userId } });               // Delete 2
```

A student who submits their exam in the gap between Delete 1 and Delete 2 will have their answers deleted while their attempt row survives, resulting in a corrupted state: an attempt with no answers.

## Repro

1. Student begins an exam attempt (active `CourseExamAttempt` row + `CourseExamAnswer` rows).
2. Instructor triggers exam reset — Delete 1 removes the answers.
3. Student submits exam in the gap (~0–100ms) — new answers written to the now-empty attempt.
4. Delete 2 removes the attempt — answers are orphaned.

Result: student's submission silently lost; attempt row gone; student re-takes an exam they already submitted.

## Fix

Wrap both deletes in `prisma.$transaction`:
```ts
await prisma.$transaction([
  prisma.courseExamAnswer.deleteMany({ where: { attempt: { examId, userId } } }),
  prisma.courseExamAttempt.deleteMany({ where: { examId, userId } }),
]);
```

## Related

- EXP-276: Exam reset BOLA (missing ownership check) — fixed in PR #801 (same file)
- PR #801 commit `c350550`: added ownership guard but left two-step delete in place

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
