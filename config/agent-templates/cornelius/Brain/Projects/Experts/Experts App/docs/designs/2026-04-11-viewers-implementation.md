---
title: "VIEWERS IMPLEMENTATION"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/viewers-implementation"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  🧠 First: clarify the requirement

You want to show something like:

👀 7 people are viewing this course
Avatars: A, B, C…

Important characteristics:

Read-only for users

Low importance (nice-to-have)

Approximate is OK

Doesn’t need millisecond accuracy

Must not block page load

This immediately rules out:

per-user SSE

per-tab streams

high-frequency updates

✅ Correct mental model

This is a “derived snapshot”, not real-time presence

So we’ll use:

Redis TTL keys

lightweight heartbeats

optional SSE summary

graceful degradation

🏗️ Architecture (simple & scalable)
Client (heartbeat)
↓
API (stateless)
↓
Redis (TTL presence)
↓
Snapshot query
↓
UI

🧩 Step 1 — Redis data model (important)

We track viewers per resource, not global presence.

Redis keys
viewers:post:{postId} → SET of userIds
viewers:course:{courseId}
viewers:event:{eventId}

Each entry has TTL.

Implementation pattern:

SADD viewers:post:123 user_456
EXPIRE viewers:post:123 30

TTL:

20–40 seconds is perfect

auto-cleanup

no disconnect handling needed

🔁 Step 2 — Client heartbeat (VERY lightweight)

Runs:

on page mount

every ~25 seconds

on visibility change

on route change

Client hook
useEffect(() => {
const sendHeartbeat = () => {
fetch("/api/viewers/heartbeat", {
method: "POST",
body: JSON.stringify({
type: "post",
id: postId,
}),
keepalive: true,
});
};

sendHeartbeat();
const interval = setInterval(sendHeartbeat, 25000);

return () => clearInterval(interval);
}, [postId]);

⚠️ Important:

fire-and-forget

do NOT await

do NOT block rendering

🧠 Step 3 — API handler
// POST /api/viewers/heartbeat
export async function POST(req: Request) {
const { type, id } = await req.json();
const userId = await getUserIdFromSession();

if (!userId) return new Response("ok");

const key = `viewers:${type}:${id}`;

await redis.multi()
.sadd(key, userId)
.expire(key, 30)
.exec();

return new Response("ok");
}

This endpoint:

is cheap

idempotent

stateless

scales horizontally

📊 Step 4 — Fetch snapshot (NOT streamed)

On page load (or polling every 10–15s):

GET /api/viewers?type=post&id=123

Response:

{
"count": 7,
"users": [
{ "id": "u1", "avatar": "..." },
{ "id": "u2", "avatar": "..." }
]
}

Use this to render:

👀 7 people viewing

🚀 Optional: SSE summary (ONLY if you want “live” feel)

⚠️ This is optional.

If you already have a shared SSE stream:

{
"type": "viewers_update",
"resource": "post:123",
"count": 7
}

Rules:

max once every 5–10 seconds

coalesced

count only

no per-user events

❌ What NOT to do (very important)

Never:

stream join/leave events

open SSE per post

open SSE per viewer

broadcast avatars in real time

rely on disconnect events

🧠 Why this works so well

✔ Redis TTL handles disconnects
✔ No blocking connections
✔ No stale state
✔ No over-pushing
✔ Accurate enough
✔ Scales beautifully

This is exactly how:

Medium

Notion

GitHub

Coursera

implement “currently viewing”.

🏁 Final recommendation
Use:

HTTP heartbeat

Redis TTL

snapshot fetch

optional SSE summary

Do NOT:

use SSE for raw presence

open multiple streams

block page rendering

TL;DR

“Who’s viewing” ≠ presence

It’s a TTL-based snapshot

Heartbeat → Redis

Fetch count → UI

SSE only for summaries (optional)
