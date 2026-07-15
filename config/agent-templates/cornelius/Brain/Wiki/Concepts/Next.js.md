---
title: "Next.js"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "tech/next-js"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Next.js.md"
---

# Next.js

Next.js is the application framework behind the Experts App. In this vault it usually means app-router structure, server/client boundaries, route handlers, metadata, and how product architecture maps onto the framework.

## Core concerns

- app-router route organization
- server vs client component boundaries
- locale-aware routing
- metadata and SEO behavior
- API route composition inside the same app

## Why it appears so often

Many Experts conversations are really Next.js architecture conversations in disguise: navigation, auth guards, page loading, metadata, or build/runtime behavior.

## Working principle

Use the framework to clarify boundaries, not blur them. Shared product logic should not be trapped inside page files just because the framework makes it convenient.

## Related

- [[Wiki/Concepts/React]]
- [[Wiki/Concepts/TypeScript]]
- [[Wiki/Concepts/i18n]]
- [[Wiki/Concepts/SEO]]
