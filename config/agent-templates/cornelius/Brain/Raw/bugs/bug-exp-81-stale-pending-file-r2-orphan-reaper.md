---
title: "EXP-81 — Stale pending file row cleanup + R2 orphan reaper"
date: "2026-05-22"
status: open
resolution: unknown
tags: [bug, storage, cleanup, project/experts]
linear: "https://linear.app/experts/issue/EXP-81/bug-stale-pending-file-row-cleanup-r2-orphan-reaper"
fingerprint: "834b7e67b87f"
---

## Summary

Two cleanup gaps exist after EXP-72 (storage quota gate, PR #408): (1) `File` rows stuck in `pending` status longer than the upload TTL are never cleaned up — they hold space against the quota indefinitely; (2) R2 objects whose corresponding DB rows were deleted (or whose upload was aborted after the R2 PUT completed) become orphans that occupy real R2 storage but are invisible to the quota system.

## Root cause

No scheduled cleanup for stale `pending` File rows. No R2 orphan reaper that cross-references DB records against R2 object listings.

## Agent fingerprint

`<!-- agent-fp: 834b7e67b87f -->`

## Status

`open` — Backlog. Depends on EXP-72 (merged PR #408). Can run in parallel with EXP-80 (race-safe ledger).

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
