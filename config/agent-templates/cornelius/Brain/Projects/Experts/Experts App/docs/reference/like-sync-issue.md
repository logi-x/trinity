---
title: "LIKE SYNC ISSUE"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/like-sync-issue"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  Q: Ok, sort of fixed most of the issues, except for when a comment is liked by a user, it never gets updated in other user browser unless, revalidateOnFocus, revalidateOnReconnect or page refresh, shouldn't that be handled by polling ?

A: Yes — it should be handled by polling, and the fact that it only updates on revalidateOnFocus is the key clue.

This means your polling loop is not actually responsible for likes, even if you think it is.

Let’s diagnose this precisely and fix it cleanly.

What’s actually happening (root cause)

Right now you have two separate data worlds:

State world (SWR / page data)

Comments + likes are fetched via SWR

Revalidated on focus / reconnect

Event world (polling / realtime sync)

Handles things like:

new comments

presence

notifications

❌ Likes are not emitted as events

So when User A likes a comment:

Server updates DB ✔

User A sees optimistic update ✔

Other users:

❌ receive no event

❌ no SWR mutation

❌ no revalidation

✔ update only when focus refresh happens

This is expected behavior given your architecture.

Important mental model (this is the key)

Polling does nothing unless you tell it what to poll for

Polling ≠ magic refresh
Polling only works if likes are part of the sync stream or explicitly trigger SWR updates.

Right now:

Comments are events

Presence is state

Likes are silent DB writes

You have 3 correct ways to fix this

(choose one, don’t mix randomly)

OPTION 1 — Likes as realtime EVENTS (recommended)

Treat likes exactly like comments:

1️⃣ Emit a comment.liked event on the server

When a like happens:

emitEvent({
type: "comment.liked",
payload: {
commentId,
delta: +1, // or -1
userId,
},
});

Store it in your existing activity / events table.

2️⃣ PollingTransport receives it
poller.onEvent((event) => {
switch (event.type) {
case "comment.liked":
applyLikeDelta(event.payload);
break;
}
});

3️⃣ Update UI immediately (without SWR refetch)
function applyLikeDelta({ commentId, delta }) {
setComments((prev) =>
prev.map((c) =>
c.id === commentId
? { ...c, likesCount: c.likesCount + delta }
: c
)
);
}

✅ Other users see updates within polling interval
✅ No focus refresh needed
✅ No refetch storm

This is how Reddit, Slack, Discord do it.

OPTION 2 — Explicit SWR mutation trigger (simpler)

If you don’t want likes as events:

1️⃣ After liking, trigger SWR revalidation manually

On success:

mutate(`/api/comments?postId=${postId}`);

2️⃣ Other users rely on polling to invalidate

You add a lightweight poll endpoint:

GET /api/comments/version?postId=123

Returns:

{ "version": 42 }

If version changes → call mutate().

This works, but:

More fetches

Heavier than events

Less “realtime feeling”

OPTION 3 — Periodic likes-only poll (not ideal)

Every N seconds:

GET /api/comments/likes?postId=123

Then diff and update.

This scales poorly and feels clunky.
I don’t recommend it unless you’re under time pressure.

Why OPTION 1 is the correct architectural fix

Because likes are:

Small

Frequent

Incremental

Ordered

Not worth refetching entire comments list

That’s exactly what event streams are for.

Why revalidateOnFocus “fixes” it

Because it forces:

GET /api/comments?postId=123

Which re-reads the DB and hides the architectural gap.

But:

Focus-based correctness is accidental correctness

You already sensed this — your instinct is right.

How often should likes update via polling?

Same as comments:

Poll interval: 5–10s

Jitter: ±15%

If page hidden: 30–60s

Likes don’t need millisecond accuracy — they just need to eventually converge.

One more subtle but important rule
Do NOT broadcast “full counts”

Always broadcast deltas:

{ "delta": +1 }

Not:

{ "likesCount": 37 }

Why?

Avoid race conditions

Multiple likes can coalesce

Order-independent

TL;DR (pin this)

Polling didn’t “miss” the like

Likes were never part of the poll stream

revalidateOnFocus hides the issue

Fix by:

emitting comment.liked events OR

explicitly invalidating SWR

Best fix = likes as events

Events update UI, not refetch state
