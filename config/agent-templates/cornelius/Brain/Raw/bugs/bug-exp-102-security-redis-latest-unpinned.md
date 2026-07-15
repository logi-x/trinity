---
title: "EXP-102 — redis:latest unversioned image in Docker Compose"
date: "2026-05-24"
status: resolved
resolution: "PR #458: pin redis image to redis:7.2-alpine in all Compose files. Eliminates silent breakage from upstream image changes."
tags: [bug, infrastructure, docker, dependencies, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-102"
fingerprint: "agent-fp:R2-redis-latest-pin-001"
---

## Summary

All Docker Compose files used `image: redis:latest`, an unversioned tag that silently resolves to whatever Redis major version Docker Hub publishes at pull time. A major Redis version bump (e.g., 7 → 8) could introduce breaking changes or altered default configs on the next `docker compose pull`.

## Root cause

Convenience tag `latest` was used at initial scaffolding and never pinned to a specific version.

## Agent fingerprint

`<!-- agent-fp:R2-redis-latest-pin-001 -->`

## Status

Resolved — PR #458 merged 2026-05-24.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
