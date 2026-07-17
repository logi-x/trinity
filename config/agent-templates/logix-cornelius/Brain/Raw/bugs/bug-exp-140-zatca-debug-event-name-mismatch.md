---
title: "EXP-140: ZATCA debug event name mismatch exposes gov API responses via global DEBUG flag"
linear_id: "EXP-140"
agent_fp: "a6d7ead53650"
date: "2026-05-26"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, zatca, information-disclosure, debug, project/experts]
category: "bug"
source: "automation"
---

# EXP-140: ZATCA debug event name mismatch exposes gov API responses via global DEBUG flag

**Linear:** [EXP-140](https://linear.app/experts/issue/EXP-140) | **Fingerprint:** `<!-- agent-fp: a6d7ead53650 -->` | **Severity: Medium**

## Summary

In `report-to-zatca.ts`, the debug event is emitted as `"debug.zatca.report.response"` but the guard condition checks for `DEBUG_ZATCA` specifically. The actual trigger is `DEBUG=true` (the global debug flag), not `DEBUG_ZATCA`. This means sensitive government API response data — including ZATCA clearance tokens and taxpayer VAT numbers — flows to Redis pub/sub and structured logs whenever `DEBUG=true` is set, even in production if an operator enables global debug mode for troubleshooting an unrelated issue.

## Impact

- **Information disclosure**: ZATCA clearance tokens (government-issued) and taxpayer VAT numbers are logged and published to Redis when `DEBUG=true`.
- **Not directly externally exploitable**, but the guard is misconfigured in a way that makes accidental production exposure likely during incident response (operators commonly set `DEBUG=true` to diagnose issues).
- **Regulatory concern**: ZATCA clearance tokens and taxpayer VAT numbers are sensitive government data; logging them without explicit opt-in may conflict with ZATCA API terms of service.

## Root Cause

The guard checks `process.env.DEBUG_ZATCA` but the actual global debug flag used elsewhere in the codebase is `process.env.DEBUG`. The debug event fires whenever `DEBUG=true` because the event name pattern (`debug.*`) matches on the global `DEBUG` flag, not the intended `DEBUG_ZATCA` flag.

## Fix

Change the guard to check `process.env.DEBUG_ZATCA === 'true'` exclusively. Remove the dependency on the global `DEBUG` flag for ZATCA-specific debug output. Consider using a scoped debug namespace (`DEBUG=zatca:*`) consistent with the `debug` npm package conventions.

## Related

- EXP-141 (credentials committed to git — related ZATCA security concern)
- EXP-142 (ZATCA_FORCE flags lack production guard)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
