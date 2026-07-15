---
title: "Admin nav is defined once in `admin-nav.ts` as a typed `AdminNavItem[]` array; breadcrumb, sidebar, and grouped nav all "
date: "2026-06-05"
decision: "Admin nav is defined once in `admin-nav.ts` as a typed `AdminNavItem[]` array; breadcrumb, sidebar, and grouped nav all derive from it. No component may hard-code admin nav entries. (Orbit Foundation "
stakeholders: "Logix"
review_by: "2026-09-05"
source: "[[Raw/sources/2026-06-06-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Admin nav is defined once in `admin-nav.ts` as a typed `AdminNavItem[]` array; breadcrumb, sidebar, and grouped nav all derive from it. No component may hard-code admin nav entries. (Orbit Foundation 1a, PR #867)

**Rationale:** Prior admin shell had three sync-prone nav sources (ADMIN_SHELL navItems, AdminNavbar subcomponents, hardcoded sidebar routes). Consolidation is the load-bearing prerequisite for Orbit slices 1b–1d (kit, ⌘K registry, dashboard) — all consume the same nav contract. Any divergence causes silently stale breadcrumbs or dead nav links.

**Stakeholders:** Logix

**Source:** [[Raw/sources/2026-06-06-experts-agent-digest.md]]
