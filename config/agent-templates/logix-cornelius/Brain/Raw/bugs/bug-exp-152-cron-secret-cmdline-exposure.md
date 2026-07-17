---
title: "EXP-152: CRON_SECRET exposed in cron sidecar process arguments via curl -H Authorization"
linear_id: "EXP-152"
agent_fp: "a672576f84bf"
date: "2026-05-27"
severity: "Medium"
status: "resolved"
resolution: "merged PR #566"
tags: [bug, security, docker, project/experts]
category: "bug"
source: "automation"
---

# EXP-152: CRON_SECRET in cron sidecar process args

**Linear:** [EXP-152](https://linear.app/experts/issue/EXP-152) | **Fingerprint:** `a672576f84bf`

## Summary
Production and staging cron sidecar containers passed `CRON_SECRET` as a `-H "Authorization: Bearer ${CRON_SECRET}"` CLI argument to curl. Readable from `/proc/<pid>/cmdline` for the full duration of each HTTP call.

## Fix
PR #566: CRON_SECRET written to `/run/curl-auth.conf` at startup (mode 0600, `umask 0077`). Curl invocations use `--config /run/curl-auth.conf`. Secret never appears in process args.

## Related
EXP-167 (Redis password same class), EXP-168 (Docker secrets class-level sweep)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
