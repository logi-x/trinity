---
title: "next-intl"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "tech/next-intl", "topic/next-intl"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/next-intl.md"
---

# next-intl

`next-intl` is the concrete i18n library wiring used by the Experts App. It is the implementation layer beneath the broader [[Wiki/Concepts/i18n]] topic.

## What it handles

- localized routing helpers
- locale-aware `Link` and router behavior
- message loading and translation lookup
- server/client translation APIs

## Practical rule

When a conversation says "i18n bug" in the web app, it is often really a `next-intl` wiring or usage issue: wrong import source, bad locale wrapper placement, or metadata generation that ignored locale context.

## Related

- [[Wiki/Concepts/i18n]]
- [[Wiki/Concepts/Next.js]]
- [[Projects/Experts/Experts App/docs/designs/2026-04-11-i18n-migration-guide]]
