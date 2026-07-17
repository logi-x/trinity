---
title: "Inertia.js"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "tech/inertia-js"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Inertia.js.md"
---

# Inertia.js

Inertia.js belongs primarily to the HoWA side of the vault rather than the current Experts web stack. When it appears in conversations, it usually points to Laravel-driven SPA behavior, page props, and server-driven navigation patterns.

## Main relevance here

- HoWA architecture and legacy/reference patterns
- Laravel controller to frontend page handoff
- form handling and validation in an Inertia workflow
- navigation/state behavior without a fully separate frontend API

## Why this topic still matters

Even though Experts is Next.js-first, Inertia remains useful context when:

- comparing architecture tradeoffs across projects
- reading older HoWA decisions
- translating Laravel-era patterns into newer app-router patterns
- understanding how previous product assumptions shaped current work

## Conceptual contrast

Inertia compresses the backend/frontend boundary compared with the Experts App approach. That makes it productive for some product surfaces, but it changes how routing, data fetching, and state ownership are reasoned about.

## Related

- [[Entities/Projects/HoWA]]
- [[Projects/HoWA/README]]
- [[Wiki/Concepts/Laravel]]
- [[Wiki/Concepts/APIs]]
- [[Wiki/Concepts/Documentation]]
