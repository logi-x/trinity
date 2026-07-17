---
title: "Experts App — Bugs & Ops"
date: "2026-06-30"
tags: ["project/experts", "topic/bugs", "topic/ops"]
category: "projects/experts"
up: "[[Entities/Projects/Experts App]]"
updated: "2026-07-15"
---

# Experts App — Bugs & Ops

↑ [[Entities/Projects/Experts App|Experts App]]

Operational surfaces for the Experts App. The underlying notes live in the vault's `Raw/`
ingest zone (where the Experts fleet routines — scout / rover / airlock / beacon — write them),
so they are **surfaced here, not moved**: those paths are hardcoded across the routine loops and
fleet contracts, and relocating them would break the automation.

## Bug tracker

Live view of all Experts bug notes (`Raw/bugs/`, one note per bug):

![[Raw/bugs/Bugs.base]]

## Agent / fleet state

- [[Raw/agent-state/findings-index|Findings index]] — running-routine memory (verified findings)
- [[Raw/agent-state/board-audit-log|Board audit log]] — GitHub issue-board hygiene snapshots

## Convention — bug notes must backlink here

A `.base` **embed does not create a graph edge**, so a bug note that only appears in the
table above shows as an **orphan** in the graph view. Every note in `Raw/bugs/` therefore
carries a real wikilink back to this hub as a footer:

```markdown
---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
```

When creating a new bug note, append that footer (full-path wikilink, vault convention) so it
joins the graph cluster instead of floating free. This hub is the single backlink target for
all Experts bug notes — it pulls the whole `Raw/bugs/` set into the Experts App neighbourhood.

Every bug note also carries the **`experts`** tag in its `tags:` frontmatter (alongside `bug`
and any domain tags), so the whole set is reachable via the tag pane / `#experts` graph filter.
