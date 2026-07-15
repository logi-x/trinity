---
title: "EXP-58 — Upload transactional integrity: pending→ready File status + storage-janitor + orphan sweep"
date: "2026-05-21"
status: resolved
resolution: fixed — PR #311 (pending→ready flow) + PR #337 (storage-janitor + orphan sweep cron)
tags: [bug, security, data-integrity, upload, storage-janitor, cron, project/experts]
linear: "https://linear.app/experts/issue/EXP-58"
fingerprint: "32f9c0969d97"
---

## Summary

Original upload path could leave dangling R2 objects (DB row created but R2 PUT failed) or dangling attachments (attachment scope removed but File/R2 retained). No janitor existed to clean up orphaned objects.

## Repro

1. Start an upload; interrupt after DB row creation but before R2 PUT completes
2. Observe: DB row with status `pending` persists indefinitely with no R2 object
3. Remove an attachment scope; observe: File and R2 object retained with no cleanup

## Agent fingerprint

`<!-- agent-fp: 32f9c0969d97 -->`

## Status

`resolved` — PR #311 adds `File.status: pending→ready` two-phase commit; PR #337 introduces storage-janitor cron sweep.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
