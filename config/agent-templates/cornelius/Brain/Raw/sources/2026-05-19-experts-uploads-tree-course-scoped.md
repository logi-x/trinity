---
title: Experts — Course-Scoped Upload Tree Refactor (19 May 2026)
date: 2026-05-19
tags: [project/experts-app, session, storage, uploads, r2, refactor, courses, project/experts]
related:
  - "[[Raw/sources/2026-05-18-experts-schema-naming-and-asset-xor]]"
  - "[[Raw/guides/2026-05-18-schema-naming]]"
  - "[[Wiki/Concepts/Prisma]]"
---

# Course-Scoped Upload Tree Refactor

Third part of the schema-naming/asset cleanup arc. Schema rename + asset XOR landed on `refactor/schema-naming-course-prefix-20260518` (yesterday). This branch — `refactor/uploads-tree-course-scoped-20260518` — addresses the storage-layout half of the original conversation: course-related uploads were scattered across `uploads/course-assets/`, `uploads/module-assets/`, `uploads/lesson-content/`, `uploads/quiz/`, `uploads/quiz-questions/`, `uploads/exam-questions/`, with no way to enumerate "everything belonging to course X".

## Shipped (branch, unpushed)

| Commit     | Scope                                                              |
| ---------- | ------------------------------------------------------------------ |
| `8a111018` | uploads: course-scoped upload tree (`uploads/courses/<id>/...`)    |

Branched off `refactor/schema-naming-course-prefix-20260518` because the new path resolver depends on the renamed Prisma fields (`courseQuizQuestion.quizId`, `courseExamQuestion.examId`, `courseModule.courseId`) — push order: schema branch first, uploads branch second.

## New write paths

| Domain            | Old key                                  | New key                                                                |
| ----------------- | ---------------------------------------- | ---------------------------------------------------------------------- |
| `courses`         | `uploads/courses/<courseId>/<f>`         | `uploads/courses/<courseId>/<f>` (unchanged)                           |
| `course-assets`   | `uploads/course-assets/<courseId>/<f>`   | `uploads/courses/<courseId>/assets/<f>`                                |
| `module-assets`   | `uploads/module-assets/<moduleId>/<f>`   | `uploads/courses/<courseId>/modules/<moduleId>/<f>`                    |
| `lesson-content`  | `uploads/lesson-content/<lessonId>/<f>`  | `uploads/courses/<courseId>/lessons/<lessonId>/<f>`                    |
| `quiz`            | `uploads/quiz/<quizId>/<f>`              | `uploads/courses/<courseId>/quizzes/<quizId>/<f>`                      |
| `quiz-questions`  | `uploads/quiz-questions/<qId>/<f>`       | `uploads/courses/<courseId>/quizzes/<quizId>/questions/<qId>/<f>`      |
| `exam-questions`  | `uploads/exam-questions/<qId>/<f>`       | `uploads/courses/<courseId>/exams/<examId>/questions/<qId>/<f>`        |
| `community`       | `uploads/community/<entityId>/<f>`       | unchanged (not course-scoped)                                          |
| `draft-courses`   | `uploads/draft-courses/<userId>/<f>`     | unchanged (no course exists yet at upload time)                        |

## Key implementation decision

`authorizeDomainAccess` was already navigating the entity hierarchy to check ownership. Instead of adding a *second* query later just to resolve `courseId`, each branch was extended with a Prisma `select` that pulls the ancestor IDs *during the auth check*, then returns a fully-built `pathPrefix` string. The route became:

```ts
const key = `uploads/${authResult.pathPrefix}/${filename}`;
```

Zero extra DB roundtrips, path-building logic lives where the entity hierarchy is already known. This is a pattern worth reaching for whenever an auth function and a path/URL builder need the same ancestry — fold them.

## Backward compatibility

- Already-uploaded files at old keys remain untouched. Their stored URLs in `course_*_assets.url` / `Attachment` rows still resolve.
- **No fallback read logic in the codebase** — user (Ahmed) decided old files will be manually deleted or moved out-of-band rather than carry dual-read complexity in the download path.
- No DB backfill script.

## What was deliberately NOT done

- Renaming the `domain` form values (`module-assets`, `quiz-questions`, etc.) — they're still the contract between client uploaders and the route. Changing them is a separate, larger refactor touching every uploader component.
- Cleaning up `lesson-resources` test fixture strings in `upload-public-asset.command.test.ts` — already on the cosmetic-followup row from 2026-05-17. Kept commit focused on write-path behavior.

## Pending

- [ ] Push `refactor/schema-naming-course-prefix-20260518` then `refactor/uploads-tree-course-scoped-20260518` to origin (awaiting explicit "push now")
- [ ] Open two PRs (uploads PR stacks on schema PR)
- [ ] Out-of-band: manual file move / delete in R2 for old keys
- [ ] Optional follow-up: prep `aws s3` (or wrangler r2) snippets to assist the manual move — not in scope unless requested

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
