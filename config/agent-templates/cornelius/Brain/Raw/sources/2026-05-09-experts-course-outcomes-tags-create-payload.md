---
title: "Experts Course Outcomes Tags Create Payload"
date: "2026-05-09"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts course outcomes and tags create payload fix

Date: 2026-05-09

## Context

The creator course form has an "Outcomes & Tags" section for learning outcomes, requirements, and tags. The form state and API schema both support these fields, and course updates already sent them through the update payload.

## Finding

New course creation used `buildCourseCreatePayload`, which omitted `learningOutcomes`, `requirements`, and `tags`. As a result, values entered in the create flow were dropped before `/api/v1/courses` received the request.

## Change

Updated `apps/experts-app/src/lib/courses/catalog/forms/course.mapper.ts` so create and update payload builders normalize list fields by trimming entries and filtering blanks, and so create payloads include learning outcomes, requirements, and tags.

Added focused tests in `apps/experts-app/src/lib/courses/catalog/forms/__tests__/course.mapper.test.ts`.

Follow-up: `CourseExtrasSection` was wired through raw React Hook Form `setValue`, which did not mark the course form dirty. Updated `apps/experts-app/src/lib/courses/catalog/forms/course-form.tsx` to route outcomes, requirements, and tags changes through the form hook's `updateField`, preserving `shouldDirty` and `shouldValidate`.

## Verification

- `pnpm vitest run src/lib/courses/catalog/forms/__tests__/course.mapper.test.ts`
- `pnpm typecheck:touched -- src/lib/courses/catalog/forms/course.mapper.ts src/lib/courses/catalog/forms/__tests__/course.mapper.test.ts`
- `pnpm typecheck:touched -- src/lib/courses/catalog/forms/course-form.tsx`
- `npx gitnexus detect-changes -r experts`

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
