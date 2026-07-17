---
title: "Dedicated Learner Workspace Plan"
date: "2026-04-18"
tags: [plan, project/experts]
category: "plan"
---

# Dedicated Learner Workspace + LMS Bridge Overhaul

## Summary

Implement this work on a new branch named `codex/learner-layout-lms-bridge`.

This branch should treat learner experience as a first-class workspace, not just a single large `/learn` page. The core move is to introduce a dedicated learner layout system that borrows structural discipline from `CreatorLayout` and the shared `AppSidebarShell` approach, while keeping the learner tone focused, progress-oriented, and less “operations dashboard”.

The result should align three layers:

- a reusable learner workspace shell/layout
- a refactored LMS course player under `/courses/[id]/learn`
- a creator curriculum studio that previews and explains the exact learner experience it produces

## Implementation Changes

### 1. Add a dedicated learner layout system

- Create a learner-specific layout component, for example `src/components/learner/LearnerLayout` or `LearnerWorkspaceShell`, instead of keeping all player chrome inside the route page.
- Use the creator/admin structural system as reference, specifically:
  - shared shell ideas from `AppSidebarShell`
  - consistent header, breadcrumb, sticky chrome, and side-panel composition
  - clean page framing with a clear main content plane and supporting navigation rail
- Do not clone creator/admin visually. Adapt the system for learners:
  - emphasize progress, resume state, module flow, and “up next”
  - reduce management-style actions and dashboard density
  - keep the shell calmer and more immersive than creator/admin
- The learner layout should support:
  - sticky top bar
  - optional curriculum rail
  - optional contextual side panel
  - mobile drawer mode
  - focus mode
  - page title, breadcrumbs, progress badge, and resume context
- Scope this layout to learner-facing course consumption first; do not generalize it prematurely into a global shell for all student pages in this branch.

### 2. Refactor `/courses/[id]/learn` into a real course player

- Break the current monolithic page into route-level orchestration plus local slices:
  - `sections/` for player UI blocks
  - `logic/` for page-scoped state and workflows
  - `types/` for player-specific models
  - optional `domain/` for pure progress/unlock/view-model helpers
- Introduce a page-scoped hook such as `use-course-player` responsible for:
  - auth and enrollment gating
  - course/modules/progress/quiz-progress loading
  - privileged-viewer handling
  - resume target resolution
  - unlock/access calculations
  - item selection and previous/next navigation
  - lesson detail/resource loading and caching
  - completion/certificate flow
- Rebuild the player inside the new learner layout with:
  - top workspace bar
  - left curriculum outline rail
  - center lesson/quiz surface
  - right context panel for metadata, resources, unlock rules, and module state
- Improve the LMS behavior and clarity:
  - show “why locked” instead of only “locked”
  - show “resume”, “current”, and “up next” as explicit states
  - show lesson type, duration, quiz rules, and prerequisites before starting
  - show active lesson resources/downloads in-context
  - keep focus mode, but make it a layout concern rather than a large in-page branch
- Preserve current route URL and enrollment rules.

### 3. Upgrade creator curriculum into a learner-aware studio

- Keep the existing vertical-slice structure under `app/(i18n)/_shared/creator/courses/[id]/curriculum`, but evolve it into a learner-aware curriculum studio.
- Update the curriculum shell so creators can understand the learner outcome of what they build:
  - outline rail with module/item summaries
  - central editor workspace
  - readiness/context panel
- Add curriculum signals that map directly to learner experience:
  - draft vs published quiz visibility
  - prerequisite chains and unlock impact
  - missing content/media/resource blockers
  - module duration and item totals
  - preview target links into learner flow
- Add lesson resource authoring using the existing lesson resource backend:
  - list
  - create
  - edit
  - delete
  - downloadable vs external-link state
- Replace the current publish/readiness messaging with a curriculum-state-driven readiness summary tied to actual learner-facing completeness.

### 4. Create a shared learner/creator parity layer

- Add shared page-local view-model utilities so both surfaces speak the same LMS language:
  - item states such as `draft`, `published`, `locked`, `available`, `current`, `completed`, `upNext`
  - module summaries such as duration, visible item count, hidden quiz count, completion readiness
  - resume/start target selection
  - unlock explanation strings or reason codes
- Prefer enriching existing DTO usage over inventing parallel frontend-only contracts.
- If needed, extend lesson detail/list payloads so resources and learner-relevant metadata are consistently available in both creator preview and learner consumption flows.
- For authenticated GETs introduced during the refactor, align to existing app fetch conventions and prefer `useApiQuery` where the route is client-fetched and persistent.

## Public APIs / Interfaces

- Add learner layout-level component interfaces for:
  - learner shell props
  - learner rail state
  - learner context panel state
  - player header state
- Add shared internal types for:
  - course player item state
  - learner resume target
  - curriculum readiness summary
  - unlock reason / visibility reason
- Preserve existing URLs, lifecycle endpoints, progress endpoints, and quiz flow routes.
- Only extend DTOs where needed to expose already-existing curriculum/resource information more consistently.

## Test Plan

- Add unit tests for shared LMS view-model logic:
  - unlock state mapping
  - resume target selection
  - module summary aggregation
  - readiness blocker derivation
- Add tests for learner player behavior:
  - locked item handling
  - next/up-next transitions
  - resume selection
  - resource visibility for active lessons
- Add tests for creator curriculum behavior:
  - readiness warnings for draft quizzes and missing media/content/resources
  - preview/deep-link target generation
  - resource CRUD state updates
- Run `pnpm test` and `pnpm typecheck` in `apps/experts-app` before finalizing implementation.

## Assumptions

- The dedicated learner layout is a new learner-facing shell inspired by creator/admin structure, not a direct reuse of admin/creator visual patterns.
- This branch is intentionally end-to-end: learner layout, learner player, and creator curriculum parity all ship together.
- Existing lesson resource support is already present in the backend and should be surfaced rather than redesigned.
- Publish/archive lifecycle rules remain as-is unless a concrete implementation blocker appears.
- The learner layout is initially scoped to course consumption routes, with future broader learner workspace adoption left for later branches.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
