---
title: "Operation - query"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["ops", "query"]
category: "tools/ops"
source: "generated"
source_id: "Tools/Ops/query.md"
---

# Operation - query

Use when the user asks a question about the vault.

## Steps

1. Identify likely entry points from memory. Read [[Index]] only if the relevant pages are not obvious.
2. Open only the smallest set of relevant notes.
3. Check freshness metadata on the key pages before answering:
   - `freshness`
   - `verified`
   - `source_of_truth`
   - `verify_with`
4. For current-state, latest, open-issue, deployment, roadmap, or status questions, follow [[Tools/Ops/verify-current]] before presenting a volatile or live page as current truth.
5. Answer from the vault first, with wikilink citations.
6. Clearly label anything added from general knowledge as outside-vault context.
7. If the synthesis is durable, offer to save it to [[Tools/Templates/concept|Concept]], [[Tools/Templates/project-hub|Project Hub]], [[Tools/Templates/decision|Decision]], or [[Tools/Templates/summary]] form.
8. Append to [[Log]] only when a durable note was created or materially updated.

## Output Standard

- Start with the direct answer.
- Cite pages with `[[wikilinks]]`.
- For volatile/live pages, state the `verified` date and what was checked now.
- Mention uncertainty explicitly.
- Do not create pages unless the user asks or the answer should become durable vault knowledge.
