---
title: "EXP-273 — Release workflow has no force_build_realtime input — realtime image lags the release version"
date: "2026-06-02"
status: resolved
resolution: "merged via PR #761 (2026-06-02)"
tags: [bug, ci, release, realtime, project/experts]
linear: "https://linear.app/experts/issue/EXP-273/bug-release-workflow-has-no-force-build-realtime-input-realtime-image"
fingerprint: "7d65c8b1dd47"
---

## Summary

`.github/workflows/experts-app.yml` exposed `force_build_app` and `force_build_worker` dispatch inputs but had no equivalent `force_build_realtime`. The `detect-changes` gate for realtime only flips `realtime=true` on `apps/experts-realtime/**` source changes; both the build/push and container-recreate steps are gated on that flag. A release that bumps app/worker without touching realtime source left realtime un-rebuilt, un-retagged, and un-recreated — drifting versions behind with no operator lever to fix it.

## Root cause

`.github/workflows/experts-app.yml` — `workflow_dispatch` inputs section (~L28–34). `force_build_realtime` input was absent; the realtime build/push and recreate steps had no override path.

Fix: add `force_build_realtime` input mirroring the app/worker inputs, wire it through `FORCE_BUILD_REALTIME` into `detect-changes`, and gate realtime build+recreate steps on the flag. Released via PR #761.

## Agent fingerprint

`<!-- agent-fp: 7d65c8b1dd47 -->`

## Status

`resolved` — Done. Merged via PR #761 (2026-06-02T04:06Z). Same-day open+close.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
