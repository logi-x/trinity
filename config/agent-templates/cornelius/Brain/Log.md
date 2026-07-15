---
title: "Activity Log"
date: "2026-04-12"
tags: ["log", "meta"]
category: "meta"
source: "generated"
source_id: "Log.md"
---

> **LLM instructions:** Append a new entry here after every ingest, filed query result, or lint pass. Never edit previous entries. Format: `## [YYYY-MM-DD] <type> | <title>` where type is one of: `ingest`, `query`, `lint`, `maintenance`.
> To find the last N entries: grep `^## \[` Log.md | tail -N

---

## [2026-05-03] maintenance | Add LLM skills registry

Documented the source-of-truth pattern for reusable LLM skills: keep executable skills under `/home/logix/.agents/skills`, expose them to client-specific directories with symlinks, and use the vault for routing, purpose, durable decisions, and project links.

Pages touched:

- `Agents/LLM Skills Registry.md` (created)
- `Agents/Agents.md`
- `Entities/Agents.md`
- `Wiki/Concepts/Skills.md`
- `index.md`
- `Log.md`

---

## [2026-04-12] maintenance | Bootstrap index.md and Log.md

Created `index.md` (wiki catalog) and `Log.md` (this file) to implement the LLM Wiki pattern. Updated `CLAUDE.md` with ingest, query, and lint workflows.

Pages touched: `index.md`, `Log.md`, `CLAUDE.md`

---

## [2026-04-12] ingest | Experts Platform Review Call — 06 November 2025

Ingested 85-minute Arabic-language product review call between Logix and client Adnan Ishgi (Experts LMS). Extracted 15 decisions, 11 action items, and a 3-bullet summary.

Pages touched:

- `Projects/Experts/meetings/experts-06-11-2025.md` (created — client note)
- `Action-Tracker.md` (created — 11 actions logged)
- `Decision-Log.md` (created — 15 decisions logged)
- `index.md` (added Client Notes, Trackers sections)

---

## [2026-04-13] maintenance | Create meeting agenda for 14 April 2026 client call

Created meeting agenda for tomorrow's Experts platform review with Adnan Ishgi and Ahmad Zahid. Covers progress since Nov 2025, v1.1 certification depth milestone, critical path to July launch (courses, events, billing), and open action items.

Pages touched:

- `Raw/meetings/agenda-14-04-2026.md` (created — meeting agenda)
- `index.md` (added Meetings section)

---

## [2026-04-13] query | Experts project roadmap and status snapshot

Generated a full status snapshot of the Experts LMS project covering all 14 phases, current position (Phase 7 in progress), critical path to mid-July 2026 soft launch, and open stakeholder actions.

Pages touched:

- `Projects/Experts/snapshots/status-2026-04-13.md` (created — dated status snapshot)
- `Entities/Projects/Experts.md` (added Status Snapshots section with wikilink)
- `index.md` (added snapshot to Projects — Documentation table)

---

## [2026-04-13] maintenance | Add Jeddah place entity and tag all Jeddah-based entities

Created Jeddah place entity and applied place/jeddah tags + location wikilinks across all Jeddah-based people and organizations. Updated Riyadh with people/org sections.

Pages created:

- `Entities/Places/Jeddah.md` — place entity with people and org tables

Pages updated:

- `Entities/Places/Riyadh.md` — added People and Organizations sections (Ahmed Sulaimani, Logix)
- `Entities/People/Adnan Ishgi.md` — place/jeddah tag + Jeddah wikilink
- `Entities/People/Ahmed Zahid.md` — place/jeddah tag + Jeddah wikilink
- `Entities/People/Saba Lanqa.md` — place/jeddah tag + Jeddah wikilink
- `Entities/People/Abdul Hayee.md` — place/jeddah tag + Jeddah wikilink
- `Entities/Organizations/Experts Company Ltd.md` — place/jeddah tag + Jeddah wikilink
- `Entities/Organizations/Samaya.md` — place/jeddah tag + Jeddah wikilink
- `index.md` — added Jeddah to Places table

---

