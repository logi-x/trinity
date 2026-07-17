---
title: "EXP-84 — JWT role-staleness in event list — revoked admin bypasses host check on POST /api/v1/events"
date: "2026-05-22"
status: resolved
resolution: merged PR #406
tags: [bug, security, authorization, jwt, events, project/experts]
linear: "https://linear.app/experts/issue/EXP-84/security-jwt-role-staleness-in-event-list-revoked-admin-bypasses-host"
fingerprint: "d72831b12e3e"
---

## Summary

`POST /api/v1/events` used `session.user.isAdmin` (JWT-derived) in the `isAdmin` flag passed to `handleEventCreate`. A user whose admin role was revoked in the DB but who holds a still-valid JWT could create events with elevated admin privileges (bypassing instructor-only / publication / free-plan price guards) for up to 30 days — the JWT session lifetime.

Same vulnerability class as EXP-69, EXP-78, EXP-85.

## Root cause

`app/api/v1/events/route.ts` — POST handler passed `isAdmin: Boolean(session?.user?.roles?.includes('admin'))` to the command layer instead of a fresh DB lookup.

## Agent fingerprint

`<!-- agent-fp: d72831b12e3e -->`

## Status

`resolved` — merged PR #406 (2026-05-22T22:57Z). `isAdmin` now derived from `prisma.user.findUnique` at request time.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
