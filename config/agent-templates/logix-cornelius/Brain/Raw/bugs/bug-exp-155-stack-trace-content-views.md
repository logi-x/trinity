---
title: "EXP-155: Stack trace AND error.message unconditionally exposed in content-views 500 responses"
linear_id: "EXP-155"
agent_fp: "934996db875e"
spinoff_of: "EXP-132"
date: "2026-05-27"
severity: "Medium"
status: "resolved"
resolution: "merged PR #556"
tags: [bug, security, api, project/experts]
category: "bug"
source: "automation"
---

# EXP-155: Stack trace + error.message in content-views

**Linear:** [EXP-155](https://linear.app/experts/issue/EXP-155) | **Fingerprint:** `934996db875e`

## Summary
`GET` and `POST /api/v1/content/views/[contentType]/[contentId]` exposed both `stack` AND `error.message` unconditionally. Spun off EXP-163/164/165 (stats/track/batch routes same class).

## Fix
PR #556 (field-level), PR #557 (class-level ESLint enforcement).

## Related
EXP-132 (parent), EXP-163, EXP-164, EXP-165 (spinoffs)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
