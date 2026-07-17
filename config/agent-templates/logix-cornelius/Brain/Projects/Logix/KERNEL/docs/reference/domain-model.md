---
title: "Domain Model"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/architecture"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
source_id: "docs/architecture/domain-model.md"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# Domain Model

Canonical schema: `` `packages/db/prisma/schema.prisma` `` (relative to **logix-kernel** root). Phase 1 domains:

| Domain | Scope |
| ------ | ----- |
| Identity | Users, roles, permissions, sessions |
| Clients & projects | Client 360, project 360, environments, commands, health checks, documents |
| Requests | Client work items, comments, status events, kanban |
| Vault | Folders, files, versions, shares, access logs |
| Brand & portfolio | Brand kits, assets, business logic docs, published work |
| Proposals & finance | Templates, line items, events, payments, recurring plans |
| Agents | Profiles, skills, tools, project access, contexts, mock runs |
| Memory | Single searchable table, kind-specific `data`, links, pgvector-ready embeddings, FTS |
| Repositories | Metadata, branches, commands, health, pull requests |
| Workflows | Graph nodes/edges, triggers, mock run history |
| Events / audit / activity / notifications / settings | Operating trail and workspace config |

Conventions: cuid IDs and timestamps on mutable models; money as `Decimal(12,2)`; default currency SAR; Saudi VAT default 15%.
