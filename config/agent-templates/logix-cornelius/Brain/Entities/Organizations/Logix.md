---
title: "Logix Inc."
date: "2026-04-13"
tags: ["entity", "organization", "project/logix"]
category: "entity/organization"
source: "generated"
source_id: "Entities/Organizations/Logix.md"
aliases: ["Logix", "Logix Inc.", "logi-x", "Logix, Inc."]
updated: "2026-07-15"
---

# Logix Inc

Software development company founded and owned by [[Entities/People/Ahmed Sulaimani]]. Based in Riyadh, Saudi Arabia. Builds scalable full-stack platforms, SaaS applications, LMS systems, and automation infrastructure primarily for the Saudi and regional market.

---

## Identity

| Field          | Value                                                                  |
| -------------- | ---------------------------------------------------------------------- |
| Legal name     | Logix, Inc.                                                            |
| Domain         | logi-x.org                                                             |
| GitHub         | [logi-x](https://github.com/logi-x)                                    |
| Primary email  | <admin@logi-x.org>                                                     |
| Support email  | <contact@logi-x.org>                                                   |
| Security email | <admin@logi-x.org>                                                     |
| Location       | Sulaiman Al-Ghunaim St., Al-Hokair Center, An Nahdah, Riyadh 13222, SA |
| Founded        | 2023                                                                   |

---

## People

| Person                              | Role                                                       |
| ----------------------------------- | ---------------------------------------------------------- |
| [[Entities/People/Ahmed Sulaimani]] | Founder & CEO — full-stack architect, 10+ years experience |

---

## Virtual Workforce (AI Staff)

Simulated leadership team and specialist personas used for decision simulation — board meetings, architecture reviews, product debates. These are **advisory characters, not real employees**; see [[Entities/Agents/Workforce]] for the full org chart, councils, and decision tiers.

| Tier        | Members                                                                                                                                                                                                                                                                                                                                                   |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Executive   | [[Entities/Agents/Staff/Alexander Morgan\|CEO]], [[Entities/Agents/Staff/Natalie Brooks\|COO]], [[Entities/Agents/Staff/Benjamin Carter\|CFO]], [[Entities/Agents/Staff/Marcus Chen\|CTO]], [[Entities/Agents/Staff/Sophia Bennett\|CPO]], [[Entities/Agents/Staff/Isabella Rossi\|CMO]], [[Entities/Agents/Staff/Rachel Kim\|CLO]]                       |
| Engineering | [[Entities/Agents/Staff/Emma Rodriguez\|Architect]], [[Entities/Agents/Staff/David Hassan\|Backend]], [[Entities/Agents/Staff/Olivia Martinez\|Frontend]], [[Entities/Agents/Staff/Ryan Nakamura\|Mobile]], [[Entities/Agents/Staff/Ethan Brooks\|DevOps]], [[Entities/Agents/Staff/Noah Richardson\|Security]], [[Entities/Agents/Staff/Ava Clarke\|AI]] |
| Experts     | [[Entities/Agents/Staff/Elena Marino\|Education]], [[Entities/Agents/Staff/James Foster\|Community]], [[Entities/Agents/Staff/Marco Ricci\|Events]]                                                                                                                                                                                                       |
| Councils    | [[Entities/Agents/Councils/Executive Council]], [[Entities/Agents/Councils/Technical Council]], [[Entities/Agents/Councils/Experts Council]]                                                                                                                                                                                                              |

---

## Services

| Area                       | Detail                                                                    |
| -------------------------- | ------------------------------------------------------------------------- |
| Web & App Development      | Full-stack Next.js, Laravel, React, Node.js applications                  |
| UI/UX Design & Development | Component systems, HeroUI, Tailwind CSS                                   |
| SaaS Platform Engineering  | Multi-tenant apps, subscription billing, analytics                        |
| LMS & Digital Education    | Course platforms, instructor tools, certificate generation                |
| Payment & Compliance       | Stripe, Noon, Tabby integrations; ZATCA Phase 2 e-invoicing               |
| Real-Time Systems          | WebSockets, SSE, Redis pub/sub, presence and notification infrastructure  |
| Cloud & Infrastructure     | Docker-based environments, Nginx, CI/CD via GitHub Actions, Vercel        |
| Hosting & Domains          | VPS, dedicated server provisioning, SSL, Cloudflare DNS                   |
| Workflow Automation        | N8N-based automation pipelines (see [[Entities/Projects/Logix N8N Core]]) |
| AI & MCP Infrastructure    | MCP server tooling (see [[Entities/Projects/Logix MCP Core]])             |
| SEO & Marketing Tech       | Structured data, sitemaps, OG tags, vector/semantic search                |
| Maintenance & Support      | Ongoing platform maintenance, incident response                           |

---

## Core Tech Stack

### Frontend

- Next.js 16 (App Router), React 19, TypeScript
- Tailwind CSS v4, HeroUI v3, shadcn/ui
- Inertia.js (Laravel apps), SwiftUI (iOS)

### Backend

- Node.js / TypeScript (Next.js API routes, CQRS domain pattern)
- Laravel (PHP) — used in HoWA and legacy projects
- Prisma ORM, PostgreSQL, Redis, BullMQ

### Auth & Security

- NextAuth v5, OAuth (Google, GitHub, Apple), Argon2

### Infrastructure

- Docker + Docker Compose, Nginx, GitHub Actions CI/CD
- Vercel (frontend), self-hosted runners, Buildx for Docker images
- WSL2 for local development

### Testing

- Vitest (unit + integration), Playwright (E2E)

---

## Portfolio

### Client Projects

| Project                       | Client                                         | Status                                    |
| ----------------------------- | ---------------------------------------------- | ----------------------------------------- |
| [[Entities/Projects/Experts]] | [[Entities/Organizations/Experts Company Ltd]] | Active — soft launch target mid-July 2026 |
| [[Entities/Projects/HoWA]]    | House of Wisdom Academy                        | Active                                    |

### Internal Products

| Project                              | Description                              |
| ------------------------------------ | ---------------------------------------- |
| [[Entities/Projects/Logix ETF]]      | ETF tracking and data platform           |
| [[Entities/Projects/Logix MCP Core]] | MCP server infrastructure for AI tooling |
| [[Entities/Projects/Logix N8N Core]] | N8N workflow automation core             |

---

## Architecture Specializations

- **CQRS-influenced domain layer** — commands, handlers, queries, DTOs, mappers per domain; no business logic in routes
- **Multi-tenant SaaS** — tenant-level config, custom domains, subscription billing
- **Real-time infrastructure** — SSE-based updates, Redis pub/sub, presence tracking, leader election between tabs
- **Modular monorepo** — Turborepo + pnpm workspaces; shared packages across apps
- **ZATCA Phase 2** — XML generation, cryptographic signing, QR generation, immutable invoice audit trail
- **i18n** — Arabic / English / Spanish via next-intl; RTL-aware layouts

---

## Domain Expertise

Ahmed combines 10+ years of software engineering with product-minded thinking, enabling Logix to align technical decisions with business outcomes — monetisation, scalability, analytics, and operational efficiency. Deep experience in the Saudi market including ZATCA compliance, regional payment providers (Noon, Tabby), and Arabic-first UX.

---

## Related

- [[Entities/People/Ahmed Sulaimani]] — founder profile
- [[Entities/Projects/Logix]] — portfolio hub (project view)
- [[Projects/Logix/README]] — umbrella docs
- [[Agents/Context Packs/Logix]] — agent context pack
