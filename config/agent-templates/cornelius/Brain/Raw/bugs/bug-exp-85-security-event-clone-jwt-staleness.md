---
title: "EXP-85 — JWT role-staleness in event clone — revoked admin bypasses host check (EXP-78 follow-up)"
date: "2026-05-22"
status: resolved
resolution: merged PR #410
tags: [bug, security, authorization, jwt, events, project/experts]
linear: "https://linear.app/experts/issue/EXP-85/security-jwt-role-staleness-in-event-clone-revoked-admin-bypasses-host"
fingerprint: "f5c264dbf6b4"
---

## Summary

`POST /api/v1/events/[id]/clone` passed `isAdmin` from `EventCloneSchema`/`EventCloneCommand` (sourced from `session.user.roles`, JWT-derived) into `handleEventClone`. A user with a revoked admin role but a valid JWT could bypass the host check inside `handleEventClone` and clone any private event, then own the clone — for up to 30 days.

Same vulnerability class as EXP-69, EXP-78, EXP-84.

## Root cause

`app/api/v1/events/[id]/clone/route.ts` + `src/lib/events/handlers/event-clone.handler.ts` — `isAdmin` was part of the command payload rather than being DB-derived inside the handler.

## Agent fingerprint

`<!-- agent-fp: f5c264dbf6b4 -->`

## Status

`resolved` — merged PR #410 (2026-05-23T00:46Z). `isAdmin` removed from schema/command; handler derives it from `prisma.user.findUnique` in `Promise.all` with the event lookup. Null user row yields `isAdmin: false`.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
