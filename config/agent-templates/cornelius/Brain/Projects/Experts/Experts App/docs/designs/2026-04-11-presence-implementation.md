---
title: "PRESENCE IMPLEMENTATION"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/presence-implementation"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  🧠 First: what “user presence” actually is

Before tools, define the problem.

Presence ≠ real-time feed

Presence answers questions like:

Who is online?

Who is viewing this post?

Is user X active or idle?

Has user X disconnected?

Presence is:

ephemeral

high-churn

stateful

frequently changing

not business-critical

That combination is dangerous for SSE if misused.

❌ Why your SSE presence implementation caused stalls

You likely did one (or more) of these:

🚨 Common mistakes (very common)

One SSE connection per presence scope

per room

per post

per component

Broadcasting presence updates too frequently

mouse move

scroll

focus

heartbeat every few seconds

Presence stream mixed with critical streams

feed

notifications

likes

Presence blocking page hydration

client waits on SSE before rendering

No idle timeout

zombie connections

stalled sockets

Any of these will:

eat connection slots

block HTTP

stall rendering

feel “randomly slow”

🚦 VERY IMPORTANT: When you should NOT use SSE
❌ Do NOT use SSE for:

Presence heartbeats

Cursor movement

Typing indicators

Rapid state changes

Per-user ephemeral state

High-frequency signals

Presence updates are too chatty.

SSE is optimized for:

server → client push at low to moderate frequency

Presence is:

client → server heartbeat + fan-out

That’s the mismatch.

✅ When SSE IS the right tool

Use SSE for:

Likes count updates

New posts/comments

Notifications

System status

Progress updates

Metrics

Feed updates

All of these are:

event-based

meaningful

low frequency

server-originated

🧩 The CORRECT way to build presence (battle-tested)
🏗️ Correct architecture (this matters)
Client
└── lightweight heartbeat (HTTP)
Backend
├── Redis (presence state)
└── optional SSE summary updates

Presence should be pull + heartbeat, not pure push.

✅ Step 1 — Presence state lives in Redis (not DB)

Redis key design:

presence:user:{userId} = {
lastSeen: timestamp,
page: "/community/123",
tabId: "abc"
}
TTL = 30–60 seconds

Client sends heartbeat:

POST /api/presence/heartbeat
{
page: "/community/123",
tabId: "abc"
}

Frequency:

every 20–30 seconds

on visibility change

on route change

✅ Step 2 — Presence is derived, not streamed

You do NOT stream every join/leave.

Instead:

Store presence

Query when needed

Optionally push summary snapshots

Example:

{
"onlineCount": 7,
"users": ["u1", "u2", "u3"]
}

✅ Step 3 — OPTIONAL SSE for presence (only summaries)

If you want “live” presence:

✔ Use ONE shared SSE stream
✔ Push coalesced updates
✔ Max once every 5–10 seconds

Example SSE event:

{
"type": "presence_snapshot",
"scope": "post:123",
"onlineCount": 7
}

NOT:

"user A joined"
"user B left"
"user A moved mouse"

🚨 Absolute rule for presence

Presence must degrade gracefully

If presence breaks:

the app must still load

feed must still work

likes must still update

Presence should never block rendering.

🧪 Client-side rules (important)
✔ Presence heartbeat must:

run in useEffect

be fire-and-forget

not block UI

be cancellable

stop on tab hidden

❌ Must NOT:

await responses

open SSE

re-render page

create dependencies

🧠 The golden decision table
Use case SSE? Why
Likes count ✅ Event-based
New comment ✅ Event-based
Notifications ✅ Event-based
Feed updates ✅ Event-based
Presence ❌ (mostly) High churn
Typing indicator ❌ Too chatty
Cursor position ❌ Insane
System status ✅ Slow changes
🏁 Final verdict (important)
You did the RIGHT thing by stopping.

Presence + SSE is a trap if done naïvely.

Correct approach:

Redis TTL-based presence

HTTP heartbeat from client

Optional SSE summaries only

Never stream individual presence events

Never block UI on presence

TL;DR (memorize this)

Presence ≠ feed

SSE ≠ heartbeat

Presence is ephemeral

SSE is event-based

Presence should be pull + TTL

SSE only for coalesced summaries
