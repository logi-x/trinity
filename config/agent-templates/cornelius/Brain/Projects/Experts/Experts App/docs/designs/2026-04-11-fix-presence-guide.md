---
title: "FIX PRESENCE GUIDE"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/fix-presence-guide"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  PART 1

Q: There're so many issues, I wish if I could say that presence is accurate, but it's far from it... Some of the issues: 1- User first visits a post 12 seeconds then shows 1 person is viewing, then another 12 seconds still shows 1 person is viewing -> on the next /api/viewers trigger the user disappears and never appears again unless page refreshed, and same cycle over and over again 2- 2 useres same/different posts, sometimes it shows the user preesent in the wrong post eveen after leaving the post and is present in a different post 3- most of the time changes are reflected only because of revalidateOnFocus: true -> leaving the page then revisiting it...

A: You’re not imagining it — what you’re describing are classic failure modes of naïve heartbeat-based presence.
The important part: all three symptoms come from the same two root causes, not three separate bugs.

Let’s go step by step, tie each symptom to the cause, then I’ll give you a presence model that actually converges, even with polling, multi-tab, and focus changes.

The two real root causes (everything flows from these)
Root cause A — heartbeat is not deterministic

Right now, presence depends on:

timers (setInterval)

focus / visibility events

polling timing

race conditions between tabs

That means:

sometimes the heartbeat arrives late, sometimes early, sometimes not at all

Presence systems must not depend on “best effort” timing.

Root cause B — presence keys are not owned

You’re likely doing something like:

presence:post:123:user:abc (TTL 30s)

but:

user opens post A

user navigates to post B

heartbeat for A and B race

TTLs expire independently

server has no idea which scope is current

Result:

ghost presence, wrong post, disappearing users

Everything you listed is explained by these two.

Let’s map them directly.

Why each of your issues happens
Issue 1

User appears → disappears → never appears again unless refresh

What’s happening

First heartbeat arrives → presence key created

Next heartbeat is skipped because:

tab hidden for a moment

browser throttled timers

leader tab changed

TTL expires

No further heartbeat → user disappears forever

Because:

presence depends on a timer that is not guaranteed to run

This is expected browser behavior, not your bug.

Issue 2

User appears in the wrong post even after leaving

What’s happening

User leaves post A

You rely on TTL to expire A

User enters post B

Heartbeat for B arrives before A expires

Now user exists in both scopes

Or worse: only A survives due to timing

Because:

presence scopes are independent and never revoked

TTL alone is not enough.

Issue 3

Presence updates only when revalidateOnFocus triggers

What’s happening

Focus event causes SWR refetch

Refetch hides presence bugs

Polling / heartbeat alone isn’t keeping things consistent

This is your system accidentally correcting itself via focus events.

The missing concept: presence must be stateful, not inferred

Right now you’re doing:

“If I recently heard from user → assume presence”

That is inference-based presence — it never converges.

What you need is:

“User explicitly declares what they are viewing now”

That’s state-based presence.

The correct presence model (this fixes all 3 issues)
1️⃣ Presence is a SINGLE authoritative state per user

Instead of many keys per scope:

❌ BAD

presence:post:123:user:abc
presence:post:456:user:abc

✅ GOOD

presence:user:abc → { scope: "post:123", ts }

Only one scope is allowed at a time.

2️⃣ Presence updates are idempotent and explicit

Client does not say:

“I’m still here”

Client says:

“I am now viewing X”

Client → server
POST /presence/enter
{
"scope": "post:123"
}

Server:

SET presence:user:abc "post:123" EX 45

If user navigates:

POST /presence/enter
{
"scope": "post:456"
}

Server:

SET presence:user:abc "post:456" EX 45

👉 Old scope is automatically overwritten
👉 No ghosts
👉 No races
👉 No ambiguity

3️⃣ Heartbeat becomes a refresh, not a declaration

Heartbeat is only:

“I’m still in the same place”

POST /presence/refresh

Server:

EXPIRE presence:user:abc 45

If refresh stops → user disappears
If refresh continues → presence is stable

No scope change during refresh.

4️⃣ Viewers list is derived, not stored

To get viewers of post:123:

SCAN presence:user:\*
FILTER value == "post:123"

Or better:

Maintain a reverse index (explained below)

Fixing multi-tab correctly (critical)

Tabs must not compete.

Rule

Only ONE tab per user may send presence

You already have leader election — now presence must obey it.

if (isLeaderTab) {
enterScope(postId)
startRefreshLoop()
}

Other tabs:

do nothing

do not heartbeat

do not enter scopes

Correct client lifecycle (this matters)
useEffect(() => {
if (!isLeaderTab) return

enterScope(`post:${postId}`)

const id = setInterval(() => {
if (document.visibilityState === "visible") {
refreshPresence()
}
}, 15000)

return () => {
clearInterval(id)
// OPTIONAL: explicit leave
leavePresence()
}
}, [postId, isLeaderTab])

Key detail

Presence is set once on enter

Refreshed periodically

Scope only changes on navigation

Server-side reverse index (recommended)

Instead of scanning:

On enter
SET presence:user:abc "post:123" EX 45
SADD presence:scope:post:123 abc
EXPIRE presence:scope:post:123 45

On scope change
// remove from old scope
SREM presence:scope:post:123 abc

