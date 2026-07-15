---
title: "EXP-111 — storage-pending-reaper and storage-orphan-reaper CRON_SECRET timing-unsafe"
date: "2026-05-25"
status: open
resolution: unknown
tags: [bug, security, cron, auth, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-111"
fingerprint: "agent-fp:R2-cron-timing-unsafe-reapers-001"
---

## Summary

`storage-pending-reaper` and `storage-orphan-reaper` cron routes authenticate `CRON_SECRET` with a plain `!==` string comparison. This is timing-unsafe: a timing oracle attack can recover the secret character by character. Additionally, when `CRON_SECRET` env var is unset, the comparison evaluates `undefined !== undefined` → `false`, granting access to any caller.

## Root cause

PR #470 (`reservation-cleanup`) introduced the correct pattern: `crypto.timingSafeEqual(Buffer.from(secret), Buffer.from(CRON_SECRET))` with a hard throw when `CRON_SECRET` is missing. The reaper routes predate this PR and use the old timing-unsafe pattern.

## Agent fingerprint

`<!-- agent-fp:R2-cron-timing-unsafe-reapers-001 -->`

## Status

Open — High severity (fail-open on missing secret). Requires uniform remediation pass across all cron routes.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
