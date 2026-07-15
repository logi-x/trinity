---
title: "Testing"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "topic/testing"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Testing.md"
---

# Testing

Testing in this vault usually means confidence work around the Experts app: validating auth flows, route protection, admin behavior, payments, and UI states before shipping changes into an already-moving product.

## What gets tested most often

- auth and permission boundaries
- payment and billing flows
- route-level behavior in the app router
- form validation and edge-case UI states
- regression coverage after refactors

## Practical split

- unit/integration tests for business logic and route handlers
- UI/component tests for interaction-heavy surfaces
- browser/manual verification for critical end-to-end flows

## Common lessons from conversations

- permission bugs often need both page-level and API-level tests
- search and derived data can leak protected content if not explicitly tested
- fragile tests are usually a sign that responsibilities are too coupled
- "works locally" is not enough for billing, auth, or admin control paths

## Why this topic matters

Testing is a forcing function for architecture quality. The same conversations that reference testing often expose missing boundaries, unclear contracts, or product flows that were never made explicit.

## Related

- [[Wiki/Concepts/Auth]]
- [[Wiki/Concepts/Access Control]]
- [[Wiki/Concepts/APIs]]
- [[Wiki/Concepts/Webhooks]]
