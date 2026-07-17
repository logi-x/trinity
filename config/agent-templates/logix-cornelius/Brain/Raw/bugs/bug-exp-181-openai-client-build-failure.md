---
title: "EXP-181: App image build fails — module-level OpenAI client throws when OPENAI_SECRET absent"
linear_id: "EXP-181"
agent_fp: "manual-exp181"
date: "2026-05-29"
severity: "Urgent"
status: "resolved"
resolution: "merged PR #589 — lazy getOpenAI() singleton"
tags: [bug, ai, build, project/experts]
category: "bug"
source: "automation"
---

# EXP-181: Module-level OpenAI client breaks build

**Linear:** [EXP-181](https://linear.app/experts/issue/EXP-181) | **Fingerprint:** `manual-exp181`

## Summary
The app Docker image build (`pnpm build`) failed during Next.js page-data collection because `embedding-sync.service.ts` instantiated `new OpenAI()` at module level. After the EXP-168 secret-file migration, `OPENAI_SECRET` is no longer available at build time, causing an immediate throw that blocked the build.

## Fix
PR #589: module-level `new OpenAI()` replaced with a lazy `getOpenAI()` singleton that defers construction to first call. Build no longer requires `OPENAI_SECRET` in the build environment.

## Related
EXP-168 (Docker secrets migration)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
