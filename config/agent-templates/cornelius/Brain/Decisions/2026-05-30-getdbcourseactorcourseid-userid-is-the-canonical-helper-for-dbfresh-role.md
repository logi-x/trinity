---
title: "`getDbCourseActor(courseId, userId)` is the canonical helper for DB-fresh role lookup on course routes; inline `db.user."
date: "2026-05-30"
decision: "`getDbCourseActor(courseId, userId)` is the canonical helper for DB-fresh role lookup on course routes; inline `db.user.findUnique` role checks within course handlers are prohibited."
stakeholders: "Logix"
review_by: "2026-08-30"
source: "[[Raw/sources/2026-05-28-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `getDbCourseActor(courseId, userId)` is the canonical helper for DB-fresh role lookup on course routes; inline `db.user.findUnique` role checks within course handlers are prohibited.

**Rationale:** PR #658 introduced the shared helper to resolve EXP-197/199 (JWT staleness on course curriculum and lifecycle routes). Centralizes the DB query and the actor shape; prevents individual handlers from independently implementing subtly different privilege checks. All new course route handlers must call `getDbCourseActor` rather than inline the DB check.

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-05-28-experts-agent-digest.md]]
