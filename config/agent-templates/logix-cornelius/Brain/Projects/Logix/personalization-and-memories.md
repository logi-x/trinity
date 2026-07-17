---
title: "Logix — Personalization & Agent Memories"
date: "2026-07-11"
updated: "2026-07-11"
up: "[[Entities/Projects/Logix]]"
tags: ["project/logix", "reference", "meta"]
category: "reference"
source: "generated"
source_id: "Projects/Logix/personalization-and-memories.md"
---

↑ [[Entities/Projects/Logix|Logix]]

# Logix — Personalization & Agent Memories

Refined AI-assistant personalization profile and working memories for [[Entities/People/Ahmed Sulaimani|Ahmed Sulaimani]] / [[Entities/Projects/Logix|Logix]]. Use as the durable source for assistant custom-instructions and context.

## Personalization

Entrepreneur and full-stack developer based in Saudi Arabia, and founder of **Logix Digital Solutions Est.** — an all-in-one digital solutions company that empowers e-commerce entrepreneurs and businesses to navigate online digital marketing with ease. Logix provides the tools, resources, and guidance to streamline operations, optimize sales, and maximize ROI for clients.

**Engineering stack.** Builds primarily in TypeScript across Node.js, Next.js, and PostgreSQL, reaching for Python when the job calls for it, and styling with TailwindCSS. Mobile: Swift (iOS) and Kotlin (Android). Go-to infrastructure stack is Docker, Traefik, Redis, and BullMQ, alongside tooling like Prisma, Turborepo, and self-hosted CI.

**Outside of work.** Interests include web development, tennis, and swimming.

**Services Logix provides to clients:**

- **IT Services** — front-end and back-end web development, app development, API development, and UI/UX design.
- **Hosting Services** — cloud hosting and domain & DNS management.
- **Media Buying** — paid campaigns across Facebook, Google, Instagram, LinkedIn, X (Twitter), TikTok, Snapchat, Pinterest, YouTube, Reddit, Twitch, Discord, and more.
- **Creative Services** — logo design, branding, and graphic design.
- **Content Creation** — blog and article writing, social media content, video content, and more.

## Memories

**Overview.** Actively building Logix and its platforms. Most work centers on architecting large, multi-application codebases, sharpening development workflows and infrastructure, and designing polished user experiences — with a strong bias toward long-term maintainability, automation, and high-quality engineering. Alongside the products, runs client-facing digital services and marketing.

**Experts platform.** Flagship project — see [[Entities/Projects/Experts]] / [[Entities/Projects/Experts App]]. A **full-stack Next.js** LMS (`apps/experts-app`): App Router UI, versioned REST APIs under `app/api/v1`, PostgreSQL via Prisma, and NextAuth v5 — a Node ≥22 / pnpm 10 monorepo that also includes workers, realtime, a shared Prisma package, and the native SwiftUI **Experts OS** client. (Older references to a separate Laravel API as the main backend are out of date.) Current focus: expanding infrastructure, refining OpenAPI integration, improving frontend architecture, building finance and reporting features, evolving the AI capabilities, and continuing work on course management, events, community, and related features. Prefers scalable designs and invests heavily in evaluating architecture before implementation.

**Logix Kernel (in progress — `/home/logix/logix-kernel`).** Current build — see [[Entities/Projects/Logix Kernel]]. The **Logix Command Center**, an internal operating system for the business rather than a generic admin app. Turborepo/pnpm monorepo with a Next.js web app plus API, assistant, CLI, MCP, and worker apps, and domain packages (`@logix/domain`, `@logix/permissions`, `@logix/events`, `@logix/sdk`, Prisma DB, etc.). Phase 1 covers auth/RBAC, clients, projects, vault, proposals, invoices, requests, an agents registry, memory, repository metadata, a workflows foundation, search, and dashboard. Principles: typed contracts (TypeScript strict, Zod at boundaries), permissions enforced in the API, domain events + audit logging on important mutations, durable seed data over placeholders, and agent-ready surfaces.

**HOWA — House of Wisdom Academy (shipped — `/home/logix/howa`).** See [[Entities/Projects/HoWA]]. An online education / e-learning platform delivering high-quality online courses to learners of all levels, with a hub for knowledge-sharing and community. Built as a Laravel v13 + Inertia application with separate admin, client, and server apps. Core domain: courses, instructors, students, enrollment orders, invoices and coupons, services, support, and newsletters, plus billing features like refunds and tax calculation. (An ETF/investment module also exists but is a secondary feature slated for deprecation — not part of the core.)

**Development workflow.** Invests heavily in modern engineering practices: Git worktrees, protected long-lived branches, PR-based development, Docker, Traefik, self-hosted GitHub Actions runners, and automated deployments. Continually looks for ways to cut setup time, automate repetitive tasks, and improve code intelligence (code-graph / MCP tooling) so large codebases stay easy to navigate and evolve.

**Product design.** Cares about distinctive interfaces over common templates. For Experts, has explored multiple interactive hero concepts — space-inspired experiences, realistic depth effects, liquid-glass styling, editorial layouts, and other highly polished directions. Favors interfaces that feel modern, interactive, and memorable while staying clean and professional.

**Business.** Operates Logix, a Saudi Arabia–based digital solutions business spanning software engineering, web and mobile development, hosting and infrastructure, UI/UX, creative services, media buying, and marketing. Alongside building the products (Experts, Logix Kernel, HOWA), prepares client documentation, marketing and advertising strategies, and platform capabilities such as campaigns, coupons, and analytics.
