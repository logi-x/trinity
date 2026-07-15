---
title: "The pending-first upload pattern (create `File` row with `status: \"pending\"` + `Attachment` in one `$transaction` BEFORE"
date: "2026-05-31"
decision: "The pending-first upload pattern (create `File` row with `status: \"pending\"` + `Attachment` in one `$transaction` BEFORE the R2 PUT; flip to `\"ready\"` after success) is now universal across all upload"
stakeholders: "Logix"
review_by: "2026-08-31"
source: "[[Raw/sources/2026-05-31-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** The pending-first upload pattern (create `File` row with `status: "pending"` + `Attachment` in one `$transaction` BEFORE the R2 PUT; flip to `"ready"` after success) is now universal across all upload routes. No route may perform an R2 PUT before its `File` row exists in DB.

**Rationale:** EXP-230 / PR #690 was the last of the original 5 PUT-first routes (identified in incident #5 remediation, 2026-05-14). Converting community-thumbnail and lesson-video closes the class. Any future upload route that writes to R2 must follow this pattern — the pending-first invariant is enforced structurally by code review and the storage-pending-reaper cron.

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-05-31-experts-agent-digest.md]]