## [2026-04-13] maintenance | Add Organizations category and client/people entities

Refactored entity graph to introduce Organizations as a first-class category. Extracted contact data from `prisma/seeders/01-users.ts`.

Pages created:

- `Entities/Organizations/Logix.md` — Logix Inc. company entity
- `Entities/Organizations/Experts Company Ltd.md` — legal operator of Experts LMS
- `Entities/Organizations/Samaya.md` — partner/client organization
- `Entities/People/Adnan Ishgi.md` — Founder & CEO, Experts Company Ltd (primary client contact)
- `Entities/People/Ahmed Zahid.md` — Co-founder & CFO, Experts Company Ltd
- `Entities/People/Saba Lanqa.md` — Founder & CEO, Experts Company Ltd and HoWA
- `Entities/People/Abdul Hayee.md` — CFO, Samaya

Pages updated:

- `Entities/People/Ahmed Sulaimani.md` — added contact info and Logix org link
- `Entities/Projects/Experts.md` — added Organizations and Key People sections
- `index.md` — added Entities — Organizations section; expanded Entities — People table

---

## [2026-04-13] maintenance | Vault structure cleanup — remove stub entity pages, switch to tag-based discovery

Removed all Tech/ and Topics/ stub pages that had no real content. These were dead-ends for LLM queries; tags already captured the same relationships. Kept 21 project-specific Topics pages for enrichment. Stripped dead `## Links` sections from 726 conversation files.

Deleted:

- `Entities/Tech/` — all 42 stub pages removed (folder kept, empty)
- `Wiki/Concepts/` — 61 stub pages deleted; 21 knowledge pages retained

Retained Topics (to be enriched):
ZATCA, Auth, Payments, Noon Payments, Processing Fees, Affiliate System,
Instructor Certification, Skills, Community, Access Control, WebSockets,
i18n, Monorepo, Storage, PDF, SwiftUI, GSD, Cursor Rules, Graphify, PRD,
ui-ux-pro-max

Conversation files updated:

- 726/781 files cleaned of dead `*` and dead `Wiki/Concepts/*` links

Pages updated:

- `index.md` — replaced Entities — Tech section with note-only reference; trimmed Topics table to 21 live pages
- `_tools/cleanup_stub_links.py` — new maintenance script for stripping dead links

---

## [2026-04-13] maintenance | Enrich 4 high-value Topics pages

Replaced 4 stub pages with rich project-specific knowledge synthesised from project docs, V3/V4 doc set, and CLAUDE.md.

Pages enriched:

- `Wiki/Concepts/ZATCA.md` — full pipeline (invoice → BullMQ → worker → XML → sign), key files, worker architecture principle, ZatcaDocument states, known gotcha
- `Wiki/Concepts/Auth.md` — NextAuth v5 setup, providers, server/client usage, identity-vs-method edge case, AuthIdentity data model, Experts OS session notes
- `Wiki/Concepts/Payments.md` — Stripe/Noon/Tabby providers, billing flow, subscription gating, refund model (time + progress gated), webhook patterns, payout schedule
- `Wiki/Concepts/i18n.md` — URL-based locale routing, 3 locales (en/ar/es), RTL Arabic, \_shared/ implementation pattern, next-intl wiring, new page checklist, per-locale sitemaps

---

## [2026-04-13] maintenance | Enrich 3 more Topics pages

Pages enriched:

- `Wiki/Concepts/Access Control.md` — auth layers, `requireAdmin()` pattern, course access guard (known enrollment bypass bug Apr 2026), realtime channel auth, page-level guard placement rule
- `Wiki/Concepts/Monorepo.md` — full package map (experts-app/realtime/prisma/os), runtime requirements, root convenience scripts, worker commands, experts-prisma usage rule, end-to-end data flow, quality gate
- `Wiki/Concepts/WebSockets.md` — experts-realtime architecture, event envelope contract, Redis channel map with priorities, transport decision matrix, one-socket-per-leader-tab pattern, auth flow, keep-alive and presence behaviour

---

## [2026-04-13] maintenance | Enrich remaining 14 Topics pages

