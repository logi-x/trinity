---
title: "WebSockets"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "topic/websockets"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/WebSockets.md"
---

# WebSockets — Realtime Patterns

Realtime infrastructure for the Experts platform: WebSocket gateway, Redis pub/sub, event contract, and presence.

## Architecture

The realtime layer is a **separate optional service** (`apps/experts-realtime`). The main app (`experts-app`) publishes events to Redis; the gateway fans them out to subscribed WebSocket clients.

```
experts-app
  └─ publishEvent(channel, type, data) → Redis pub/sub
                                              └─ apps/experts-realtime (port 3026)
                                                   └─ WebSocket clients (browser / Experts OS)
```

## `apps/experts-realtime`

| Concern      | Detail                                           |
| ------------ | ------------------------------------------------ |
| Stack        | `ws` + `ioredis` + `jose` (JWT verification)     |
| Default port | `3026` — `PORT` or `REALTIME_PORT` env           |
| Redis        | `REDIS_URL` (default `redis://127.0.0.1:6379`)   |
| Dev command  | `pnpm experts:realtime:dev` (from monorepo root) |

## Event Envelope

All transports (Redis, WebSocket, polling fallback) normalize to the same `RealtimeEvent` shape:

```typescript
{
  type: string;      // e.g. "notification_created", "like_added"
  payload: object;   // domain payload — varies by type
  ts: number;        // Unix ms
  channel?: string;  // Redis channel (optional)
}
```

Note: legacy paths may use `data` instead of `payload` — clients should prefer `payload`.

## Redis Channel Map

Clients subscribe only to channels they are authorized to hear (`sanitizeRealtimeChannels` in `src/lib/realtime/channel-auth.ts`):

| Priority | Channel                                       | Purpose                       |
| -------- | --------------------------------------------- | ----------------------------- |
| P0       | `notifications:user:<userId>`                 | In-app notifications          |
| P1       | `post:<uuid>:events`                          | Post + comment thread updates |
| P1       | `likes:post:<uuid>`                           | Post reactions / counts       |
| P1       | `likes:comment:<uuid>`                        | Comment reactions             |
| P2       | `ratings:<type>:<uuid>`                       | Ratings stream                |
| P2       | `feed:posts` / `feed:courses` / `feed:events` | Feed invalidation             |
| P2       | `presence:user:<userId>`                      | Own presence stream           |

Max **64 channels per socket**. Authorization rules are mirrored in `apps/experts-realtime/channel-sanitize.ts`.

## Transport Decision Matrix

| Use case                             | Transport                                                           |
| ------------------------------------ | ------------------------------------------------------------------- |
| Notifications, community posts/likes | WebSocket (if `NEXT_PUBLIC_REALTIME_WS_URL` set) → polling fallback |
| Admin tables, analytics, dashboards  | `useApiQuery` / SWR — no WebSocket                                  |
| Viewer counts, health widgets        | SWR `refreshInterval`                                               |
| Console diagnostics                  | Native SSE (unchanged)                                              |

## WebSocket Client Pattern — One Socket Per Tab Leader

The coordinator uses **one long-lived WebSocket per leader tab**. Channel changes are sent on the existing socket — no reconnect for channel churn:

```json
// Subscribe
{ "op": "subscribe", "channels": ["notifications:user:abc123"] }

// Unsubscribe
{ "op": "unsubscribe", "channels": ["notifications:user:abc123"] }
```

The server responds with `subscription_ack` (channel: "system") confirming sanitize results.

## Authentication Flow

1. Client mints a short-lived JWT via `POST .../token` with `{ "channels": [] }`
2. JWT carries `sub` (userId) for channel authorization only
3. Channels are added post-handshake via `subscribe` messages
4. Env: `NEXT_PUBLIC_REALTIME_WS_URL` + `REALTIME_WS_SECRET` (shared HMAC, min 32 bytes)

**Important:** Connection JWT is only checked at handshake. Expiry does not close an already-open socket.

## Keep-Alive and Presence

- Server sends **WebSocket ping** every 25s (override with `WS_PING_INTERVAL_MS`) — prevents proxy idle timeouts (typical idle cut: 60–120s)
- Missed pong = dead connection → socket closed (`WS_PONG_LIVENESS=true` default)
- **Presence** is separate from ping/pong — clients must send `presence_heartbeat` messages on their own interval
- When a signed-in user's socket count reaches zero, an **offline grace period** (`PRESENCE_OFFLINE_GRACE_MS`, default 4000ms) fires before marking offline — prevents flash-offline on quick leader-tab reconnect

## Redis Publish (from experts-app)

```typescript
// src/lib/redis.ts
publishEvent(channel, eventType, data);
// Publishes: { type, channel, timestamp, ...data }
```

## Open Hardening

- **RESOLVED 2026-06-06 (EXP-262 / PR #879):** there is now a **per-user WebSocket connection cap**. `apps/experts-realtime/src/server.ts` enforces `MAX_WS_PER_USER` (default **10**) in the connect path via the atomic count returned by `incrWsConnectionCount` (race-safe under burst): over the cap → a `connection_rejected` system message, then `closeAll()` rolls the count back via `decrWsConnectionCount` and drops the socket (set `MAX_WS_PER_USER=0` to disable). The signed-in WS JWT TTL was also dropped **24h → 1h** (`token/route.ts`), bounding the window for a leaked token. Complements EXP-274's `mem_limit` (infra blast-radius bound) and EXP-260. **Still deferred:** ioredis subscriber pooling (one ioredis client per socket) and an explicit Redis `maxclients` ceiling for the realtime pool — larger follow-ups, not yet filed.

## Related

- [[Wiki/Concepts/Access Control]]
- [[Wiki/Concepts/Monorepo]]
- [[Projects/Experts/Experts App/docs/reference/realtime-contract]]
- [[Projects/Experts/DEVELOPER_GUIDE]]
