---
title: "EXP-54 — Unauthenticated /internal/debug/* credential leak + community IDOR + markdown XSS + Tabby fail-open"
date: "2026-05-21"
status: resolved
resolution: fixed — PR referenced in incident#1 remediation; all findings closed
tags: [bug, security, credentials, idor, xss, authentication, urgent, project/experts]
linear: "https://linear.app/experts/issue/EXP-54"
fingerprint: "eb17b849c258"
---

## Summary

Bundled finding from incident#1 (2026-05-13). Five critical vulnerabilities:
1. `/internal/debug/*` routes unauthenticated — leaked credentials/tokens
2. Community post IDOR — any user could edit/delete another user's post
3. Stored markdown XSS in `MarkdownPreview.tsx` — `skipHtml=false` without sanitizer
4. Tabby payment webhook fail-open — missing signing secret silently passed verification
5. CRON_SECRET bypass — cron routes accessible without secret

## Repro

1. Call `/api/v1/internal/debug/accounts` anonymously — observe credential dump
2. POST to community post edit endpoint with another user's post ID — observe success
3. Create post with `<script>alert(1)</script>` — observe execution on render
4. POST to Tabby webhook without `X-Tabby-Signature` — observe success
5. Call any `/api/v1/internal/cron/*` route without `Authorization: Bearer` — observe success

## Agent fingerprint

`<!-- agent-fp: eb17b849c258 -->`

## Status

`resolved` — all five findings closed. See [[Raw/sources/2026-05-13-experts-security-incident-1-remediation]].

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
