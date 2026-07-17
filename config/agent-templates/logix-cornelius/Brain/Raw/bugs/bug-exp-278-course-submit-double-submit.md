---
title: "EXP-278 — handleCourseSubmit missing 'pending' guard — instructor can double-submit while course is under review"
date: "2026-06-02"
status: open
resolution: unknown
tags: [bug, courses, authorization, state-machine, project/experts]
linear: "https://linear.app/experts/issue/EXP-278/bug-handlecoursesubmit-missing-pending-guard-instructor-can-double"
fingerprint: "7a77f4e88d1c"
---

## Summary

`handleCourseSubmit` in `src/lib/courses/catalog/handlers/course-submit.handler.ts` guards against re-submitting an **approved** course (added by EXP-234, PR #732) but has no guard for re-submitting a course that is already `approvalStatus === "pending"`. An instructor can double-submit a course under review, resetting the review state, sending duplicate admin notification emails, and potentially clearing admin review notes.

## Root cause

`apps/experts-app/src/lib/courses/catalog/handlers/course-submit.handler.ts/handleCourseSubmit` — only checks `approvalStatus !== "approved"`. Missing: `approvalStatus !== "pending"` guard (or more precisely, only `"draft"` or `"rejected"` should be submittable).

Fix: extend the approval-status guard to also reject re-submission when `approvalStatus === "pending"`.

## Agent fingerprint

`<!-- agent-fp: 7a77f4e88d1c -->`

## Status

`open` — Backlog (High). Logical follow-up to EXP-234 (approved guard). Same file, adjacent gap.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
