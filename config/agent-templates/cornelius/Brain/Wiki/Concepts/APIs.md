---
title: "APIs"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "topic/apis"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/APIs.md"
---

# APIs

API work in this vault is mostly about the Experts platform: locale-aware web app routes, `app/api/v1/*` handlers, auth-protected mutations, and keeping the iOS client aligned with the same contracts.

## Core patterns

- Prefer thin HTTP handlers and move business logic into domain modules.
- Use `auth()` first, then permission checks, then handler logic.
- Return structured JSON errors instead of throwing framework-specific exceptions deep in the stack.
- Keep API routes locale-neutral even when the UI is locale-scoped.

## Experts conventions

The web app uses Next.js route handlers under `app/api/v1/`. Most conversation references cluster around:

- auth and session-aware endpoints
- admin APIs with `requireAdmin()`
- payment and webhook flows
- content access checks for courses, events, and creator tooling

## Repeated concerns in conversations

- keeping the API contract aligned with [[Wiki/Concepts/Auth]] and [[Wiki/Concepts/Access Control]]
- avoiding route leaks where page-level access exists but API-level access does not
- making webhook consumers idempotent and traceable
- keeping mobile clients compatible with the same response shapes

## What this topic usually means in the vault

When conversations link to `[[Wiki/Concepts/APIs]]`, they are usually discussing contract design, route shape, auth guards, request validation, or integration points between the Experts app and external providers.

## Related

- [[Wiki/Concepts/Auth]]
- [[Wiki/Concepts/Access Control]]
- [[Wiki/Concepts/Webhooks]]
