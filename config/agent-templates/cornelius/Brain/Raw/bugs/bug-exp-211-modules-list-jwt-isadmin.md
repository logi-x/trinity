---
title: "EXP-211: Course modules list trusts JWT isAdmin — revoked admin reads unpublished modules"
linear_id: "EXP-211"
agent_fp: "auto"
date: "2026-05-30"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, auth, jwt-staleness, security, project/experts]
category: "bug"
source: "automation"
---

# EXP-211: Modules list JWT isAdmin staleness

**Linear:** [EXP-211](https://linear.app/experts/issue/EXP-211) | **Status:** Open

## Summary
The course modules list endpoint gates on `session.user.isAdmin` from the JWT without re-deriving the role from the database. A revoked admin can continue to read unpublished module lists for any course until their JWT expires.

## Fix Needed
Re-derive admin/instructor role from DB before returning the module list. Use `getDbCourseActor` (PR #658) as the canonical pattern.

## Related
- EXP-209 (resolved PR #654), EXP-212, EXP-213 — same JWT staleness class
- PR #658 — getDbCourseActor canonical helper

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