Pages enriched:

- `Wiki/Concepts/Affiliate System.md` - affiliate/referral billing context, attribution, commission interaction with payouts and payments
- `Wiki/Concepts/Instructor Certification.md` - instructor approval, trust signals, publishing gates, onboarding role in Experts
- `Wiki/Concepts/Community.md` - community as a core Experts domain, launch posture, relationship to realtime and Experts OS
- `Wiki/Concepts/PDF.md` - async PDF generation role, worker model, billing/certificate document use cases
- `Wiki/Concepts/Storage.md` - persistent artifact strategy, compliance retention, generated file context
- `Wiki/Concepts/Processing Fees.md` - fee treatment across gateways, margin and payout implications
- `Wiki/Concepts/Noon Payments.md` - Saudi/MENA payment gateway role inside the Experts commerce stack
- `Wiki/Concepts/Skills.md` - agent-skill meaning, reuse pattern, distinction from end-user skill data
- `Wiki/Concepts/SwiftUI.md` - Experts OS framing, native-client stance, key entry points
- `Wiki/Concepts/GSD.md` - phased planning/execution model and relation to roadmap/state workflows
- `Wiki/Concepts/Cursor Rules.md` - mirrored `.cursor/rules` purpose, main rulesets, relation to agent guidance
- `Wiki/Concepts/Graphify.md` - graph workflow role in the vault and `graphify-out/` context
- `Wiki/Concepts/PRD.md` - product requirements document concept and link to execution workflows
- `Wiki/Concepts/ui-ux-pro-max.md` - named design-review skill/workflow and relation to agent skills

---

## [2026-04-13] maintenance | Update CLAUDE.md to reflect new vault structure

Updated `CLAUDE.md` to document the tag-based discovery model, curated Topics/ layer, and new entity rules introduced during this session.

Changes:

- Added Codex to conversation sources list
- Corrected Entities/ folder description (removed Tech/, added Organizations/)
- Added `updated` field to frontmatter schema
- Added "Entity Structure — Tags vs WikiLinks" section with decision table
- Updated Ingest workflow step 4 — generic tech names use tags, not entity page links
- Added `cleanup_stub_links.py` to maintenance scripts list

---

## [2026-04-13] maintenance | Organize \_tools by purpose

Reorganized `_tools/` into purpose-based folders while keeping the documented top-level command paths stable via wrapper scripts.

Changes:

- Added `_tools/frontmatter/`, `_tools/linking/`, `_tools/cleanup/`, `_tools/indexing/`, `_tools/reports/`
- Kept top-level `_tools/*.py` entry points as thin wrappers
- Added `_tools/README.md` documenting the layout
- Added `_tools/.gitignore` for `__pycache__/` and `.pyc`
- Updated `AGENTS.md` and `CLAUDE.md` to explain the new internal layout

---

## [2026-04-13] maintenance | Rewrite Experts App brain vault entry points

Replaced the stale monolithic `CLAUDE.md` and duplicate `AGENTS.md` in `Projects/Experts/Experts App/` with lightweight bridge pages that reflect the correct role of the brain vault vs. the repo.

Pages updated:

- `Projects/Experts/Experts App/CLAUDE.md` — replaced with navigation page: maps live repo files (monorepo root → app level → `.claude/`), links all 16 Topics pages as the WHY layer, documents the sync model
- `Projects/Experts/Experts App/AGENTS.md` — replaced with bridge page: points to live repo AGENTS.md as source of truth, maps Topics pages by feature area, documents session-close pattern for capturing new decisions

---

## [2026-04-13] maintenance | Wire repo CLAUDE.md + AGENTS.md to brain vault

Updated all four repo entry point files to add specific brain vault paths and a Session Close section.

Files updated:

- `/home/logix/experts/CLAUDE.md` — added brain vault paths (entity hub, context pack, rules index, topic table), Session Close section
- `/home/logix/experts/AGENTS.md` — same additions
- `/home/logix/experts/apps/experts-app/CLAUDE.md` — added brain vault paths with full topic-to-file lookup table, Session Close section
- `/home/logix/experts/apps/experts-app/AGENTS.md` — added brain vault paths, Session Close section

