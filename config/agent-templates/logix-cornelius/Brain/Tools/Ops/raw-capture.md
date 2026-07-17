---
title: "Operation - raw capture"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["ops", "raw"]
category: "tools/ops"
source: "generated"
source_id: "Tools/Ops/raw-capture.md"
---

# Operation - raw capture

Use when adding evidence to [[Raw]].

## Decision Rule

Put it in Raw only if it is source material that should remain stable:

- external article
- transcript
- meeting source
- imported bug or finding
- review output
- original plan
- research capture
- binary/source asset
- automation state

Put it in [[Inbox]] if it is a daily note, scratch thought, draft, or something that needs later triage.

## Steps

1. Choose the closest Raw folder from [[Raw]].
2. Create a file with a descriptive title and date when useful.
3. Preserve the source content as-is.
4. Add frontmatter with source metadata when practical.
5. Do not summarize inside Raw.
6. If the source matters, create a [[Summaries|summary]] and link it back.

## Filename Pattern

Prefer:

```text
Raw/<type>/<YYYY-MM-DD>-<short-slug>.md
```

Use original filenames for assets and transcripts when that preserves provenance.

## After Capture

Run:

```bash
python3 Tools/Scripts/raw_inventory.py
python3 Tools/Scripts/vault_lint.py
```

