---
title: "EXP-212: Lesson and quiz subroutes trust JWT isAdmin — 4 routes affected"
linear_id: "EXP-212"
agent_fp: "auto"
date: "2026-05-30"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, auth, jwt-staleness, security, project/experts]
category: "bug"
source: "automation"
---

# EXP-212: Lesson/quiz subroutes JWT staleness

**Linear:** [EXP-212](https://linear.app/experts/issue/EXP-212) | **Status:** Open

## Summary
4 lesson and quiz subroutes under the course tree trust `session.user.isAdmin` from the JWT without DB re-derivation. Same staleness class as EXP-209/211/213, introduced by PR #619.

## Affected Routes
Lesson create, lesson update, quiz create, quiz update (exact paths TBD by implementor).

## Fix Needed
Re-derive admin/instructor role from DB in each of the 4 affected routes. Use `getDbCourseActor` (PR #658) as the canonical pattern.

## Related
- EXP-209 (resolved PR #654), EXP-211, EXP-213 — same class
- PR #658 — getDbCourseActor canonical helper

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
