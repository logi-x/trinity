---
title: "Monorepo Map"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/architecture"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
source_id: "README.md"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# Monorepo Map

Paths are relative to **logix-kernel** root (`repo_root`).

| Path | Purpose |
| ---- | ------- |
| `apps/web` | Next.js command center and client portal |
| `apps/api` | Fastify v1 API, domain modules, OpenAPI |
| `apps/worker` | BullMQ worker; Phase 1 embedding stub queue |
| `apps/cli` | `logix` terminal interface (`@logix/cli`) |
| `apps/mcp` | MCP stdio server (Phase 2) |
| `packages/db` | Prisma schema, migrations, seed |
| `packages/domain` | Zod contracts, DTOs, status transitions, money |
| `packages/auth` | scrypt passwords, opaque hashed sessions |
| `packages/permissions` | Typed role/action policy engine |
| `packages/events` | DomainEvent, AuditLog, ActivityFeed |
| `packages/protocol` | CLI/context/runner/artifact/hook contracts |
| `packages/openapi` | OpenAPI fetch/check tooling |
| `packages/sdk` | Typed HTTP client for v1 API |
| `packages/logger` | pino with secret redaction |

## Local ports

| Service | Default |
| ------- | ------- |
| Web | `3060` (`WEB_URL`) |
| API | `3061` (`API_URL`) |

CLI resolves `LOGIX_BASE_URL`, `API_URL`, profile config, then `.env` before fallback.
