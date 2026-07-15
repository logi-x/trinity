---
title: "EXP-189: src/lib/** globally ESLint-ignored — error-disclosure sink rule can't fire on lib-tree response builders"
linear_id: "EXP-189"
agent_fp: "manual-exp189"
date: "2026-05-29"
severity: "Medium"
status: "open"
resolution: "unknown"
tags: [bug, security, eslint, project/experts]
category: "bug"
source: "automation"
---

# EXP-189: ESLint sink rule bypassed for src/lib/**

**Linear:** [EXP-189](https://linear.app/experts/issue/EXP-189) | **Fingerprint:** `manual-exp189`

## Summary
`apps/experts-app/eslint.config.mjs` includes `"src/lib/**"` in its global `ignores` array. The `no-restricted-syntax` error-disclosure sink rule (no caught `error.message` in `NextResponse.json`, including two-step pattern) can never fire on any file in `src/lib/`. `prisma-error.handler.ts:65` P2002 column-name disclosure lives in this tree. Estimated ~44 pre-existing lint errors would surface if the ignore is removed.

## Repro
Remove `"src/lib/**"` from ESLint global ignores and run `pnpm lint` — 44+ violations expected.

## Related
EXP-170 (parent error-disclosure sweep), EXP-187 (two-step pattern fix), EXP-188 (duplicate, cancelled)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
