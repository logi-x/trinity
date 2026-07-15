---
title: "Operation - ingest"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["ops", "ingest"]
category: "tools/ops"
source: "generated"
source_id: "Tools/Ops/ingest.md"
---

# Operation - ingest

Use when the user says `ingest <url or file>`.

## Steps

1. If the source is a URL, follow [[Tools/Ops/raw-capture]] and save the full text under `Raw/` with source metadata.
2. If the source is already in [[Inbox]] or [[Raw]], start from that note.
3. Create `Wiki/Summaries/S - <Title>.md` using [[Tools/Templates/summary]].
4. Extract claims, numbers, dates, named entities, decisions, and action items.
5. Update the relevant pages:
   - people, organizations, places, projects, and agents in [[Entities]]
   - concepts in [[Concepts]]
   - project-local context in [[Projects]]
   - action items in [[Actions]]
   - decisions in [[Decisions]]
6. Add backlinks from touched pages to the summary.
7. Update [[Index]] only for a new major hub or entry point.
8. Append a dated entry to [[Log]] with pages touched.
9. Run `python3 Tools/Scripts/vault_lint.py`.

## Rules

- Do not invent facts.
- Mark unsupported claims as unverified.
- Keep Raw content immutable after creation.
- Prefer updating existing pages over creating duplicates.