Previously: all four files said "use Obsidian notes" with no actual paths. Sessions had no instruction to write decisions back to the vault. Now: every session starts with concrete vault reads and ends with a capture ritual.

---

## [2026-04-13] maintenance | Add coverage_report.py for conversations

New script `_tools/reports/coverage_report.py` audits knowledge-graph coverage across all 780 conversation files.

Findings (first run):

- 11 files (1.4%) fully unprocessed — old ChatGPT off-topic files (2023–2025)
- 316 files (40.5%) fully covered (tagged + entity linked)
- 453 files (58.1%) tagged but no entity WikiLinks — main gap
- Claude/claude-code: 93–100% linked; ChatGPT: only 11% linked
- 0 files linked-but-untagged

Features:

- Per-source breakdown table with progress bars
- 4-quadrant coverage matrix
- Oldest untagged files list (ingest queue)
- Tagged-but-no-link list (quick-win queue)
- `--source`, `--untagged N`, `--no-link N` flags

Also added all report/audit scripts to CLAUDE.md maintenance scripts section.

---

## [2026-04-13] maintenance | Define completed-action archiving convention

Established the archive convention for Action-Tracker.md and documented it as a workflow in CLAUDE.md.

Changes:

- `Action-Tracker.md` — updated instruction note with Status values and archiving rule; added `## Archive` section with 4-column table (`Closed | Owner | Action | Source`) — archive rows are automatically skipped by morning_digest.py and audit_index.py (4 cols < 6 col guard)
- `CLAUDE.md` — added "Workflow: Close an Action" (mark complete → archive → decision follow-up → log)

---

## [2026-04-13] maintenance | Add Review By to Decision-Log + stale decision lint

Added `Review By` column (ISO date) to Decision-Log.md and wired stale-decision checks into both audit tools.

Changes:

- `Decision-Log.md` — added `Review By` column; assigned review dates to all 15 decisions (3 already stale: payout schedule, soft launch scope, launch target — all 12d overdue, relevant to 2026-04-14 meeting)
- `_tools/indexing/audit_index.py` — added `check_stale_decisions()`, `--decisions` flag, stale section shown by default in full audit runs
- `_tools/reports/morning_digest.py` — added `stale_decisions()` and "Stale Decisions" section to daily digest

---

## [2026-04-13] maintenance | Upgrade morning_digest.py to scan Action-Tracker.md

Replaced the memory-file scan in `morning_digest.py` with a direct Action-Tracker.md parser.

Changes to `_tools/reports/morning_digest.py`:

- Added `ACTION_TRACKER` path constant
- Added `_parse_deadline()` — handles ISO dates, month+year strings ("Mid-July 2026"), ASAP
- Added `_parse_tracker_row()` — parses markdown table rows into dicts
- Added `parse_tracker_actions()` — filters active rows by: Critical/High priority, ASAP deadline, or overdue parseable date
- Replaced memory-scan output in `main()` with grouped tracker output (CRITICAL → OVERDUE → ASAP → HIGH)
- Removed now-unused `ACTION_PATTERNS`, `extract_actions_from_memory()`, `scan_memory_index()`

Output verified: 9 actions surface correctly from current Action-Tracker.md

---

## [2026-04-13] maintenance | Remove \_tools wrappers and add shared path detection

Flattened `_tools` usage to real script paths and added shared cross-platform path detection for the vault.

Changes:

- Updated `AGENTS.md` and `CLAUDE.md` to reference internal script paths directly
- Removed top-level wrapper scripts and the `_tools/_run_tool.py` shim
- Added `_tools/shared_paths.py` for shared vault/Raw/memory path detection
- Updated `_tools` scripts to use the shared helper across Windows, macOS, and Linux
- Kept Windows vault support for `%USERPROFILE%\\Desktop\\brain` and a fallback for `%USERPROFILE%\\OneDirive\\Desktop\\brain`
- Kept macOS/Linux vault support for `~/brain`
- Added `BRAIN_RAW_ROOT` override support for raw import paths

