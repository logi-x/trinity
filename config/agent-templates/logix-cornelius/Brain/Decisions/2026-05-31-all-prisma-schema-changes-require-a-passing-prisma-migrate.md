---
title: "All Prisma schema changes require a passing `prisma migrate diff --shadow-database-url` CI check before merge; schema↔mi"
date: "2026-05-31"
decision: "All Prisma schema changes require a passing `prisma migrate diff --shadow-database-url` CI check before merge; schema↔migration drift is a hard CI gate, not a code-review item."
stakeholders: "Logix"
review_by: "2026-08-31"
source: "[[Raw/sources/2026-05-31-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** All Prisma schema changes require a passing `prisma migrate diff --shadow-database-url` CI check before merge; schema↔migration drift is a hard CI gate, not a code-review item.

**Rationale:** EXP-227 / PR #681. EXP-220 (missing `deleted_at` migration) and EXP-169 (squashed applied migrations) demonstrate that migration drift goes undetected without an automated check. The shadow-DB diff exits 1 on any detected drift, catching both forgotten migrations and modified-applied-migration violations before they reach any environment. The 2026-05-28 "never modify applied migrations" convention covers the complementary invariant.

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-05-31-experts-agent-digest.md]]
