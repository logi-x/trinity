---
title: "`File.bucket` is the source of truth for which R2 bucket a file object lives in; all delete, sweep, and cleanup operatio"
date: "2026-05-27"
decision: "`File.bucket` is the source of truth for which R2 bucket a file object lives in; all delete, sweep, and cleanup operations must use `File.bucket` to route the R2 `DeleteObjectCommand` — hardcoded buck"
stakeholders: "Logix"
review_by: "2026-08-27"
source: "[[Raw/sources/2026-05-28-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `File.bucket` is the source of truth for which R2 bucket a file object lives in; all delete, sweep, and cleanup operations must use `File.bucket` to route the R2 `DeleteObjectCommand` — hardcoded bucket names are prohibited.

**Rationale:** EXP-145/EXP-146. After the EXP-77 origin split, objects are distributed across at least three buckets (`user-uploads`, `media`, `certifications`). Hardcoded bucket names in sweep/delete paths silently 404 on cross-bucket objects, leaving orphans and inflating quota.

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-05-28-experts-agent-digest.md]]
