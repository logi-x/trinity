---
title: "Experts creator form validation tracker"
date: "2026-04-14"
project: "Experts App"
source: "codex session"
tags: ["project/experts", "creator", "forms", "validation", "zod", "ux"]
---

# Summary

Added a Zod-backed validation tracker to creator course and event forms so disabled save/publish actions explain exactly which schema checks are still blocking progress.

## Changes made

- Added a shared validation tracker component at `apps/experts-app/src/components/forms/validation-tracker.tsx`.
- Updated `useCourseForm` and `useEventForm` to expose deduplicated schema issues from `CourseFormSchema.safeParse(...)` and `EventFormSchema.safeParse(...)`.
- Switched form-level `isValid` gating in both hooks to use the derived Zod issue list so the UI and the disabling logic share the same source of truth.
- Rendered the tracker beside creator sidebar actions in both course and event form shells.
- Mapped schema paths to user-facing field labels and translated the messages through existing creator validation namespaces.
- Added tracker copy to `en`, `ar`, and `es` creator course/event message files.

## Verification

- `pnpm exec prettier --write` ran on all touched files.
- Targeted `eslint --no-ignore` on touched TS/TSX files passed with one existing warning in `use-course-form.ts` from the React Compiler / React Hook Form `watch()` integration.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