// add to new scope
SADD presence:scope:post:456 abc

On refresh
EXPIRE presence:user:abc 45
EXPIRE presence:scope:post:456 45

Viewers query
SCARD presence:scope:post:456
SMEMBERS presence:scope:post:456

This gives:

O(1) viewers count

No scanning

No ghosts

No cross-post leakage

Why this fixes ALL your issues
Issue Fixed because
User disappears randomly refresh no longer changes scope
Wrong post presence scope is singular
Requires focus revalidation state converges without focus
Multi-tab chaos only leader updates
Ghost users explicit overwrite
Presence accuracy rule (important mindset shift)

Presence is “recent intent”, not truth

Even Slack / Google Docs allow:

10–30s delay

soft disappearance

approximation

What matters is:

stability

correct scope

predictable behavior

Not millisecond accuracy.

TL;DR (pin this)

TTL-only presence will always glitch

Presence must be single-scope per user

Enter is explicit

Refresh only extends TTL

Scope changes overwrite

Leader tab only

Reverse index for viewers

PART 2

Q: There's an issue with "leader" approach, a user can't exist in two posts simultaneously...

A: You’re absolutely right — and this is an important catch 👍
What you just uncovered is a conceptual mismatch between leader election and presence semantics.

Let’s fix it properly.

The core contradiction (why you’re stuck)

Earlier we combined two ideas:

Leader tab → only one tab talks to the server

Presence = “what user is viewing”

Those two conflict when:

A single user legitimately views multiple scopes at the same time
(e.g. two posts in two tabs)

So this statement becomes false:

“A user can only exist in one presence scope”

That assumption does not hold for your product.

Good news: the solution is not to abandon leader election — it’s to change what the leader owns.

The correct mental model (this resolves everything)
❌ Wrong model

Leader tab represents the user

✅ Correct model

Leader tab represents the browser, and tracks multiple scopes

Presence is multi-scope, but single transport.

The winning model: Multi-scope presence with single leader
Key ideas

A user can be present in N scopes

Each tab declares its own scope

Leader tab aggregates scopes and syncs them

Server presence is (user, scope), not just user

This is how Slack, Notion, Google Docs handle it.

Revised presence architecture (stable & accurate)
1️⃣ Presence is (userId, scopeId)

Presence key:

presence:scope:{scopeId}:user:{userId}

Examples:

presence:post:123:user:abc
presence:post:456:user:abc

✔ User can exist in multiple scopes
✔ Presence is scoped
✔ No overwriting

2️⃣ Tabs declare local intent, not server presence

Each tab knows:

const localScope = `post:${postId}`

On mount:

bc.postMessage({ type: "enter", scope: localScope })

On unmount:

bc.postMessage({ type: "leave", scope: localScope })

Tabs never talk to server directly.

3️⃣ Leader tab aggregates scopes

Leader keeps a set:

const activeScopes = new Set<string>();

On BroadcastChannel messages:
if (msg.type === "enter") {
activeScopes.add(msg.scope);
}
if (msg.type === "leave") {
activeScopes.delete(msg.scope);
}

This set represents:

“All scopes this browser is currently viewing”

4️⃣ Leader syncs all active scopes to server
Periodic heartbeat (every 10–15s):
POST /presence/sync
{
scopes: ["post:123", "post:456"]
}

Server behavior

For each scope:

SET presence:scope:post:123:user:abc EX 45
SET presence:scope:post:456:user:abc EX 45

Also:

Remove user from scopes not included in payload

This makes presence idempotent and convergent.

5️⃣ Leaving a tab is deterministic (no TTL guessing)

When a tab closes or navigates away:

bc.postMessage({ type: "leave", scope })

Leader removes scope immediately and syncs on next heartbeat.

No more:

ghost presence

waiting for TTL

wrong post showing user

TTL becomes fail-safe, not correctness logic.

Why this fixes all previous issues

Let’s map directly.

Your issue #1

User appears → disappears → appears again only on refresh

Fixed because

Presence is refreshed as long as any tab still declares the scope

TTL expiry only happens if all tabs stop declaring

Your issue #2

User appears in wrong post after navigating

Fixed because

Leaving a tab explicitly removes scope

Leader sends authoritative scope list

Server removes stale scopes immediately

Your issue #3

Presence only updates on focus

Fixed because

Presence is state-driven, not event-driven

Focus just affects heartbeat frequency, not correctness

Important rule (this is the real takeaway)

Leader election is for network efficiency, not semantic authority

The leader:

batches updates

reduces load

coordinates tabs

The tabs:

own truth about what is being viewed

Practical constraints (so you don’t over-engineer)
Reasonable limits

Max scopes per user: 5–10

Heartbeat interval: 10–15s

TTL: 30–45s

This keeps:

Redis keys bounded

Presence accurate

Load predictable

Presence API (final shape)
Sync (authoritative)
POST /presence/sync
{
scopes: ["post:123", "post:456"]
}

Read viewers
GET /presence/viewers?scope=post:123

Response:

{
"count": 2,
"users": [{ "id": "...", "name": "...", "avatar": "..." }]
}

TL;DR (pin this)

A user can be in multiple scopes

Leader does transport, not truth

Tabs declare scopes

Leader aggregates

Server stores (user, scope)

TTL is safety, not logic
