---
title: "GraphQL"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "tech/graphql"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/GraphQL.md"
---

# GraphQL

GraphQL is not the dominant app contract in the current Experts stack, but it appears in conversations as a comparison point, integration option, or legacy/alternate API style under consideration.

## What it usually means here

- deciding between REST-style route handlers and GraphQL schemas
- discussing typed client/server contracts
- comparing resolver complexity against simpler route-level APIs
- evaluating whether a product surface benefits from flexible querying

## Why it matters even when not primary

GraphQL tends to surface when the team is feeling pain in one of these areas:

- over-fetching or under-fetching data
- fragmented frontend data requirements
- duplicated contract logic across many endpoints
- uncertainty about ownership of aggregation logic

## Practical vault takeaway

In this brain, GraphQL is best treated as an architectural option to compare against the existing Experts API approach, not as the assumed default.

## Related

- [[Wiki/Concepts/APIs]]
- [[Wiki/Concepts/JavaScript]]
- [[Wiki/Concepts/Postgres]]
- [[Projects/Experts/DEVELOPER_GUIDE]]
