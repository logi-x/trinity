---
title: "EXP-227: [infra] CI guard for Prisma schema↔migration drift (shadow-DB migrate diff)"
linear_id: "EXP-227"
agent_fp: "auto"
date: "2026-05-31"
severity: "Medium"
status: "resolved"
resolution: "PR #681 — added shadow-DB prisma migrate diff CI job; catches schema↔migration drift before merge"
tags: [bug, infra, ci, prisma, project/experts]
category: "bug"
source: "automation"
---

# EXP-227: CI guard for Prisma schema↔migration drift

**Linear:** [EXP-227](https://linear.app/experts/issue/EXP-227) | **Status:** Resolved (PR #681)  
**Follow-up of:** EXP-220 (PR #679)

## Summary
EXP-220 shipped a `deleted_at` migration that had been authored but silently never committed (blanket `*.sql` in `.gitignore`). PR #679 fixed the immediate bug and added a scoped `.gitignore` negation. This follow-up adds a CI job that runs `prisma migrate diff --shadow-database-url` to automatically detect any schema↔migration drift on every PR.

## Fix
PR #681 adds a "Migration Drift" CI job that runs `prisma migrate diff --shadow-database-url` and exits 1 on any detected drift.

## Related
- EXP-220 (missing deleted_at migration, resolved PR #679)
- EXP-169 (squashed applied migrations, 2026-05-28)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
