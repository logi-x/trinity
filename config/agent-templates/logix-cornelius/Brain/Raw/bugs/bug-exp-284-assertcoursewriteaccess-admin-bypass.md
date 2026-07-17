---
title: "EXP-284 — assertCourseWriteAccess admin bypass"
date: "2026-06-02"
updated: "2026-06-02"
tags: ["bug", "courses", "authorization", "security", project/experts]
category: "bug"
source: "agent-scan"
source_id: "Raw/bugs/bug-exp-284-assertcoursewriteaccess-admin-bypass.md"
status: open
resolution: unknown
---

# EXP-284 — assertCourseWriteAccess admin bypass: any admin can force-submit any instructor's course

**Linear:** https://linear.app/experts/issue/EXP-284  
**FP:** `20ca5e858867`  
**Severity:** High  
**Status:** open  
**Filed:** 2026-06-02  
**Routine:** R3

## File / Symbol

`apps/experts-app/src/lib/courses/catalog/guards/course-access.guard.ts` — `assertCourseWriteAccess`

## Repro

1. Authenticate as a DB-fresh admin (not the course instructor)
2. `POST /api/v1/creator/courses/{ANY_COURSE_UUID}/submit` with a valid admin session
3. Guard short-circuits at `if (isAdmin) { return {ok: true} }` before any `courseInstructor` query
4. Submit succeeds; course enters review queue without the admin having any instructor relationship

## Root Cause

`assertCourseWriteAccess` at lines 17–18: `if (isAdmin) { return {ok: true}; }` fires before the `prisma.courseInstructor.findFirst` ownership lookup. Any caller with `isAdmin: true` is granted write access to any course regardless of whether `userId` appears in `courseInstructor`.

## Impact

Any admin can force-submit any instructor's course to the review queue, potentially triggering approval workflows, notifications, email sequences, and publishing flows for courses the admin has no legitimate relationship with. Expanding blast radius of a compromised admin account.

## Note

Distinct from the JWT staleness class (EXP-241 — already resolved): `isAdmin` IS derived from DB via `getDbCourseActor`. The bypass occurs after a correct DB-fresh check — the ownership query is simply skipped entirely for admins.

## Agent Fingerprint

`<!-- agent-fp: 20ca5e858867 -->`

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
