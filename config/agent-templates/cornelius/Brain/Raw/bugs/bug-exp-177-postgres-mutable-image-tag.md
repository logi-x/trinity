---
title: "EXP-177 — pgvector:pg16 mutable undigested image tag in production postgres service"
date: "2026-05-28"
status: open
resolution: unknown
tags: [bug, infrastructure, docker, security, supply-chain, project/experts]
linear: "https://linear.app/experts/issue/EXP-177"
fingerprint: "7274890de478"
---

## Summary
The `experts-prd-postgres` service in `docker/production/docker-compose.yml` uses `pgvector/pgvector:pg16` — a mutable, undigested image tag. Docker will pull whatever image the registry serves for that tag on the next `docker compose pull`, with no cryptographic guarantee of content integrity. A compromised or accidentally updated image would deploy silently.

## Root cause
Mutable tags (`pg16`) do not pin to a specific image digest. The fix is to append the image SHA256 digest: `pgvector/pgvector:pg16@sha256:<current-digest>`. The digest can be obtained via `docker manifest inspect pgvector/pgvector:pg16`. Apply the same fix to the staging compose file if present.

## Agent fingerprint
`<!-- agent-fp: 7274890de478 -->`

## Status
`open` — Backlog (Medium). Supply-chain risk on next container pull; no active exploitation path.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
