---
title: "EXP-124: Storage reservation DELETE endpoint lacks user_id ownership check"
linear_id: "EXP-124"
agent_fp: "7c049d9fa99b"
date: "2026-05-25"
severity: "High"
status: "Backlog"
tags: [bug, security, storage, idor, project/experts]
category: "bug"
source: "automation"
---

# EXP-124: Storage reservation DELETE endpoint lacks user_id ownership check

**Linear:** EXP-124 | **Fingerprint:** `<!-- agent-fp: 7c049d9fa99b -->` | **Severity: High**

## Summary

The `DELETE /api/v1/internal/storage/reservations/:id` endpoint (introduced with EXP-80's reservation-cleanup cron sidecar) deletes a reservation by `id` without verifying that the authenticated user owns the reservation. Any authenticated user who knows or can guess another user's `reservationId` can cancel that user's reservation.

## Impact

- **IDOR (Insecure Direct Object Reference)**: User A can cancel User B's active upload reservation.
- Cancelling a reservation while User B's upload is in-flight causes the subsequent `finalize` to fail (reservation not found), dropping the upload silently.
- In a DoS scenario, an attacker could rapidly cancel all active reservations for a target user, preventing them from uploading any files.

## Root Cause

The DELETE handler performs:
```ts
await db.userStorageReservation.delete({ where: { id: reservationId } });
```
without adding `userId: session.user.id` to the where clause.

## Fix

Scope the deletion to the authenticated user:
```ts
await db.userStorageReservation.deleteMany({
  where: { id: reservationId, userId: session.user.id },
});
```
Return 404 (not 403) if no rows are deleted to avoid confirming reservation existence to unauthorized callers.

## Related

- EXP-80 (advisory-lock reservation ledger)
- EXP-122 (stale reservation quota-bypass)
- EXP-121 (used_bytes decrement on deletion)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
