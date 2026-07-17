---
title: "All domain-specific route handlers must resolve actor permissions via a DB-authoritative helper (e.g. `getDbCommunityAct"
date: "2026-05-31"
decision: "All domain-specific route handlers must resolve actor permissions via a DB-authoritative helper (e.g. `getDbCommunityActor` for community routes), never from JWT claims alone. Each domain should have "
stakeholders: "Security / Logix / Backend"
review_by: "2026-08-31"
source: "[[Raw/sources/2026-05-31-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** All domain-specific route handlers must resolve actor permissions via a DB-authoritative helper (e.g. `getDbCommunityActor` for community routes), never from JWT claims alone. Each domain should have its own canonical actor-resolution helper.

**Rationale:** EXP-241: JWT role-staleness confirmed in community routes. The `getDbCourseActor` helper (2026-05-30 decision) is course-scoped; community routes lack an equivalent. Establishing the domain-actor pattern per namespace prevents recurring security gaps as new route domains are added.

**Stakeholders:** Security / Logix / Backend

**Source:** [[Raw/sources/2026-05-31-experts-agent-digest.md]]
