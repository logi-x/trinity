---
title: "EXP-256: Migration 000000 raw DELETE references hardcoded 'userId' column — fails if column pre-renamed"
date: "2026-06-01"
status: open
resolution: unknown
tags: [bug, db, migrations, project/experts]
linear: "https://linear.app/experts/issue/EXP-256/bug-migration-000000-raw-delete-references-hardcoded-userid-column"
fingerprint: "a255a6272d63"
---

## Summary

Migration `20260601000000_storage_alerts_enforce_unique_user` contains a raw SQL `DELETE` that references the `"userId"` column by its camelCase (Prisma model-layer) name with no column-existence guard. The EXP-248 fix (PR #719, merged the same day) renamed that column to `user_id`. Environments where PR #719 migrations run before this migration will fail with column-not-found on the raw DELETE. This creates an ordering-sensitive migration fragility.

## Location

`prisma/migrations/20260601000000_storage_alerts_enforce_unique_user/migration.sql` — raw `DELETE FROM "storage_alerts" a USING "storage_alerts" b WHERE a."userId" = b."userId"...`

## Repro Steps

1. Apply migration `20260601000000` on a DB where `storage_alerts."userId"` has already been renamed to `"user_id"` by the EXP-248 migration.
2. Observe `column storage_alerts.userId does not exist` error.

## Agent Fingerprint

`a255a6272d63` (R3)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
