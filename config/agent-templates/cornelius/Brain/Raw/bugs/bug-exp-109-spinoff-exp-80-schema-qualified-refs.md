---
title: "EXP-109 — [spinoff: EXP-80] Schema-qualified Prisma model refs in reservation flow"
date: "2026-05-24"
status: resolved
resolution: "PR #464: added schema-qualified references (public.user_storage_reservations, public.user_storage_usage) to all Prisma raw queries in the reservation flow to avoid cross-schema ambiguity."
tags: [bug, storage, prisma, database, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-109"
fingerprint: "agent-fp:R5-exp80-schema-refs-001"
---

## Summary

Prisma raw queries in the EXP-80 storage reservation flow referenced `user_storage_reservations` and `user_storage_usage` without schema qualification. In a multi-schema Postgres setup, unqualified table names resolve to the connection's `search_path`, which could differ between app and migration contexts.

## Root cause

The EXP-80 implementation used `$queryRaw` with unqualified table names. Schema qualification is required for raw queries to guarantee correct resolution regardless of `search_path`.

## Agent fingerprint

`<!-- agent-fp:R5-exp80-schema-refs-001 -->`

## Status

Resolved — PR #464 merged 2026-05-24.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
