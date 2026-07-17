---
title: "EXP-100 — cf-ipcountry header spoof bypasses Tabby KSA restriction when origin is reachable directly"
date: "2026-05-24"
status: open
resolution: unknown
tags: [bug, security, payments, tabby, eligibility, header-injection, project/experts]
linear: "https://linear.app/experts/issue/EXP-100/bug-cf-ipcountry-header-spoof-bypasses-tabby-ksa-restriction-when"
fingerprint: "302812779a63"
---

## Summary

`resolveTabbyEligibility` trusts the `CF-IPCountry` header unconditionally to determine KSA eligibility for Tabby payments. An attacker who discovers the origin IP (via CT logs, DNS history, or enumeration) can bypass Cloudflare entirely, send a request directly to the origin server with a forged `CF-IPCountry: SA` header, and pass the KSA eligibility check without being in Saudi Arabia.

All three Tabby-affected routes use this resolver: eligibility, enroll, and register.

## Root cause

`apps/experts-app/src/lib/payments/eligibility/payment-eligibility.ts / resolveTabbyEligibility` — the function reads `CF-IPCountry` from the incoming request headers and returns `true` for `SA`. Because Cloudflare strips and injects this header on legitimate traffic, the approach is valid behind Cloudflare. However, when the origin is directly reachable (bypassing Cloudflare), any client can send any value for this header.

Fix: supplement the `CF-IPCountry` check with origin validation — either require a shared secret header that Cloudflare injects (and the origin validates), or check the connecting IP against Cloudflare's published IP ranges (readily available via `api.cloudflare.com/client/v4/ips`), or bind the origin to loopback/VPN only so direct access is impossible.

## Agent fingerprint

`<!-- agent-fp: 302812779a63 -->`

## Status

`open` — Todo (No priority set). Tabby KSA restriction bypassable by header spoofing when origin is exposed. Affects all three Tabby eligibility surfaces. Related to EXP-99 (subscription checkout missing gate) and EXP-96 (course/event checkout fix).

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
