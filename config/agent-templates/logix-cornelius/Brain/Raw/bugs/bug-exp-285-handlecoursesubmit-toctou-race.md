---
title: "EXP-285 — handleCourseSubmit TOCTOU race"
date: "2026-06-02"
updated: "2026-06-02"
tags: ["bug", "courses", "race-condition", "concurrency", project/experts]
category: "bug"
source: "agent-scan"
source_id: "Raw/bugs/bug-exp-285-handlecoursesubmit-toctou-race.md"
status: open
resolution: unknown
---

# EXP-285 — handleCourseSubmit read+write not atomic: TOCTOU race dormant until EXP-278 fix

**Linear:** https://linear.app/experts/issue/EXP-285  
**FP:** `4cbf93d87242`  
**Severity:** Medium (dormant; escalates to High once EXP-278 is fixed)  
**Status:** open  
**Filed:** 2026-06-02  
**Routine:** R3

## File / Symbol

`apps/experts-app/src/lib/courses/catalog/handlers/course-submit.handler.ts` — `handleCourseSubmit`

## Root Cause

`handleCourseSubmit` reads `publishingStatus`/`approvalStatus` in a `findUnique` and then writes in a separate `update` with no enclosing transaction and no optimistic lock. Two concurrent submit requests can both pass the state guards (both reads observe the pre-write state) before either write commits.

## Relationship to EXP-278

Currently dormant because EXP-278 (missing `approvalStatus !== "pending"` guard) means concurrent submits can succeed anyway. Once EXP-278 is fixed, the TOCTOU window becomes a concrete double-submit bypass: two requests race past the guard simultaneously. **EXP-278 and EXP-285 must be fixed atomically in a single `$transaction`.** A PR fixing only EXP-278 without the transaction wrapper should be blocked by the gatekeeper.

## Fix Guidance

Wrap the `findUnique` + `update` in `prisma.$transaction` with `isolationLevel: Serializable` or use `update` with a compound `where: { id, approvalStatus: { notIn: ['pending', 'approved'] } }` and check the result count.

## Agent Fingerprint

`<!-- agent-fp: 4cbf93d87242 -->`

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
