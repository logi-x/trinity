---
title: "EXP-198: JWT role-staleness on creator event detail GET — revoked admin reads private event data"
linear_id: "EXP-198"
agent_fp: "5a05720d6738"
date: "2026-05-29"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, auth, events, project/experts]
category: "bug"
source: "automation"
---

# EXP-198: JWT role-staleness on creator event detail GET

**Linear:** [EXP-198](https://linear.app/experts/issue/EXP-198) | **Fingerprint:** `5a05720d6738`

## Summary
The creator event detail `GET /api/v1/creator/events/[id]` reads `isAdmin` from `session.user.roles` (JWT claim) rather than deriving it from the database. A revoked admin's stale JWT allows them to read private `meetingUrl` and `locationDetails` (including Zoom passwords) for any event, bypassing the host-or-admin guard.

## Location
`apps/experts-app/app/api/v1/creator/events/[id]/route.ts:23`

## Related
EXP-69, 78, 84, 85, 88, 89, 90, 91 (same class), EXP-197, EXP-199 (same PR surface)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
