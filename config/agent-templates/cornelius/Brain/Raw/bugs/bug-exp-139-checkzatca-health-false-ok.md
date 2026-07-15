---
title: "EXP-139: checkZatca health check returns ok when environment-specific ZATCA endpoint is missing"
linear_id: "EXP-139"
agent_fp: "60a80638abd7"
date: "2026-05-26"
severity: "High"
status: "open"
resolution: "unknown"
tags: [bug, zatca, health-check, billing, project/experts]
category: "bug"
source: "automation"
---

# EXP-139: checkZatca health check returns ok when environment-specific ZATCA endpoint is missing

**Linear:** [EXP-139](https://linear.app/experts/issue/EXP-139) | **Fingerprint:** `<!-- agent-fp: 60a80638abd7 -->` | **Severity: High**

## Summary

`checkZatca()` in the admin health route accepts **any** ZATCA endpoint (`ZATCA_PRODUCTION_ENDPOINT || ZATCA_SANDBOX_ENDPOINT`) as sufficient to return `ok`. But `resolveZatcaConfig()` performs an **environment-specific** lookup: if `getDefaultZatcaEnvironment()` returns `"production"`, it requires `ZATCA_PRODUCTION_ENDPOINT` specifically. If only `ZATCA_SANDBOX_ENDPOINT` is set, the health check returns `ok` but every actual ZATCA report call throws. The health check masks a misconfiguration that causes silent ZATCA reporting failures in production.

## Impact

- **False health signal**: The admin health dashboard reports ZATCA as healthy when it is not. Operations teams relying on health checks for deployment go/no-go decisions will miss a ZATCA misconfiguration.
- **Saudi ZATCA Phase 2 compliance risk**: Silent ZATCA reporting failures mean government e-invoice clearance is not happening. Sustained failure is a regulatory compliance violation.
- **Introduced by commit `a422e0c`** (ZATCA env vars unification, PR #503).

## Root Cause

```typescript
// checkZatca() — too permissive:
const endpoint = process.env.ZATCA_PRODUCTION_ENDPOINT || process.env.ZATCA_SANDBOX_ENDPOINT;
if (!endpoint) return { status: 'error', ... };
return { status: 'ok' };

// resolveZatcaConfig() — environment-specific:
const env = getDefaultZatcaEnvironment(); // returns 'production' in prod
const endpoint = env === 'production'
  ? process.env.ZATCA_PRODUCTION_ENDPOINT  // throws if absent
  : process.env.ZATCA_SANDBOX_ENDPOINT;
```

The health check uses an `||` fallback that `resolveZatcaConfig` does not share.

## Fix

Replace the permissive check in `checkZatca()` with a call to `resolveZatcaConfig()` (or mirror its environment-specific lookup). If `resolveZatcaConfig()` would throw for the current environment, return `{ status: 'error' }`.

## Related

- PR #503 (introduced this regression)
- EXP-136, EXP-137 (resolved in same PR)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
