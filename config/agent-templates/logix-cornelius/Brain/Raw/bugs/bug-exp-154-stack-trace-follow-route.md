---
title: "EXP-154: Stack trace unconditionally exposed in POST+DELETE /follow 500 responses"
linear_id: "EXP-154"
agent_fp: "b3683e1f8c84"
spinoff_of: "EXP-132"
date: "2026-05-27"
severity: "Medium"
status: "resolved"
resolution: "merged PR #552"
tags: [bug, security, api, project/experts]
category: "bug"
source: "automation"
---

# EXP-154: Stack trace in follow/unfollow route

**Linear:** [EXP-154](https://linear.app/experts/issue/EXP-154) | **Fingerprint:** `b3683e1f8c84`

## Summary
`POST` and `DELETE /api/v1/users/[username]/follow` catch blocks included `stack` in 500 responses unconditionally. Class-level fix (PR #557) now enforces `APP_ENV` guard via ESLint.

## Fix
PR #552, class-level fix PR #557.

## Related
EXP-132 (parent), EXP-153, EXP-155

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
