---
title: "EXP-88 — JWT role-staleness in PUT /api/v1/events/[id] — revoked admin edits any event"
date: "2026-05-23"
status: open
resolution: unknown
tags: [bug, security, authorization, jwt, events, project/experts]
linear: "https://linear.app/experts/issue/EXP-88/security-jwt-role-staleness-in-put-apiv1eventsid-revoked-admin-edits"
fingerprint: "0253a1037e64"
---

## Summary

`PUT /api/v1/events/[id]` gates on `isAdmin` at two points in the handler (outer host-or-admin check; isFeatured/force-unpublish/archive guards), deriving the value from `session.user.roles` (JWT-derived). A user whose admin role was revoked in the DB but who holds a still-valid JWT can edit any non-archived event's content, set `isFeatured`, force-unpublish, or archive any event they do not host — for up to 30 days.

Same vulnerability class as EXP-69, EXP-78, EXP-84, EXP-85.

## Root cause

`app/api/v1/events/[id]/route.ts` — PUT handler: `isAdmin` derived from JWT session claim, not from `prisma.user.findUnique`.

## Agent fingerprint

`<!-- agent-fp: 0253a1037e64 -->`

## Status

`open` — Todo (Urgent). Should be batched with EXP-89 and EXP-90 in a single PR targeting `app/api/v1/events/[id]/route.ts`.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
