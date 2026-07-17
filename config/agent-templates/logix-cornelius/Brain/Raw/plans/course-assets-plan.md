---
title: "Course Assets Plan"
date: "2026-04-17"
tags: [plan, project/experts]
category: "plan"
---

# Course Media Platform Refactor

## Summary

Yes, this is doable. For the "course media platform" goal, it is better than keeping `imageUrl` / `fileUrl` / `videoUrl` scalars, but not as a single overloaded `CourseResource` table that directly replaces everything.

Recommended direction:

- introduce a canonical course-scoped asset record for uploaded/external media
- attach that asset to lessons and questions through owner-specific join tables
- keep lesson primary video as a role on the lesson attachment, not as a special scalar column
- migrate quiz/exam questions from `imageUrl` / `fileUrl` to ordered asset lists

This gives you dynamic uploads, removes the one-video-per-lesson constraint, and avoids turning one table into a polymorphic catch-all with mixed invariants.

## Key Changes

### Data model

Use `CourseAsset` as the canonical media record, not `CourseResource`.
Reason:

- "asset" fits video, image, file, and link
- "resource" is still useful as a lesson/question usage role, but it is too narrow for all media

Add:

- `CourseAsset`
  - `id`, `courseId`
  - `kind`: `image | file | video | link`
  - `source`: `upload | external`
  - `url`
  - `fileId?` or `attachmentId?` for uploaded assets
  - `mimeType?`, `size?`, `title?`
  - `createdAt`, `updatedAt`
- `LessonAsset`
  - `lessonId`, `assetId`
  - `role`: `primary_video | resource`
  - `position`
  - `title?`
  - `isDownloadable?`
- `QuizQuestionAsset`
  - `questionId`, `assetId`
  - `role`: `image | attachment`
  - `position`
- `CourseExamQuestionAsset`
  - `questionId`, `assetId`
  - `role`: `image | attachment`
  - `position`

Keep `LessonResource`, `Lesson.videoUrl`, `QuizQuestion.imageUrl/fileUrl`, and `CourseExamQuestion.imageUrl/fileUrl` temporarily during rollout only.

### Why not one monolithic `CourseResource`

Do not model this as one table with `ownerType + ownerId` for everything.
Reason:

- lesson primary video and lesson downloadable resource have different behavior
- question assets are ordered and constrained differently
- Prisma and validation stay much clearer with explicit relations
- owner-specific joins are easier to query, validate, and migrate safely

### API and DTO changes

Move question payloads from:

- `imageUrl?: string | null`
- `fileUrl?: string | null`

to:

- `assets?: Array<{ id?: string; url: string; kind: "image" | "file"; mimeType?: string | null; position: number }>`

Move lesson payloads from:

- `videoUrl?: string | null`
- `resources?: LessonResourceDTO[]`

to:

- `assets?: Array<{ id?: string; url: string; kind: "video" | "file" | "link"; role: "primary_video" | "resource"; title?: string | null; isDownloadable?: boolean; position: number }>`

UI defaults:

- keep the unified `QuestionAssetUploader`
- keep `quiz-dialog` and `exam-dialog` constrained to `maxImages=1` and `maxFiles=1` for now
- the component stays general-case; limits become data/config, not schema-driven

### Rollout strategy

1. Add new tables and relations without removing legacy columns.
2. Backfill:
   - `Lesson.videoUrl` -> `CourseAsset(kind=video)` + `LessonAsset(role=primary_video)`
   - `LessonResource` rows -> `CourseAsset(kind=file|link)` + `LessonAsset(role=resource)`
   - `QuizQuestion.imageUrl/fileUrl` -> `QuizQuestionAsset`
   - `CourseExamQuestion.imageUrl/fileUrl` -> `CourseExamQuestionAsset`
3. Update read paths to prefer new relations and fall back to legacy columns if no assets exist.
4. Update create/update handlers and Zod schemas to write only the new model.
5. Update curriculum state and DTO mappers to expose asset arrays.
6. After one full release and verified backfill, remove legacy columns/tables.

## Test Plan

- Prisma migration test: backfill creates the correct asset and join rows for existing lessons, quiz questions, and exam questions.
- Lesson read/write tests: primary video and supplemental resources round-trip through the new relations.
- Quiz/exam create/update tests: ordered asset arrays persist correctly and replace the old scalar behavior.
- Compatibility tests: legacy rows still read correctly before cleanup.
- UI tests:
  - unified dropzone routes images vs non-images correctly
  - `maxImages` / `maxFiles` still constrain quiz/exam dialogs
  - removing one asset does not affect the others

## Assumptions

- Uploaded files should continue using the existing `file` / `attachment` pipeline; `CourseAsset` is the course-domain wrapper, not a replacement for storage metadata.
- Links remain first-class assets, not uploads.
- For v1 of this refactor, quiz/exam question roles remain `image` and `attachment`; no mixed arbitrary roles yet.
- For v1 rollout, lesson primary video remains a single logical slot in the UI even though the schema no longer hardcodes that restriction.
- Naming default is `CourseAsset`; if you strongly want `CourseResource`, keep that name only if you also accept that it now means "any course media", not just downloadable resources.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
