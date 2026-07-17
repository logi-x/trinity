---
title: "EXP-69 — Production/staging secrets committed to git + role revocation does not invalidate JWT sessions"
date: "2026-05-21"
status: open
resolution: unknown — no PR yet
tags: [bug, security, secrets, credentials, jwt, authentication, urgent, project/experts]
linear: "https://linear.app/experts/issue/EXP-69"
fingerprint: "a0b8f55e493a"
---

## Summary

Two findings from incident#17:
1. `apps/experts-app/.env.production`, `.env.staging`, `.env.e2e`, and `slack.secret` are tracked in git — all production secrets (DB credentials, auth secrets, API keys) are in the git history and accessible to anyone with repo access
2. Removing a user's role from the DB does not invalidate existing JWTs — a revoked admin/instructor continues to have those privileges until token expiry

## Repro

1. `git log --all --full-history -- apps/experts-app/.env.production` — observe secret values
2. Extract JWT from a session; update user role to non-admin in DB; re-send request with old JWT — observe admin-level access still granted

## Agent fingerprint

`<!-- agent-fp: a0b8f55e493a -->`

## Status

`open` — CRITICAL. Rotate all secrets in `.env.production`, `.env.staging`, `.env.e2e`, `slack.secret`. Purge from git history. Action-Tracker deadline 2026-05-23.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
