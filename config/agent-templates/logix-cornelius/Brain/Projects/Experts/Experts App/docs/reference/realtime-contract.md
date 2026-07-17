---
title: "Realtime event contract (WebSocket + polling)"
date: "2026-04-11"
tags: ["project/experts", "docs/v4", "topic/realtime", "topic/api"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Realtime event contract (WebSocket + polling)

This document defines the wire format shared by:

- Redis pub/sub (`publishEvent` in `src/lib/redis.ts`)
- `GET /api/v1/internal/realtime/sync` (polling fallback)
- WebSocket payloads from `experts-realtime`

## Event envelope (`RealtimeEvent`)

All transports normalize to this shape (camelCase):

| Field     | Type              | Description                                           |
| --------- | ----------------- | ----------------------------------------------------- |
| `type`    | string            | Event name, e.g. `notification_created`, `like_added` |
| `payload` | object            | Domain payload (varies by `type`)                     |
| `ts`      | number            | Unix ms                                               |
| `channel` | string (optional) | Redis channel the event was published on              |

Legacy: some paths still attach `data`; clients should prefer `payload`.

## Redis publish format

`publishEvent(channel, eventType, data)` publishes JSON:

```json
{
  "type": "<eventType>",
  "channel": "<channel>",
  "timestamp": 1234567890123,
  "...": "spread from data when object"
}
```

The WebSocket server maps `timestamp` → `ts` and builds `payload` from the rest (excluding `type`, `channel`, `timestamp`).

## Priority channels (low-latency / WS-first)

Subscribe only to channels the user is allowed to hear (see `sanitizeRealtimeChannels` in `src/lib/realtime/channel-auth.ts`).

| Priority | Channel pattern                               | Purpose                       |
| -------- | --------------------------------------------- | ----------------------------- |
| P0       | `notifications:user:<userId>`                 | In-app notifications          |
| P1       | `post:<uuid>:events`                          | Post + comment thread updates |
| P1       | `likes:post:<uuid>`                           | Post reactions / counts       |
| P1       | `likes:comment:<uuid>`                        | Comment reactions             |
| P2       | `ratings:<type>:<uuid>`                       | Ratings stream                |
| P2       | `feed:posts` / `feed:courses` / `feed:events` | Feed invalidation             |
| P2       | `presence:user:<userId>`                      | Own presence stream (if used) |

## Transports

| Use case                                    | Transport                                                         |
| ------------------------------------------- | ----------------------------------------------------------------- |
| Notifications, community post/comment/likes | WebSocket when `NEXT_PUBLIC_REALTIME_WS_URL` is set; else polling |
| Admin tables, analytics, dashboards         | `useApiQuery` / SWR (no WS)                                       |
| Viewer counts, health widgets               | SWR `refreshInterval`                                             |
| Console diagnostics                         | Native SSE (unchanged)                                            |

## Configuration

| Variable                      | Where                      | Purpose                                                                         |
| ----------------------------- | -------------------------- | ------------------------------------------------------------------------------- |
| `NEXT_PUBLIC_REALTIME_WS_URL` | Next.js (public)           | WebSocket base URL, e.g. `ws://localhost:3026` or `wss://realtime.example.com`  |
| `REALTIME_WS_SECRET`          | Next.js + experts-realtime | Shared HMAC secret for short-lived connection tokens (min 32 bytes recommended) |

## WebSocket: dynamic channel subscription (one long-lived socket)

The global coordinator uses **one** WebSocket per leader tab. When the merged hook channel set changes, the client sends **`subscribe`** / **`unsubscribe`** JSON on the existing socket — **no** reconnect for channel churn.

| Client message | Shape                                           | Server behavior                                                                                                                                                                                          |
| -------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `subscribe`    | `{ "op": "subscribe", "channels": string[] }`   | Each name is authorized with the same rules as `sanitizeRealtimeChannels` (mirrored in `experts-realtime` `channel-sanitize.ts`). Max **64** channels per message; max **64** Redis channels per socket. |
| `unsubscribe`  | `{ "op": "unsubscribe", "channels": string[] }` | Drops Redis subscriptions that are active on this socket.                                                                                                                                                |

**Authenticated** clients should mint a session JWT with `POST …/token` and body `{ "channels": [] }` (empty). The JWT carries `sub` only for channel authorization; Redis topics are added only via `subscribe` messages. **Anonymous** clients still send explicit `channels` in the token request; the server seeds initial Redis subscriptions from the JWT so behavior stays correct for guests.

**Rollout:** Deploy `experts-realtime` that accepts empty channel lists for signed-in users **before or with** the Next.js app that requests those tokens. An older gateway rejects empty JWT channel lists at handshake (403).

## Keep-alive, pong liveness, and proxies

`experts-realtime` sends **WebSocket ping** frames on a timer (default every **25s**, override with `WS_PING_INTERVAL_MS`). Browsers answer with **pong** automatically, which prevents many L7 proxies and load balancers from treating the connection as idle (common idle cuts are ~60–120s).

By default (`WS_PONG_LIVENESS=true`), the service also treats a **missed pong** (no reply before the next ping tick) as a dead half-open connection and **closes** the socket. That is separate from application **presence**: `ws.ping()` / pong does **not** refresh `presence:*` TTL. Signed-in clients should keep sending `presence_heartbeat` (or viewer ops that refresh presence) on the same WebSocket on whatever interval matches your product policy.

If sockets still drop at a fixed interval, raise idle/read timeouts on the path (Traefik entrypoint `transport.respondingTimeouts`, AWS ALB idle timeout, Cloudflare, etc.). The connection JWT is only checked at **handshake**; expiry does not close an already-open socket by itself.

## Subscription acknowledgements

After each `subscribe` / `unsubscribe` message, the server may send **`subscription_ack`** (`channel: "system"`) so clients and operators can see sanitize results, cap drops, and Redis failures. Shape is documented in `apps/experts-realtime/README.md`.

## Presence when the socket closes

For **signed-in** users, the gateway tracks an **open WebSocket count** in Redis per `userId`. When the count reaches **zero**, it waits **`PRESENCE_OFFLINE_GRACE_MS`** (default **4000**) and calls **offline** only if the count is still zero—so a quick leader-tab reconnect does not flash offline. **Anonymous** connections do not participate in this path; presence TTL behavior is unchanged for guests.

Mid-connection **permission or session revocation** is still not re-checked on the open socket; shorten JWT TTL or recycle connections if you need tighter revocation.
