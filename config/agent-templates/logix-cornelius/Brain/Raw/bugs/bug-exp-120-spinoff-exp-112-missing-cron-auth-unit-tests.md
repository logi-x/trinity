---
title: "EXP-120: Missing auth unit tests for cron routes"
linear_id: "EXP-120"
agent_fp: "c0d66a2c089b"
spinoff_of: "EXP-112"
date: "2026-05-25"
severity: "Low"
status: "Todo"
tags: [bug, testing, cron, project/experts]
category: "bug"
source: "automation"
---

# EXP-120: Missing auth unit tests for cron routes

**Linear:** EXP-120 | **Fingerprint:** `<!-- agent-fp: c0d66a2c089b -->` | **Spinoff of:** EXP-112

## Summary

None of the cron routes have unit tests that verify: (a) the `timingSafeEqual` behaviour rejects incorrect secrets, (b) missing `CRON_SECRET` environment variable causes a 403 (fail-closed), (c) correct secret returns 200. The absence of these tests allowed EXP-111/EXP-112/EXP-114–EXP-116 to exist undetected.

## Impact

- No regression protection for the `timingSafeEqual` cron auth invariant.
- Any future cron route added without tests could silently regress to `!==` comparison.
- Test gap allows security regressions to merge undetected.

## Root Cause

No test suite coverage requirement for cron route authentication. Tests were written for the business logic of each cron handler but not for the auth layer.

## Fix

Add tests for each cron route (or for the shared `verifyCronSecret` helper once extracted per EXP-116):

```ts
describe("verifyCronSecret", () => {
  it("returns 403 when CRON_SECRET is missing from env", ...);
  it("returns 403 when Authorization header is absent", ...);
  it("returns 403 when secret is wrong", ...);
  it("returns null (passes) when secret is correct", ...);
});
```

## Related

- EXP-112 (parent — embedding janitor timing-unsafe), EXP-116 (extract shared helper)
- EXP-111, EXP-114, EXP-115 (routes that need coverage)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
