---
title: "EXP-213: Course-create handler trusts JWT isAdmin — revoked admin can create courses"
linear_id: "EXP-213"
agent_fp: "auto"
date: "2026-05-30"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, auth, jwt-staleness, security, project/experts]
category: "bug"
source: "automation"
---

# EXP-213: Course-create JWT staleness

**Linear:** [EXP-213](https://linear.app/experts/issue/EXP-213) | **Status:** Open

## Summary
The course-create handler gates on `session.user.isAdmin` from the JWT without re-deriving the role from the DB. A revoked admin retains the ability to create new courses until their JWT expires (up to 30 days).

## Fix Needed
Re-derive admin/instructor role from DB before allowing course creation. Use `getDbCourseActor` (PR #658) or equivalent DB-fresh role check.

## Related
- EXP-209 (resolved PR #654), EXP-211, EXP-212 — same JWT staleness class
- PR #658 — getDbCourseActor canonical helper

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
