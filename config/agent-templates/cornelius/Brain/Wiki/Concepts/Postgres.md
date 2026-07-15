---
title: "Postgres"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "tech/postgresql", "topic/postgres"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Postgres.md"
---

# Postgres

Postgres in this vault usually means the operational database layer behind Experts: schema design, query behavior, Prisma integration, and data-shape decisions that affect performance and correctness.

## Typical discussion areas

- schema modeling for product features
- migrations and rollout safety
- query correctness and relation loading
- performance issues hidden behind ORM abstractions
- access patterns for search, analytics, and admin views

## Experts context

Most product data in the Experts app flows through Prisma onto PostgreSQL. Conversations that link here usually involve:

- enrollment and course data
- payment and commission records
- user/account/auth tables
- admin reporting and filtering

## Practical rules

- design tables for the product workflow, not just the UI shape
- be explicit about nullable fields and lifecycle state
- inspect generated queries when Prisma behavior feels surprising
- treat data migrations as product changes, not just technical chores

## Relationship to Prisma

Prisma is the access layer; Postgres is the source of truth. When a conversation says "Prisma problem," it is often really a modeling or relational constraint problem that belongs here too.

## Related

- [[Wiki/Concepts/Prisma]]
- [[Wiki/Concepts/APIs]]
- [[Wiki/Concepts/Auth]]
- [[Projects/Experts/DEVELOPER_GUIDE]]