## [2026-04-13] maintenance | Add pending-ingest queue to morning digest

Extended `_tools/reports/morning_digest.py` with a `Pending Ingests` section.

Changes:

- Added backlog detection for `Raw/sources/` files older than 24 hours
- Suppresses files already referenced in vault `source_id:` or `source_path:` metadata
- Keeps the existing `New Sources (last 24 h)` section separate from the older ingest backlog

## [2026-04-13] maintenance | Add curated conversation metadata script

Added `_tools/linking/curate_conversation_metadata.py` to rebuild conversation tags and topic links from conversation content instead of stale metadata.

Changes:

- Re-derives canonical `project/*`, `topic/*`, and `tech/*` tags from title + conversation body
- Strips existing `## Links` sections before matching so old wiki links do not reinforce bad tags
- Removes project/person wiki links and rebuilds topic-only links from curated tags
- Suppresses known false positives from path-only matches such as `/home/logix`, `community` app paths, and tool-skill noise
- Normalizes malformed legacy tags like bare `heroui` into canonical prefixed tags such as `tech/heroui`
- Documented the new script in `AGENTS.md`, `CLAUDE.md`, and `_tools/README.md`

## [2026-04-13] maintenance | Add conversation filename shortener

Added `_tools/conversations/shorten_conversation_filenames.py` to shorten imported conversation note filenames while preserving stable uniqueness.

Changes:

- Renames conversation files to `YYYY-MM-DD - short-slug (hash).md`
- Drops repeated source tokens from filenames because the folder already encodes the source
- Builds shorter slugs from note frontmatter titles with path/URL/prompt noise stripped out
- Preserves a short stable hash so similar conversations stay unique
- Updates exact `Conversations/...` wiki links across the vault after rename
- Documented the script in `AGENTS.md`, `CLAUDE.md`, and `_tools/README.md`

## [2026-04-13] maintenance | Enrich top linked thin topic pages

Expanded the most-linked pointer-style topic pages that conversations were already using as hubs.

Pages enriched:

- `Wiki/Concepts/APIs.md`
- `Wiki/Concepts/JavaScript.md`
- `Wiki/Concepts/Node.js.md`
- `Wiki/Concepts/Webhooks.md`
- `Wiki/Concepts/Affiliates.md`
- `Wiki/Concepts/Documentation.md`
- `Wiki/Concepts/Postgres.md`
- `Wiki/Concepts/Marketing.md`
- `Wiki/Concepts/SEO.md`
- `Wiki/Concepts/Testing.md`

Selection was based on current conversation wiki-link frequency among thin pages:

- APIs (191)
- JavaScript (109)
- Node.js (47)
- Webhooks (43)
- Affiliates (41)
- Documentation (40)
- Postgres (31)
- Marketing (27)
- SEO (24)
- Testing (22)

## [2026-04-13] maintenance | Enrich 5 more linked thin topic pages

Expanded a second wave of thin topic pages that still appeared frequently enough in conversation links to deserve real content.

Pages enriched:

- `Wiki/Concepts/AGENTS.md`
- `Wiki/Concepts/CSS.md`
- `Wiki/Concepts/Inertia.js.md`
- `Wiki/Concepts/Analytics.md`
- `Wiki/Concepts/GraphQL.md`

Selection was based on the next most-linked thin pages after the first wave:

- AGENTS.md (21)
- CSS (20)
- Inertia.js (17)
- Analytics (16)
- GraphQL (5)

## [2026-04-13] maintenance | Enrich tech topic pages and replace dead redirects

Expanded the most-used tech topic pages and converted a batch of `Entities/Tech/*` redirect stubs into real notes under `Wiki/Concepts/`.

Pages enriched:

