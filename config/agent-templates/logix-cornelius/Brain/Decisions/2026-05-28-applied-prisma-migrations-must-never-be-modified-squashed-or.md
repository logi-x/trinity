---
title: "Applied Prisma migrations must never be modified, squashed, or deleted in-place after being applied to any environment. "
date: "2026-05-28"
decision: "Applied Prisma migrations must never be modified, squashed, or deleted in-place after being applied to any environment. Only forward-only additive migrations are permitted; squashing applied migration"
stakeholders: "Logix"
review_by: "2026-06-11"
source: "[[Raw/sources/2026-05-28-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Applied Prisma migrations must never be modified, squashed, or deleted in-place after being applied to any environment. Only forward-only additive migrations are permitted; squashing applied migrations causes P3005/P3006 checksum drift on all environments that ran the original, blocking all future `prisma migrate deploy` calls.

**Rationale:** EXP-169: commit `02266b32` squashed two already-applied migrations. Every environment that ran EXP-118 will fail `prisma migrate deploy` — a deployment blocker. Recovery requires restoring original migration file contents or adding a drift-reset migration. The project migration guide must document this invariant and the recovery procedure.

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-05-28-experts-agent-digest.md]]
