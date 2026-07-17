---
title: "EXP-57 — Per-user storage quota missing on /api/v1/internal/upload"
date: "2026-05-21"
status: open
resolution: unknown — rate-limit shipped (PR #310), quota not yet implemented
tags: [bug, security, dos, upload, quota, business-logic, project/experts]
linear: "https://linear.app/experts/issue/EXP-57"
fingerprint: "bf13d711cd77"
---

## Summary

Upload route has per-user rate limiting (PR #310) but no cumulative storage quota. An authenticated user can upload an unbounded total volume of data, exhausting R2 storage and incurring unbounded cost.

## Repro

1. Authenticate as any user
2. Upload files repeatedly until rate limit resets, cycling through sessions
3. Observe: no 413 or quota-exceeded error regardless of total uploaded size

## Agent fingerprint

`<!-- agent-fp: bf13d711cd77 -->`

## Status

`open` — rate-limit shipped, per-user quota still open. See Action-Tracker 2026-05-21.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
