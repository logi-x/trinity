---
title: "EXP-216: getSitemapBaseUrl() uses X-Forwarded-Host header — host spoofing risk"
linear_id: "EXP-216"
agent_fp: "auto"
date: "2026-05-30"
severity: "Medium"
status: "resolved"
resolution: "PR #665 — use getPublicBaseUrl() from canonical resolver"
tags: [bug, url, security, seo, project/experts]
category: "bug"
source: "automation"
---

# EXP-216: getSitemapBaseUrl X-Forwarded-Host spoofing

**Linear:** [EXP-216](https://linear.app/experts/issue/EXP-216) | **Status:** Resolved (PR #665)

## Summary
`getSitemapBaseUrl()` derived the sitemap base URL from the `X-Forwarded-Host` request header. In environments where Cloudflare is not the only path to the origin, this header can be spoofed, causing the sitemap to reference attacker-controlled hostnames.

## Fix
PR #665 replaced the `X-Forwarded-Host` derivation with a call to `getPublicBaseUrl()` from `src/lib/config/app-url.ts`, which uses the build-time `NEXT_PUBLIC_APP_URL` env var.

## Related
- EXP-204, EXP-217, EXP-218 — same canonical-app-URL class

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
