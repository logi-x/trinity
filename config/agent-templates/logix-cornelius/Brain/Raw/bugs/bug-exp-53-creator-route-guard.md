---
title: "EXP-53 — Creator route guard disabled in proxy.ts; /creator/* accessible to any authenticated user"
date: "2026-05-20"
status: open
resolution: unknown
tags: [bug, security, auth, route-guard, medium, project/experts]
linear: "https://linear.app/experts/issue/EXP-53"
fingerprint: "95412bb984d6"
---

## Summary

The creator route guard in `apps/experts-app/proxy.ts` that should restrict `/creator/*` pages to users with the `instructor` or `admin` role is disabled (commented out or removed). Any authenticated user — including plain learners — can navigate to the creator workspace UI pages without being redirected.

Note: underlying API routes enforce role-based access via `assertCourseWriteAccess` and similar guards, so data mutations remain protected. The proxy-level guard is a UI-layer concern (redirecting non-instructors before they reach the creator shell), but its absence is a regression from the intended access model.

## Repro

1. Log in as a learner account (no instructor or admin role).
2. Navigate directly to `/creator/courses`.
3. Observe: creator dashboard renders instead of redirecting to home or returning 403.

## Agent fingerprint

`<!-- agent-fp: 95412bb984d6 -->`

## Status

`open` — no PR yet. Fix: re-enable the creator route guard in `proxy.ts` that checks `session.user.roles` includes `instructor` or `admin` before serving `/creator/*` routes.

Note: a working-tree WIP in `proxy.ts` (dev WS endpoints in base CSP, flagged in 2026-05-20 session notes) may conflict — verify the guard fix does not interact with that change.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
