---
title: "EXP-193 — [spinoff: EXP-174] Strict channel isolation — events emitted for unsubscribed post channels in realtime sync"
date: "2026-05-29"
status: resolved
resolution: "hasPostEventsChannel || short-circuit dropped at both emit sites via PR #614; strict isChannelRequested used. Isolation regression test added."
tags: [bug, api, realtime, isolation, project/experts]
linear: "https://linear.app/experts/issue/EXP-193/spinoff-exp-174-fix-channel-isolation-events-emitted-for-unsubscribed"
fingerprint: "f77e9e808a26e47341fb7a2b55e72d5b9f2a4368"
---

## Summary

`apps/experts-app/app/api/v1/internal/realtime/sync/route.ts:415,436` — the post-channel emit guards used `hasPostEventsChannel || isChannelRequested(postChannel)`. Because `hasPostEventsChannel` is true whenever **any** requested channel looks like a `post:events` channel, a client subscribed to `post:A:events` also received like events tagged `channel: post:B:events` for every other post it owns — over-delivery of own data (not a cross-user IDOR).

## Root cause

Coarse aggregate flag `hasPostEventsChannel` short-circuited the specific `isChannelRequested(postChannel)` check at both emit sites. The flag's correct role is work-gate ("should this block run at all?"), not emit-gate.

## Spinoff from

EXP-174 (realtime sync IDOR). Filed by R5 (gatekeeper) during EXP-174 PR review.

## Agent fingerprint

`<!-- agent-fp: f77e9e808a26e47341fb7a2b55e72d5b9f2a4368 -->`

## Status

`resolved` — `hasPostEventsChannel ||` short-circuit dropped at both emit sites in PR #614 (commit bd2212c7). `hasPostEventsChannel` retained as coarse work-gate only. Isolation regression test added.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
