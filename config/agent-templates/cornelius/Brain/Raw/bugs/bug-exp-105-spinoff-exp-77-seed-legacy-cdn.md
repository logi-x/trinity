---
title: "EXP-105 — [spinoff: EXP-77] Seed data migration list from existing R2 keys"
date: "2026-05-24"
status: resolved
resolution: "PR #460: added a one-off migration script that enumerates existing R2 keys matching legacy path prefixes and writes them to a migration tracking table for the CDN cutover."
tags: [bug, storage, r2, migration, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-105"
fingerprint: "agent-fp:R5-exp77-seed-cdn-migration-001"
---

## Summary

EXP-77 planned a CDN migration for files stored under legacy R2 path prefixes, but no migration tracking list was seeded. Without a list of affected keys, the CDN cutover would silently miss pre-existing files.

## Root cause

The EXP-77 PR added the new upload path tree but did not enumerate existing legacy keys. The migration script was deferred and never created.

## Agent fingerprint

`<!-- agent-fp:R5-exp77-seed-cdn-migration-001 -->`

## Status

Resolved — PR #460 merged 2026-05-24.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
