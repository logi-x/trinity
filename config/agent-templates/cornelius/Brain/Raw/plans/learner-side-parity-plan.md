---
title: "Learner Side Parity Plan"
date: "2026-04-18"
tags: [plan, project/experts]
category: "plan"
---

# Learner-Side Parity Plan for April 18

## Summary

Yesterday’s creator-side work in `apps/experts-app` landed in four main areas that now need learner parity:

- `multi_select` question support is present in creator flows and already partially supported by learner question controls.
- Course exams were added as a new top-level assessment section and are already visible in `/courses/[id]/learn`.
- Question-level asset upload was added for quiz and exam authoring.
- A broader course media model now supports course-level assets plus lesson/question assets.

Today’s scope is the full learner journey, with parity-first sequencing:

1. make learner APIs carry the new creator-authored data,
2. make learner runtime/components render it correctly,
3. surface course-level assets in learner/public course views where they belong.

## Key Changes

### Assessment runtime parity

- Update quiz and course-exam attempt/start responses to include question asset data, not just `text`, `type`, and `options`.
- Normalize quiz and course-exam question payloads to the same learner-facing shape so both players use the same rendering contract.
- Keep `multi_select` behavior as the canonical multi-answer type for both quizzes and course exams; no alternate learner-only type mapping.
- Ensure submitted/passed/retry flows preserve compatibility with existing attempt/result handling.

### Learner assessment UI

- Extend `QuizQuestionView` so questions can render attached media/files in addition to the question text and options.
- Support both question asset roles:
  - `image` rendered inline above or near the prompt
  - `attachment` rendered as downloadable/openable supporting material
- Reuse the same enriched question renderer in both `QuizPlayer` and `CourseExamPlayer` so exams and quizzes stay visually/functionally aligned.
- Preserve current answer controls:
  - radio-style selection for `multiple_choice` and `true_false`
  - checkbox selection for `multi_select`

### Learn workspace parity

- Keep the current course exam section in `/courses/[id]/learn` as the learner entry point for exams.
- Ensure the learner workspace can consume the updated course/lesson/question asset DTOs without falling back to legacy-only fields.
- Continue treating lesson assets with `primary_video` as the playable video source and `resource` assets as learner resources; do not regress existing lesson resource rendering.

### Course detail and public learner surfaces

- Surface `courseLevelAssets` on the learner/public course detail page, likely in the overview/curriculum area rather than hiding them behind creator-only flows.
- Show these assets in a simple learner-facing format by type:
  - images previewable inline
  - files/links/video assets presented as clear open/download actions
- Keep previews/public detail read-only; no creator affordances leak into learner/public views.
- Do not broaden scope into creator curriculum UI changes unless a learner blocker is discovered.

## Public Interfaces / Data Contracts

- `GET/POST /api/v1/quizzes/[id]/start`
  - expand in-progress question payloads to include question assets
- `GET/POST /api/v1/course-exams/[id]/start`
  - expand in-progress question payloads to include question assets
- Shared learner question view model
  - should include `id`, `text`, `type`, `options`, and `assets`
- No schema redesign is planned today; use the existing `QuestionAssetDTO`, `CourseAssetDTO`, and current Prisma asset relations.

## Test Plan

- API tests for quiz start/status responses covering a question with:
  - no assets
  - one image asset
  - one attachment asset
  - `multi_select` options
- Equivalent API tests for course exam start/status responses.
- Component tests for `QuizQuestionView` verifying:
  - `multi_select` still works
  - image assets render
  - attachment assets render as actionable links/buttons
- Learner flow checks for:
  - quiz pass/fail/retry still works
  - course exam start/submit/retry still works
  - lesson video/resource rendering still works with asset-backed lessons
  - course detail page shows course-level assets without breaking existing tabs/layout

## Assumptions

- “Most of yesterday’s work needs to be reflected in today’s work” means learner parity, not new creator authoring features.
- Course exams stay a separate learner section after curriculum completion, matching the current `/learn` page behavior.
- `multi_select` is already the intended new question type; no new learner-side answer model is needed beyond wiring/parity.
- Course-level assets should be visible on learner-facing course detail surfaces, but not editable there.
- Existing legacy lesson resources remain supported as fallback, but asset-backed lesson/question data is the primary path going forward.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
