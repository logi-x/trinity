---
title: "EXP-89 — JWT role-staleness in DELETE /api/v1/events/[id] — revoked admin permanently deletes any event"
date: "2026-05-23"
status: open
resolution: unknown
tags: [bug, security, authorization, jwt, events, project/experts]
linear: "https://linear.app/experts/issue/EXP-89/security-jwt-role-staleness-in-delete-apiv1eventsid-revoked-admin"
fingerprint: "5b2fd78b32ae"
---

## Summary

`DELETE /api/v1/events/[id]` has a single authorization gate: `if (!isHost && !session?.user?.roles?.includes('admin'))`. The `isAdmin` check trusts the JWT. A user whose admin role was revoked in the DB but who holds a still-valid JWT can permanently delete any event with zero registrations that they do not host — for up to 30 days.

Same vulnerability class as EXP-69, EXP-78, EXP-84, EXP-85, EXP-88.

## Root cause

`app/api/v1/events/[id]/route.ts` — DELETE handler: admin check reads `session?.user?.roles?.includes('admin')` (JWT-derived) rather than a fresh DB lookup.

## Agent fingerprint

`<!-- agent-fp: 5b2fd78b32ae -->`

## Status

`open` — Todo (Urgent). Should be batched with EXP-88 and EXP-90 in a single PR targeting `app/api/v1/events/[id]/route.ts`.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
