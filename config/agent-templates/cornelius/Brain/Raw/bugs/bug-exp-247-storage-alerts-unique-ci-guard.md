---
title: "EXP-247: storage_alerts UNIQUE(userId) never reached prod — migration edited in place after apply"
date: "2026-06-01"
status: resolved
resolution: "merged PR #717"
tags: [bug, db, migrations, ci, project/experts]
linear: "https://linear.app/experts/issue/EXP-247/db-storage-alerts-uniqueuserid-never-reached-prod-migration-edited-in"
fingerprint: "9f3b6c1e80a2"
---

## Summary

Migration `20260524000001_storage_alert` was edited in place after it had been applied to environments. It swapped an `INDEX(userId, sent_at)` for a `UNIQUE(userId)`. Prisma replays migrations by name; the edit never re-ran on already-migrated environments. Envs deployed before the edit kept the old non-unique index — `UNIQUE(userId)` never reached staging or production. Fresh DBs (CI, new installs) had the unique constraint while existing envs did not, creating a schema split. PR #717 adds a forward-only migration to enforce the constraint plus a CI immutability guard to prevent recurrence.

## Location

`prisma/migrations/20260524000001_storage_alert/migration.sql` (retroactively edited)

## Repro Steps

1. Apply original migration (INDEX variant).
2. Edit migration file to use UNIQUE.
3. `prisma migrate deploy` on the already-migrated env — no change applied; UNIQUE never enforced.

## Agent Fingerprint

`9f3b6c1e80a2` (R3)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
