---
title: "EXP-87 — File.size column is Int32 — overflows at ~2.1GB; migrate to BigInt before any tier exceeds 2GB"
date: "2026-05-23"
status: open
resolution: unknown
tags: [bug, security, storage, schema, data-integrity, project/experts]
linear: "https://linear.app/experts/issue/EXP-87/security-filesize-column-is-int32-overflows-at-21gb-migrate-to-bigint"
fingerprint: "2d5b36fd7b73"
---

## Summary

The `File.size` column in the Prisma schema is typed as `Int` (Int32), which overflows at ~2,147,483,647 bytes (~2.1 GB). The current uniform quota is 1 GB (safe today), but EXP-72 (quota gate) and EXP-80 (usage ledger) together will make 2 GB reachable per user in production as quota tiers grow. Uploading a file ≥ 2.1 GB will silently corrupt the `size` value, breaking quota enforcement and usage reporting.

## Root cause

`prisma/schema.prisma` — `File.size Int` should be `File.size BigInt`.

## Migration path

1. Create Prisma migration changing `File.size` from `Int` to `BigInt`.
2. Update all TypeScript callers that treat `File.size` as `number` to handle `bigint` (or serialize as string for JSON transport).
3. Deploy before any quota tier exceeds 2 GB.

## Agent fingerprint

`<!-- agent-fp: 2d5b36fd7b73 -->`

## Status

`open` — Backlog. Safe today (1 GB uniform quota). Hard prerequisite of quota tier roadmap. Surfaced during EXP-72 merge review.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
