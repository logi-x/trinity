---
title: "EXP-188 — [spinoff: EXP-170] ESLint sink rule permanently bypassed for all src/lib/** files due to global ignore entry (DUPLICATE → EXP-189)"
date: "2026-05-29"
status: resolved
resolution: "Cancelled as duplicate of EXP-189. The distinct concern (un-ignore src/lib/** and fix ~44 pre-existing lint errors) is tracked under EXP-189 which remains open."
tags: [bug, platform, eslint, error-disclosure, project/experts]
linear: "https://linear.app/experts/issue/EXP-188/spinoff-exp-170-eslint-sink-rule-permanently-bypassed-for-all-srclib"
fingerprint: "5f549d4217a8"
---

## Summary

`apps/experts-app/eslint.config.mjs:115` global `ignores` includes `"src/lib/**"`, exempting all files in `src/lib/` — including `src/lib/errors/api-error.ts` and route-handler helpers — from the `no-restricted-syntax` sink rule. A developer following the convention of putting shared logic in `src/lib/` could introduce an error-disclosure path that would never be caught by the lint rule.

## Status

`resolved (cancelled)` — Duplicate of EXP-189 which captures the same concern with more detail. EXP-189 remains **open**.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
