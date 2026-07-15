---
title: "EXP-112 — CRON_SECRET timing-unsafe comparison in embedding-sync janitor"
date: "2026-05-25"
status: open
resolution: unknown
tags: [bug, security, cron, auth, embeddings, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-112"
fingerprint: "agent-fp:R2-cron-timing-unsafe-janitor-001"
---

## Summary

The embedding-sync janitor cron route (`/api/v1/internal/ai/embeddings/sync`) uses a plain `!==` comparison for `CRON_SECRET` authentication. Same vulnerability class as EXP-111: timing-unsafe and fail-open when the env var is missing.

## Root cause

The janitor route was implemented before the `timingSafeEqual` pattern was established by PR #470. Both EXP-111 and EXP-112 are part of the same pre-#470 timing-unsafe pattern that now requires a uniform remediation pass.

## Agent fingerprint

`<!-- agent-fp:R2-cron-timing-unsafe-janitor-001 -->`

## Status

Open — same class as EXP-111. Fix: replace `!==` with `crypto.timingSafeEqual`; throw on missing secret.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
