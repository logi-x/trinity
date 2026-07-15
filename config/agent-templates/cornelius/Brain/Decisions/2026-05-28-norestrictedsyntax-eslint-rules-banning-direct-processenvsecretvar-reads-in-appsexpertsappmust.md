---
title: "`no-restricted-syntax` ESLint rules banning direct `process.env.<SECRET_VAR>` reads in `apps/experts-app/`must be mainta"
date: "2026-05-28"
decision: "`no-restricted-syntax` ESLint rules banning direct `process.env.<SECRET_VAR>` reads in `apps/experts-app/`must be maintained; all runtime-secret reads must go through`runtime-secrets.ts` (file-based D"
stakeholders: "Logix"
review_by: "2026-08-28"
source: "[[Raw/sources/2026-05-28-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `no-restricted-syntax` ESLint rules banning direct `process.env.<SECRET_VAR>` reads in `apps/experts-app/`must be maintained; all runtime-secret reads must go through`runtime-secrets.ts` (file-based Docker secret hydration), not direct env access.\*\*

**Rationale:** PR #583 (EXP-168 ESLint guard). After the Docker secrets migration, direct `process.env.REDIS_PASSWORD` etc. reads break in production (the secret is not in the env, only at `/run/secrets/`). The lint rule catches drift at CI time, before it causes a silent runtime failure. New service secrets must add a corresponding `no-restricted-syntax` entry and a `runtime-secrets.ts` reader.

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-05-28-experts-agent-digest.md]]
