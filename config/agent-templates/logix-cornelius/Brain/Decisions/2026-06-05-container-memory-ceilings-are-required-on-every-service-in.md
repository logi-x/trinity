---
title: "Container memory ceilings are required on every service in all three compose environments (production, staging, dev); Co"
date: "2026-06-05"
decision: "Container memory ceilings are required on every service in all three compose environments (production, staging, dev); Compose-v2 syntax only (`mem_limit`/`memswap_limit`/`shm_size`, NOT `deploy.resour"
stakeholders: "Platform, Logix"
review_by: "2026-09-05"
source: "[[Raw/sources/2026-06-06-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Container memory ceilings are required on every service in all three compose environments (production, staging, dev); Compose-v2 syntax only (`mem_limit`/`memswap_limit`/`shm_size`, NOT `deploy.resources` which is Swarm-only). Postgres is additionally tuned via `command:` GUC flags per tier. (EXP-274, PR #865)

**Rationale:** No container had a memory ceiling; a runaway query, pgvector index build, or WebSocket heap spike could OOM the kernel, crashing the whole VPS (live enrollments, payments, ZATCA invoices all at risk). Sizing is environment-stratified: production 4 GB, staging 2 GB, dev 1 GB.

**Stakeholders:** Platform, Logix

**Source:** [[Raw/sources/2026-06-06-experts-agent-digest.md]]
