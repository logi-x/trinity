---
title: "EXP-70 — Password-reset URL poisoning via Origin/Host + account enumeration + /console/health disclosure"
date: "2026-05-21"
status: open
resolution: unknown — no PR yet
tags: [bug, security, authentication, host-header, enumeration, information-disclosure, project/experts]
linear: "https://linear.app/experts/issue/EXP-70"
fingerprint: "e20b15a445a8"
---

## Summary

Three findings from incident#18:
1. Forgot-password route uses `Origin`/`Host` header from the request to build the reset URL, allowing an attacker to poison the link to an attacker-controlled domain
2. Forgot-password route returns different responses for known vs unknown emails, enabling account enumeration
3. `/console/health` endpoint is unauthenticated and discloses server internals

## Repro

1. POST to `/api/auth/forgot-password` with `Host: evil.example.com` — observe reset email contains `evil.example.com` link
2. POST same endpoint with known vs unknown email — observe differing response bodies/status codes
3. GET `/console/health` without authentication — observe server internals

## Agent fingerprint

`<!-- agent-fp: e20b15a445a8 -->`

## Status

`open` — HIGH. No PR yet. Action-Tracker deadline 2026-05-28.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
