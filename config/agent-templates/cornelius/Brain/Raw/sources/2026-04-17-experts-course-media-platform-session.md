---
title: "Experts — course media platform refactor and multi-asset curriculum follow-up"
date: "2026-04-17"
updated: "2026-04-17"
tags: ["project/experts", "topic/lms", "topic/assessments", "topic/storage", "source/session"]
category: "Raw/sources"
source: "generated"
source_id: "Raw/sources/2026-04-17-experts-course-media-platform-session.md"
---

# Experts — course media platform refactor and multi-asset curriculum follow-up

Session capture for `apps/experts-app` after implementing the course-domain media refactor and then fixing creator-side multi-upload behavior for question assets.

## What was done

### 1. Added a course-domain asset model

Implemented a new canonical media layer in Prisma:

- `CourseAsset`
- `LessonAsset`
- `QuizQuestionAsset`
- `CourseExamQuestionAsset`

Enums were added for:

- asset kind/source
- lesson asset role
- quiz question asset role
- course exam question asset role

This avoids keeping lesson video and question media trapped in one-off scalar URL fields.

### 2. Added migration + backfill

A Prisma migration was created to:

- add the new asset tables
- backfill lesson `videoUrl` into `LessonAsset(role=primary_video)`
- backfill `LessonResource` rows into `LessonAsset(role=resource)`
- backfill quiz question `imageUrl` / `fileUrl`
- backfill course exam question `imageUrl` / `fileUrl`

Legacy columns and `LessonResource` were intentionally kept in place for rollout compatibility.

### 3. Rewired lesson / quiz / exam write paths

Updated creator-domain handlers and routes so they now write the new asset relations while still tolerating legacy request and response shapes.

Scope included:

- lesson create/update/detail
- lesson resource create/update/delete syncing into `LessonAsset`
- quiz create/update + creator fetch
- course exam create/update + creator fetch

DTO/helper layer was added so asset mapping and legacy fallback logic are centralized.

### 4. Updated seed data to exercise the new model

`prisma/seeders/03-courses.ts` now seeds:

- course-level assets
- lesson primary video + additional lesson resource asset
- quiz questions with multiple assets
- course exams with multiple assets on questions

The seeder was adjusted so complex media rows are created after course/module/lesson records exist, which kept Prisma nested-create typing manageable.

### 5. Fixed creator multi-upload behavior

The actual `QuestionAssetUploader` component was not the problem. The bug was in creator dialog state:

- quiz and exam question forms still stored only `imageUrl` and `fileUrl`
- every upload replaced the previous URL

Fixed by changing creator question state to:

- `imageUrls: string[]`
- `fileUrls: string[]`

Upload handlers now append unique URLs, and remove handlers delete only the selected URL. API payload building still derives `assets[]` from those arrays and also preserves the first-item legacy fallback fields for compatibility.

## Verification completed

Focused verification only:

- `prisma format`
- `prisma generate`
- targeted helper test for asset normalization/fallback
- touched-file typechecks for the refactor slices
- touched-file typecheck for the updated course seeder

No full repo-wide test or typecheck gate was run in this session.

## What is still pending

### Rollout cleanup

- remove legacy response/request fallback fields once the migration has been exercised in a real environment and no consumers still depend on `imageUrl` / `fileUrl` / `videoUrl`
- eventually remove old schema columns and `LessonResource` once the new model is fully adopted

### Creator UX follow-up

- lesson editing still behaves like a single-primary-video UI even though the persistence layer now supports more flexible assets
- question asset UI now supports multiple uploads, but there is still no richer asset ordering or metadata editing UI

### Runtime confidence

- run the migration against a real seeded database and validate backfill counts/content
- run broader tests once unrelated repo-wide failures are under control

## Repo areas touched

- `apps/experts-app/prisma/schema.prisma`
- `apps/experts-app/prisma/migrations/20260417170000_add_course_media_platform/migration.sql`
- `apps/experts-app/src/lib/courses/assets/*`
- curriculum lesson / quiz / exam handlers and creator routes
- creator curriculum quiz/exam dialog state
- `apps/experts-app/prisma/seeders/03-courses.ts`

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
