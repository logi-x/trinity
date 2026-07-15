---
title: "Persistent Postgres data volumes are required in all environments; the canonical volume mount path is `/var/lib/postgres"
date: "2026-06-01"
decision: "Persistent Postgres data volumes are required in all environments; the canonical volume mount path is `/var/lib/postgresql`. Ephemeral PGDATA (container writable layer) is prohibited; any container re"
stakeholders: "Infra, DBA"
review_by: "2026-06-08"
source: "[[Raw/sources/2026-06-01-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Persistent Postgres data volumes are required in all environments; the canonical volume mount path is `/var/lib/postgresql`. Ephemeral PGDATA (container writable layer) is prohibited; any container recreate must not destroy data.

**Rationale:** Production Postgres had no data volume since the initial deployment — a single `docker compose up` after an image change would have caused total data loss (customers, payments, ZATCA invoices).

**Stakeholders:** Infra, DBA

**Source:** [[Raw/sources/2026-06-01-experts-agent-digest.md]]
