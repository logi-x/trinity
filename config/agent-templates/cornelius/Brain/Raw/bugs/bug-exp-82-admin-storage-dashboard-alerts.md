---
title: "EXP-82 — Admin storage dashboard + over-quota alerts"
date: "2026-05-22"
status: open
resolution: unknown
tags: [bug, storage, admin, project/experts]
linear: "https://linear.app/experts/issue/EXP-82/bug-admin-storage-dashboard-over-quota-alerts"
fingerprint: "04250008207c"
---

## Summary

After the EXP-72 quota gate and EXP-80 race-safe ledger land, there is no admin visibility into per-user storage usage or over-quota events. An admin storage dashboard reading from the `UserStorageUsage` ledger and a quota-breach alert mechanism are needed before the system is operationally complete.

## Root cause

No admin dashboard surface for storage usage. No alerting on quota approach or breach.

## Agent fingerprint

`<!-- agent-fp: 04250008207c -->`

## Status

`open` — Backlog. Depends on EXP-72 (quota gate) and EXP-80 (race-safe ledger). Best done after the ledger lands so the dashboard reads `usedBytes` from `UserStorageUsage` rather than a slow `aggregate()` per request.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