- `Wiki/Concepts/Prisma.md`
- `Wiki/Concepts/Next.js.md`
- `Wiki/Concepts/HeroUI.md`
- `Wiki/Concepts/React.md`
- `Wiki/Concepts/pnpm.md`
- `Wiki/Concepts/Laravel.md`
- `Wiki/Concepts/TypeScript.md`
- `Wiki/Concepts/Docker.md`
- `Wiki/Concepts/shadcn-ui.md`
- `Wiki/Concepts/Vercel.md`
- `Wiki/Concepts/Nginx.md`
- `Wiki/Concepts/ESLint.md`
- `Wiki/Concepts/Prettier.md`
- `Wiki/Concepts/Vitest.md`
- `Wiki/Concepts/Stripe.md`
- `Wiki/Concepts/next-intl.md`
- `Wiki/Concepts/Laravel Sanctum.md`
- `Wiki/Concepts/Tailwind CSS.md`

Selection was guided by current conversation tech-tag frequency, with highest-signal stack pieces prioritized first:

- Prisma (137)
- Next.js / nextjs (117+)
- HeroUI (114)
- React (105)
- pnpm (50)
- Laravel (48)
- Vitest (45)
- Stripe (41)
- ESLint (39)
- Docker (32)
- shadcn-ui (31)
- Vercel (25)
- next-intl (10)

## [2026-04-13] maintenance | Fix stale tech links in Entities index

Updated `Entities/Entities.md` to stop linking to the old nonexistent `Entities/Tech/*` layer.

Changes:

- Repointed `Next.js`, `React`, `TypeScript`, `Prisma`, `Docker`, and `Vercel` to `Wiki/Concepts/*`
- Kept `Postgres` and `Tailwind CSS` under `Wiki/Concepts/*`

## [2026-04-13] maintenance | Expand Entities index to full topic list

Updated `Entities/Entities.md` so the Topics section points to the current full `Wiki/Concepts/*` inventory instead of a tiny partial subset.

Changes:

- Added the rest of the topic and tech-topic pages already present under `Wiki/Concepts/`
- Kept the list aligned with the actual vault structure rather than the removed `Entities/Tech/*` idea

## [2026-04-14] maintenance | Track Experts App v1.1.5 RC in vault + experts Cursor rule

- Created `Projects/Experts/Experts App/reports/release-v1.1.5.md` (stakeholder summary, links to `CHANGELOG.md` / `CHANGELOG_RAW.md` in repo, Google Doc tab).
- Updated `Entities/Projects/Experts App.md` (Releases section), `index.md` (Projects — Documentation table).
- Added `brain-vault-obsidian.mdc` in **experts** monorepo (`.cursor/rules/`) mirroring `apps/experts-app/AGENTS.md` and `CLAUDE.md` vault workflow.

Pages touched: `release-v1.1.5.md`, `Experts App.md`, `index.md`, `Log.md`; repo: `experts/.cursor/rules/brain-vault-obsidian.mdc`

---

## [2026-04-15] ingest | Experts Platform Review — 14 April 2026

Wrote meeting notes for the 14 April 2026 Experts platform review with Adnan Ishgi and Ahmed Zahid. No transcript was available; notes reconstructed from agenda and live codebase audit. Covers 7 topics: app launch readiness assessment (codebase-based), July 2026 launch date confirmation, marketing plan (Adnan), teaser campaign (Ahmed), FutureX.sa registration reminder, Experts portfolio (Adnan), and User Guide (Ahmed Zahid). 12 new actions logged.

Pages touched:

- `Projects/Experts/meetings/experts-14-04-2026.md` (created — client note)
- `Action-Tracker.md` (added 12 new actions from this meeting)
- `index.md` (added meeting to Meetings table)

---

## [2026-04-17] ingest | Experts exams vs quizzes — vault track + implementation status

Captured product criteria (placement, stakes, policy, UX, reporting), the two engineering options (quiz `assessmentKind` vs separate exam entity), and current repo state: `CourseExam` + creator APIs + curriculum inline editor and i18n; no learner flow, policy, cert linkage, or unified quiz kind yet. Linked from [[Entities/Projects/Experts App]]; logged open action and decision row.

Pages touched:

- `Raw/sources/2026-04-17-experts-exams-vs-quizzes-curriculum.md` (created)
- `Entities/Projects/Experts App.md` (Course exams vs quizzes section)
- `Action-Tracker.md` (one new row)
- `Decision-Log.md` (one new row)
- `index.md` (Meetings table)
- `Log.md` (this entry)
---

