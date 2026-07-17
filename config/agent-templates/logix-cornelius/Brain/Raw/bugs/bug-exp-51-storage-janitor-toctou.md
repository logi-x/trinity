---
title: "EXP-51 — TOCTOU: R2 deleted before DB guard in pending-file sweep corrupts ready file records"
date: "2026-05-20"
status: resolved
resolution: "Merged PR #348 (commit 5877e626): operation order swapped — file.deleteMany runs first; deletePublicAsset only called when deleted.count > 0."
tags: [bug, storage-janitor, race-condition, toctou, high, project/experts]
linear: "https://linear.app/experts/issue/EXP-51"
fingerprint: "9a8cca3642bf"
---

## Summary

`runStorageJanitorSweep` deleted the R2 object before running the atomic DB guard (`file.deleteMany`). If an upload-confirm request raced in that window and flipped `File.status` to `ready`, the DB guard correctly matched 0 rows (file is now ready) but could not undo the R2 deletion. Result: a `ready` `File` record pointing at a non-existent R2 key — any subsequent GET on the file silently returns 404.

## Repro

1. Start a file upload (`File.status = pending`).
2. Trigger the pending-file sweep.
3. Sweep deletes the R2 object.
4. Upload-confirm sets `File.status = ready`.
5. DB guard in sweep matches 0 rows; rows not deleted.
6. File record is `ready` but R2 key does not exist — file requests return 404.

## Agent fingerprint

`<!-- agent-fp: 9a8cca3642bf -->`

## Resolution

Merged PR #348 (commit `5877e626`): `file.deleteMany` (DB guard) now runs first; `deletePublicAsset` (R2 delete) is only called when `deleted.count > 0`. A raced file returns 0 from `deleteMany` and R2 is never touched. Race-scenario test now asserts R2 is only called for confirmed-deleted rows.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
