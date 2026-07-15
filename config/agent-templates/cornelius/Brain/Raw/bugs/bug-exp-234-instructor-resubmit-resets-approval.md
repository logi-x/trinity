---
title: "EXP-234: Instructor can re-submit an approved course, silently resetting admin approval"
linear_id: "EXP-234"
agent_fp: "auto"
date: "2026-05-31"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, courses, approval, project/experts]
category: "bug"
source: "automation"
---

# EXP-234: Course re-submission overwrites approved status

**Linear:** [EXP-234](https://linear.app/experts/issue/EXP-234) | **Status:** Backlog

## Summary
`handleCourseSubmit` guards only against `publishingStatus === "archived"`. It does not check `approvalStatus`, so an already-approved course can be re-submitted, resetting `approvalStatus` from `"approved"` to `"pending"` and forcing a full re-review cycle — silently destroying the admin's prior approval.

## File
`apps/experts-app/src/lib/courses/catalog/handlers/course-submit.handler.ts` — `handleCourseSubmit`

## Repro
1. Admin approves a course (set `approvalStatus: "approved"`).
2. Instructor calls the submit endpoint again.
3. `approvalStatus` is reset to `"pending"` — admin's approval is silently voided.

## Fix
Add a guard that rejects re-submission when `approvalStatus === "approved"` (or require the instructor to explicitly unpublish first).

## Related
- EXP-235 (admin can approve rejected course directly)
- EXP-226 (course-create hardcodes approvalStatus: approved)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
