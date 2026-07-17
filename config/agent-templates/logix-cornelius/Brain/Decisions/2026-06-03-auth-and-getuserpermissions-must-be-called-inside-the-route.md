---
title: "`auth()` and `getUserPermissions()` must be called inside the route handler's outermost `try` block, not before it; any "
date: "2026-06-03"
decision: "`auth()` and `getUserPermissions()` must be called inside the route handler's outermost `try` block, not before it; any throwable call outside the try block bypasses `safeErrorJson` and can expose raw"
stakeholders: "Logix, Security"
review_by: "2026-09-03"
source: "[[Raw/sources/2026-06-03-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `auth()` and `getUserPermissions()` must be called inside the route handler's outermost `try` block, not before it; any throwable call outside the try block bypasses `safeErrorJson` and can expose raw framework errors on a degraded-auth event. Enforced by a new ESLint `no-auth-before-try` rule scoped to `app/api//route.ts`.\*\*

**Rationale:** EXP-293 generalizes EXP-287 (seed, fixed PR #792). The `safeErrorJson` choke point (betweenness 0.237, 269 edges) only protects code it wraps. The safeErrorJson god-node audit (`graphify-out/safeErrorJson-audit.md`) found 37 such handlers. The lint rule prevents regression. Defense-in-depth class (0 confirmed live leaks with current infrastructure), not 37 individual vulnerabilities.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-06-03-experts-agent-digest.md]]
