---
title: "EXP-108 — [spinoff: EXP-100] Subscription locale fallback when CF-IPCountry absent"
date: "2026-05-24"
status: resolved
resolution: "PR #463: when CF-IPCountry header is absent (direct-to-origin requests or non-Cloudflare traffic), the subscription locale resolver now falls back to the user's stored locale field rather than returning undefined."
tags: [bug, locale, subscriptions, cloudflare, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-108"
fingerprint: "agent-fp:R5-exp100-locale-fallback-001"
---

## Summary

After EXP-100, the subscription checkout locale resolver only read from `CF-IPCountry`. When the header was absent (e.g., internal health checks, staging direct-to-origin), locale resolved to `undefined`, breaking eligibility checks.

## Root cause

The EXP-100 fix removed the DB-write path but did not add a fallback for the header-absent case. The locale resolver became `CF-IPCountry || undefined` instead of `CF-IPCountry || user.locale`.

## Agent fingerprint

`<!-- agent-fp:R5-exp100-locale-fallback-001 -->`

## Status

Resolved — PR #463 merged 2026-05-24.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
