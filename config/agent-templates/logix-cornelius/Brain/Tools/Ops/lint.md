---
title: "Operation - lint"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["ops", "lint"]
category: "tools/ops"
source: "generated"
source_id: "Tools/Ops/lint.md"
---

# Operation - lint

Use when the user asks to check vault health or before completing broad edits.

## Mechanical Checks

Run:

```bash
python3 Tools/Scripts/vault_lint.py
```

The script checks:

- YAML frontmatter parse errors.
- missing frontmatter in maintained areas.
- broken wikilinks outside code spans and code fences.
- old v1 paths such as `raw/` and `Entities/Topics/` in maintained routing files.
- misplaced topic pages under `Entities/`.
- summary files that do not start with `S - `.

## Review Checks

Report, but do not auto-rewrite without judgment:

- duplicate pages with the same concept/entity.
- stale claims without source links.
- project docs that should be summarized.
- Raw notes that should be processed into [[Summaries]].
- entity mentions that occur repeatedly without a page.

