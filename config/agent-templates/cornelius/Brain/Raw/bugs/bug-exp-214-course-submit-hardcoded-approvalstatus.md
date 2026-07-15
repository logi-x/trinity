---
title: "EXP-214: Course submit hardcodes approvalStatus=approved — bypasses review queue"
linear_id: "EXP-214"
agent_fp: "auto"
date: "2026-05-30"
severity: "High"
status: "resolved"
resolution: "PR #664 — fix approvalStatus to pending on submit"
tags: [bug, courses, workflow, project/experts]
category: "bug"
source: "automation"
---

# EXP-214: Course-submit hardcoded approvalStatus=approved

**Linear:** [EXP-214](https://linear.app/experts/issue/EXP-214) | **Status:** Resolved (PR #664)

## Summary
The course-submit handler set `approvalStatus: 'approved'` as a hardcoded value instead of `'pending'`. Every submitted course bypassed the review queue and went live immediately, regardless of whether an admin had reviewed it.

## Impact
All course submissions were auto-approved. Instructors could publish any course content without admin review. Admin review workflow was completely bypassed.

## Fix
PR #664 corrected the hardcoded value to `'pending'`, restoring the review queue flow.

## Related
- Course lifecycle routes (EXP-197, EXP-199) — resolved by PR #658

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
