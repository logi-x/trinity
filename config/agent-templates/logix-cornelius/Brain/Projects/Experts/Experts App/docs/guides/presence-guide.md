---
title: "PRESENCE GUIDE"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/presence-guide"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  First: redefine what “presence” really is

Before choosing a solution, decide which level you actually need.

Presence levels (most apps overestimate)

Hard realtime
“User is online right now, disappears instantly when tab closes”

Soft realtime (most platforms)
“User was active in the last N seconds”

Contextual presence
“User is viewing this page”

Aggregated presence
“12 people are viewing this event”

👉 Experts only needs #2–#4, not #1.

Slack, Notion, GitHub, Google Docs all use soft presence, not connection truth.

Why connection-bound presence is fragile

SSE / WS presence assumes:

Connection == human attention

That’s false because:

Tabs go backgrounded

Mobile OS suspends networking

Proxies kill idle connections

Users open 5 tabs

Laptop sleeps

So SSE presence lies, just in a different way.

The correct model: heartbeat-based presence

Presence becomes:

“User has sent a heartbeat recently”

Not:

“Socket is open”

Core building block: Presence heartbeat
Client → Server (periodic)
POST /api/presence/heartbeat
{
"scope": "event:123",
"state": "viewing"
}

Server stores (Redis ideal)
presence:event:123:user:abc → expires in 30s

If it expires → user is gone.

Why this is better than SSE
Aspect SSE Heartbeat
Multi-tab ❌ breaks ✅ handled
Background tabs ❌ noisy ✅ slowed
Mobile ❌ unreliable ✅ resilient
Load ❌ per-connection ✅ cheap writes
Meaning ❌ connection ✅ activity
How often should heartbeat run?
Golden rule

Heartbeat interval < TTL / 2

Recommended values

Heartbeat: 10–15s

TTL: 30–45s

This gives:

Smooth presence

Low traffic

Fast disappearance

Presence types & exact implementation
1️⃣ “Online / Active” presence (global)

Meaning: user active anywhere

Client

setInterval(() => {
if (document.visibilityState === "visible") {
sendHeartbeat("global");
}
}, 15000);

Server

SET presence:user:abc "1" EX 45

2️⃣ “Viewing this page” (event / course)

Meaning: user is on this specific page

Client

useEffect(() => {
const id = setInterval(() => {
if (document.visibilityState === "visible") {
sendHeartbeat(`event:${eventId}`);
}
}, 10000);

return () => clearInterval(id);
}, [eventId]);

Server

SET presence:event:123:user:abc EX 30

3️⃣ Viewers count (aggregated)

Server

KEYS presence:event:123:user:\*

or better:

SCARD presence:event:123:viewers

(using Redis SET with TTL)

Client

Poll viewers count every 10–15s

Or piggyback on your PollingTransport

Handling multi-tab correctly (important)

Without SSE, every tab would heartbeat — bad.

Solution: BroadcastChannel leader

Exactly like polling.

Only the leader tab sends heartbeats.

if (isLeaderTab) {
startPresenceHeartbeat();
}

Other tabs:

Do nothing

Presence remains accurate

Visibility-aware presence (huge UX win)

Never send presence if tab is hidden:

if (document.visibilityState !== "visible") return;

This avoids:

False viewers

Inflated counts

Battery drain

Presence states (optional but powerful)

Instead of boolean:

state: "viewing" | "typing" | "idle"

TTL varies:

typing → 10s

viewing → 30s

idle → 60s

This is how Slack shows “typing…” without sockets.

What about “typing indicators”?

Same system, shorter TTL:

Heartbeat every 2–3s

TTL 5–6s

Only while input focused

No socket required.

Presence API design (simple)
Write
POST /presence/heartbeat

Read
GET /presence/viewers?scope=event:123

Returns:

{
"count": 12,
"users": [{ id, name, avatar }]
}

How this fits your new polling architecture

You now have:

PollingTransport → events

Presence heartbeat → soft realtime

BroadcastChannel → multi-tab safety

All stateless. All scalable.

TL;DR (pin this)

Presence ≠ connection

Presence = recent activity

SSE presence is fragile

Heartbeats + TTL is correct

Leader tab sends heartbeats

Poll viewers every 10–15s

Visibility-aware = accurate presence

Final recommendation for Experts
Use:

Heartbeat-based presence

Redis TTL

BroadcastChannel leader

Polling for viewer counts

Avoid:

Connection-bound presence

“Socket = online” logic

Per-tab presence updates

This is the exact model used by:

Slack (soft presence)

Notion

Google Docs (except for live cursors)

GitHub
