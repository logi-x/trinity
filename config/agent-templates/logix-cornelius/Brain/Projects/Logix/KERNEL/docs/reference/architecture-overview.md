---
title: "Architecture Overview"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/architecture"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
source_id: "docs/architecture/overview.md"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# Architecture Overview

Logix Kernel is a TypeScript monorepo. The web app only talks to the Fastify API through `@logix/sdk`; the API owns business logic and writes through `@logix/db`; background work is isolated in `apps/worker`.

```mermaid
flowchart LR
  Browser["Browser"] --> Web["apps/web Next.js"]
  Web --> SDK["@logix/sdk"]
  SDK --> API["apps/api Fastify"]
  API --> Domain["@logix/domain"]
  API --> Permissions["@logix/permissions"]
  API --> Events["@logix/events"]
  API --> DB["@logix/db Prisma"]
  Worker["apps/worker BullMQ"] --> DB
  Worker --> Redis["Redis"]
  API --> Redis
  DB --> Postgres["PostgreSQL + pgvector"]
  API --> MinIO["MinIO vault storage"]
```

## Contracts

- API responses use `ApiOk<T>` or `ApiErr` only.
- Important mutations write domain events, audit logs, and activity feed items.
- Client actors are scoped by `actor.clientIds`; security is enforced server-side, not by hiding UI.

## Product shape

Phase 1 is a **command-center foundation**, not a generic admin dashboard. Domain pages expose operational context, activity, links, status, and workflow surfaces instead of raw table dumps.

## Related

- [[Projects/Logix/KERNEL/docs/reference/domain-model|Domain model]]
- [[Projects/Logix/KERNEL/docs/reference/permissions|Permissions]]
- [[Projects/Logix/KERNEL/docs/decisions/ADR 0004 — Web Through SDK Only|ADR 0004 — Web through SDK only]]
