---
title: "Postgres environment version parity is required; staging must run the same major version as production. Staging was sile"
date: "2026-06-01"
decision: "Postgres environment version parity is required; staging must run the same major version as production. Staging was silently running pg18 while production ran pg16 (PR #714 corrected staging to pg16; "
stakeholders: "Infra, Backend"
review_by: "2026-06-15"
source: "[[Raw/sources/2026-06-01-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Postgres environment version parity is required; staging must run the same major version as production. Staging was silently running pg18 while production ran pg16 (PR #714 corrected staging to pg16; PR #724 subsequently moved all envs to pg18 together). Any future major version upgrade must be applied to staging first, validated, then applied to production — never unilaterally to one env.

**Rationale:** Silent staging-to-prod version drift made staging an unintended pg18 canary; pg18+pgvector is untested at production scale and was a candidate cause of staging DB connection drops.

**Stakeholders:** Infra, Backend

**Source:** [[Raw/sources/2026-06-01-experts-agent-digest.md]]
