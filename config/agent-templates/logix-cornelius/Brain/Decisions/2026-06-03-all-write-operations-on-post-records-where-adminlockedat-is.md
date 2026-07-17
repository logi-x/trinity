---
title: "All write operations on `Post` records where `adminLockedAt IS NOT NULL` must verify the lock inside a database transact"
date: "2026-06-03"
decision: "All write operations on `Post` records where `adminLockedAt IS NOT NULL` must verify the lock inside a database transaction; a bare `findUnique` + `update` split is a TOCTOU vulnerability exploitable "
stakeholders: "Logix, Security"
review_by: "2026-09-03"
source: "[[Raw/sources/2026-06-03-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** All write operations on `Post` records where `adminLockedAt IS NOT NULL` must verify the lock inside a database transaction; a bare `findUnique` + `update` split is a TOCTOU vulnerability exploitable with concurrent requests. The correct atomic pattern is `prisma.post.update({ where: { id, adminLockedAt: null }, data: ... })`, which pushes the predicate into the DB UPDATE WHERE clause.

**Rationale:** EXP-295/296/297. PR #792 added `adminLockedAt` for admin content governance but only guarded the PUT `isPublished` path with a pre-fetch read-check-write pattern. EXP-295: DELETE has no lock check at all (100% reproducible, 1 request). EXP-296: PUT is exploitable ~65% of the time with 10 concurrent requests. EXP-297: thumbnail POST has a 50–200ms race window during `arrayBuffer()` processing. The atomic WHERE-predicate fix closes all three cases without a Prisma `$transaction` wrapper.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-06-03-experts-agent-digest.md]]
