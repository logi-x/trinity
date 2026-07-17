---
title: "EXP-130: Video upload+delete cycle depletes user_storage_usage causing phantom quota"
linear_id: "EXP-130"
agent_fp: "7e218630cc7a"
date: "2026-05-26"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, storage, video, quota, ledger, project/experts]
category: "bug"
source: "automation"
---

# EXP-130: Video upload+delete cycle depletes user_storage_usage causing phantom quota

**Linear:** [EXP-130](https://linear.app/experts/issue/EXP-130) | **Fingerprint:** `<!-- agent-fp: 7e218630cc7a -->` | **Severity: High**

## Summary

The EXP-121 fix (PR #493) added `releaseStorageBytes()` calls to the DELETE video route and `runOrphanAttachmentSweep`. However, the video POST upload route does not go through `reserveStorageBytes` / `promoteReservation` — it uploads directly to R2 outside the reservation system. This creates a one-directional asymmetry: the ledger is never incremented when a video is uploaded via the video route, but `releaseStorageBytes` decrements `used_bytes` when the video is deleted. Result: `used_bytes` goes negative or under-reports available storage, causing phantom quota availability or, conversely, phantom quota lockout depending on execution order.

## Impact

- Instructors who upload and delete course videos repeatedly will accumulate negative `used_bytes` debt, making their storage appear larger than it is (phantom available space).
- The same asymmetry exists in `runOrphanAttachmentSweep`: the orphan sweep calls `releaseStorageBytes` for files that were never tracked in the reservation ledger, creating the same negative drift.
- Quota enforcement via `/api/v1/internal/upload` becomes unreliable: users can exceed their actual quota because the ledger under-reports consumption.

## Root Cause

The video route (`POST /api/v1/courses/[id]/modules/[moduleId]/lessons/[lessonId]/video`) uses `enforceStorageQuota` against the raw `file.aggregate` sum, then uploads directly to R2 without creating a reservation row or calling `promoteReservation`. It therefore never contributes to `user_storage_usage.used_bytes`. The EXP-121 fix was correct for files that go through the reservation path, but the video route and orphan sweep both call `releaseStorageBytes` without a matching increment on the upload side.

## Repro Steps

1. Instructor uploads a 200 MB video via `POST /api/v1/courses/{id}/modules/{mid}/lessons/{lid}/video`.
2. Verify `user_storage_usage.used_bytes` for the instructor's user ID — it is **not incremented** (video route bypasses reservation).
3. Instructor deletes the video via `DELETE /api/v1/courses/{id}/modules/{mid}/lessons/{lid}/video`.
4. `releaseStorageBytes` is called — `used_bytes` is decremented by the video's file size.
5. `used_bytes` is now negative (or lower than actual committed storage), reporting phantom available quota.

## Fix

Either: (a) route video uploads through `reserveStorageBytes` / `promoteReservation` so the video route contributes to the ledger symmetrically, or (b) gate `releaseStorageBytes` calls to only files that were originally tracked via `promoteReservation` (i.e., check for a `user_storage_usage` row before decrementing). Option (a) is architecturally preferred for consistency.

## Related

- EXP-121 (used_bytes decrement fix that introduced this regression)
- EXP-80 (reservation ledger design)
- EXP-131 (video DELETE removes R2 before DB transaction — related video route issue)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
