---
title: "Video Player Gated Plan"
date: "2026-04-17"
tags: [plan, project/experts]
category: "plan"
---

# Video Lesson Completion Gate Plan

## Summary

- Store this plan in the vault at `/home/logix/brain/Projects/Experts/Experts App/planning/research/2026-04-17-video-lesson-completion-gating.md`.
- Goal: require native video lessons to be genuinely watched before `Mark Complete` is allowed, with server-side enforcement so users cannot bypass the rule from the client.
- Product rule locked for this phase:
  - video lessons require `95% watched coverage` or `ended`
  - skipped segments do not count
  - enforcement is server-backed
  - new YouTube/Vimeo-style embeds should be disabled for new or edited lessons; this phase keeps direct file URLs and native player sources

## Implementation Changes

- Add persisted per-user video watch state for lessons instead of overloading `LessonProgress`.
  - Introduce a dedicated lesson-video watch record keyed by `userId + lessonId`.
  - Persist at minimum: `durationSec`, `watchedRanges`, `watchedPercent`, `lastPositionSec`, `eligibleAt`, timestamps.
  - Keep `LessonProgress` as the completion record; do not merge watch-tracking and completion into one row.

- Add a pure watch-coverage utility in the learning domain.
  - Input: prior watched ranges plus a newly watched segment.
  - Output: normalized merged ranges, covered percent, and `isEligible`.
  - Eligibility rule: `true` when merged coverage reaches `95%` of duration, or when the player emits `ended`.

- Extend the native `VideoPlayer` contract so the learn flow can observe enough playback detail.
  - Keep existing `onProgress` and `onEnded`.
  - Add callbacks for `loadedmetadata` and seek transitions so the hook can detect skipped gaps.
  - Do not add provider-SDK work in this phase; this logic is only for the native player branch.

- Add a dedicated client hook for lesson watch gating.
  - Name it at the learn/player layer, e.g. `useVideoLessonCompletionGate`.
  - Responsibilities:
    - initialize from persisted watch state for the current lesson
    - accumulate watched segments only during real playback
    - ignore skipped-ahead gaps
    - throttle writes to the watch-progress API
    - expose `watchedPercent`, `isEligible`, `isSyncing`, and button-copy/state for the learn UI
  - Reset cleanly when the learner switches lessons.

- Add watch-progress API surface under the existing course/lesson route shape.
  - Add a thin route such as `app/api/v1/courses/[id]/modules/[moduleId]/lessons/[lessonId]/watch-progress/route.ts`.
  - `GET`: return persisted watch state for the current learner and lesson.
  - `POST`: validate payload with Zod, merge ranges in a handler, compute eligibility, and upsert the watch row.
  - Keep route -> handler -> Prisma separation consistent with the repo’s CQRS-style pattern.

- Enforce the rule in lesson completion.
  - Update `app/api/v1/courses/[id]/progress/route.ts` so `POST` checks whether the lesson is a native video lesson and, if so, requires an eligible watch record before completion can be written.
  - Return a clear `409` response for “video not fully watched”.
  - Keep prerequisite enforcement intact and run both checks before upserting `LessonProgress`.

- Update the learn experience.
  - In `use-course-player`, load the watch gate only for native video lessons.
  - Disable `Mark Complete` until the hook reports eligibility.
  - Show progress-aware helper text instead of a generic disabled button.
  - On success, keep the existing optimistic lesson completion flow and next-item navigation.

- Tighten creator-side input rules for future compatibility.
  - In the curriculum lesson editor, remove or disable YouTube/Vimeo embed acceptance for new or edited video lessons.
  - Keep direct MP4/MOV/HLS URLs and uploaded lesson videos supported.
  - Update validation and i18n copy so the field clearly expects a direct playable media URL, not a third-party watch page.

## API / Type Changes

- New persistence model for video watch state with a Prisma migration.
- New DTO/schema for watch-progress reads and writes.
- `VideoPlayer` props gain seek/metadata event callbacks needed by the gate hook.
- Learn UI state gains a video-watch eligibility model distinct from `LessonProgress`.
- Completion API behavior changes:
  - native video lesson + not eligible => reject completion
  - non-video lessons => unchanged
  - legacy external embed lessons => unchanged in this phase

## Test Plan

- Unit test the range-merging utility:
  - overlapping ranges merge correctly
  - skipped gaps remain uncovered
  - repeated reports are idempotent
  - `95%` threshold and `ended` both unlock eligibility

- Handler and route tests:
  - watch-progress `POST` merges persisted ranges and returns updated eligibility
  - progress completion rejects native video lessons without eligible watch state
  - progress completion still respects prerequisites
  - non-video lessons still complete without watch-state checks

- UI tests around the learn flow:
  - `Mark Complete` is disabled for an unfinished native video lesson
  - the button enables after enough watched coverage or an ended event
  - switching lessons resets gate state correctly
  - completed lessons still render as completed after reload

- Regression checks:
  - direct uploaded video lessons still play in the native player
  - direct file URLs still work
  - legacy YouTube/Vimeo lessons remain viewable and do not break the learn page

## Assumptions And Defaults

- Existing completed lesson records are grandfathered; this phase does not retroactively reopen already-completed lessons.
- Legacy external embed lessons are not migrated in this phase; they remain playable and keep the old completion behavior until a separate migration/removal effort is approved.
- New/edited creator flows should stop encouraging third-party embeds and steer authors toward uploaded videos or direct media URLs compatible with the native player.
- The current playback-rate cap remains in place; this phase does not add stricter anti-speed rules beyond the existing player behavior.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
