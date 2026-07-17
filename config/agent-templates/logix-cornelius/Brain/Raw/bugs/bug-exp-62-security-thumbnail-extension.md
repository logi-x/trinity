---
title: "EXP-62 — Thumbnail upload extension derived from client filename instead of validated MIME"
date: "2026-05-21"
status: resolved
resolution: fixed — PR #315 (commit 9e1b7def)
tags: [bug, security, upload, mime, xss, asset-origin, project/experts]
linear: "https://linear.app/experts/issue/EXP-62"
fingerprint: "5bff6a2d626a"
---

## Summary

Thumbnail routes used the client-supplied filename to derive the stored object extension, allowing mismatched MIME/extension (e.g., upload a JS file as `thumbnail.jpg`). This could be served misleadingly by the CDN with wrong MIME type.

## Repro

1. POST to thumbnail upload with a JavaScript payload but filename ending in `.jpg`
2. Observe: stored with `.jpg` extension regardless of actual content type
3. CDN serves with `image/jpeg` MIME, masking executable content

## Agent fingerprint

`<!-- agent-fp: 5bff6a2d626a -->`

## Status

`resolved` — PR #315 derives extension from server-validated MIME type, not client filename.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
