---
title: "SEO"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "topic/seo", "seo"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/SEO.md"
---

# SEO

SEO in this vault is primarily about Experts App discoverability: locale-aware routing, metadata generation, structured indexing, and making public pages rank without breaking product architecture.

## Core concerns

- canonical URLs and alternates
- locale-specific sitemap generation
- metadata per route and per content type
- keeping public pages crawlable while private/product routes remain protected

## Experts context

SEO work is tightly tied to the i18n architecture:

- locale-prefixed public routes
- `hreflang` coverage
- per-locale sitemap output
- public profiles and content pages with durable URLs

## Repeated conversation themes

- metadata for course, event, and creator pages
- avoiding duplicate or thin public pages
- routing decisions that impact search indexing
- balancing marketing needs with app-router complexity

## Rule of thumb

If a page needs to be found by search engines, SEO decisions must be part of the route and metadata design from the start, not a patch added after the page ships.

## Related

- [[Wiki/Concepts/i18n]]
- [[Wiki/Concepts/Marketing]]
- [[Projects/Experts/Experts App/docs/designs/2026-04-11-i18n-migration-guide]]
