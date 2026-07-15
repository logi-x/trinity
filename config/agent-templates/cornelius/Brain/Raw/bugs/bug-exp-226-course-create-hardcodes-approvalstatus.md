---
title: "EXP-226: course-create route hardcodes approvalStatus: \"approved\", bypassing moderation queue"
linear_id: "EXP-226"
agent_fp: "c44abea9d11a"
date: "2026-05-31"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, security, courses, approval, project/experts]
category: "bug"
source: "automation"
---

# EXP-226: course-create hardcodes `approvalStatus: "approved"`

**Linear:** [EXP-226](https://linear.app/experts/issue/EXP-226) | **Status:** Open  
**Spinoff of:** EXP-213 (R5)

## Summary
`POST /api/v1/courses` passes `approvalStatus: "approved"` as a hardcoded default in the `CourseCreateSchema.safeParse` call. Any authenticated instructor can create a course that is immediately approved without admin review.

## File
`apps/experts-app/app/api/v1/courses/route.ts:159`

## Repro
1. Authenticate as an instructor.
2. POST to `/api/v1/courses` with a valid course payload.
3. The created course has `approvalStatus: "approved"` — it skips the moderation queue.

## Fix
Change the hardcoded `approvalStatus: "approved"` to `approvalStatus: "pending"` in the schema parse defaults so new courses enter the review queue.

## Related
- EXP-213 (JWT staleness on course-create, resolved PR #678)
- EXP-214 (course-submit hardcodes approvalStatus, resolved PR #673)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
