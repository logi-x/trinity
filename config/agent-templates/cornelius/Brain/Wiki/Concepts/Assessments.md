---
title: "Assessments"
date: "2026-04-17"
updated: "2026-04-17"
tags: ["entity", "topic", "lms", "assessments"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Assessments.md"
---

# Assessments

## Experts app

### 2026-04-17 — `multi_select` question type

- `multi_select` is now the next supported assessment question type after `multiple_choice` and `true_false`.
- Quiz and course exam attempt answers store one row per selected option instead of assuming a single `optionId` per question.
- Grading for `multi_select` is strict exact-set matching in v1:
  the learner only gets credit when the selected option set exactly equals the correct option set.
- Submit APIs remain backward-compatible with the existing single-select payload shape by accepting `optionId` and normalizing it to `optionIds[]`.
- Creator validation requires at least 2 correct options for `multi_select`.

### 2026-04-17 — course media platform refactor for assessments

- Quiz questions and course exam questions now persist media through a shared course-domain asset model instead of treating media as only `imageUrl` / `fileUrl` scalars.
- New Prisma relations were added in `apps/experts-app`:
  - `CourseAsset`
  - `LessonAsset`
  - `QuizQuestionAsset`
  - `CourseExamQuestionAsset`
- Backfill migration logic was added so legacy lesson video, lesson resources, quiz question media, and course exam question media can populate the new asset tables without removing the old columns yet.
- Creator read/write paths for quizzes and exams now write the new asset relations while still returning legacy `imageUrl` / `fileUrl` fallbacks for compatibility.
- Lesson primary video is now also represented as a lesson asset (`primary_video`) and lesson resources are mirrored into `LessonAsset(role=resource)`.
- Seed data was updated to exercise the new model with:
  - course-level assets
  - lesson multi-assets
  - quiz-question multi-assets
  - course exams with multi-asset questions
- Creator quiz/exam authoring now keeps question media in `imageUrls[]` / `fileUrls[]` client state, so `QuestionAssetUploader` can append multiple uploads instead of replacing the previous item when `maxImages` / `maxFiles` are raised.

### Pending follow-up after the media refactor

- The API and DTO layer still carries first-item legacy fallbacks (`imageUrl` / `fileUrl`) for compatibility; these can be removed after one clean release and migration confidence.
- Lesson editing UX still exposes a single logical primary video slot even though persistence now supports more flexible lesson assets.
- Dedicated UI for browsing/reordering all question assets is still minimal; current creator dialogs now support multiple uploads, but they do not yet expose richer per-asset metadata or ordering controls.
- Full repo-wide verification and live migration execution were not completed in the implementation session; only focused generation, tests, and touched-file typechecks were run.
