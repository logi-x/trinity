---
title: "EXP-48 — Orphan-sweep every-filter silently skips files with multiple orphaned attachments"
date: "2026-05-20"
status: open
resolution: unknown
tags: [bug, storage-janitor, prisma, high, project/experts]
linear: "https://linear.app/experts/issue/EXP-48"
fingerprint: "18063f5fd318"
---

## Summary

`runOrphanAttachmentSweep` in `storage-janitor.sweeps.ts` uses `every: { id: orphan.id, ...scopeChecks }` as the atomic DB guard inside `file.deleteMany`. Prisma translates `every` to `NOT EXISTS (... WHERE NOT (condition))`. When a file has two orphaned attachments A1 and A2:

- Processing A1: A2 fails `id = A1.id` → `every` is false → `deleteMany` matches 0 rows → skip.
- Processing A2: A1 fails `id = A2.id` → same result → skip.

Neither attachment is ever cleaned. The sweep never converges regardless of how many times it runs.

Secondary bug: `deletePublicAsset` (R2 HTTP DELETE) was called *before* the atomic DB check. When the DB guard failed, the R2 object was already deleted but `File`/`Attachment` rows remained — permanent R2/DB state divergence.

## Repro

1. Create a `File` record with two `Attachment` rows (A1, A2), both orphaned (no back-relations on any scope table).
2. Trigger `POST /api/v1/internal/storage-janitor/orphan-sweep`.
3. Observe: 0 rows cleaned; both attachments and file remain.
4. Repeat — sweep never converges.

## Agent fingerprint

`<!-- agent-fp: 18063f5fd318 -->`

## In-flight fix

PR #345 (`fix/agent/exp-48-orphan-sweep-every-filter`) — **gatekeeper BLOCKED**: the proposed `AND: [{attachments: {none: {id: {not: orphan.id}}}}]` guard is incorrect for the multi-attachment case. Needs redesign.

## Status

`open` — PR #345 gatekeeper blocked. Redesign required before merge.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
