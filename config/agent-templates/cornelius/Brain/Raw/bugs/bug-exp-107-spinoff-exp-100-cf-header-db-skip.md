---
title: "EXP-107 — [spinoff: EXP-100] Route-level CF-IPCountry DB-write skip"
date: "2026-05-24"
status: resolved
resolution: "PR #462: added a route-level guard that detects CF-IPCountry in the incoming request and explicitly skips the locale DB-write path. Locale is now resolved from the stored user record only."
tags: [bug, security, cloudflare, locale, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-107"
fingerprint: "agent-fp:R5-exp100-cf-db-skip-001"
---

## Summary

After EXP-100 fixed the primary subscription checkout path, R5 identified that two additional routes still wrote `CF-IPCountry` to the user's locale field when processing authenticated requests. These routes were not covered by the EXP-100 PR.

## Root cause

The EXP-100 fix was applied to the checkout-eligibility route only. The CF-IPCountry write logic was duplicated in two other route handlers that were not audited in the original PR.

## Agent fingerprint

`<!-- agent-fp:R5-exp100-cf-db-skip-001 -->`

## Status

Resolved — PR #462 merged 2026-05-24.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
