---
title: "EXP-113 — checkAndSendStorageAlerts has no cron route — dead unreachable function"
date: "2026-05-25"
status: open
resolution: unknown
tags: [bug, storage, cron, dead-code, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-113"
fingerprint: "agent-fp:R2-dead-alert-function-001"
---

## Summary

`checkAndSendStorageAlerts()` is fully implemented in `lib/storage/alerts.ts` — it queries usage, compares against thresholds (80%, 100%), and dispatches `StorageWarningNotification` / `StorageLimitNotification` emails. However, no cron route calls it. The function is dead code: it cannot be triggered in production.

## Root cause

EXP-82 (admin storage dashboard) and EXP-106 (notification wiring) were focused on the dashboard UI and transactional email dispatch. The periodic alert check was implemented but the Docker cron sidecar schedule was not updated to add a corresponding cron route.

## Agent fingerprint

`<!-- agent-fp:R2-dead-alert-function-001 -->`

## Status

Open — decision required: (a) add `/api/v1/internal/storage/check-alerts` cron route + Docker sidecar schedule entry, or (b) refactor as an event-driven hook from the reservation-finalize path. See architecture-reviewer note in today's digest.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
