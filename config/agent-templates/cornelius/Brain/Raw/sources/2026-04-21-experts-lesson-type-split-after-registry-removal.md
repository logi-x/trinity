---
title: "Experts Lesson Type Split After Registry Removal"
date: "2026-04-21"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts lesson-type split after registry removal

Date: 2026-04-21
Repo: `/home/logix/experts`
App: `apps/experts-app`

## Decision

`src/lib/courses/curriculum/lessons/registry.ts` should not be revived.

The lesson system no longer benefits from a registry abstraction because:

- quizzes and exams are separate curriculum items, not lesson-type plugins
- the active editor and learner flows already branch directly in the main surfaces
- leaving an unused registry creates misleading architecture with no runtime value

## Chosen direction

Keep direct per-type implementations for lesson content, with explicit handling for:

- `video`
- `text`
- `pdf`
- `audio`
- `presentation`

`text`, `pdf`, `audio`, and `presentation` should no longer be treated as one generic "text-like" implementation.

## Implemented in this session

Authoring components were split into distinct lesson-type forms:

- `src/lib/courses/curriculum/lessons/lesson-types/text/text.form.tsx`
- `src/lib/courses/curriculum/lessons/lesson-types/pdf/pdf.form.tsx`
- `src/lib/courses/curriculum/lessons/lesson-types/audio/audio.form.tsx`
- `src/lib/courses/curriculum/lessons/lesson-types/presentation/presentation.form.tsx`

Learner components were split into distinct lesson-type renderers:

- `src/lib/courses/curriculum/lessons/lesson-types/text/text.renderer.tsx`
- `src/lib/courses/curriculum/lessons/lesson-types/pdf/pdf.renderer.tsx`
- `src/lib/courses/curriculum/lessons/lesson-types/audio/audio.renderer.tsx`
- `src/lib/courses/curriculum/lessons/lesson-types/presentation/presentation.renderer.tsx`

Active app surfaces now use explicit lesson-type branches instead of a generic fallback:

- creator editor:
  `app/(i18n)/_shared/creator/courses/[id]/curriculum/sections/lesson-dialog.tsx`
- learner player:
  `app/(i18n)/_shared/courses/[id]/learn/sections/lesson-player.tsx`

Translations were extended so each lesson type has its own labels and empty states in:

- `src/i18n/messages/{en,ar,es}/creator/courses.ts`
- `src/i18n/messages/{en,ar,es}/courses/learn.ts`

## Practical model going forward

- `video` stays media-first with upload/probe/completion logic
- `text` stays markdown-first
- `pdf` is document-first with notes below
- `audio` is audio-first with recording/playback plus notes
- `presentation` is deck-first with embedded slides plus notes

If a future abstraction is needed, it should be designed around the shipped surfaces, not around the old lesson registry concept.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
