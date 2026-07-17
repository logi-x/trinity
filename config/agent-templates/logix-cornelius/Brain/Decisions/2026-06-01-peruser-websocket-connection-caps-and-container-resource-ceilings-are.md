---
title: "Per-user WebSocket connection caps and container resource ceilings are required on the realtime service; the `upgrade` h"
date: "2026-06-01"
decision: "Per-user WebSocket connection caps and container resource ceilings are required on the realtime service; the `upgrade` handler must enforce the cap by rejecting new connections once the per-user limit"
stakeholders: "Security / Infra"
review_by: "2026-09-01"
source: "[[Raw/sources/2026-06-01-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Per-user WebSocket connection caps and container resource ceilings are required on the realtime service; the `upgrade` handler must enforce the cap by rejecting new connections once the per-user limit is reached, not merely counting them. The realtime container must specify `mem_limit` + `cpus` in all compose environments.

**Rationale:** EXP-260/EXP-262. `incrWsConnectionCount` in `presence-redis.ts` increments a Redis counter but the upgrade handler never checks the result against a ceiling. An authenticated user holding 24h WS JWTs can open unlimited parallel connections, exhausting Redis connection pool slots for all users. Unauthenticated actors can OOM the host without a memory ceiling.

**Stakeholders:** Security / Infra

**Source:** [[Raw/sources/2026-06-01-experts-agent-digest.md]]
