---
title: "EXP-190: Prisma migrate container can't resolve DATABASE_URL from Docker secret"
linear_id: "EXP-190"
agent_fp: "manual-exp190"
date: "2026-05-29"
severity: "High"
status: "resolved"
resolution: "merged PR #606 — DATABASE_URL hydration in prisma.config.ts from Docker secret file"
tags: [bug, prisma, docker, project/experts]
category: "bug"
source: "automation"
---

# EXP-190: Prisma migrate container can't resolve DATABASE_URL

**Linear:** [EXP-190](https://linear.app/experts/issue/EXP-190) | **Fingerprint:** `manual-exp190`

## Summary
After the EXP-168 Docker secrets migration removed `env_file: .env` from all services, the `experts-prisma` migration container (`prisma migrate deploy`) began failing with `PrismaConfigEnvError: Cannot resolve environment variable: DATABASE_URL`. The container has `/run/secrets/database_url` mounted but `prisma.config.ts` only reads `process.env.DATABASE_URL`.

## Fix
PR #606: `apps/experts-prisma/prisma.config.ts` hydrates `DATABASE_URL` from `DATABASE_URL_FILE` env var or `/run/secrets/database_url` (matching the `runtime-secrets.ts` pattern). Operator: rebuild prisma image before next `migrate deploy`.

## Related
EXP-168 (Docker secrets class migration)

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
