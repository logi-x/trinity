---
title: "EXP-166: commissions/approve-pending route exposes raw error.message in 500 responses"
linear_id: "EXP-166"
agent_fp: "c19c55c23978"
spinoff_of: "EXP-116"
date: "2026-05-28"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, api, project/experts]
category: "bug"
source: "automation"
---

# EXP-166: commissions route error.message exposure

**Linear:** [EXP-166](https://linear.app/experts/issue/EXP-166) | **Fingerprint:** `c19c55c23978`

## Summary
`POST` and `GET /api/v1/admin/commissions/approve-pending` catch blocks return `error instanceof Error ? error.message : "..."` unconditionally. No `APP_ENV` guard. Raw Prisma/DB error text emitted to any authenticated admin.

## Location
`apps/experts-app/app/api/v1/admin/commissions/approve-pending/route.ts:112-114` (POST), `:166-168` (GET)

## Fix
Apply `safeErrorJson` helper from PR #557.

## Related
EXP-116 (parent), EXP-132 (class)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
