---
title: "EXP-60 — CDN/Traefik/R2 hardening: nosniff, script-src exclusion, R2 bucket-listing, Content-Disposition"
date: "2026-05-21"
status: canceled
resolution: deferred — all items are infra-side (Cloudflare/R2 config), not code-side
tags: [bug, security, infra, cdn, traefik, csp, canceled, project/experts]
linear: "https://linear.app/experts/issue/EXP-60"
fingerprint: "57b049e61f2c"
---

## Summary

Incident#7 identified four CDN/Traefik/R2 hardening items: (1) `X-Content-Type-Options: nosniff` on cdn.experts.com.sa, (2) CSP `script-src` exclusion for CDN (already verified safe), (3) R2 bucket-listing disabled, (4) `Content-Disposition: attachment` passthrough. All are infra-side and outside the app codebase.

## Repro

N/A — infra configuration items, not reproducible via application code

## Agent fingerprint

`<!-- agent-fp: 57b049e61f2c -->`

## Status

`canceled` — deferred to infra ops. Not actionable via code PRs.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
