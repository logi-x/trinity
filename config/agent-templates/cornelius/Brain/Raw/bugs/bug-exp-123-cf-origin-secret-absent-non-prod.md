---
title: "EXP-123: CF_ORIGIN_SECRET absent on non-prod — trusts all cf-ipcountry headers"
linear_id: "EXP-123"
agent_fp: "453fb1cbfad9"
date: "2026-05-25"
severity: "Medium"
status: "Todo"
tags: [bug, security, cloudflare, geo-restriction, project/experts]
category: "bug"
source: "automation"
---

# EXP-123: CF_ORIGIN_SECRET absent on non-prod — trusts all cf-ipcountry headers

**Linear:** EXP-123 | **Fingerprint:** `<!-- agent-fp: 453fb1cbfad9 -->` | **Severity: Medium**

## Summary

The Cloudflare origin verification pattern (introduced with EXP-100 fix) uses `CF_ORIGIN_SECRET` to validate that the `cf-ipcountry` header comes from a real Cloudflare edge node and not from a spoofed header. On non-prod environments (staging, dev, e2e) where `CF_ORIGIN_SECRET` is absent, the code falls back to trusting all `cf-ipcountry` headers unconditionally.

This means KSA geo-restriction and Tabby eligibility checks in non-prod environments are trivially bypassable by setting `cf-ipcountry: SA` in any request.

## Impact

- Staging/dev environments cannot be used to accurately test geo-restriction behaviour.
- Tabby integration testing in staging accepts any `cf-ipcountry: SA` header without validation.
- If a non-prod environment is accidentally used in production (shared hostname, misconfigured load balancer), the bypass extends to production.

## Root Cause

The `CF_ORIGIN_SECRET` check was designed as a production-only guard. The non-prod fallback (`trust all headers`) was intentional for ease of local development, but was not scoped to `localhost` or explicitly documented as a security boundary.

## Fix

Restrict the "trust all" fallback to `NODE_ENV=development` and `localhost`-only origins. For staging environments, require `CF_ORIGIN_SECRET` to be set (even if it's a test value) to accurately simulate production geo-restriction behaviour.

## Related

- EXP-100 (CF-IPCountry spoofing fix)
- EXP-129 (Tabby verify/webhook KSA bypass — payment path variant)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
