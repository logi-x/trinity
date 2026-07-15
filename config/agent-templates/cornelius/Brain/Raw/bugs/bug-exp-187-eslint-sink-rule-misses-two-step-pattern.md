---
title: "EXP-187 — [spinoff: EXP-170] ESLint error-disclosure sink rule misses two-step pattern (const message = error.message; NextResponse.json)"
date: "2026-05-29"
status: resolved
resolution: "ESLint VariableDeclarator selector added to catch the two-step capture pattern via PR #604."
tags: [bug, platform, eslint, error-disclosure, project/experts]
linear: "https://linear.app/experts/issue/EXP-187/spinoff-exp-170-eslint-error-disclosure-sink-rule-misses-two-step"
fingerprint: "5f40cac28e45"
---

## Summary

The ESLint `no-restricted-syntax` sink rule (added by PR #557, EXP-132 class) matched `.message` only when it appeared *directly* inside `NextResponse.json(...)`. The two-step pattern `const message = error.message; return NextResponse.json({error: message})` was not caught, allowing ~134 sites that used this pattern to escape lint enforcement.

## Root cause

`apps/experts-app/eslint.config.mjs:81-83` — AST selector only targeted `CallExpression[callee.object.name='NextResponse']…MemberExpression[property.name='message']` without a `VariableDeclarator` selector for the intermediate capture.

## Spinoff from

EXP-170 (class-level sweep, gatekeeper attempt-2 BLOCK). The two-step pattern was the dominant form in the codebase (~134 sites).

## Agent fingerprint

`<!-- agent-fp: 5f40cac28e45 -->`

## Status

`resolved` — Fixed in PR #604. `VariableDeclarator` selector added to catch `const message/errorMessage/msg/errMsg = error.message` capture patterns.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
