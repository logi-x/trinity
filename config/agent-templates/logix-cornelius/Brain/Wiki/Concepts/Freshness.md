---
title: "Freshness"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["meta", "freshness", "ops"]
category: "wiki/concepts"
source: "generated"
source_id: "Wiki/Concepts/Freshness.md"
---

# Freshness

Freshness metadata tells LLMs whether a page is durable memory or stale-prone operational state.

## Frontmatter Fields

```yaml
freshness: volatile
verified: "2026-06-11"
source_of_truth: "/home/logix/experts"
verify_with:
  - "git log"
  - "GitHub issues and PRs"
  - "Linear"
```

## Levels

| Level | Meaning | Query behavior |
| ----- | ------- | -------------- |
| `stable` | Rarely changes, like identity or historical facts. | Cite normally. |
| `slow` | Changes monthly or by milestone. | Mention verified date when relevant. |
| `volatile` | Changes weekly/daily. | Verify before saying "current". |
| `live` | Requires source check every time. | Must verify or clearly refuse current certainty. |

## Rule

If a user asks "current", "latest", "open", "status", "today", "now", or similar, and the relevant page is `volatile` or `live`, follow [[Tools/Ops/verify-current]].

