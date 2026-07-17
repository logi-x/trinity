---
title: "All internal and admin cron routes must use `timingSafeCompareCronSecret` (constant-time comparison) and fail closed (re"
date: "2026-05-25"
decision: "All internal and admin cron routes must use `timingSafeCompareCronSecret` (constant-time comparison) and fail closed (return 401) when `CRON_SECRET` is absent or mismatched; `requireAdmin` fallback fo"
stakeholders: "Logix, Security"
review_by: "2026-08-25"
source: "[[Raw/sources/2026-05-25-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** All internal and admin cron routes must use `timingSafeCompareCronSecret` (constant-time comparison) and fail closed (return 401) when `CRON_SECRET` is absent or mismatched; `requireAdmin` fallback for missing secrets is prohibited.

**Rationale:** EXP-111/112/113/116/119 class. Plain `!==` comparison leaks secret length via timing side-channel; fail-open to `requireAdmin` when secret unset allows any admin to trigger mass R2 deletion or quota manipulation.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-25-experts-agent-digest.md]]
