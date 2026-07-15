---
title: "Experts Lesson Resources Lazy Create"
date: "2026-04-21"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts lesson resources lazy-create fix

Date: 2026-04-21
Repo: `/home/logix/experts`
App: `apps/experts-app`

## Problem

In the creator curriculum editor, lesson resources could only be listed/added/removed after a lesson had already been created and saved.

This felt inconsistent because media upload paths already used `ensureLessonForUpload(...)` to lazily create the lesson during lesson creation.

## Cause

The restriction was mostly a UI gate, not a unique backend product rule:

- the resource panel was only rendered when `editingLesson` existed
- resource API routes are lesson-scoped (`/lessons/[lessonId]/resources`) and therefore need a persisted lesson id
- because the panel was hidden for unsaved lessons, creators were forced into an unnecessary save-first step

## Fix

The resource panel now renders during lesson creation as well.

When the creator adds the first resource while no persisted lesson exists yet, the panel calls the existing lazy-create flow (`ensureLessonForUpload(true)`) first, then posts the resource to the lesson-scoped resource endpoint.

## Decision

Lesson resources should follow the same lazy-create model as lesson media uploads:

- creator can begin resource work before explicitly saving
- first resource add creates the lesson record if needed
- resource listing/deleting still remain lesson-scoped after that lesson exists

This keeps the backend model intact while removing the misleading creator UX.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
