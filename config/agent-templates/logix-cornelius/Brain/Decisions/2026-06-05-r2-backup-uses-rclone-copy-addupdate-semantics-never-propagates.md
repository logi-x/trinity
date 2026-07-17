---
title: "R2 backup uses `rclone copy` (add/update semantics, never propagates deletes) into `backups/YYYY-MM-DD/<bucket>/` dated "
date: "2026-06-05"
decision: "R2 backup uses `rclone copy` (add/update semantics, never propagates deletes) into `backups/YYYY-MM-DD/<bucket>/` dated prefixes. Backup is an opt-in `backup` compose profile, not a default service. ("
stakeholders: "Logix, Ops"
review_by: "2026-09-05"
source: "[[Raw/sources/2026-06-06-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** R2 backup uses `rclone copy` (add/update semantics, never propagates deletes) into `backups/YYYY-MM-DD/<bucket>/` dated prefixes. Backup is an opt-in `backup` compose profile, not a default service. (EXP-275, PR #864)

**Rationale:** R2 has no native object versioning or undelete. `rclone sync` would replicate deletes → a misconfig/leaked-credential delete on any day would erase prior backups. Dated-prefix isolation means each day is an independent snapshot; a bad day cannot corrupt past ones. Opt-in profile prevents accidental runs consuming credits/bandwidth.

**Stakeholders:** Logix, Ops

**Source:** [[Raw/sources/2026-06-06-experts-agent-digest.md]]
