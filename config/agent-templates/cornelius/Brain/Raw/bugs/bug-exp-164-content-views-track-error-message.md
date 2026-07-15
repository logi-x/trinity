---
title: "EXP-164: error.message unconditionally exposed in content-views track route"
linear_id: "EXP-164"
agent_fp: "d86d455719c3"
spinoff_of: "EXP-155"
date: "2026-05-28"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, api, project/experts]
category: "bug"
source: "automation"
---

# EXP-164: error.message in content-views track route

**Linear:** [EXP-164](https://linear.app/experts/issue/EXP-164) | **Fingerprint:** `d86d455719c3`

## Summary
`POST /api/v1/content/views/track` catch block returns `details: error instanceof Error ? error.message : "Unknown error"` unconditionally.

## Location
`apps/experts-app/app/api/v1/content/views/track/route.ts:325`

## Fix
Apply `safeErrorJson` helper or APP_ENV guard.

## Related
EXP-155 (parent), EXP-163, EXP-165

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
