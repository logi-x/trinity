---
title: "Storage quota enforcement is a hard gate, not a soft warning; all R2-write routes must call `enforceStorageQuota` before"
date: "2026-05-23"
decision: "Storage quota enforcement is a hard gate, not a soft warning; all R2-write routes must call `enforceStorageQuota` before accepting upload data."
stakeholders: "Logix, Security"
review_by: "2026-08-23"
source: "[[Raw/sources/2026-05-23-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Storage quota enforcement is a hard gate, not a soft warning; all R2-write routes must call `enforceStorageQuota` before accepting upload data.

**Rationale:** EXP-72/EXP-86. Quota without enforcement is advisory only; users can bypass it by racing the check. Rate-limit before formData parse to prevent bandwidth waste on over-quota requests.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-23-experts-agent-digest.md]]
