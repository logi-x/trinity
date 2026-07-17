---
title: "EXP-208: post likes-changed realtime events expose liker userId to anonymous callers"
linear_id: "EXP-208"
agent_fp: "auto"
date: "2026-05-30"
severity: "Medium"
status: "resolved"
resolution: "PR #655 — strip userId from liker objects emitted in post:<id>:likes-changed events"
tags: [bug, realtime, pii, security, project/experts]
category: "bug"
source: "automation"
---

# EXP-208: likes channel liker userId exposure

**Linear:** [EXP-208](https://linear.app/experts/issue/EXP-208) | **Status:** Resolved (PR #655)

## Summary
The realtime sync channel `post:<id>:likes-changed` emitted the full liker object including `userId`. Since published posts are accessible to anonymous callers, any subscriber could enumerate the user IDs of all users who liked a given post.

## Impact
User ID enumeration at zero authentication cost via realtime WebSocket subscription. Compounds with EXP-195 (liker PII in post events, still open).

## Fix
PR #655 stripped `userId` from liker objects before emitting on the `likes-changed` channel.

## Related
- EXP-195 — liker userId in post:<id>:events (still open)
- EXP-174 — IDOR in realtime sync (resolved PR #612)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
