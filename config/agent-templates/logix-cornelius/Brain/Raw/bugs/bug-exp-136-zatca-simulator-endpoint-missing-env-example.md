---
title: "EXP-136: ZATCA_SIMULATOR_ENDPOINT consumed in zatca.config.ts but absent from .env.example"
linear_id: "EXP-136"
agent_fp: "201f41ef3af9"
date: "2026-05-26"
severity: "Low"
status: "resolved"
resolution: "closed via PR #503 (ZATCA env vars unification) — simulator mode now returns reportingEndpoint=undefined; ZATCA_SIMULATOR_ENDPOINT key removed from config"
tags: [bug, completeness, zatca, env, project/experts]
category: "bug"
source: "automation"
---

# EXP-136: ZATCA_SIMULATOR_ENDPOINT consumed in zatca.config.ts but absent from .env.example

**Linear:** [EXP-136](https://linear.app/experts/issue/EXP-136) | **Fingerprint:** `<!-- agent-fp: 201f41ef3af9 -->` | **Severity: Low** | **Status: Resolved**

## Summary

`zatca.config.ts` read `process.env.ZATCA_SIMULATOR_ENDPOINT ?? process.env.ZATCA_SANDBOX_ENDPOINT` but `ZATCA_SIMULATOR_ENDPOINT` was absent from `.env.example`. A developer running the ZATCA simulator locally had no documented env name.

## Resolution

Closed via PR #503 (ZATCA env vars unification, 2026-05-26). The simulator mode was refactored to return `reportingEndpoint: undefined`, meaning local validation only with no remote endpoint required. `ZATCA_SIMULATOR_ENDPOINT` was removed from `zatca.config.ts` entirely. No documentation addition needed — the key no longer exists.

## Related

- EXP-137 (ZATCA_REPORTING_ENDPOINT legacy fallback — resolved in same PR)
- PR #503

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
