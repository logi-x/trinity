---
title: "EXP-169: Prisma migration checksum drift blocks prisma migrate deploy"
linear_id: "EXP-169"
agent_fp: "28f8a0440001"
date: "2026-05-28"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, prisma, migrations, project/experts]
category: "bug"
source: "automation"
---

# EXP-169: Prisma migration checksum drift

**Linear:** [EXP-169](https://linear.app/experts/issue/EXP-169) | **Fingerprint:** `28f8a0440001`

## Summary
Commit `02266b32` squashed two already-applied migrations in-place (`20260524000001_storage_alert`). Any environment that applied EXP-118's migration will have a checksum mismatch and `prisma migrate deploy` will fail with P3005/P3006 errors, blocking all future migrations.

## Location
`apps/experts-app/prisma/migrations/20260524000001_storage_alert/migration.sql`

## Impact
**Deployment blocker.** All future schema migrations are blocked on any environment with EXP-118 applied (staging, production if already deployed).

## Repro
1. Apply EXP-118 migration to a clean database.
2. Pull commit `02266b32`.
3. Run `prisma migrate deploy`.
4. Observe P3005/P3006 checksum drift error.

## Fix
Create a new additive migration that correctly applies the missing unique constraint without modifying existing migration files. Never squash already-applied migrations.

## Decision-Log
See "Prisma migration workflow" note: applied migrations must never be mutated in-place.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
