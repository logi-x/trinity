---
title: "EXP-250: R2_API_TOKEN env defined but no caller reads it"
linear_id: "EXP-250"
agent_fp: "b509d8df0101"
date: "2026-06-01"
severity: "Low"
status: "open"
resolution: "unknown"
tags: [bug, completeness, storage, project/experts]
category: "bug"
source: "automation"
---

# EXP-250: R2_API_TOKEN declared in .env.example but never read

**Linear:** [EXP-250](https://linear.app/experts/issue/EXP-250/completeness-r2_api_token-env-defined-but-no-caller-reads-it) | **Status:** Todo

## Summary
`R2_API_TOKEN` is declared in `.env.example` but no application code, worker, or route ever reads `process.env.R2_API_TOKEN`. It was added as a placeholder for planned Cloudflare REST API management operations (bucket CORS, lifecycle rules, provisioning automation) that were never implemented.

## File
`apps/experts-app/.env.example` — `R2_API_TOKEN`

## Fix
Either implement the intended Cloudflare management-plane automation (requires separate RFC), or remove `R2_API_TOKEN` from `.env.example` and any docker-compose env blocks to avoid operator confusion.

## Related
None.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
