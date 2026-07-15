---
title: "ZATCA debug and force-fail flags (`DEBUG_ZATCA`, `ZATCA_FORCE_REPORT_FAIL`, `ZATCA_FORCE_SIGN_FAIL`) must be scoped to n"
date: "2026-05-26"
decision: "ZATCA debug and force-fail flags (`DEBUG_ZATCA`, `ZATCA_FORCE_REPORT_FAIL`, `ZATCA_FORCE_SIGN_FAIL`) must be scoped to non-production environments; any of these flags active in production is a misconf"
stakeholders: "Logix, Compliance"
review_by: "2026-08-26"
source: "[[Raw/sources/2026-05-26-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** ZATCA debug and force-fail flags (`DEBUG_ZATCA`, `ZATCA_FORCE_REPORT_FAIL`, `ZATCA_FORCE_SIGN_FAIL`) must be scoped to non-production environments; any of these flags active in production is a misconfiguration that must be surfaced at startup.

**Rationale:** EXP-140/EXP-142. `ZATCA_FORCE_REPORT_FAIL=true` in production silently suppresses all government invoice reporting — a compliance violation with immediate legal consequences. The flag was keyed off the global `DEBUG` env var, which can be set for unrelated reasons.

**Stakeholders:** Logix, Compliance

**Source:** [[Raw/sources/2026-05-26-experts-agent-digest.md]]
