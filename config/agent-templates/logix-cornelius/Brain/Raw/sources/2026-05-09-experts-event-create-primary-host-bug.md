---
title: "Experts Event Create Primary Host Bug"
date: "2026-05-09"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts event create primary host bug

Date: 2026-05-09
Project: Experts

## Summary

Fixed an event creation bug where submitting the creator in the Hosts & Speakers payload as `guest` created an event with no primary `host`.

## Root cause

`apps/experts-app/src/lib/events/handlers/event-create.handler.ts` normalized submitted hosts by preserving the first role for each user. If the creator appeared in the submitted `hosts` array as `guest`, the normalizer did not upgrade them to `host`. `handleEventDetail` requires a primary host and returns `404` when no host with role `host` exists, so the newly created event could not be opened from the creator event detail endpoint.

## Fix

`normalizeHosts` now always writes the creator entry as `{userId: command.userId, role: "host"}` after de-duplicating submitted hosts. This preserves invited guest/co-host entries while guaranteeing every created event has a primary host.

## Verification

- `pnpm exec vitest run src/lib/events/handlers/__tests__/event-create.handler.test.ts`
- `pnpm typecheck:touched -- src/lib/events/handlers/event-create.handler.ts src/lib/events/handlers/__tests__/event-create.handler.test.ts`
- `npx gitnexus detect-changes -r experts`

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
