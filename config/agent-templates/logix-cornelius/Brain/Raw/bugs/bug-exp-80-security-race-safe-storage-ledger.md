---
title: "EXP-80 — Race-safe storage usage ledger (UserStorageUsage + reservation flow)"
date: "2026-05-22"
status: open
resolution: unknown
tags: [bug, security, storage, concurrency, project/experts]
linear: "https://linear.app/experts/issue/EXP-80/security-race-safe-storage-usage-ledger-userstorageusage-reservation"
fingerprint: "c3eb6a48c4db"
---

## Summary

The current storage quota gate (EXP-72, PR #408) enforces a per-user cap by aggregating `File.size` via `prisma.file.aggregate()` at upload time. Under concurrent uploads, two requests can both read the quota as under-limit before either write completes, causing the actual stored bytes to exceed the limit (classic TOCTOU / read-modify-write race). A race-safe `UserStorageUsage` ledger with atomic increments or a pre-upload reservation flow is required.

## Root cause

`app/api/v1/internal/upload/route.ts` — quota check and upload are not atomic. Two concurrent uploads for the same user can both pass the preflight check before either's `File` row is committed, collectively exceeding the quota.

## Agent fingerprint

`<!-- agent-fp: c3eb6a48c4db -->`

## Status

`open` — Backlog. Depends on EXP-72 (quota gate, merged PR #408). Ready to flip to Todo immediately.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
