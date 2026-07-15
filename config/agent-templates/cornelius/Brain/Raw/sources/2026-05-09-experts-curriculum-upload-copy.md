---
title: "Experts Curriculum Upload Copy"
date: "2026-05-09"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts curriculum upload copy fix

Date: 2026-05-09

## Context

In `/creator/courses/[id]/curriculum`, uploading a PDF/document before a lesson exists could show "Add a lesson title before uploading a video." The same `ensureLessonForUpload` helper is shared by video uploads, lesson asset uploads, and lesson resource uploads.

## Change

Added an optional upload kind to `ensureLessonForUpload` so non-video upload flows pass `asset` and video upload flows pass `video`.

Updated non-video upload fallback copy in English, Arabic, and Spanish:

- English: "Save the lesson first before uploading a file."
- Arabic: "احفظ الدرس أولاً قبل رفع الملف."
- Spanish: "Guarda la lección antes de subir un archivo."

## Verification

- `pnpm typecheck:touched -- 'app/(i18n)/_shared/creator/courses/[id]/curriculum/logic/use-curriculum.ts' 'app/(i18n)/_shared/creator/courses/[id]/curriculum/sections/lesson-dialog.tsx' 'app/(i18n)/_shared/creator/courses/[id]/curriculum/sections/curriculum-builder-shell.tsx' src/i18n/messages/en/creator.json src/i18n/messages/ar/creator.json src/i18n/messages/es/creator.json`
- `npx gitnexus detect-changes -r experts`

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
