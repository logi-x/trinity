---
title: "Critical Facts"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["index", "meta"]
category: "meta"
source: "generated"
source_id: "Wiki/Concepts/CRITICAL_FACTS.md"
---

# Critical Facts - read first

> Operating contract for `/home/logix/brain-v2`. Discovery entry: [[Index]]; schema: [[CLAUDE.md]]; agent routing: [[AGENTS.md]].

## Structure

- `index.md` is curated, not exhaustive. It points to hubs and major entry points.
- `Entities/` is only for named graph nodes: people, organizations, places, projects, and agents.
- `Wiki/Concepts/` is for topics, technologies, systems, frameworks, and recurring themes.
- `Projects/` stores project-local context. Each project should have a single hub in `Entities/Projects/`.
- `Raw/` is immutable source material.
- `Inbox/` is where daily notes, scratch thoughts, and triage captures belong.
- `Wiki/Summaries/` is processed source knowledge.
- `Actions/` and `Decisions/` are operational memory.
- `Tools/` contains relocated tooling and maintenance artifacts.
- `Wiki/Freshness.md` is the dashboard for volatile/live pages that need source-of-truth checks.

## Path Changes From Brain V1

- `Raw/` became `Raw/`.
- `Wiki/Concepts/` became `Wiki/Concepts/`.
- `Action-Tracker.md` moved to `Actions/Action-Tracker.md`.
- `Decision-Log.md` moved to `Decisions/Decision-Log.md`.
- Runtime/tooling weight such as `.git`, `node_modules`, `.venv`, and `.codegraph` was intentionally not copied.

## Rules

- Keep `/home/logix/brain` untouched.
- Use wikilinks for real internal pages and Markdown links for external URLs.
- Use tags for generic classification when a page link adds no useful context.
- Keep `Log.md` append-only.
- For current/latest/status questions, follow [[Tools/Ops/verify-current]] and state the `verified` date for volatile/live pages.
- For broad edits, validate links and frontmatter before closing.

## Standard Operations

- Query: [[Tools/Ops/query]]
- Verify current: [[Tools/Ops/verify-current]]
- Raw capture: [[Tools/Ops/raw-capture]]
- Ingest: [[Tools/Ops/ingest]]
- Project update: [[Tools/Ops/project-update]]
- Lint: [[Tools/Ops/lint]]
- Daily digest: [[Tools/Ops/daily-digest]]

## Validation Command

```bash
python3 Tools/Scripts/vault_lint.py
```

## Templates

New maintained pages should start from [[Tools/Templates/README]].
