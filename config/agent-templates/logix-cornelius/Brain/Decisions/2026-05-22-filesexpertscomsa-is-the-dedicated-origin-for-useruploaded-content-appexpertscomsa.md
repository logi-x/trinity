---
title: "`files.experts.com.sa` is the dedicated origin for user-uploaded content; `app.experts.com.sa` serves only app routes an"
date: "2026-05-22"
decision: "`files.experts.com.sa` is the dedicated origin for user-uploaded content; `app.experts.com.sa` serves only app routes and static assets. All R2 user-upload URLs must use the `files.*` origin. CSP `img"
stakeholders: "Logix, Security"
review_by: "2026-08-22"
source: "[[Raw/sources/2026-05-22-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `files.experts.com.sa` is the dedicated origin for user-uploaded content; `app.experts.com.sa` serves only app routes and static assets. All R2 user-upload URLs must use the `files.*` origin. CSP `img-src` and `media-src` must include `files.experts.com.sa` and exclude legacy `*.r2.dev` paths.

**Rationale:** EXP-77 origin split shipped via PR #454. Mixed origins (app + files) created CSP violations and CDN key collisions.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-22-experts-agent-digest.md]]
