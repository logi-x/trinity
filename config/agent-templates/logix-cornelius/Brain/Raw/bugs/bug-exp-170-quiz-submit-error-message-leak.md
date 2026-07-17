---
title: "EXP-170: quiz submit route leaks raw error.message via safeErrorJson publicMessage parameter"
linear_id: "EXP-170"
agent_fp: "55d3c00efde3"
date: "2026-05-28"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, api, project/experts]
category: "bug"
source: "automation"
---

# EXP-170: quiz submit error.message leak

**Linear:** [EXP-170](https://linear.app/experts/issue/EXP-170) | **Fingerprint:** `55d3c00efde3`

## Summary
`POST /api/v1/quizzes/attempts/[id]/submit` passes `error.message` as the `publicMessage` parameter to `safeErrorJson`. Unlike `stack`, `publicMessage` is emitted unconditionally in all environments. Raw Prisma/internal error text (e.g., unique constraint violations, FK violations) is exposed in the response body.

## Location
`apps/experts-app/app/api/v1/quizzes/attempts/[id]/submit/route.ts/POST`

## Impact
Any authenticated user who triggers a Prisma-level exception (duplicate answer submission, FK violation) receives raw database error text in the response body in production.

## Fix
Remove `error.message` from `publicMessage` parameter. Use a static user-facing message or omit `publicMessage` entirely.

## Related
EXP-132 (class), EXP-163/164/165/166 (same pattern)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
