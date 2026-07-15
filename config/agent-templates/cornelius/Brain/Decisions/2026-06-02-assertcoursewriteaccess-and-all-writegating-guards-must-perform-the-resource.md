---
title: "`assertCourseWriteAccess` and all write-gating guards must perform the resource ownership DB query regardless of `isAdmi"
date: "2026-06-02"
decision: "`assertCourseWriteAccess` and all write-gating guards must perform the resource ownership DB query regardless of `isAdmin` flag; bare admin-bypass returning `{ok: true}` before ownership check is proh"
stakeholders: "Security, Logix"
review_by: "2026-09-02"
source: "[[Raw/sources/2026-06-02-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `assertCourseWriteAccess` and all write-gating guards must perform the resource ownership DB query regardless of `isAdmin` flag; bare admin-bypass returning `{ok: true}` before ownership check is prohibited. Admin access grants management privilege but not implicit write ownership over arbitrary resources.

**Rationale:** EXP-284. `if (isAdmin) return {ok:true}` in `course-access.guard.ts` skips the `courseInstructor` DB query entirely — any admin can force-submit any instructor's course. Fix must query ownership first; admins may have a separate management bypass only with explicit audit logging. Distinct from the JWT-staleness class (EXP-241): `isAdmin` IS DB-fresh here; the ownership DB query is simply skipped.

**Stakeholders:** Security, Logix

**Source:** [[Raw/sources/2026-06-02-experts-agent-digest.md]]
