---
title: "Experts Protected Attachment Delivery Route"
date: "2026-04-21"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts protected attachment delivery route

Date: 2026-04-21
Repo: `/home/logix/experts`
App: `apps/experts-app`

## Summary

Implemented the first app-controlled delivery layer for uploaded course attachments.

Instead of exposing raw storage URLs directly for uploaded assets, DTO mappers now emit:

- `/api/v1/attachments/:id/content`

That route:

- authenticates when needed
- checks whether the requester may access any course asset linked to the attachment
- redirects to a short-lived signed R2 URL

## Shipped files

- `app/api/v1/attachments/[id]/content/route.ts`
- `src/lib/storage/attachments/attachment-access.ts`
- `src/lib/storage/attachments/attachment-content-url.ts`
- `src/lib/courses/assets/course-asset.helpers.ts`
- `src/lib/courses/curriculum/lessons/mappers/lesson.mapper.ts`
- `app/api/v1/attachments/[id]/content/__tests__/route.test.ts`

## Current access rules

- admin: allowed
- course instructor for the linked course: allowed
- learner with completed enrollment for the linked course: allowed
- anonymous users: denied by default

Exception kept intentionally for compatibility:

- published course-level assets remain anonymously accessible through the route
- this preserves public course detail/media behavior while moving uploaded lesson/question assets behind app checks

## Current scope

Covered automatically by mapper URL rewriting when the asset has `attachmentId`:

- course assets
- lesson primary uploaded assets
- lesson uploaded resources
- quiz question assets
- exam question assets

Not changed yet:

- storage privacy itself; uploaded files may still live in a public/static bucket
- legacy fields that only store raw URLs without attachment-backed records
- stricter lesson-level gating like free-preview exceptions

## Why this shape

Used `auth check -> signed redirect` instead of full proxy streaming because it:

- keeps authorization in the app
- avoids serving large files through Next route handlers
- gives a clean migration path toward private buckets later

## Follow-up

- move protected uploads to a private course bucket
- tighten rules for course-level assets if product decides they should no longer be public on published course pages
- add richer gating for free lessons / preview rules if needed

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
