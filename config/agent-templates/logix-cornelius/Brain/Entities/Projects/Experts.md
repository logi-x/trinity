---
title: "Experts"
date: "2026-04-10"
status: "active"
freshness: "volatile"
verified: "2026-06-11"
source_of_truth: "/home/logix/experts"
verify_with:
  - "git log"
  - "GitHub issues and PRs"
  - "Linear"
tags: ["project/experts"]
category: "entity/project"
source: "generated"
source_id: "Entities/Projects/Experts.md"
updated: "2026-07-15"
---

# Experts (vault)

Umbrella folder for **Experts** product notes in this vault:

- **[[Entities/Projects/Experts App|Experts App]]** — Next.js full-stack LMS (web) — docs, guides, rules, working surfaces.
- **[[Entities/Projects/Experts OS|Experts OS]]** — SwiftUI native Apple client — docs, roadmap.

## Organizations

| Role                       | Entity                                         |
| -------------------------- | ---------------------------------------------- |
| Operated by                | [[Entities/Organizations/Experts Company Ltd]] |
| Partner / content provider | [[Entities/Organizations/Samaya]]              |

## Key People

| Person                              | Role                                       |
| ----------------------------------- | ------------------------------------------ |
| [[Entities/People/Ahmed Sulaimani]] | Lead developer                             |
| [[Entities/People/Adnan Ishgi]]     | Founder & CEO (Experts Company Ltd)        |
| [[Entities/People/Ahmed Zahid]]     | Co-founder & CFO (Experts Company Ltd)     |
| [[Entities/People/Saba Lanqa]]      | Founder & CEO (Experts Company Ltd / HoWA) |

## Status Snapshots

| Date                                                         | Summary                                                                                        |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| [[Projects/Experts/snapshots/status-2026-04-13\|2026-04-13]] | Phase 7 in progress; v1.0 shipped; courses/events/billing on critical path to July 2026 launch |

## Links

- [[Entities/Projects/Experts]]
- [[Entities/Projects/Experts App|Experts App]]
- [[Entities/Projects/Experts OS|Experts OS]]
- [[Projects/Experts/DEVELOPER_GUIDE|Developer guide]]
- [[Projects/Experts/CONTRIBUTING|CONTRIBUTING]]

<p align="left"><a href="https://experts.com.sa" target="_blank"><img src="https://i.ibb.co/CJGyzJs/logo-full-512.png" width="400" alt="Experts Logo"></a></p>

