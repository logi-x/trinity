---
title: "EXP-101 — Production PostgreSQL (5432) and Redis (6379) bound to 0.0.0.0 — database ports publicly reachable, bypassing any OS firewall"
date: "2026-05-24"
status: open
resolution: unknown
tags: [bug, security, infrastructure, docker, postgres, redis, network-exposure, project/experts]
linear: "https://linear.app/experts/issue/EXP-101/security-production-postgresql-5432-and-redis-6379-bound-to-0000"
fingerprint: "a37207aca1c4"
---

## Summary

`docker/production/docker-compose.yml` (introduced by PR #436) binds PostgreSQL to `0.0.0.0:5432:5432` and Redis to `0.0.0.0:6379:6379` on the production VPS. Docker's iptables injection inserts `ACCEPT` rules in the `DOCKER` chain that take precedence over UFW and other OS-level firewall rules. Both database ports are publicly reachable from the internet, not just from the application containers.

This means anyone with network access to the VPS IP can attempt to connect directly to PostgreSQL and Redis without any OS-level firewall mitigation.

## Root cause

`docker/production/docker-compose.yml` — `ports: "5432:5432"` for `experts-prd-postgres` and `ports: "6379:6379"` for `experts-prd-redis`. Docker's networking model bypasses UFW/iptables rules not explicitly placed in the `DOCKER-USER` chain when `ports:` is specified. Introduced by PR #436 (Cleanup/docker remote branch, merged 2026-05-24).

Fix: restrict both bindings to loopback-only — `127.0.0.1:5432:5432` and `127.0.0.1:6379:6379`. Application containers should communicate with the database via Docker internal networks, not via host-bound ports.

## Agent fingerprint

`<!-- agent-fp: a37207aca1c4 -->`

## Status

`open` — Backlog (High). Production database ports publicly reachable. Requires immediate ops action: edit `docker/production/docker-compose.yml` and restart affected services. Introduced same day as filing.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
