---
title: "EXP-175 — cron sidecar lost APP_BASE_URL after PR #566 removed env_file — all 8 cron tasks silently failing"
date: "2026-05-28"
status: open
resolution: unknown
tags: [bug, infrastructure, docker, cron, regression, project/experts]
linear: "https://linear.app/experts/issue/EXP-175"
fingerprint: "468ada456745"
---

## Summary
PR #566 (EXP-152 fix) removed `env_file: .env` from the cron sidecar service in `docker/production/docker-compose.yml` and `docker/staging/docker-compose.yml` to prevent CRON_SECRET from appearing in process arguments. However, `APP_BASE_URL` was not added to the explicit `environment:` block that replaced it. All 8 cron tasks that call internal routes via `${APP_BASE_URL}/api/v1/internal/...` silently fail because the base URL evaluates to an empty string, making every curl call target a malformed URL.

## Root cause
`env_file: .env` was the implicit source of `APP_BASE_URL` for the cron sidecar. When PR #566 removed it in favour of an explicit `environment:` block containing only `CRON_SECRET`, `APP_BASE_URL` was not carried over. The fix is to add `APP_BASE_URL` to the `environment:` block in both `docker/production/docker-compose.yml` and `docker/staging/docker-compose.yml`.

## Agent fingerprint
`<!-- agent-fp: 468ada456745 -->`

## Status
`open` — Backlog (High). All 8 cron tasks silently failing since PR #566 deploy. Requires immediate patch; deadline 2026-05-29.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