[![Experts App CI](https://github.com/logi-x/experts/actions/workflows/experts-app.yml/badge.svg)](https://github.com/logi-x/experts/actions/workflows/experts-app.yml)

[![wakatime](https://wakatime.com/badge/github/logi-x/experts.svg)](https://wakatime.com/badge/github/logi-x/experts)

[![Contribute](https://img.shields.io/badge/Contribute-Guidelines?color=2a86b5)](https://github.com/logi-x/experts/blob/main/CONTRIBUTING.md)
[![Code of Conduct](https://img.shields.io/badge/Code%20of%20Conduct-Conduct?color=2a86b5)](https://github.com/logi-x/experts/blob/main/CODE_OF_CONDUCT.md)
[![License](https://img.shields.io/badge/License-MIT?color=2a86b5)](https://github.com/logi-x/experts/blob/main/LICENSE)

**Vault (Obsidian):** [[Projects/Experts/CONTRIBUTING|CONTRIBUTING]] — use `wikilinks` for vault notes; for repo paths use backticks + root label or GitHub URLs (see brain `` `.cursor/rules/obsidian-wikilinks-vs-repo-paths.mdc` ``).

## Overview

Experts LMS monorepo docs and Cursor-rule mirrors live under [[Entities/Projects/Experts App|Experts App]] in this vault (same content as the `logi-x/experts` clone’s docs + `.cursor/rules`). **Architecture entry point:** [[Projects/Experts/DEVELOPER_GUIDE|Developer guide]].

## What this is

**Experts** is an online learning platform (LMS): courses, enrollments, events, community, certificates, billing, admin and creator tools, and more.

The **primary codebase** here is a **full-stack Next.js application** (`apps/experts-app`): App Router UI, versioned REST APIs under `app/api/v1`, **PostgreSQL** via **Prisma**, and **NextAuth v5**. Older docs that describe a separate Laravel API as the main backend are **out of date** for this repository.

### Documentation

| Doc                                | Audience          |
| ---------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| [[Projects/Experts/DEVELOPER_GUIDE | Developer guide]] | Full monorepo architecture (web, workers, realtime, prisma package, Experts OS), setup, APIs, testing, deploy — **start here** |

## Repository layout

Paths are relative to the **monorepo** checkout on disk. **Vault mirror** of the web app: [[Entities/Projects/Experts App|Experts App]].

| Path                                                                                          | Purpose                                                                                     |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [`apps/experts-app/`](https://github.com/logi-x/experts/tree/main/apps/experts-app)           | Main product — Next.js 16, Prisma, APIs, UI, workers (PDF/ZATCA queues), Vitest, Playwright |
| [`apps/experts-realtime/`](https://github.com/logi-x/experts/tree/main/apps/experts-realtime) | Optional WebSocket gateway (Redis pub/sub)                                                  |
| [`apps/experts-prisma/`](https://github.com/logi-x/experts/tree/main/apps/experts-prisma)     | Optional Prisma migrate/deploy helpers for containers                                       |
| [`apps/experts-os/`](https://github.com/logi-x/experts/tree/main/apps/experts-os)             | Native Experts OS app (Swift / Xcode)                                                       |
| [`docker/`](https://github.com/logi-x/experts/tree/main/docker)                               | Staging / production–oriented compose (not required for default local web dev)              |

| Page                                                                     | Summary                                                                         |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| [[Experts Dashboard]]                                                    | ⚠ Cross-folder triage: overdue actions, open high/critical bugs, decisions due  |
| [[Projects/Experts/Experts App/Bugs & Ops]]                              | Bug tracker (`Raw/bugs/`, 224 notes) + agent/fleet state                        |
| [[Projects/Experts/Experts App/Plans & Sessions]]                        | Implementation plans (`Raw/plans/`) + session/research sources (`Raw/sources/`) |
| [[Projects/Experts/Experts App/docs]]                                    | Experts App curated docs (reference / designs / guides), grouped by area        |
| [[Projects/Experts/Experts App/Experts App Map.canvas\|Experts App Map]] | Visual project map — entry → hubs → architecture → CQRS domains                 |
| [[Projects/Experts/Experts App/Payments Flow.canvas\|Payments Flow]]     | Visual money-flow zoom — checkout → settlement → ZATCA → payout                 |

## Quick start

**Requirements:** Node **≥ 22**, **pnpm 10.x**, PostgreSQL (and Redis if you run queues or realtime).

```bash
pnpm install
cd apps/experts-app
# cp .env.example .env and configure; add .env.test for Vitest — see AGENTS.md
pnpm db:migrate   # or db:push per team practice
pnpm dev # http://localhost:3025
```

From the **repo root**, scripts delegate into the app:

```bash
pnpm experts:dev
pnpm experts:build
pnpm experts:test
pnpm experts:typecheck:tsc
pnpm experts:realtime:dev
```

## Stack (web app)

- **Framework:** Next.js 16 (App Router), React 19, Turbopack dev/build where configured
- **Styling:** Tailwind CSS v4; **HeroUI v3** primary UI; shadcn/Radix fallbacks
- **Data:** PostgreSQL, Prisma 7, `@prisma/adapter-pg`
- **Auth:** NextAuth v5
- **i18n:** next-intl — locales **en**, **ar**, **es** — `` `src/i18n/messages/` `` (relative to **`experts-app`** root)
- **Queues:** BullMQ + Redis (workers in app package)
- **Tests:** Vitest; Playwright for E2E
- **CI:** [`.github/workflows/experts-app.yml`](https://github.com/logi-x/experts/blob/main/.github/workflows/experts-app.yml) (relative to monorepo root)

## Product highlights

- Course catalog, learning flows, quizzes and assignments, certificates
- Events, community, profiles and social features
- Payments (Stripe, regional providers as configured)
- Admin and creator consoles

## Contributing

See [[Projects/Experts/CONTRIBUTING|CONTRIBUTING.md]] (vault) or [CONTRIBUTING on GitHub](https://github.com/logi-x/experts/blob/main/CONTRIBUTING.md). Commit messages: imperative, sentence-case. Prefer `pnpm experts:lint` / `pnpm experts:test` before opening a PR when you change behavior.

## Security

Report vulnerabilities to **admin@logi-x.org** (see section below in license block for contact).

## License

Experts LMS is a proprietary software application developed and owned by **Logix Inc<sup><sub>©</sub></sup>**. This software is licensed, not sold, and its use is subject to the terms and conditions outlined in this license agreement. By installing, accessing, or using Experts LMS, you agree to comply with the following terms:

1. **License grant:** **Logix Inc<sup><sub>©</sub></sup>** grants you a non-exclusive, non-transferable, and limited license to use Experts LMS solely for personal or internal business purposes. You are not permitted to modify, distribute, sublicense, or resell the software or any portion of it.

2. **Restrictions:** You may not reverse engineer, decompile, or disassemble Experts LMS or attempt to derive the source code. Unauthorized reproduction, duplication, distribution, or use of the software outside the terms of this license is strictly prohibited.

3. **Updates and support:** **Logix Inc<sup><sub>©</sub></sup>** may, at its discretion, provide updates, enhancements, or support for Experts LMS. This license does not guarantee access to future versions or support services unless explicitly stated in a separate agreement.

4. **Intellectual property:** All rights, title, and interest in Experts LMS, including any intellectual property rights, remain the sole property of **Logix Inc<sup><sub>©</sub></sup>**. This license does not grant you any rights to trademarks, service marks, or logos associated with Experts LMS.

5. **Termination:** This license is effective until terminated. Your rights under this license will terminate automatically without notice if you fail to comply with any of its terms. Upon termination, you must cease all use of Experts LMS and destroy all copies in your possession.

6. **Disclaimer of warranty:** Experts LMS is provided "as is" without warranty of any kind, either express or implied. **Logix Inc<sup><sub>©</sub></sup>** does not warrant that the software will be error-free or uninterrupted.

7. **Limitation of liability:** In no event shall **Logix Inc<sup><sub>©</sub></sup>** be liable for any damages arising out of the use or inability to use Experts LMS, including but not limited to lost profits, business interruption, or loss of data.

By using Experts LMS, you acknowledge that you have read, understood, and agreed to be bound by the terms of this license agreement. If you do not agree to these terms, you must not install, use, or access Experts LMS.

## Contact

Questions or support: [admin@logi-x.org](mailto:admin@logi-x.org).

## Contributors

- Ahmed Sulaimani — [@xcode-it](https://github.com/xcode-it) — [![wakatime](https://wakatime.com/badge/user/7fd023f4-368a-4fe7-8bc6-31deba4218b5.svg)](https://wakatime.com/@7fd023f4-368a-4fe7-8bc6-31deba4218b5)
## LLM Entry Points

- Status: Main Experts platform project hub.
- Start here: this entity hub, then the project-local docs below.
- [[Projects/Experts/Experts]]
- [[Projects/Experts/Experts Dashboard]]
- [[Projects/Experts/Experts App/Bugs & Ops]]
- [[Projects/Experts/Experts App/Plans & Sessions]]
- Actions: [[Actions/Action-Tracker]]
- Decisions: [[Decisions/Decision-Log]]

## Update Rules

- Keep this hub concise and durable.
- Put detailed working context under `Projects/`.
- Put reusable ideas under [[Concepts]].
- Put source-derived summaries under [[Summaries]].
