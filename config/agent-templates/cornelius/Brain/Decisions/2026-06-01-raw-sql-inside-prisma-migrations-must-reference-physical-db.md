---
title: "Raw SQL inside Prisma migrations must reference physical DB column names (snake_case, as mapped by `@map()`), never Pris"
date: "2026-06-01"
decision: "Raw SQL inside Prisma migrations must reference physical DB column names (snake_case, as mapped by `@map()`), never Prisma model-layer field names (camelCase). When in doubt, use `prisma migrate diff`"
stakeholders: "Backend / DBA"
review_by: "2026-09-01"
source: "[[Raw/sources/2026-06-01-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Raw SQL inside Prisma migrations must reference physical DB column names (snake_case, as mapped by `@map()`), never Prisma model-layer field names (camelCase). When in doubt, use `prisma migrate diff` output (Prisma-generated SQL) instead of handwritten raw DML.

**Rationale:** EXP-256. Migration `20260601000000` hardcoded `"userId"` in a raw DELETE while EXP-248 (PR #719) simultaneously renamed the column to `user_id`. Environments applying migrations in a different order fail with column-not-found. This invariant complements the 2026-05-28 "never modify applied migrations" rule — together they govern both migration immutability and migration correctness.

**Stakeholders:** Backend / DBA

**Source:** [[Raw/sources/2026-06-01-experts-agent-digest.md]]
