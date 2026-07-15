---
title: "EXP-71 — App takes full CSP ownership with per-request nonce + JsonLd conversions (Phase 4B)"
date: "2026-05-21"
status: open
resolution: in-review — PR #324 merged; production cutover pending (Traefik header removal)
tags: [bug, security, csp, nonce, json-ld, xss, defense-in-depth, project/experts]
linear: "https://linear.app/experts/issue/EXP-71"
fingerprint: "e2e233c4f650"
---

## Summary

Phase 4B of the CSP migration (incident#10): app fully owns the CSP via per-request nonce (PR #324), all 21+ JSON-LD blocks converted to use `<JsonLd>` component with nonce, `unsafe-inline` removed. Production cutover requires Traefik to stop injecting `headers.contentSecurityPolicy` (which overrides the app header). Deployment sequence: app deploys FIRST, then Traefik config removed.

## Repro

1. Deploy Phase 4B app build to production while Traefik still sets `headers.contentSecurityPolicy`
2. Observe: Traefik header overrides app CSP, nonce-based policy not active
3. Remove Traefik header after app deploy — observe app CSP active

## Agent fingerprint

`<!-- agent-fp: e2e233c4f650 -->`

## Status

`open` (In Review) — production cutover pending. Action-Tracker deadline 2026-05-30.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
