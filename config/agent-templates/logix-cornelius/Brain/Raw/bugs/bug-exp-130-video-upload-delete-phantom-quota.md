---
title: "EXP-130: Video upload+delete cycle depletes user_storage_usage causing phantom quota on /internal/upload"
linear_id: "EXP-130"
agent_fp: "7e218630cc7a"
date: "2026-05-26"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, storage, ledger, video, project/experts]
category: "bug"
source: "automation"
---

# EXP-130: Video upload+delete cycle depletes user_storage_usage causing phantom quota on /internal/upload

**Linear:** [EXP-130](https://linear.app/experts/issue/EXP-130/bug-video-uploaddelete-cycle-depletes-user-storage-usage-causing) | **Fingerprint:** `<!-- agent-fp: 7e218630cc7a -->` | **Severity: High**

## Summary

The `releaseStorageBytes()` call added by EXP-121 (PR #493) decrements `user_storage_usage.used_bytes` on every lesson-video deletion. However, the lesson-video **upload** path (`POST /api/v1/courses/{id}/modules/{mid}/lessons/{lid}/video`) uses the **old `enforceStorageQuota` aggregate check** — not the `reserveStorageBytes` reservation system. This means deletions decrement a balance that was never incremented via the new ledger, producing phantom quota deductions and allowing uploads that would otherwise be blocked.

## Trigger Scenario

**Preconditions:** An instructor has files tracked by the reservation system (`user_storage_usage.used_bytes` = 500 MB from `/api/v1/internal/upload` uploads).

1. Instructor uploads a 200 MB lesson video via `POST /api/v1/courses/{id}/modules/{mid}/lessons/{lid}/video`. `enforceStorageQuota` checks `file.aggregate` (700 MB < 1 GB quota → passes). `user_storage_usage.used_bytes` is **not updated** — old path does not write to the ledger.
2. Instructor deletes the video via `DELETE /api/v1/courses/{id}/modules/{mid}/lessons/{lid}/video`. `releaseStorageBytes(userId, 200 MB)` runs unconditionally → decrements `used_bytes` from 500 MB to 300 MB.
3. Ledger now shows 300 MB, but actual reservation-tracked bytes total 500 MB. A 200 MB phantom credit has been injected.
4. Instructor tries to upload a 650 MB file via `/api/v1/internal/upload`. Quota check: 300 MB (ledger) + 650 MB (reservation) = 950 MB < 1 GB → **allowed**. Actual post-upload usage would be 1150 MB — 150 MB over quota.

## Root Cause

Two parallel quota accounting systems are operating simultaneously:

- `/api/v1/internal/upload` → uses `reserveStorageBytes` → increments `user_storage_usage.used_bytes`
- `POST /api/v1/.../video` (lesson-video upload) → uses `enforceStorageQuota` (aggregate `file._sum.size`) → **does not update** `user_storage_usage.used_bytes`

EXP-121 added `releaseStorageBytes()` to the video DELETE handler unconditionally, without checking whether the deleted file was originally tracked in the reservation system. The decrement runs even when the corresponding upload never incremented the ledger.

## Fix Direction

Option 1 (preferred): migrate the lesson-video upload path to `reserveStorageBytes` (tracked as EXP-103), making the upload symmetric with the delete. `releaseStorageBytes` is then correct by construction.

Option 2 (interim): guard `releaseStorageBytes()` to only decrement if the file's bytes were actually tracked in `user_storage_usage` — e.g. check whether `user_storage_usage.used_bytes` would go negative, or tag files at upload time to indicate which accounting system tracked them.

Option 1 is preferred as it eliminates the dual-system split entirely.

## Related

- [EXP-103](https://linear.app/experts/issue/EXP-103) — migrate 5 remaining upload routes to `reserveStorageBytes`
- [EXP-121](https://linear.app/experts/issue/EXP-121) — deletion decrement fix (PR #493) that introduced this asymmetry
- [EXP-80](https://linear.app/experts/issue/EXP-80) — reservation ledger
- [EXP-131](https://linear.app/experts/issue/EXP-131) — R2-before-DB ordering bug in the same DELETE handler

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
