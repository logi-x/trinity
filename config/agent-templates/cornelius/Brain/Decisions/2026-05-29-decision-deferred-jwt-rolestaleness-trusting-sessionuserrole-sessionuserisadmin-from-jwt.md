---
title: "Decision deferred: JWT role-staleness (trusting `session.user.role` / `session.user.isAdmin` from JWT without DB re-deri"
date: "2026-05-29"
decision: "Decision deferred: JWT role-staleness (trusting `session.user.role` / `session.user.isAdmin` from JWT without DB re-derivation) remains unaddressed at the infrastructure or middleware level; per-route"
stakeholders: "Security, Auth"
review_by: "2026-06-05"
source: "[[Raw/sources/2026-05-28-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Decision deferred: JWT role-staleness (trusting `session.user.role` / `session.user.isAdmin` from JWT without DB re-derivation) remains unaddressed at the infrastructure or middleware level; per-route `db.user.findUnique` patching continues until a middleware-layer DB role-resolution solution is scheduled.

**Rationale:** 11 confirmed instances in 30 days (EXP-69/70/78/79/88/89/90/91/93/88/89 and related); PR #619 course-lifecycle expansion immediately generated 3 more spinoffs (EXP-197/198/199). Cost of structural fix (e.g. `auth()` wrapper that enriches session with live DB role on every protected request) is high — requires refactoring all `getServerSession` call sites — and no sprint is scheduled. Per-route patching is the accepted interim posture; each new route touching admin/instructor privilege must add its own DB check.

**Stakeholders:** Security, Auth

**Source:** [[Raw/sources/2026-05-28-experts-agent-digest.md]]
