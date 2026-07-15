---
title: "EXP-246: Postgres has no persistent data volume in any env — container recreate wipes the database"
date: "2026-06-01"
status: resolved
resolution: "merged PR #715"
tags: [bug, infra, docker, data-loss, project/experts]
linear: "https://linear.app/experts/issue/EXP-246/infra-postgres-has-no-persistent-data-volume-in-any-env-container"
fingerprint: "7c2e5a91d4f0"
---

## Summary

The Postgres services in production, staging, and dev compose files had no data volume defined (`volumes:` section absent at service and top level). PGDATA lived in the container's ephemeral writable layer. Any container recreate (image change, `docker compose down/up`, version upgrade, config edit) would silently destroy the entire database including all customer data, payments, and ZATCA invoices.

## Location

`docker/production/docker-compose.yml`, `docker/staging/docker-compose.yml`, `docker/dev/docker-compose.yml` — Postgres service definitions (no `volumes:` entry)

## Repro Steps

1. `docker compose pull` + `docker compose up -d` on production (any image change triggers recreate).
2. Postgres initialises fresh empty cluster in new container writable layer.
3. All existing data is gone.

## Agent Fingerprint

`7c2e5a91d4f0` (R3)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
