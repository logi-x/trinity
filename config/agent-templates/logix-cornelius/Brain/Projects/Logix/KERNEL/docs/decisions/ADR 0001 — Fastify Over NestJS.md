---
title: "ADR 0001 — Fastify Over NestJS"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/adr"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
source_id: "docs/adr/0001-fastify-over-nestjs.md"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# ADR 0001: Fastify Over NestJS

## Status

Accepted.

## Context

Phase 1 needs a typed API with thin route handlers, Zod validation, OpenAPI generation, fast tests through `app.inject()`, and low ceremony for many domain modules.

## Decision

Use Fastify 5 with `fastify-type-provider-zod`, `@fastify/swagger`, and explicit `routes.ts` / `service.ts` / `schemas.ts` module boundaries.

## Consequences

The API remains lightweight and testable. Business logic must stay in services because Fastify does not impose that structure for us. Response schemas are success-only because error envelopes are handled globally.
