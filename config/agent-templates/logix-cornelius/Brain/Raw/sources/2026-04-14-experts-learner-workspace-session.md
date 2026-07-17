---
title: "Experts Learner Workspace Session"
date: "2026-04-14"
tags: ["project/experts", "project/experts-app", "topic/lms", "topic/learner-layout", "topic/course-player"]
category: "session-log"
source: "codex"
source_id: "Raw/sources/2026-04-14-experts-learner-workspace-session.md"
---

# Experts Learner Workspace Session

- Scope: Learner workspace and LMS bridge workstream for `apps/experts-app`.
- Status: In Progress.
- Focus today: Shared LMS view-model parity between `/courses/[id]/learn` and creator curriculum, plus targeted learner UX improvements.

## Progress

- [x] Reset implementation context to `~/brain-v2/Raw/plans/PLAN.md`.
- [x] Confirmed branch context on `codex/learner-layout-lms-bridge`.
- [x] Added a dedicated learner shell at `src/components/learner/LearnerWorkspaceLayout.tsx`.
- [x] Added route-local learner types for `/courses/[id]/learn`.
- [x] Rewired `/courses/[id]/learn` to render through the new learner shell instead of owning the workspace chrome inline.
- [x] Extracted all page state and workflows into `logic/use-course-player.ts`.
- [x] Split page UI into `sections/` slices: `lesson-list`, `progress-card`, `lesson-player`, `module-overview`, `loading-state`, `cert-modal`, `item-icon`.
- [x] Rewrote `page.tsx` as a thin orchestration layer (~290 lines, down from ~1150).
- [x] Added creator curriculum parity signals to `curriculum-modules.tsx`: module total duration, per-module blocker count, per-item missing content/media warnings, prerequisite indicators, Preview as Learner link.
- [x] Created `lesson-resource-panel.tsx`: lesson resource CRUD (currently add/list/delete in code) wired into the lesson editor in `curriculum-builder-shell.tsx`.
- [x] Tightened learner player typing to use the course DTO instructors directly instead of `any`.
- [x] Aligned `lesson-resource-panel.tsx` to the repo's HeroUI patterns for `Select` and `Switch`.
- [x] Confirmed WSL-based command execution now works for direct project paths and reran project checks from `/home/logix/experts/apps/experts-app`.
- [x] Confirmed full `pnpm typecheck` now runs against the actual app and is red because of pre-existing repo-wide issues outside this branch.
- [ ] Finish the new shared LMS view-model layer under `src/lib/courses/lms/` and wire learner sections onto it.
- [ ] Surface active lesson resources and explicit locked/up-next/resume states in the learner UI.
- [ ] Reuse the same blocker/preview logic inside creator curriculum.
- [ ] Add targeted unit tests for unlock mapping, resume target resolution, blocker derivation, and module summaries.

## Notes

- The learner experience is now being treated as a first-class workspace rather than a single large route component.
- `use-course-player.ts` owns the route orchestration, but shared LMS state still needed to be centralized because access state, resume behavior, up-next logic, and creator readiness were being derived in multiple places.
- A new pure utility layer is now being introduced at `apps/experts-app/src/lib/courses/lms/view-model.ts` to centralize:
  - item state mapping (`draft`, `locked`, `available`, `current`, `completed`, `upNext`)
  - unlock reason derivation
  - resume/start target resolution
  - module summary aggregation
  - learner preview deep-link generation
  - lesson content blocker derivation
- The learner route is being updated to support `?item=` deep-links so creator preview actions can open a specific learner item instead of only the root `/learn` page.
- The learner player is also being updated to expose active lesson resources from lesson detail DTOs, not just author them on the creator side.
- Current uncommitted work in progress touches:
  - `app/(i18n)/_shared/courses/[id]/learn/logic/use-course-player.ts`
  - `app/(i18n)/_shared/courses/[id]/learn/page.tsx`
  - `app/(i18n)/_shared/courses/[id]/learn/sections/lesson-list.tsx`
  - `app/(i18n)/_shared/courses/[id]/learn/sections/lesson-player.tsx`
  - `app/(i18n)/_shared/courses/[id]/learn/sections/module-overview.tsx`
  - `app/(i18n)/_shared/courses/[id]/learn/types.ts`
  - `src/lib/courses/lms/view-model.ts`
  - `src/lib/courses/lms/__tests__/view-model.test.ts`
- The branch still contains the earlier two-file cleanup on the learner shell/page to remove dead props.

## Verification

- `pnpm typecheck` now executes in WSL against the real app.
- Current red status is dominated by existing unrelated repo-wide ESLint/typecheck issues such as:
  - `app/(i18n)/_shared/admin/views/page.tsx`
  - `src/hooks/use-realtime.ts`
  - `src/hooks/use-scoped-presence.ts`
  - script files using forbidden `require()`
- Branch-local verification still needs to be rerun after the new LMS view-model slice is finished.

## Links

- [[Entities/Projects/Experts]]
- [[Entities/Projects/Experts App]]

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
