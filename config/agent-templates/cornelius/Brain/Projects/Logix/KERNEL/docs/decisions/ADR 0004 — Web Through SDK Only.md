---
title: "ADR 0004 — Web Through SDK Only"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/adr"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
source_id: "docs/adr/0004-web-through-sdk-only.md"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# ADR 0004: Web Through SDK Only

## Status

Accepted.

## Context

The web app must not become a second business-logic layer or bypass API permissions.

## Decision

`apps/web` calls the Fastify API through `@logix/sdk`. Browser requests use the same-origin `/api/v1/*` rewrite so the session cookie stays first-party; server components forward cookies to `API_URL`.

## Consequences

Permissions and audit behavior stay centralized in the API. The SDK becomes the contract that future CLI and integration layers can reuse.

See [[Projects/Logix/KERNEL/docs/reference/architecture-overview|Architecture overview]].
