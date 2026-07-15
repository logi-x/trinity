---
title: "Experts Lesson Asset Upload Input"
date: "2026-04-21"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts lesson asset upload input

Date: 2026-04-21
Repo: `/home/logix/experts`
App: `apps/experts-app`

## Decision

Do not rename `src/components/ui/question-asset-uploader.tsx` into a global uploader.

Keep it dedicated to quiz/exam question attachments because that UI handles:

- multiple images and files
- attachment gallery/list rendering
- per-item remove/open/download controls

Lesson media needs a different contract:

- one primary asset URL/file per lesson type
- URL paste plus file upload
- no multi-attachment grid

## Implementation

Added a separate reusable component:

- `src/components/ui/single-asset-source-input.tsx`

It combines:

- URL field
- upload button
- drag-and-drop file zone via `AssetDropzone`

It is now used by lesson type forms for:

- PDF
- Audio
- Presentation

## Supporting change

`src/components/ui/asset-dropzone.tsx` now accepts an `accept` filter so lesson uploaders can restrict file kinds cleanly without affecting question attachments.

## Product behavior

Non-video lesson media now supports either:

- pasting a hosted URL
- uploading a file directly

Uploads reuse the existing lesson lazy-create flow, so creators can upload lesson assets before manually saving the lesson first.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
