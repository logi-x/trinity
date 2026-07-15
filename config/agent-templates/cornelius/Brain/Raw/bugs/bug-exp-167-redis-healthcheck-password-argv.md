---
title: "EXP-167: Redis healthcheck exposes REDIS_PASSWORD in process arguments"
linear_id: "EXP-167"
agent_fp: "4c90b482dd97"
spinoff_of: "EXP-152"
date: "2026-05-28"
severity: "Medium"
status: "resolved"
resolution: "merged PR #568"
tags: [bug, security, docker, project/experts]
category: "bug"
source: "automation"
---

# EXP-167: Redis healthcheck password in process args

**Linear:** [EXP-167](https://linear.app/experts/issue/EXP-167) | **Fingerprint:** `4c90b482dd97`

## Summary
Redis healthcheck used `redis-cli -a "${REDIS_PASSWORD}" ping` and startup used `redis-server --requirepass "${REDIS_PASSWORD}"`. Both expose `REDIS_PASSWORD` via `/proc/<pid>/cmdline` and `ps aux`.

## Fix
PR #568: healthcheck uses `REDISCLI_AUTH` env var (no `-a` arg). Startup writes `requirepass` to a tmpfs-mounted `/tmp/redis.conf` (mode 0600) and execs `redis-server /tmp/redis.conf`.

## Related
EXP-152 (parent), EXP-168 (Docker secrets class-level sweep)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
