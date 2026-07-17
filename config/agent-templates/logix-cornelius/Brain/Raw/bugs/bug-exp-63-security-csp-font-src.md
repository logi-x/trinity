---
title: "EXP-63 — Drop raw.githubusercontent.com from font-src; CSP report endpoint + HSTS hardening"
date: "2026-05-21"
status: open
resolution: partial — CSP report endpoint shipped PR #316; self-hosted fonts still open
tags: [bug, security, csp, font-src, hsts, defense-in-depth, project/experts]
linear: "https://linear.app/experts/issue/EXP-63"
fingerprint: "80198be9cf82"
---

## Summary

Incident#11 found: (A) CSP `font-src` allows `raw.githubusercontent.com` — a public CDN not under platform control could serve substitute fonts or be used to exfiltrate via timing; (B) CSP report endpoint needed for observability. Sub-item A (report endpoint) shipped PR #316. Sub-item B (self-hosted fonts) still open.

## Repro

Check `proxy.ts` `font-src` directive — observe `raw.githubusercontent.com` still listed after PR #316.

## Agent fingerprint

`<!-- agent-fp: 80198be9cf82 -->`

## Status

`open` — sub-item A (report endpoint) resolved; sub-item B (self-host fonts, drop `raw.githubusercontent.com`) still open. See Action-Tracker 2026-05-21.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
