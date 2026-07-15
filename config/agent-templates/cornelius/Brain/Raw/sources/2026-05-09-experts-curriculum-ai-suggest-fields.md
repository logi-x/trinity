---
title: "Experts Curriculum Ai Suggest Fields"
date: "2026-05-09"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts curriculum AI Suggest field coverage

Date: 2026-05-09

## Context

AI Suggest was available for course/event authoring and lesson body drafting, but not for curriculum module title/description or lesson title/summary. Course AI suggested tags also normalized to lowercase, while the desired convention is camelCase by default.

## Change

Added AI Suggest to curriculum authoring fields:

- Module title
- Module description
- Lesson title
- Lesson summary/description

The suggestion context now supports module-specific and lesson-specific metadata:

- course title
- course description
- module title
- lesson type
- existing module titles to avoid duplicates

Updated the AI suggest API to accept `module` as an entity type and tune title/description prompt requirements for modules and lessons.

Follow-up: split curriculum summary generation into its own `summary` field type. Course/event card copy keeps using `description`, while module descriptions and lesson summaries now call `summary` with shorter learner-facing constraints.

Updated course extras AI tag acceptance so selected AI tags are normalized to camelCase.

## Verification

- `pnpm typecheck:touched -- app/api/v1/ai/suggest/route.ts src/hooks/use-ai-suggest.ts 'app/(i18n)/_shared/creator/courses/[id]/curriculum/page.tsx' 'app/(i18n)/_shared/creator/courses/[id]/curriculum/sections/curriculum-builder-shell.tsx' 'app/(i18n)/_shared/creator/courses/[id]/curriculum/sections/module-dialog.tsx' 'app/(i18n)/_shared/creator/courses/[id]/curriculum/sections/lesson-dialog.tsx' src/lib/courses/catalog/forms/sections/course-extras-section.tsx`
- `npx gitnexus detect-changes -r experts`

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
