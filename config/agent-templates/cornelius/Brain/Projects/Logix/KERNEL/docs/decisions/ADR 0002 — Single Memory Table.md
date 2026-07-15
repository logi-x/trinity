---
title: "ADR 0002 — Single Memory Table"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/adr"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
source_id: "docs/adr/0002-single-memory-table.md"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# ADR 0002: Single Memory Table

## Status

Accepted.

## Context

The roadmap needs decisions, ADRs, incidents, runbooks, client notes, project notes, agent context, proposal notes, repository notes, and loop summaries to share search, visibility, links, and future embeddings.

## Decision

Use one `Memory` table with a `kind` enum and structured JSON `data` for kind-specific fields.

## Consequences

FTS, links, and entity associations are simpler. Kind-specific validation lives in domain/API boundaries rather than separate database tables.

See [[Projects/Logix/KERNEL/docs/reference/memory-system|Memory system]].
