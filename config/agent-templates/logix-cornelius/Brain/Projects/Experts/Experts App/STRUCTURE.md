---
title: "Course domain notes (not full repo tree)"
date: "2026-04-11"
tags: ["project/experts", "topic/structure"]
category: "projects/experts"
up: "[[Entities/Projects/Experts App]]"
updated: "2026-07-15"
---

# Course domain notes (not full repo tree)

↑ [[Entities/Projects/Experts App|Experts App]]

This file captures **conventions and mental model for the courses subdomain** under `src/lib/courses/`. For the full monorepo layout, see [[Projects/Experts/DEVELOPER_GUIDE|Developer guide]].

---

lib/
├── courses/
│ ├── catalog/ // course as a product (done)
│ │ ├── commands/
│ │ ├── handlers/
│ │ ├── dto/
│ │ └── mappers/
│ ├── enrollments/ // access control (user ↔ course) (done)
│ ├── curriculum/ // modules & lessons (structure only) (pending)
│ ├── quizzes/ // assessment engine (pending)
│ ├── progress/ // learning state & resume (pending)
│ ├── certificates/ // outcome (pending)
│ └── shared/ // course-specific shared helpers (pending)

etc...

Suggested convention
File Responsibility
_.schema.ts Validation
_.command.ts Typed intent (interface/type)
_.handler.ts Domain logic
_.dto.ts Output shape
\*.types.ts Shared value objects

Data model (current)

- Course
  - Core: title, description, shortDescription, thumbnailUrl, level, duration
  - Pricing: price, isFree, processingEntityId
  - Visibility: isPublished, publishingStatus (draft | submitted | approved | rejected | published | archived)
  - Moderation: approvalStatus (draft | pending | approved | rejected), approvedById, approvedAt
  - Relations: category, instructors, modules, lessons, enrollments, certificates, lessonProgress
- CourseInstructor (pivot)
  - role (primary | co_instructor | contributor)
  - revenueShare, isVisible
- Module + Lesson
  - Ordered by position
  - Lesson has isFree, type, duration, videoUrl, content

Permissions (who can do what)

- Create draft
  - role: instructor (must exist in CourseInstructor as primary)
  - admin can create any course on behalf
- Update draft
  - primary instructor or admin
  - co_instructor can edit content but not pricing/status (if we want stricter rules)
- Submit for approval
  - primary instructor or admin
  - Sets publishingStatus = submitted, approvalStatus = pending
- Approve / Reject
  - admin only
  - Approve: approvalStatus = approved, publishingStatus = approved
  - Reject: approvalStatus = rejected, publishingStatus = rejected
- Publish
  - admin or primary instructor if auto-approval is allowed
  - Sets isPublished = true, publishingStatus = published
- Archive
  - admin or primary instructor
  - Sets publishingStatus = archived, isPublished = false
- Public read
  - Only published courses (isPublished = true, publishingStatus = published)
- Owner read
  - Any course where user is in CourseInstructor
