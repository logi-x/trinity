---
title: "EXP-110 — [spinoff: EXP-80] Error handling + structured logging in reservation-cleanup cron"
date: "2026-05-24"
status: resolved
resolution: "PR #465: wrapped reservation-cleanup cron handler in try/catch with structured JSON logging (operation, duration, rows_deleted, error fields). Errors are now observable via log aggregation."
tags: [bug, storage, cron, observability, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-110"
fingerprint: "agent-fp:R5-exp80-cleanup-logging-001"
---

## Summary

The `reservation-cleanup` cron route introduced in PR #470 had no error handling or structured logging. A failed cleanup run would silently return 500 with no observability into what failed or how many rows were affected.

## Root cause

The initial implementation focused on correctness of the cleanup logic. Observability instrumentation was deferred and not added before merge.

## Agent fingerprint

`<!-- agent-fp:R5-exp80-cleanup-logging-001 -->`

## Status

Resolved — PR #465 merged 2026-05-24.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
