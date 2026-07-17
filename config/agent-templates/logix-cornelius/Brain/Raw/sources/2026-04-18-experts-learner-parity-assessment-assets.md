---
title: "Experts Learner Parity Assessment Assets"
date: "2026-04-18"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts learner parity session

- Date: 2026-04-18
- Area: `apps/experts-app`
- Theme: learner-side parity for creator-side quiz/exam/media work from 2026-04-17

## What changed

- Quiz and course-exam learner start/status payloads now include question `assets`, not just text, type, and options.
- A shared learner question DTO was introduced so quiz and exam players consume the same question contract.
- Learner question rendering now supports:
  - `multi_select`
  - inline question images
  - downloadable/openable question attachments
- Public/learner course detail now surfaces `courseLevelAssets` in the overview tab as read-only materials.
- Learner `/learn` mobile UX was refined:
  - both sticky header rows now hide together on downward scroll on mobile devices
  - the header returns on upward scroll or near the top of the page
  - the behavior uses `react-device-detect` mobile detection instead of a raw viewport-width check

## Important implementation notes

- Question assets are read from existing Prisma relations on `quizQuestion.assets` and `courseExamQuestion.assets`, then mapped via `mapQuestionAssetToDTO`.
- Lesson asset behavior was intentionally not changed:
  - `primary_video` remains the playable lesson source
  - `resource` remains learner-visible supporting material
- Learner/public asset UI is intentionally simple and read-only; no creator controls were added outside creator flows.
- For learner `/learn`, mobile-only header collapsing is now applied at the whole sticky-header wrapper level, not just the top logo row.
- The mobile header hide/show effect should avoid animating `max-height` on the measured sticky wrapper; using stable height plus `transform` and compensating negative margin is smoother and avoids scroll jitter.
- Learner `/learn` mobile content should reserve bottom spacing for the fixed lesson browser bar plus `safe-area-inset-bottom`, otherwise the last content block gets covered near the end of the page.
- Learner `/learn` mobile header hide-on-scroll should stay hidden at the bottom too; clamp scroll position to the document bounds so mobile overscroll/bounce does not falsely trigger a reveal.
- Learner `/learn` desktop sidebar bottom spacing is best owned by the scroll container in `LearnerWorkspaceLayout`, not by `lesson-list.tsx`; keep extra bottom padding on the scrollable sidebar content and avoid redundant bottom margin on the sticky aside wrapper.
- In the desktop learner sidebar, do not combine a `top` offset that already includes header spacing with an additional top margin on the sticky aside; that double-counts vertical spacing and reduces the usable scroll height.
- `/courses/[id]/learn` dev edits can appear like full page reloads even without a Fast Refresh bailout message because the route remount triggers a heavy client fetch sequence in `use-course-player` and immediately falls back to `LoadingState`.
- A concrete runtime issue in the learner header path was invalid pressable composition:
  - `LanguageSwitcher` needed `Dropdown.Trigger`
  - learn-header navigation actions should avoid nested `Link` + `Button` pressables
- Learner workspace sidebar open state is now persisted with `localStorage` under `learner-sidebar:open`, following the same hydration-first pattern used by `AdminWorkspaceShell`.
- For learner `/learn`, sidebar hydration must complete before starting the course-player fetch sequence; otherwise the page can finish loading and then visually reopen the sidebar after mount.
- Even after hydration is fixed, an already-open learner sidebar should not animate in on first paint; disable the initial `AnimatePresence` enter animation so refresh preserves the open visual state immediately.
- Course-level assets now belong primarily to `/courses/[id]/learn` as a learner resources tab on the module overview surface; the public `/courses/[id]` page no longer shows the large preview-heavy assets card.
- The learner resources tab is intentionally simple: asset list, type/mime/size metadata, and open/download actions without inline previews.

## Verification

- Targeted touched-file typecheck passed.
- Vitest passed after the change, including:
  - quiz start route coverage
  - course exam start route coverage
  - question renderer asset coverage

## Progress snapshot

### Done

- Learner quiz and course-exam start/status payloads now return question assets.
- Quiz and exam players now share one learner question contract.
- Learner question rendering now supports:
  - `multi_select`
  - inline question images
  - attachment links/files
- Public/learner course detail now shows `courseLevelAssets` in the overview tab.
- `en`, `ar`, and `es` copy was added for the new learner/detail asset UI.
- Route/component test coverage was added and checks passed.

### Pending

- Manual QA on real seeded learner flows.
- Visual/UX review for:
  - multi-asset quiz questions
  - multi-asset exam questions
  - mixed course-level asset types
- Product check on whether course-level assets should also appear inside `/courses/[id]/learn`, not only course detail.
- Possible polish for richer learner presentation of video/link course assets.

### Up next

- Run learner-flow QA on seeded course content with:
  - `multi_select` questions
  - question image + attachment combinations
  - course-level image/file/video/link assets
- Check mobile + RTL rendering.
- Decide whether any follow-up UI polish or extra learner asset surfacing is needed.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
