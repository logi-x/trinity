---
title: "EXP-195 — [bug] Liker userId exposed in realtime sync polling events for public posts — anonymous enumeration path"
date: "2026-05-29"
status: open
resolution: unknown
tags: [bug, security, api, realtime, pii, privacy, project/experts]
linear: "https://linear.app/experts/issue/EXP-195/bug-liker-userid-exposed-in-realtime-sync-polling-events-for-public"
fingerprint: "c84fb6ebe85f"
---

## Summary

EXP-174 explicitly allows anonymous callers to subscribe to published post channels: "A published post is public — its activity is already public." However, the like-event payload emitted for those public posts includes `userId` of the person who performed the like action. An unauthenticated attacker can subscribe to a public post channel and silently enumerate the user IDs of all users who have liked that post.

## Trigger scenario

1. Attacker discovers a public post ID (from a post page URL).
2. Sends unauthenticated: `GET /api/v1/internal/realtime/sync?cursor=0&channels=post:<public-post-id>:events`
3. Polls for like events — each event includes `{ userId: <liker-uuid> }`.
4. Cross-reference leaked UUIDs against other endpoints that accept userId as input.

## Root cause

Like activity events emitted on post channels include the actor `userId` without checking whether the caller is authenticated or whether the post is public. For private posts this is already gated by the `authorizedPostIds` check (EXP-174). For public posts the channel is permitted but the `userId` field in the event payload should be stripped for anonymous callers.

## Agent fingerprint

`<!-- agent-fp: c84fb6ebe85f -->`

## Status

`open` — Backlog (Medium priority). Fix: redact `userId` from like-event payloads when the requesting caller is anonymous (no session), or emit a pseudonymous counter instead. Cross-linked to EXP-174 (IDOR, resolved) and EXP-191 (rate limiting, open).

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
