---
title: "`src/lib/config/app-url.ts` is the canonical app origin resolver; all code needing the app's public base URL must import"
date: "2026-05-30"
decision: "`src/lib/config/app-url.ts` is the canonical app origin resolver; all code needing the app's public base URL must import from this module. `getAppBaseUrl()` throws in production if `NEXT_PUBLIC_APP_UR"
stakeholders: "Logix"
review_by: "2026-08-30"
source: "[[Raw/sources/2026-05-28-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `src/lib/config/app-url.ts` is the canonical app origin resolver; all code needing the app's public base URL must import from this module. `getAppBaseUrl()` throws in production if `NEXT_PUBLIC_APP_URL` is absent (fail-closed). `getPublicBaseUrl()` returns `undefined` in SSG/build contexts. ESLint bans `staging.experts.com.sa` literal in `app/`and`src/lib/`.

**Rationale:** PR #665 closed the EXP-204 canonical-app-URL class (4 issues: EXP-204, 216, 217, 218). PR #643 (attempt 1) used an `APP_BASE_URL` fallback env var; this was rejected — any fallback permits misconfigured production builds to mint broken internal Docker hostnames silently. Throwing at first request surfaces the misconfiguration before downstream damage occurs. EXP-215 (`share-utils` getShareUrl staging fallback) was missed by the PR #665 sweep and remains open.

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-05-28-experts-agent-digest.md]]
