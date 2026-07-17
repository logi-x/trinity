---
title: "EXP-262 — add per-user WebSocket connection cap (≤5 concurrent) in `apps/experts-realtime/src/server.ts` upgrade handler"
date: "2026-06-01"
owner: "Logix (Ahmed)"
due: "2026-06-08"
priority: "medium"
status: "open"
source: "[[Raw/sources/2026-06-01-experts-agent-digest.md]]"
tags: [action, project/experts]
category: "meta"
up: "[[Action-Tracker]]"
updated: "2026-07-15"
---

> ↑ [[Action-Tracker]]

EXP-262 — add per-user WebSocket connection cap (≤5 concurrent) in `apps/experts-realtime/src/server.ts` upgrade handler using `incrWsConnectionCount` result; no cap + 24h WS JWT TTL enables Redis connection pool exhaustion

**Source:** [[Raw/sources/2026-06-01-experts-agent-digest.md]]
