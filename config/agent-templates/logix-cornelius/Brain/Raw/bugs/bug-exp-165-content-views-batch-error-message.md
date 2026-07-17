---
title: "EXP-165: error.message unconditionally exposed in content-views batch route"
linear_id: "EXP-165"
agent_fp: "f8bca258fd65"
spinoff_of: "EXP-155"
date: "2026-05-28"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, api, project/experts]
category: "bug"
source: "automation"
---

# EXP-165: error.message in content-views batch route

**Linear:** [EXP-165](https://linear.app/experts/issue/EXP-165) | **Fingerprint:** `f8bca258fd65`

## Summary
`POST /api/v1/content/views/batch` catch block returns `details: error instanceof Error ? error.message : "Unknown error"` unconditionally.

## Location
`apps/experts-app/app/api/v1/content/views/batch/route.ts:275`

## Fix
Apply `safeErrorJson` helper or APP_ENV guard.

## Related
EXP-155 (parent), EXP-163, EXP-164

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
