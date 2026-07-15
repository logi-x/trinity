---
title: "Experts App v1.1.5 — release candidate"
date: "2026-04-14"
updated: "2026-04-14"
tags: ["project/experts", "project/experts-app", "topic/release", "docs/changelog"]
category: "Projects/Experts/Experts App/reports"
source: "generated"
source_id: "Projects/Experts/Experts App/reports/release-v1.1.5.md"
---

# Experts App v1.1.5 (release candidate)

**Status:** Release candidate (as of **2026-04-14**).  
**Window (changelog):** **4 April 2026** → **14 April 2026** (see repo pills for “current” if still open).

## Links

- [[Entities/Projects/Experts App|Experts App (entity hub)]]
- [Google Docs — V1.1.5 tab](https://docs.google.com/document/d/1oJb9RHMSWVPRfXk0o43Y-YH1Pn46u7SUL0Kw73v0gkU/edit?pli=1&tab=t.yq3ot18bfy8z)
- **Canonical technical log:** `` `apps/experts-app/public/reports/CHANGELOG_RAW.md` `` (**monorepo root**)
- **Published / client-readable changelog:** `` `apps/experts-app/public/reports/CHANGELOG.md` `` (**monorepo root**)

## Summary (stakeholder-facing)

- **Admin:** New workspace shell — grouped sidebar, header, breadcrumbs, profile-aware layout; **AdminNavbar**; **RTL** on admin sidebar; shared background/sidebar tokens with the main app.
- **Auth & profile:** Forgot-password and **registration** API routes (validation, tests, safer enumeration behaviour); more reliable **profile** loading after session; broad **useApiQuery** migration for authenticated GETs.
- **Payments & enrollments:** Clear UX when **payment captures** but **e-invoice** generation fails; **Enrolled / Registered** badges only when status is **completed** (not pending payment).
- **Community & social:** Thumbnails and **content cards** layout; **follow** lists with better pending/loading states; **presence** indicators and tooltips; **WebSocket** keep-alive / subscription hardening.
- **Markdown / activity:** Mentions and hashtags (including dots in names); timeline items keyboard-accessible without hydration issues.
- **Polish:** Dependency updates (e.g. AWS SDK, HeroUI), modal layering, **Courses** header press behaviour, **EN / AR / ES** copy (e.g. profile completion); staging WS config; dev-only local diagnostics on profile.

## Institutional memory

Decisions and deep dives for this work should also appear on the relevant **Wiki/Concepts/** pages (e.g. [[Wiki/Concepts/WebSockets]], [[Wiki/Concepts/Payments]], [[Wiki/Concepts/Access Control]], [[Wiki/Concepts/Community]], [[Wiki/Concepts/i18n]]) when they change long-lived behaviour — not only in this release note.
