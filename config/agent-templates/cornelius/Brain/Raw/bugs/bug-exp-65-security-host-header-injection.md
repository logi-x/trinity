---
title: "EXP-65 — Host-header injection in getRequestBaseUrl → open redirect + near-XSS on /share/* pages"
date: "2026-05-21"
status: resolved
resolution: fixed — PR #320
tags: [bug, security, host-header, open-redirect, xss, share-pages, project/experts]
linear: "https://linear.app/experts/issue/EXP-65"
fingerprint: "0997a3069ae4"
---

## Summary

The three `/share/*` pages (course, event, post) passed the result of `getRequestBaseUrl()` — which trusted `X-Forwarded-Host`/`Host` without validation — into HTML attributes. An attacker-controlled host header could produce open redirects and near-XSS conditions.

## Repro

1. Send request to `/share/course/<id>` with `Host: evil.example.com`
2. Observe: HTML response contains `evil.example.com` in `og:url` and share button hrefs

## Agent fingerprint

`<!-- agent-fp: 0997a3069ae4 -->`

## Status

`resolved` — PR #320 pins `getRequestBaseUrl` to the canonical `NEXTAUTH_URL` origin.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
