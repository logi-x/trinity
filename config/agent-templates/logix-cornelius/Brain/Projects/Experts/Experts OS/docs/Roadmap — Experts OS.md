---
title: "Roadmap — Experts OS"
date: "2026-04-11"
updated: "2026-07-01"
tags: ["project/experts", "project/experts-os", "topic/planning", "topic/roadmap", "topic/auth", "topic/design-system"]
category: "Projects/Experts/Experts OS"
type: "roadmap"
up: "[[Entities/Projects/Experts OS]]"
---

# Roadmap — Experts OS

↑ [[Entities/Projects/Experts OS|Experts OS]]

Forward planning for [[Entities/Projects/Experts OS]] — the native Apple client for the Experts
platform. This note consolidates what used to live as GSD artifacts under `apps/experts-os/.planning/`
(`PROJECT` / `ROADMAP` / `STATE` / phase plans); the GSD phase machinery has been dissolved into the
outcome-oriented summary below. See also [[Authentication and session — Experts OS]],
[[Architecture — Experts OS]], [[Testing — Experts OS]].

## Scope & constraints

Native Apple client, **iPhone-first**, with shared SwiftUI architecture for future macOS reuse.

- Reuse the existing Experts **Next.js backend as the source of truth** (`/api/v1/*`).
- Keep native **v1 simpler than the web app**.
- Preserve **design parity** with the web brand where practical.

## Current state (snapshot)

- SwiftUI iPhone-first client with **Home, Courses, Events, Community, Profile** tabs.
- Shared networking wired to the backend; **public browsing works**, native **sign-in works** against local.
- App launch opens the tab shell directly; guest auth is entered explicitly from Profile.

**Confirmed decisions:** native v1 stays simpler than web · backend is source of truth · `local`
is a first-class env (but diverges visually from `staging` due to inconsistent seed quality) ·
native `login` exists, but `register` / `forgot-password` are **not yet implemented on the backend**.

**Known gaps:** discovery surfaces feel static/data-heavy · media too vulnerable to extreme local
image aspect ratios · session handling not production-grade (token persistence should move to
**Keychain**) · local debugging too opaque on env/route errors · light verification coverage for
auth, env parity, and visual states.

## Active focus

1. Stabilize native browsing flows and data rendering
2. Harden native authentication and session behavior
3. Improve local/staging environment parity
4. Expand test coverage and polish

## Phase 01 — Bring App To Life

Make the native app feel polished, resilient, and demo-ready while keeping scope appropriate for a
simplified Apple v1. Five workstreams across three waves:

**Wave 1**
- **Discovery & visual vitality** — harden shared media rendering against bad/extreme local assets;
  recompose Home around curated summaries with stronger hierarchy; add polished localized (en/ar/es)
  metadata copy. *Goal: first screen looks like a product, not a prototype.*
- **Native auth & session completion** — add missing backend `register` + `forgot-password` native
  routes (aligned with native `login` envelope, with tests); make session persistence
  production-shaped (Keychain-backed, durable restore, honest guest/loading/auth/unavailable states);
  re-enable the full auth UI only where the backend supports it.
- **Local parity & diagnostics** — in-app local env diagnostics (effective base URL, route health,
  simulator-vs-device guidance); endpoint-aware API error surfacing in debug builds; normalize local
  seed data (sane image dimensions, realistic copy) for credible native QA.

**Wave 2**
- **Productized learner polish** — strengthen cross-screen continuity (tab shell, section headers,
  "see all" paths); increase detail-screen payoff for course/event/community; make Profile a real
  destination for guests and signed-in learners. *No fake CTAs for unsupported write paths.*

**Wave 3**
- **Verification & release confidence** — focused XCTest coverage for auth/session/environment/media;
  preview-driven verification for critical visual states; a `native-qa.md` doc covering local/staging
  runbook, seeded credentials, and the smoke-check path.

## Next phases (candidates)

1. Native auth completion (register / reset end-to-end)
2. Seed/data-quality cleanup for local development
3. Detail-screen and learner-action improvements
4. macOS-specific adaptations

## Links

- [[Entities/Projects/Experts OS]]
- [[Authentication and session — Experts OS]]
