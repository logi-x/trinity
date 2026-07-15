---
title: "EXP-78 — JWT role-staleness in event thumbnail upload — revoked admin bypasses host check"
date: "2026-05-22"
status: open
resolution: unknown
tags: [bug, security, authorization, jwt, events, project/experts]
linear: "https://linear.app/experts/issue/EXP-78/security-jwt-role-staleness-in-event-thumbnail-upload-revoked-admin"
fingerprint: "50a0efcf0017"
---

## Summary

`POST /api/v1/events/[id]/thumbnail/route.ts` introduced an access check in PR #378 that verifies the caller is either an admin or a host of the event. The admin check uses `session.user.isAdmin` (JWT-derived) rather than a fresh database lookup. A user whose admin role was revoked in the database but who holds a still-valid JWT can continue uploading thumbnails to any event for up to 30 days — the JWT session lifetime.

This is the same vulnerability class as EXP-69 (resolved 2026-05-22 via PR #375) but on a new surface introduced by the same day's PR #378.

## Attack path

1. Attacker was previously an admin; admin role revoked in DB.
2. Attacker's JWT remains valid (up to 30-day window).
3. `session.user.isAdmin` is `true` from the stale JWT.
4. Attacker calls `POST /api/v1/events/[id]/thumbnail` for any event.
5. The host check passes because `session.user.isAdmin === true`.
6. Attacker uploads arbitrary thumbnail to any event.

## Root cause

`apps/experts-app/app/api/v1/events/[id]/thumbnail/route.ts` — `POST` handler reads `isAdmin` from JWT session, not from `prisma.user.findUnique`.

## Agent fingerprint

`<!-- agent-fp: 50a0efcf0017 -->`

## Status

`open` — Backlog as of 2026-05-22.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
