---
title: "Permissions"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/auth"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
source_id: "docs/architecture/permissions.md"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# Permissions

`` `@logix/permissions` `` defines the action catalog and role policies. API services call `assertCan(actor, action, ctx)` after resolving domain context, especially `clientId`.

## Internal roles

| Role | Access |
| ---- | ------ |
| `owner`, `admin` | Full |
| `project_manager` | Broad operations; no finance write-side or identity/settings writes |
| `developer` | Project, repository, memory, workflow, request, vault writes |
| `finance` | Invoice payment/cancel/send; proposal send |
| `creative` | Brand, vault, proposal writes |

## Client roles

| Role | Access |
| ---- | ------ |
| `client_owner` | Scoped portal + proposal response |
| `client_member` | Scoped portal without proposal response |

## Client scoping

Enforced server-side. A client actor must pass `ctx.clientId` in `actor.clientIds`; foreign clients are denied even if the route URL is guessed.

`agent_service` is reserved for later phases — read-mostly with memory write capability.
