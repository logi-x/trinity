---
title: "EXP-100 — CF-IPCountry header spoofable by authenticated user → locale bypass"
date: "2026-05-24"
status: resolved
resolution: "PR #456: treat CF-IPCountry as a display-only geolocation hint for the UI only; never write it to the DB user record. Locale for payment eligibility is derived from the authenticated user's stored locale field."
tags: [bug, security, cloudflare, locale, payments, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-100"
fingerprint: "agent-fp:R2-cf-ipcountry-spoof-001"
---

## Summary

The `CF-IPCountry` header (injected by Cloudflare at the edge) was being persisted to the user's `locale` field in the database on each authenticated request. An attacker with a valid session could send a forged `CF-IPCountry` header (bypassing Cloudflare by calling the origin directly) to update their stored locale and unlock Tabby instalment payments in unsupported regions.

## Root cause

`CF-IPCountry` is a Cloudflare-injected header on requests routed through the CDN. Direct requests to the origin do not have this header set by Cloudflare, and any value in the header on such requests is attacker-controlled. Writing it to the DB conflated a display hint with authoritative identity data.

## Agent fingerprint

`<!-- agent-fp:R2-cf-ipcountry-spoof-001 -->`

## Status

Resolved — PR #456 merged 2026-05-24.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
