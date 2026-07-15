---
title: "Raw"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["meta"]
category: "raw"
source: "generated"
source_id: "Raw/Raw.md"
---

# Raw

Immutable source material and imported records.

Raw is the evidence layer. It stores material that should remain stable so future summaries, claims, decisions, and project updates can be checked against the original record.

## Rules

- Do not edit Raw content after creation except mechanical path/name maintenance.
- Process important sources into [[Summaries]].
- Link Raw records from summaries, project notes, actions, or decisions when they are evidence.
- Do not use Raw for daily notes, scratch thoughts, or planning drafts. Use [[Inbox]] for those.
- Do not summarize or interpret inside Raw. Put interpretation in [[Summaries]], [[Concepts]], [[Projects]], [[Actions]], or [[Decisions]].

## What Belongs Here

| Folder | Use for | Process into |
| ------ | ------- | ------------ |
| `articles/` | External articles and long-form references | [[Summaries]], [[Concepts]] |
| `sources/` | Session records, source notes, durable evidence | [[Summaries]], [[Projects]] |
| `transcripts/` | Verbatim meeting, call, video, or audio transcripts | [[Summaries]], [[Actions]], [[Decisions]] |
| `meetings/` | Original meeting notes and agendas | [[Projects]], [[Actions]], [[Decisions]] |
| `bugs/` | Imported bug/finding records | [[Actions]], project docs |
| `reviews/` | Security/code/product review records | [[Summaries]], [[Actions]], [[Decisions]] |
| `plans/` | Original plans as captured | [[Projects]], [[Actions]] |
| `research/` | Research source material | [[Summaries]], [[Concepts]] |
| `assets/` | Binary/image/source assets | Linked from summaries or project docs |
| `agent-state/` | Automation state and generated indexes | Operational references |

## What Does Not Belong Here

- Daily notes.
- Random scratch writing.
- LLM answers that are already synthesized.
- Working project docs that should live under [[Projects]].
- Durable ideas that should live under [[Concepts]].
- Tasks that should live under [[Actions]].
- Decisions that should live under [[Decisions]].

## Capture Flow

1. Capture exact source in Raw.
2. Create a summary in [[Summaries]] if the source matters.
3. Ripple durable facts into [[Entities]], [[Concepts]], and [[Projects]].
4. Extract operational items into [[Actions]] and [[Decisions]].
5. Link back to the Raw source or its summary.

## Tools

- [[Tools/Ops/raw-capture]] - how to add a Raw source.
- [[Tools/Templates/raw-source]] - generic Raw source template.
- [[Tools/Templates/raw-meeting]] - meeting or call source template.
- [[Tools/Templates/raw-transcript]] - transcript source template.
- [[Tools/Templates/raw-bug]] - bug/finding source template.
- `python3 Tools/Scripts/raw_inventory.py` - count and review Raw folders.
