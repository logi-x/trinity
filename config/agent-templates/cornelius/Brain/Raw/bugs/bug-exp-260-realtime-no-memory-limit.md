---
title: "EXP-260: Realtime container has no memory limit — WebSocket exhaustion causes host OOM"
date: "2026-06-01"
status: open
resolution: unknown
tags: [bug, security, infra, docker, realtime, dos, project/experts]
linear: "https://linux.app/experts/issue/EXP-260/security-realtime-container-has-no-memory-limit-websocket-exhaustion"
fingerprint: "a8c3c745818c"
---

## Summary

The `experts-prd-realtime`, `experts-stg-realtime`, and `experts-dev-realtime` services in all docker-compose files have no `mem_limit` or `cpus` constraint. An unauthenticated actor who can reach `socket.experts.com.sa` (public internet via Traefik) can open many parallel WebSocket connections, exhausting host memory and causing an OOM event that kills all co-located services (app, worker, cron).

## Location

`docker/production/docker-compose.yml` — `experts-prd-realtime` service (no `mem_limit`, no `cpus`).  
Also present in staging and dev compose files.

## Repro Steps

1. Open many parallel WebSocket connections to `wss://socket.experts.com.sa` (no authentication required for the initial upgrade).
2. Host memory exhausts; OOM killer fires; co-located services killed.

## Agent Fingerprint

`a8c3c745818c` (R3)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
