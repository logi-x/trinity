# Brain V2 Agent Index

This file is the routing index for the `/home/logix/brain-v2` Obsidian vault.

## Default Rule

Do not preload `Index.md`, `Log.md`, entity hubs, project hubs, or workflow docs by default.
Start from the specific user task, open the minimum relevant notes, and expand only when needed.

Before editing operating rules or broad structure, read [[CRITICAL_FACTS]] first.

## What This Vault Is

This repository is an Obsidian knowledge graph, not an application codebase.

Use it for:

- querying prior knowledge
- filing durable syntheses
- maintaining entity, concept, project, action, and decision notes
- ingesting immutable sources into processed wiki pages
- maintaining vault structure and metadata

## Clean Structure

Primary areas:

- `Inbox/` — quick captures waiting to be processed.
- `Raw/` — immutable source material and imported records. Do not edit Raw files after creation except path/name maintenance.
- `Wiki/Concepts/` — durable ideas, technologies, frameworks, systems, and recurring themes.
- `Wiki/Summaries/` — processed source summaries. Summary pages should start with `S - ` when newly created.
- `Entities/` — real-world or named graph nodes: people, organizations, places, projects, and agents.
- `Projects/` — project-local documentation and working context. Each project should be reached through its project entity hub.
- `Actions/` — action tracker and action-item notes.
- `Decisions/` — decision tracker and decision records.
- `Agents/` — prompts, context packs, and agent workflow notes.
- `Tools/` — vault maintenance tooling and relocated repo/tooling artifacts.

## Routing

Choose one path first:

- **Direct note edit**: open only the target note and any immediately linked note needed to verify the change.
- **Vault query / discovery**: follow [[Tools/Ops/query]]; read `Index.md` only if the relevant notes are not already known.
- **Current / latest / status questions**: follow [[Tools/Ops/verify-current]] for volatile or live pages before treating the vault as current truth.
- **Ingest / filing**: follow [[Tools/Ops/ingest]]; open the source plus the small set of destination pages being updated.
- **Raw capture**: follow [[Tools/Ops/raw-capture]]; use Raw only for stable evidence, not daily notes or scratch writing.
- **Action / decision maintenance**: open `Actions/Action-Tracker.md`, `Decisions/Decision-Log.md`, or the specific source note involved.
- **Project work**: follow [[Tools/Ops/project-update]]; open the project entity hub under `Entities/Projects/`, then the linked project-local notes under `Projects/`.
- **Tooling work**: open only the needed file under `Tools/`.
- **Lint / maintenance**: follow [[Tools/Ops/lint]] and run `python3 Tools/Scripts/vault_lint.py`.

## Links And Tags

- Use `WikiLinks` for internal vault pages.
- Use Markdown links only for external URLs.
- Use wikilinks for people, organizations, places, projects, agents, and durable concepts.
- Use tags for generic classification when a linked page would add no useful context.
- Keep claims in maintained wiki pages tied to source or summary notes where practical.

## Maintenance

- Keep `Index.md` curated: hubs and entry points only, not exhaustive deep docs.
- Keep `Log.md` append-only.
- Preserve YAML frontmatter.
- Maintain freshness metadata on high-value project, action, and decision hubs. For `volatile` and `live` pages, answer with the `verified` date unless the source of truth was checked now.
- Do not modify `.obsidian/` unless explicitly asked.
- Keep `/home/logix/brain` untouched; this v2 vault is the cleaned derivative.
- Treat `Raw/` as immutable evidence. Put daily notes and scratch work in `Inbox/`.

## Templates

Use [[Tools/Templates/README]] before creating new maintained pages. Standard templates exist for entities, concepts, summaries, project hubs, actions, decisions, raw sources, and inbox captures.

## Validation

Before closing broad edits, run:

```bash
python3 Tools/Scripts/vault_lint.py
```
