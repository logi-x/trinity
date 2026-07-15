---
title: "External API client singletons (OpenAI and any client backed by runtime secrets) must use lazy initialization via a `get"
date: "2026-05-29"
decision: "External API client singletons (OpenAI and any client backed by runtime secrets) must use lazy initialization via a `getClient()`-style factory function; module-level instantiation that reads secrets "
stakeholders: "Platform, AI"
review_by: "2026-06-12"
source: "[[Raw/sources/2026-05-28-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** External API client singletons (OpenAI and any client backed by runtime secrets) must use lazy initialization via a `getClient()`-style factory function; module-level instantiation that reads secrets at import time is prohibited.

**Rationale:** PR #589: module-level `new OpenAI()` in `openai.ts` threw at `next build` because `OPENAI_SECRET` is absent from the build environment after the EXP-168 secret-file migration. `getOpenAI()` singleton defers construction to first call, keeping the build clean and the client reachable at runtime. All new AI/external-service integrations must follow the same factory pattern.

**Stakeholders:** Platform, AI

**Source:** [[Raw/sources/2026-05-28-experts-agent-digest.md]]
