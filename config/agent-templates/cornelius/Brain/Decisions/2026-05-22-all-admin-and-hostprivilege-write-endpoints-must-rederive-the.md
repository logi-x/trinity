---
title: "All admin and host-privilege write endpoints must re-derive the user's role from the database on each request; JWT role "
date: "2026-05-22"
decision: "All admin and host-privilege write endpoints must re-derive the user's role from the database on each request; JWT role claims (`session.user.isAdmin`, `session.user.roles`) must not be trusted for au"
stakeholders: "Logix, Security"
review_by: "2026-08-22"
source: "[[Raw/sources/2026-05-22-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** All admin and host-privilege write endpoints must re-derive the user's role from the database on each request; JWT role claims (`session.user.isAdmin`, `session.user.roles`) must not be trusted for authorization.

**Rationale:** EXP-69/70/78 class. JWT tokens have up to 30-day validity; a revoked admin retains JWT claims until expiry. DB re-derivation is the only way to enforce immediate privilege revocation. Any route that gates on `session.user.isAdmin` without a DB check is a security vulnerability.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-22-experts-agent-digest.md]]
