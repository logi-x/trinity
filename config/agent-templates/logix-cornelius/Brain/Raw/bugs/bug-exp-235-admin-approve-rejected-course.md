---
title: "EXP-235: Admin can approve a rejected course directly, bypassing re-submission requirement"
linear_id: "EXP-235"
agent_fp: "auto"
date: "2026-05-31"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, courses, approval, project/experts]
category: "bug"
source: "automation"
---

# EXP-235: Admin can approve a rejected course directly

**Linear:** [EXP-235](https://linear.app/experts/issue/EXP-235) | **Status:** Backlog

## Summary
`handleCourseApprove` reads `approvalStatus` in its `select` clause but never validates it equals `"pending"` before approving. An admin can approve a course in `"rejected"` state without the instructor re-submitting, skipping the intended review cycle.

## File
`apps/experts-app/src/lib/courses/catalog/handlers/course-approve.handler.ts` — `handleCourseApprove`

## Fix
Add validation that `current.approvalStatus === "pending"` before executing the approval. Return a structured error if the course is in any other state.

## Related
- EXP-234 (instructor re-submit resets approval)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
