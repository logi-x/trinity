---
title: "EXP-274 — No container memory limits on postgres and realtime — host OOM kills DB and crashes all co-located services"
date: "2026-06-02"
status: open
resolution: unknown
tags: [bug, security, infrastructure, docker, postgres, realtime, resource-limits, project/experts]
linear: "https://linear.app/experts/issue/EXP-274/infra-add-container-memory-limits-postgres-memory-tuning-postgres-and"
fingerprint: "c3483b4cd2e6"
---

## Summary

`docker/{production,staging,data}/docker-compose.yml` has no `mem_limit`, `memswap_limit`, or `shm_size` on any container. On a VPS running multiple co-located services this is a host-OOM hazard from two independent vectors: (1) a bad Postgres query, migration, or connection spike growing RSS until the OOM-killer terminates the DB container (full outage), and (2) WebSocket flood or heap leak in the realtime service exhausting host RAM, cascading to the DB and app. Subsumes EXP-260 (realtime-only scope).

## Root cause

`docker/production/docker-compose.yml` — `experts-prd-postgres` and `experts-prd-realtime` services (and their staging/data equivalents). No `mem_limit` / `memswap_limit` / `shm_size` (Compose v2 syntax, NOT swarm `deploy.resources`). PG also needs `command:` tuning flags (`shared_buffers`, `work_mem`, `effective_cache_size`) calibrated to the available VPS RAM.

Fix requires operator coordination on VPS RAM allocation before setting specific limits.

## Agent fingerprint

`<!-- agent-fp: c3483b4cd2e6 -->`

## Status

`open` — Backlog (High). Operator-gated: requires VPS RAM audit before setting specific mem_limit values. Subsumes EXP-260.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
