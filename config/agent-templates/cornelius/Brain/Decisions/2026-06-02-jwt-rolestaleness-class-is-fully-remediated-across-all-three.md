---
title: "JWT role-staleness class is fully remediated across all three tiers (API routes, server helpers, RSC layouts); the per-r"
date: "2026-06-02"
decision: "JWT role-staleness class is fully remediated across all three tiers (API routes, server helpers, RSC layouts); the per-route DB patching posture established 2026-05-29 is now complete at the class lev"
stakeholders: "Security, Logix"
review_by: "2026-09-02"
source: "[[Raw/sources/2026-06-02-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** JWT role-staleness class is fully remediated across all three tiers (API routes, server helpers, RSC layouts); the per-route DB patching posture established 2026-05-29 is now complete at the class level. The `jwtRoleSelectors` ESLint rule covers `app/api//route.ts`, `src/lib/`, and `app//\*.ts(x)`.\*\*

**Rationale:** EXP-241 sweep closed after 4 gatekeeper attempts (PRs #756, #757). ~30 route files, ~18 RSC layout/page files, 2 server helpers covered. CI lint now prevents regression.

**Stakeholders:** Security, Logix

**Source:** [[Raw/sources/2026-06-02-experts-agent-digest.md]]
