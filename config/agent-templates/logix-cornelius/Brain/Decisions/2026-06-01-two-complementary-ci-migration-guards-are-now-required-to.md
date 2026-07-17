---
title: "Two complementary CI migration guards are now required to pass before any PR touching the Prisma schema or migration dir"
date: "2026-06-01"
decision: "Two complementary CI migration guards are now required to pass before any PR touching the Prisma schema or migration directory can merge: (1) shadow-DB drift check (`prisma migrate diff --from-migrati"
stakeholders: "Backend, CI/CD"
review_by: "2026-06-15"
source: "[[Raw/sources/2026-06-01-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Two complementary CI migration guards are now required to pass before any PR touching the Prisma schema or migration directory can merge: (1) shadow-DB drift check (`prisma migrate diff --from-migrations --to-schema`), and (2) migration-immutability check (fails any PR that modifies, renames, or deletes a migration file already present on the base branch).

**Rationale:** Guard 1 (PR #681) catches schema↔migration drift (the EXP-220 class). Guard 2 (PR #717) independently prevents retroactive corruption of applied migrations (the EXP-169/EXP-247 class). Neither guard alone covers both failure modes.

**Stakeholders:** Backend, CI/CD

**Source:** [[Raw/sources/2026-06-01-experts-agent-digest.md]]
