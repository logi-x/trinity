---
title: "Experts OS"
aliases:
  - experts-os
  - Experts OS — Home
  - Experts platform
  - experts-app
  - Experts monorepo
date: "2026-04-11"
status: "active"
freshness: "volatile"
verified: "2026-06-11"
source_of_truth: "/home/logix/experts"
verify_with:
  - "git log"
  - "GitHub issues and PRs"
tags: ["entity", "projects", "project/experts-os", "swiftui", "ios", "nextjs", "auth", "api", "networking", "design-system", "i18n", "planning", "experts-os-hub", "experts-os-product", "platform-ios", "platform-macos", "topic/swiftui", "topic/swift", "topic/auth", "topic/community", "topic/navigation", "topic/monorepo", "topic/testing", "topic/next-js", "tech/next-js", "theme-native-parity-with-web", "theme-trust-and-polish", "theme-backend-contract"]
category: "Entity/Project"
source: "generated"
source_id: "Entities/Projects/Experts OS.md"
updated: "2026-07-15"
---

# Experts OS (native)

Vault-side hub for the **SwiftUI** native Apple client (**`apps/experts-os`** in the **experts** monorepo): iPhone-first SwiftUI app, shared networking against the Experts Next.js backend (`/api/v1/*`), native auth/session, en/ar/es localization. The backend remains the source of truth. Canonical docs tree: **`Projects/Experts/Experts OS/docs/`** (`code/` symbol notes · `reference/` · `guides/` · Roadmap).

## Links

- [[Entities/Organizations/Experts Company Ltd|Experts Company Ltd]]

## Overview

**Main vault entry** for the native Apple client (**experts-os**). Deep-dive notes live under [[Projects/Experts/Experts OS/docs/reference/Glossary — Experts OS|Projects/Experts/Experts OS docs]] and experts-os rules in this vault (mirrors `apps/experts-os` + `.cursor/rules` where applicable).

#experts-os/hub #experts-os/product #project/experts-os #platform/ios #platform/macos

# Experts OS

Central **map of content** for the Experts LMS SwiftUI client (iOS + macOS). Deep-dive notes live under `Projects/Experts/Experts OS/`; use **Start here** below.

## Experts platform

Umbrella product: an **LMS** (courses, events, community, certificates) aimed at learners and instructors, with a unified web app and native clients.

#project/experts #theme/lms

## experts-app

The **Next.js** application in `apps/experts-app/`: App Router UI, Prisma + PostgreSQL, NextAuth, and **versioned HTTP API** consumed by this client.

#project/experts-app #backend/nextjs #backend/prisma

- Native calls paths under **`/api/v1/*`** (see [[Networking and API — Experts OS]]).
- JSON uses **camelCase** keys aligned with Prisma and app conventions.
- This client does not embed business rules beyond presentation; server remains authoritative.

Primary production host: `app.experts.com.sa` ([[Entities/Places/Saudi Arabia|Saudi Arabia]], [[Entities/Places/Riyadh|Riyadh]] context for product; currency **SAR** on web). Staging: `app.stg.experts.com.sa`.

## Experts monorepo

Git repository **`experts`** at the workspace root: pnpm workflows, `apps/experts-app`, optional `apps/experts-realtime`, and **`apps/experts-os`** for the Apple app.

#project/experts-monorepo

- `apps/experts-app` — see **experts-app** above.
- `apps/experts-os` — Xcode project **`Experts.xcodeproj`** (this app).
- Root `package.json` delegates scripts (e.g. `pnpm experts:dev` for web).

## What this app is

- **Product**: SwiftUI app targeting **iPhone first**, with **macOS** in the same Xcode target (multiplatform). Bundle identifier **`sa.com.experts.lms`**; targets `iphoneos`, `iphonesimulator`, `macosx`.
- **Backend**: [[#experts-app|experts-app]] (**Next.js** API at `/api/v1/*`); no separate mobile-only server.
- **Domain**: Learning and community for [[Entities/Places/Saudi Arabia|Saudi Arabia]]-hosted properties (`experts.com.sa`).

## Product stance

- **iPhone first**; macOS shares the same codebase.
- **Simpler than web** for v1 — see [[Theme — native parity with web]].
- **Backend**: [[#experts-app|experts-app]] only — no duplicate domain logic on device.

## Code map (conceptual)

- `Experts/App/` — `ExpertsApp`, [[ContentView]], [[RootTabView]], [[AuthPresentationStore]].
- `Experts/Core/` — [[SessionStore]], [[AppEnvironment]] (enum), loading helpers.
- `Experts/Networking/` — [[APIClient]], [[ExpertsAPI]], [[APIEndpoint]].
- `Experts/Features/` — Home, Courses, Events, Community, Profile, Auth.
- `Experts/Models/` — Codable DTOs for API responses.
- `Experts/DesignSystem/` — [[Design system — Experts OS]].
- `Experts/Localization/` — [[LocaleStore]].

## App entry

- `ExpertsApp` injects environment objects: [[ThemeManager]], [[LocaleStore]], [[SessionStore]], [[AppEnvironmentStore]], [[AuthPresentationStore]].

## Start here

| Topic             | Note                                        |
| ----------------- | ------------------------------------------- |
| **Docs index**    | [[Projects/Experts/Experts OS/docs/docs\|Experts OS — docs]] (live, by area) |
| Big picture       | [[Architecture — Experts OS]]               |
| API & HTTP        | [[Networking and API — Experts OS]]         |
| Login & tokens    | [[Authentication and session — Experts OS]] |
| Tabs & screens    | [[Features and navigation — Experts OS]]    |
| Colors & layout   | [[Design system — Experts OS]]              |
| Languages & RTL   | [[Localization — Experts OS]]               |
| Dev URLs & builds | [[Environments and tooling — Experts OS]]   |
| Tests             | [[Testing — Experts OS]]                    |
| Planning          | [[Roadmap — Experts OS]]   |
| People            | [[People — Experts OS]]                     |
| Terms             | [[Glossary — Experts OS]]                   |

## Related projects (repo)

- [[Projects/Experts/Experts|Experts vault tree]] — web + API (source of truth for data).
- Code lives under `apps/experts-os/` in the [[#Experts monorepo|Experts monorepo]].

## Recurring themes

- [[Theme — native parity with web]] — #theme/native-parity-with-web
- #theme/trust-and-polish — Session reliability, curated home, demo-ready feel.
- #theme/backend-contract — All shapes come from versioned REST under `/api/v1`.

Also: [[local development]].

## See also

- [[Architecture — Experts OS]]
- [[People — Experts OS]]

- Referenced in conversation notes.
- Represents a recurring workspace/product context.
## LLM Entry Points

- Status: Native app project hub.
- Start here: this entity hub, then the project-local docs below.
- [[Projects/Experts/Experts OS/docs/docs|Experts OS docs]]
- Actions: [[Actions/Action-Tracker]]
- Decisions: [[Decisions/Decision-Log]]

## Update Rules

- Keep this hub concise and durable.
- Put detailed working context under `Projects/`.
- Put reusable ideas under [[Concepts]].
- Put source-derived summaries under [[Summaries]].
