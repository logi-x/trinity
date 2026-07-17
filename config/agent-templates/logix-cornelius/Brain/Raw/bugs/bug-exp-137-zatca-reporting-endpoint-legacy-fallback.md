---
title: "EXP-137: ZATCA_REPORTING_ENDPOINT legacy fallback consumed but absent from .env.example"
linear_id: "EXP-137"
agent_fp: "f0d7bcec12bd"
date: "2026-05-26"
severity: "Low"
status: "resolved"
resolution: "closed via PR #503 (ZATCA env vars unification) — ZATCA_REPORTING_ENDPOINT legacy fallback removed from zatca.config.ts"
tags: [bug, completeness, zatca, env, project/experts]
category: "bug"
source: "automation"
---

# EXP-137: ZATCA_REPORTING_ENDPOINT legacy fallback consumed but absent from .env.example

**Linear:** [EXP-137](https://linear.app/experts/issue/EXP-137) | **Fingerprint:** `<!-- agent-fp: f0d7bcec12bd -->` | **Severity: Low** | **Status: Resolved**

## Summary

`zatca.config.ts` read `process.env.ZATCA_PRODUCTION_ENDPOINT ?? process.env.ZATCA_REPORTING_ENDPOINT` as a legacy fallback. `ZATCA_REPORTING_ENDPOINT` was absent from `.env.example`, creating an undocumented migration path for operators still using the old env var name.

## Resolution

Closed via PR #503 (ZATCA env vars unification, 2026-05-26). The `ZATCA_REPORTING_ENDPOINT` legacy fallback read was removed from `zatca.config.ts`, the health route, and the test env snapshot. Operators must use `ZATCA_PRODUCTION_ENDPOINT` going forward.

## Related

- EXP-136 (ZATCA_SIMULATOR_ENDPOINT — resolved in same PR)
- PR #503

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
