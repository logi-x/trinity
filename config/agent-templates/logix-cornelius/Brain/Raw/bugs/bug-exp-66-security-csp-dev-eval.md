---
title: "EXP-66 — CSP dev-mode unsafe-eval + localhost WebSocket — production-locked via regression test"
date: "2026-05-21"
status: resolved
resolution: fixed — PR #329
tags: [bug, security, csp, dev-mode, unsafe-eval, websocket, project/experts]
linear: "https://linear.app/experts/issue/EXP-66"
fingerprint: "df256311e5f9"
---

## Summary

After Phase 4B (PR #324), React dev tooling and HMR needed `unsafe-eval` + ws sources that must NOT leak to production. These were in the base `CSP_DIRECTIVES` instead of `DEV_ONLY_CSP_ADDITIONS`. PR #329 moves them to the dev-only block and locks with a regression test.

## Repro

1. Build production image; inspect CSP header
2. Observe: `unsafe-eval` or `ws://localhost` in production CSP

## Agent fingerprint

`<!-- agent-fp: df256311e5f9 -->`

## Status

`resolved` — PR #329 isolates dev CSP additions with regression test.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
