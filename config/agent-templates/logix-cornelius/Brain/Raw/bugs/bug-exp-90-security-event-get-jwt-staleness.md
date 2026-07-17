---
title: "EXP-90 — JWT role-staleness in GET /api/v1/events/[id] — revoked admin reads private meeting credentials"
date: "2026-05-23"
status: open
resolution: unknown
tags: [bug, security, authorization, jwt, events, credential-exposure, project/experts]
linear: "https://linear.app/experts/issue/EXP-90/security-jwt-role-staleness-in-get-apiv1eventsid-revoked-admin-reads"
fingerprint: "c53cfd8af8a6"
---

## Summary

`GET /api/v1/events/[id]` passes `isAdmin: Boolean(session?.user?.roles?.includes('admin'))` (JWT-derived) to `handleEventDetail`. For published online or hybrid events, the handler exposes `meetingUrl` (Zoom link) and `locationDetails` to any caller with `isAdmin = true`. A revoked admin with a stale JWT can read the private meeting URL (including Zoom password) and location details for any published event they are not a host of — for up to 30 days.

This is a confidentiality breach with no rollback: once the Zoom password is read, it is known.

Same vulnerability class as EXP-69, EXP-78, EXP-84, EXP-85, EXP-88, EXP-89.

## Root cause

`app/api/v1/events/[id]/route.ts` — GET handler: `isAdmin` derived from JWT session claim. No DB re-validation before returning sensitive credential fields.

## Agent fingerprint

`<!-- agent-fp: c53cfd8af8a6 -->`

## Status

`open` — Todo (High). Irreversible credential exposure risk. Should be batched with EXP-88 and EXP-89 in a single PR targeting `app/api/v1/events/[id]/route.ts`.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
