---
title: "Experts Unified Asset Source Tabs"
date: "2026-04-21"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts asset upload UX unified across curriculum surfaces

Date: 2026-04-21
Repo: `/home/logix/experts`
App: `apps/experts-app`

## Decision

Standardized creator-side asset input UX around one tabbed interaction model:

- `Upload`
- `Paste URL`
- optional `Record` for audio-only cases

`Upload` is the default selected tab.

## Applied To

- course-level assets in curriculum
- per-lesson resources
- single primary asset inputs for lesson types
- per-question assets in quizzes and course exams

## Implementation Notes

- Added shared UI shell: `src/components/ui/asset-source-tabs.tsx`
- Refactored `single-asset-source-input.tsx` to use the shared tabs
- Audio lessons now use the same shell with a third `Record` tab
- Course materials now use the same tabbed model instead of separate `Add link` and `Upload` buttons
- Lesson resources now support both upload and URL flows in the same panel
- Quiz/exam question attachments now support pasted URLs in addition to uploads

## Current Storage Reality

This change only unified the UX and upload entry points. It did not change storage/access control:

- uploads still go through `/api/v1/internal/upload`
- files are still stored in the public static R2 bucket
- stronger access control remains a later architecture task

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
