---
title: "EXP-64 — Lesson-resource Content-Disposition + per-domain MIME allowlist + RFC 5987 filenames"
date: "2026-05-21"
status: open
resolution: partial — steps 1 (cookie-scope) and 2 (Content-Disposition) complete; step 3 (per-domain MIME allowlist) open
tags: [bug, security, upload, mime, content-disposition, xss, authorization, project/experts]
linear: "https://linear.app/experts/issue/EXP-64"
fingerprint: "3570f3824763"
---

## Summary

Incident#12 identified three steps: (1) cookie-scope verification; (2) `Content-Disposition: attachment` header on lesson-resource served files to prevent in-browser execution; (3) per-domain source-code MIME allowlist in the upload route. Steps 1+2 complete. Step 3 still open.

## Repro

1. Upload a file with MIME type not in the (not-yet-implemented) per-domain allowlist
2. Observe: upload succeeds without domain-specific MIME restriction

## Agent fingerprint

`<!-- agent-fp: 3570f3824763 -->`

## Status

`open` — step 3 (per-domain MIME allowlist) pending. See Action-Tracker 2026-05-21.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
