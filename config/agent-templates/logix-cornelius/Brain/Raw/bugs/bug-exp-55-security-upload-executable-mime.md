---
title: "EXP-55 — /internal/upload allows executable MIME (text/html, text/javascript) to public R2"
date: "2026-05-21"
status: resolved
resolution: fixed — per-domain MIME allowlist added (incident#2 PR)
tags: [bug, security, upload, mime, xss, authorization, project/experts]
linear: "https://linear.app/experts/issue/EXP-55"
fingerprint: "23e901d2126d"
---

## Summary

The `/api/v1/internal/upload` route accepted any MIME type including `text/html` and `text/javascript` and stored them under attacker-chosen `domain`/`entityId` paths in the public R2 bucket, enabling stored XSS via CDN hosting.

## Repro

1. Authenticate as any user (student, creator)
2. POST multipart to `/api/v1/internal/upload` with `Content-Type: text/html` and arbitrary `domain`/`entityId`
3. Observe: file stored at public CDN URL
4. Share link — browser executes content as HTML

## Agent fingerprint

`<!-- agent-fp: 23e901d2126d -->`

## Status

`resolved` — per-domain MIME allowlist enforced in upload route.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
