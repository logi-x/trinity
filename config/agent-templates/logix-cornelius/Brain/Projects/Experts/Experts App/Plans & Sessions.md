---
title: "Experts App — Plans & Sessions"
date: "2026-07-01"
tags: ["project/experts", "topic/plans", "topic/sessions"]
category: "projects/experts"
up: "[[Entities/Projects/Experts App]]"
updated: "2026-07-15"
---

# Experts App — Plans & Sessions

↑ [[Entities/Projects/Experts App|Experts App]]

Working surfaces for the Experts App. The notes live in the vault's `Raw/` ingest zone (where the
fleet routines and working sessions write them), so they are **surfaced here, not moved** — the
paths are referenced across the routines and would break if relocated. See also
[[Projects/Experts/Experts App/Bugs & Ops|Bugs & Ops]].

## Plans

Implementation / design plans (`Raw/plans/`, one note per plan):

![[Raw/plans/Plans.base]]

## Session & research sources

Session logs, research notes, and decision sources (`Raw/sources/`, one note per source):

![[Raw/sources/Sources.base]]

## Convention — plans & sources must backlink + tag

A `.base` embed does **not** create a graph edge, so a note that only appears in the tables above
shows as an **orphan**. Every note in `Raw/plans/` and `Raw/sources/` therefore carries a real
wikilink footer back to this hub:

```markdown
---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
```

Each note also carries the **`experts`** tag (plans additionally tag `plan`; sources tag their
`category`, e.g. `session-log`), so the whole set is reachable via the tag pane / `#experts`
graph filter. When adding a new plan or source, give it `title` / `date` / `tags` / `category`
frontmatter and append the footer so it joins the cluster instead of floating free.
