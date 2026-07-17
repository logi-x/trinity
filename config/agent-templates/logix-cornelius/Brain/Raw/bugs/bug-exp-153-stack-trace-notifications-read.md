---
title: "EXP-153: Stack trace unconditionally exposed in POST /notifications/read 500 response"
linear_id: "EXP-153"
agent_fp: "4de17619b56a"
spinoff_of: "EXP-132"
date: "2026-05-27"
severity: "Medium"
status: "resolved"
resolution: "merged PR #551"
tags: [bug, security, api, project/experts]
category: "bug"
source: "automation"
---

# EXP-153: Stack trace in notifications/read

**Linear:** [EXP-153](https://linear.app/experts/issue/EXP-153) | **Fingerprint:** `4de17619b56a`

## Summary
`POST /api/v1/user/notifications/read` catch block included `stack` in 500 responses without `APP_ENV` guard. Any authenticated user who triggers a server error receives full Node.js stack trace.

## Fix
PR #551 wrapped `stack` behind `APP_ENV !== "production"` spread. Class-level fix: PR #557 `safeErrorJson` + ESLint rule prevents recurrence.

## Related
EXP-132 (parent), EXP-154, EXP-155 (same class)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
