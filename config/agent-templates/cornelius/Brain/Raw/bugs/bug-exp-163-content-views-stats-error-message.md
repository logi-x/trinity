---
title: "EXP-163: error.message unconditionally exposed in content-views stats route"
linear_id: "EXP-163"
agent_fp: "d9f0b99eeffb"
spinoff_of: "EXP-155"
date: "2026-05-28"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, api, project/experts]
category: "bug"
source: "automation"
---

# EXP-163: error.message in content-views stats route

**Linear:** [EXP-163](https://linear.app/experts/issue/EXP-163) | **Fingerprint:** `d9f0b99eeffb`

## Summary
`GET /api/v1/content/views/stats` catch block returns `details: error instanceof Error ? error.message : "Unknown error"` unconditionally. No `APP_ENV !== "production"` guard.

## Location
`apps/experts-app/app/api/v1/content/views/stats/route.ts:175`

## Fix
Apply `safeErrorJson` helper (PR #557) or wrap `details` behind `APP_ENV` guard.

## Related
EXP-155 (parent), EXP-164, EXP-165 (same batch)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
