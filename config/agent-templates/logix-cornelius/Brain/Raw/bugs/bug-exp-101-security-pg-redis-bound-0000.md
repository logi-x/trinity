---
title: "EXP-101 — Production PostgreSQL (5432) + Redis (6379) listening on 0.0.0.0"
date: "2026-05-24"
status: resolved
resolution: "PR #457: add '127.0.0.1:5432:5432' and '127.0.0.1:6379:6379' port bindings in all Docker Compose files. Loopback-only binding eliminates external DB/cache exposure."
tags: [bug, security, infrastructure, docker, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-101"
fingerprint: "agent-fp:R2-pg-redis-0000-bind-001"
---

## Summary

All Docker Compose files (production, staging, e2e) published PostgreSQL port 5432 and Redis port 6379 on `0.0.0.0` (all interfaces). On a VPS without a strict external firewall, this exposes the database and cache to the public internet.

## Root cause

Docker Compose `ports: ['5432:5432']` short syntax binds to `0.0.0.0` by default. The correct form for loopback-only is `'127.0.0.1:5432:5432'`.

## Agent fingerprint

`<!-- agent-fp:R2-pg-redis-0000-bind-001 -->`

## Status

Resolved — PR #457 merged 2026-05-24.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
