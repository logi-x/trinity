---
title: "EXP-118: StorageAlert createMany dedup race condition"
linear_id: "EXP-118"
agent_fp: "49154b8b9114"
spinoff_of: "EXP-113"
date: "2026-05-25"
severity: "Medium"
status: "Todo"
tags: [bug, storage, race-condition, project/experts]
category: "bug"
source: "automation"
---

# EXP-118: StorageAlert createMany dedup race condition

**Linear:** EXP-118 | **Fingerprint:** `<!-- agent-fp: 49154b8b9114 -->` | **Spinoff of:** EXP-113

## Summary

`checkAndSendStorageAlerts` uses `createMany` to batch-insert alert records, but does not deduplicate on `(userId, alertType)`. If the cron runs twice in rapid succession (or if the function is called from two concurrent invocations), duplicate alert records are inserted and duplicate emails are dispatched to the user.

## Impact

- Users receive multiple "80% full" or "storage limit reached" emails for the same event.
- Duplicate records inflate alert history in the admin dashboard.
- In the absence of a cron route (EXP-113), the risk is theoretical — but will materialise immediately once the function is wired.

## Root Cause

No unique constraint on `(userId, alertType, sentAt::date)` in the storage alerts table. `createMany` does not check for existing records before inserting.

## Fix

Option A: Add a unique index on `(userId, alertType, DATE(sentAt))` and use `createMany({ skipDuplicates: true })`.

Option B: Use `upsert` per-alert keyed on `(userId, alertType)` with a cooldown check (don't re-send the same alert type within 24h).

Option B is recommended — it also prevents repeated alerts on subsequent cron runs for the same over-quota user.

## Related

- EXP-113 (parent — dead checkAndSendStorageAlerts)
- EXP-106 (StorageWarningNotification emails implementation)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