## [2026-07-15] maintenance | Create brain-v2 clean structure

Created `/home/logix/brain-v2` from `/home/logix/brain` while keeping `/home/logix/brain` unchanged. Applied the cleaner structure: `Raw/`, `Inbox/`, `Wiki/Concepts/`, `Wiki/Summaries/`, typed `Entities/`, `Projects/`, `Actions/`, `Decisions/`, `Agents/`, and `Tools/`.

Pages touched:

- `AGENTS.md`
- `CLAUDE.md`
- `Wiki/Concepts/CRITICAL_FACTS.md`
- `index.md`
- `Log.md`
---

## [2026-07-15] maintenance | Optimize brain-v2 for LLM operations

Added standard operation playbooks, note templates, folder README notes, project-hub LLM entry points, and `Tools/Scripts/vault_lint.py`. Normalized maintained-note frontmatter so the lint contract is enforceable.

Pages touched:

- `AGENTS.md`
- `CLAUDE.md`
- `Wiki/Concepts/CRITICAL_FACTS.md`
- `index.md`
- `Tools/Ops/*`
- `Tools/Templates/*`
- `Tools/Scripts/vault_lint.py`
- folder README notes
- `Entities/Projects/*`
---

## [2026-07-15] maintenance | Enhance Raw evidence layer

Expanded [[Raw]] into a clearer evidence layer with placement rules, source-type guidance, Raw capture operation, Raw-specific templates, `Tools/Scripts/raw_inventory.py`, and a lint guard for daily/scratch-looking notes in Raw.

Pages touched:

- `Raw/Raw.md`
- `Tools/Ops/raw-capture.md`
- `Tools/Templates/raw-meeting.md`
- `Tools/Templates/raw-transcript.md`
- `Tools/Templates/raw-bug.md`
- `Tools/Templates/daily-note.md`
- `Tools/Scripts/raw_inventory.py`
- `Tools/Scripts/vault_lint.py`
- `AGENTS.md`
- `CLAUDE.md`
- `Wiki/Concepts/CRITICAL_FACTS.md`
- `README.md`
- `index.md`
---

## [2026-07-15] maintenance | Remove Raw random bucket

Removed ambiguous `Raw/random/` by relocating its contents to clearer homes: scratch captures to `Inbox/Legacy Random/`, review evidence to `Raw/reviews/`, plans to `Raw/plans/`, research captures to `Raw/research/`, article/system-prompt material to `Raw/articles/`, project source material to `Raw/projects/`, and agent state JSON to `Raw/agent-state/`.

Pages touched:

- `Inbox/Legacy Random/README.md`
- `Inbox/Legacy Random/*`
- `Raw/plans/*`
- `Raw/research/*`
- `Raw/reviews/*`
- `Raw/articles/*`
- `Raw/projects/*`
- `Raw/agent-state/*`
- `index.md`

---

## [2026-07-15] maintenance | Add freshness verification workflow

Added a freshness layer so volatile project and operational pages no longer masquerade as current truth. Current/latest/status queries now route through [[Tools/Ops/verify-current]], high-value hubs carry `freshness`, `verified`, `source_of_truth`, and `verify_with` metadata, and `Tools/Scripts/vault_lint.py` enforces those fields.

Pages touched:

- `Tools/Ops/verify-current.md`
- `Wiki/Concepts/Freshness.md`
- `Wiki/Freshness.md`
- `Tools/Ops/query.md`
- `Tools/Ops/project-update.md`
- `Tools/Ops/README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `Index.md`
- `Wiki/Concepts/CRITICAL_FACTS.md`
- `Entities/Projects/Experts App.md`
- `Entities/Projects/Experts.md`
- `Entities/Projects/Experts OS.md`
- `Entities/Projects/Logix Kernel.md`
- `Actions/Action-Tracker.md`
- `Decisions/Decision-Log.md`
- `Tools/Scripts/vault_lint.py`
