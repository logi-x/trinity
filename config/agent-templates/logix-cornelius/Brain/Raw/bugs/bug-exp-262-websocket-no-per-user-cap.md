---
title: "EXP-262: No per-user WebSocket connection cap — authenticated Redis exhaustion DoS"
date: "2026-06-01"
status: open
resolution: unknown
tags: [bug, security, realtime, websocket, dos, project/experts]
linear: "https://linear.app/experts/issue/EXP-262/security-no-per-user-websocket-connection-cap-authenticated-redis"
fingerprint: "b5781cc27ee7"
---

## Summary

The WebSocket upgrade handler in `apps/experts-realtime/src/server.ts` accepts all authenticated connections with no per-user concurrency limit. `incrWsConnectionCount` in `presence-redis.ts` increments a Redis counter but the result is never checked against a ceiling before accepting the connection. The WS JWT has a 24h TTL. An authenticated user can open unlimited parallel connections, exhausting the Redis connection pool (finite `maxConnections`) for all users.

## Location

- `apps/experts-realtime/src/server.ts` — upgrade handler (no per-user connection count check)
- `apps/experts-realtime/src/presence-redis.ts` — `incrWsConnectionCount` (tracks but does not enforce)
- `apps/experts-app/app/api/v1/internal/realtime/token/route.ts` — WS JWT TTL `ttlSeconds: 86400` (24h)

## Repro Steps

1. Obtain a valid WS JWT.
2. Open 1000+ parallel WebSocket connections using the same JWT.
3. Redis connection pool exhausts; new connections from other users fail.

## Agent Fingerprint

`b5781cc27ee7` (R3)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
