---
title: "EXP-218: 14 metadata and modules files use staging URL fallback"
linear_id: "EXP-218"
agent_fp: "auto"
date: "2026-05-30"
severity: "Medium"
status: "resolved"
resolution: "PR #665 — sweep 14 files to getPublicBaseUrl() canonical resolver"
tags: [bug, url, config, seo, project/experts]
category: "bug"
source: "automation"
---

# EXP-218: 14 metadata/modules files staging URL fallback

**Linear:** [EXP-218](https://linear.app/experts/issue/EXP-218) | **Status:** Resolved (PR #665)

## Summary
14 files across `app/**/metadata.ts` and `app/**/modules.ts` used a staging URL fallback pattern for OG/canonical URL generation. All produced staging-pointing URLs in production when `NEXT_PUBLIC_APP_URL` was not set at build time.

## Fix
PR #665 swept all 14 files to use `getPublicBaseUrl()` from `src/lib/config/app-url.ts`.

## Related
- EXP-204, EXP-216, EXP-217 — same class

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
