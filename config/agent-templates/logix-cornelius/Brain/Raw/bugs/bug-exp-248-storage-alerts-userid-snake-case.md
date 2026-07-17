---
title: "EXP-248: storage_alerts.userId is the only unmapped camelCase column — snake_case convention break"
date: "2026-06-01"
status: resolved
resolution: "merged PR #719"
tags: [bug, db, schema, naming, project/experts]
linear: "https://linear.app/experts/issue/EXP-248/db-snake-case-storage-alertsuserid-user-id-lone-unmapped-userid-column"
fingerprint: "c41d8e2b7a90"
---

## Summary

`storage_alerts.userId` was the only column among 41 `userId` columns in the Prisma schema that lacked an `@map("user_id")` annotation. This was a convention break originating from the EXP-82 migration. It caused an inconsistency in raw SQL queries and was the root cause of EXP-256 (migration hardcodes `"userId"` instead of `"user_id"`). Fixed by PR #719 (additive migration renaming the column + schema annotation).

## Location

`apps/experts-app/prisma/schema.prisma` — `StorageAlert` model `userId` field (missing `@map("user_id")`)

## Repro Steps

Inspect schema: `grep -n 'userId' prisma/schema.prisma | grep -v '@map'` — `StorageAlert.userId` is the only hit.

## Agent Fingerprint

`c41d8e2b7a90` (R3)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
