---
title: "EXP-142: ZATCA_FORCE_REPORT_FAIL and ZATCA_FORCE_SIGN_FAIL lack production APP_ENV guard"
linear_id: "EXP-142"
agent_fp: "88435ae7f1e0"
date: "2026-05-26"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, zatca, billing, env-guard, project/experts]
category: "bug"
source: "automation"
---

# EXP-142: ZATCA_FORCE_REPORT_FAIL and ZATCA_FORCE_SIGN_FAIL lack production APP_ENV guard

**Linear:** [EXP-142](https://linear.app/experts/issue/EXP-142) | **Fingerprint:** `<!-- agent-fp: 88435ae7f1e0 -->` | **Severity: Medium**

## Summary

Introduced in commit `a422e0c` (PR #503, 2026-05-26). `ZATCA_FORCE_REPORT_FAIL` and `ZATCA_FORCE_SIGN_FAIL` are debug/testing flags that, when set, cause all ZATCA government invoice submissions to fail silently. Neither flag has a guard that prevents it from being active in a production environment (e.g., `APP_ENV !== 'production'` check). An operator or insider who can set production worker environment variables can silently suppress all ZATCA e-invoice reporting without any distinguishing signal from a genuine API failure.

## Impact

- **Regulatory compliance risk**: Saudi ZATCA Phase 2 requires real-time invoice clearance. Sustained suppression via `ZATCA_FORCE_REPORT_FAIL=true` in production would cause all invoices to be uncleared without operator visibility into the source.
- **Insider threat vector**: Setting this flag in production is operationally indistinguishable from a transient ZATCA API outage, making deliberate suppression difficult to detect.
- The risk is classified Medium rather than High because it requires insider access to production environment variables (not externally exploitable).

## Root Cause

```typescript
// No APP_ENV guard:
if (process.env.ZATCA_FORCE_REPORT_FAIL === 'true') {
  throw new Error('ZATCA_FORCE_REPORT_FAIL set — forced failure');
}
```

The flags were designed for testing and should only be active in non-production environments.

## Fix

Add an `APP_ENV` guard:

```typescript
if (process.env.APP_ENV !== 'production' && process.env.ZATCA_FORCE_REPORT_FAIL === 'true') {
  throw new Error('ZATCA_FORCE_REPORT_FAIL set — forced failure (non-production only)');
}
```

Apply to both `ZATCA_FORCE_REPORT_FAIL` and `ZATCA_FORCE_SIGN_FAIL`. Consider a startup-time warning if either flag is set in production regardless of the guard.

## Related

- EXP-139 (ZATCA health check false-ok — related ZATCA misconfiguration)
- EXP-140 (ZATCA debug event mismatch)
- EXP-141 (credentials committed in same PR)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
