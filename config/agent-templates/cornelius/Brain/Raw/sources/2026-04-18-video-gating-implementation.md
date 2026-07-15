---
title: "Experts App video lesson gating implementation"
date: "2026-04-18"
source: "codex-session"
project: "Experts App"
tags: ["project/experts-app", "courses", "video", "completion", "gating", project/experts]
---

## Summary

Implemented server-backed gating for native course video lessons in `apps/experts-app`.

## Decisions captured

- Native video lesson completion now depends on persisted watch state, separate from `LessonProgress`.
- Eligibility unlocks when watched coverage reaches `95%` or the native player emits `ended`.
- Skipped segments are excluded by tracking watched ranges from continuous playback only.
- Legacy YouTube/Vimeo-style lessons remain viewable and keep old completion behavior for this phase.
- Creator flows for new or edited video lessons now steer authors to direct playable media URLs instead of third-party watch pages.

## Implementation notes

- Added Prisma model + migration: `LessonVideoWatchState`.
- Added watch-progress API under the lesson route shape with `GET` and `POST`.
- Enforced native-video eligibility in course lesson completion API with `409 "Video not fully watched"`.
- Extended the native `VideoPlayer` with metadata and seek callbacks for gate tracking.
- Added a learn-layer hook to fetch persisted watch state, merge local watch segments, debounce sync, and drive button/helper UI.

## Verification

- Focused Vitest coverage added for watch-range merging and the new/updated API routes.
- Full app `tsc` still reports pre-existing unrelated Next route validator errors under `.next/dev/types`.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
