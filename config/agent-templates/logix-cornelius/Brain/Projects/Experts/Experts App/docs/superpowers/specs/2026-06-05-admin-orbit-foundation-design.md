---
title: "2026 06 05 admin orbit foundation design"
date: "2026-06-05"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/specs/2026-06-05-admin-orbit-foundation-design.md"
---
# Admin Redesign — Spec 1: Orbit Foundation

- **Date:** 2026-06-05
- **Status:** Approved (design) — ready for implementation planning
- **Owner:** Admin / Platform
- **App:** `apps/experts-app`
- **Program:** Full `/admin` redesign (shell + all 11 sections). This spec is **slice 1 of 4**.

## Context

The `/admin` area has 11 sections (Dashboard, Users, Certifications, Payments, Affiliates,
Analytics/Views, Revenue, Refunds, Payouts, Events, Health) plus utility pages (Storage,
Embeddings, Processing-fee calculator, Noon webhook test). The route lives under
`app/(i18n)/_shared/admin/**`; the `en/ar/es` route trees are **thin re-export mirrors** of
`_shared` (e.g. `EnglishAdminDashboardPage` just renders the shared `AdminDashboardPage`), so
canonical work happens in `_shared/admin/**` and `src/components/admin/**` — the locale mirrors
need no change.

### Problems in the current admin (verified)

1. **Three overlapping navigation systems** fed by **two divergent lists**:
   - `AdminWorkspaceShell` renders an `AdminSidebar`, a full top `AdminNavbar` (~555 lines), **and**
     a row of quick-link `Tabs`.
   - `AdminShell.tsx` defines `ADMIN_NAV_ITEMS` (11 items incl. Revenue/Refunds/Payouts/Health)
     and passes them down, but `AdminSidebar` ignores the prop and uses its **own hardcoded
     `data.navMain`** (8 items: adds Storage, omits Revenue/Refunds/Payouts/Health). Sidebar and
     tabs therefore show **different sections**.
2. **Placeholder chrome shipped to production** — breadcrumb literally reads
   "Build Your Application → Data Fetching"; a "Cancel / Save changes" button pair renders on every
   page and does nothing.
3. **Dead code inline** — commented-out `AdminHeader`, `AdminSidebarV2`, gradient banners, and a
   duplicated commented `ADMIN_NAV_ITEMS` block in `admin-sidebar.tsx`. Hardcoded `John Doe` /
   `github.com/shadcn.png` user.
4. **Dashboard** composes 8 real data-wired panels but with ad-hoc layout/`DashboardPanel`
   styling and no "what needs me now" triage.

### Design system context

HeroUI v3 (beta) + Tailwind CSS v4, semantic tokens in `app/globals.css`. Palette: blue accent
`oklch(0.58 0.17 255.97)` (`--primary` / `--accent` / `--ring`) on neutral white/near-black
surfaces; destructive `oklch(0.7 0.19 22.23)`. Use semantic tokens (`bg-background`, `bg-card`,
`bg-muted`, `text-foreground`, `text-muted-foreground`, `border-border`, `--primary`) — not
hardcoded colors. Follow the `experts-orbit` shell guidance (flat base rail, raised primary card,
quiet toolbar, productive density) and `experts-ecosystem` for any domain/CQRS code.

## Decisions (locked during brainstorming)

| # | Decision | Choice |
|---|----------|--------|
| Scope of program | full redesign, sliced | Foundation first, then section waves |
| This slice | what we brainstormed | Spec 1 — Orbit Foundation (shell + kit + palette + dashboard) |
| Navigation model | shell shape | **A** — grouped sidebar + quiet top bar |
| Enhancement | jump-to | **B** — ⌘K command palette folded on top of A |
| Visual direction | surface treatment | **B** — elevated workspace card; **C-style dense interiors** |
| Dashboard | depth | **Full new dashboard + new metrics** (read-only queries) |
| ⌘K | scope | **Full-actions architecture** via registry; foundation ships engine + nav + search + starter actions; domain actions land with each section wave |
| Dark mode | parity | **Polish light + dark equally** |

## Goals

- Collapse navigation to **one source of truth**; delete redundant nav systems.
- Rebuild the shell as clean layers (direction B) per `experts-orbit`.
- Ship a reusable **admin design-system kit** every section will consume.
- Ship a **⌘K command palette** with an extensible action registry.
- Rebuild the **dashboard** with scannable KPIs + operations triage.
- Full **light + dark** polish; full **RTL/i18n** correctness.
- Remove all placeholder/dead chrome.

## Non-goals (deferred to waves 2–4)

- Redesigning the *content* (tables/filters/detail views) of the 11 section pages — they inherit
  the new shell + kit now, and are reworked per wave.
- Domain quick-actions beyond the cross-cutting starter set (each lands with its section).
- Any change to auth/permission boundaries (the existing admin guard in `layout.tsx` stays).

## Architecture

### A. Single navigation source of truth

New module **`src/components/admin/admin-nav.ts`** — the only place sections are defined:

```ts
export interface AdminNavItem {
  id: string;
  label: string;            // i18n key, not literal copy
  href: string;
  icon: LucideIcon;
  group: AdminNavGroup;     // "Overview" | "Operations" | "Finance" | "Insights" | "Trust & Safety" | "Tools"
  match?: (pathname: string) => boolean;
}
export const ADMIN_NAV: AdminNavItem[] = [ /* all 11 sections + utility pages, correctly grouped */ ];
export const ADMIN_NAV_GROUPS: AdminNavGroup[] = [ ... ]; // ordering
```

Both `AdminSidebar` and `CommandPalette` consume `ADMIN_NAV`. `AdminShell.tsx` stops defining its
own list.

**Grouping (authoritative):**
- **Overview:** Dashboard
- **Operations:** Users, Certifications, Storage
- **Finance:** Payments, Revenue, Refunds, Payouts, Affiliates
- **Insights:** Analytics (Views)
- **Trust & Safety:** Events, Health
- Utility pages (Embeddings, Processing-fee calculator, Noon webhook test) grouped under a
  collapsed **Tools** group, de-emphasized.

### B. Shell composition (`AdminWorkspaceShell` rebuilt)

Layers, per `experts-orbit`:
- **Base plane:** flat, quiet `AdminSidebar` — grouped nav, logo, ⌘K trigger button, footer
  utilities + **real account cluster** (from session `profile`), "Open website" link.
- **Raised workspace card:** the inset `SidebarInset` becomes the bordered, soft-shadowed primary
  surface; tight seam with the rail (no accidental gutter).
- **Quiet top bar:** sidebar toggle · **real breadcrumb** · global search · ⌘K hint · (account if
  not in sidebar). Remove the fake breadcrumb and the dead Cancel/Save buttons.
- **Page-owned header:** the shell no longer renders a hardcoded page title/actions block. Each
  page renders `<AdminPageHeader/>` itself.

**Breadcrumb derivation:** a `useAdminBreadcrumb(pathname)` helper maps the locale-stripped
pathname against `ADMIN_NAV` → `Admin / {group} / {label} / …`, RTL-aware chevrons.

### C. Reusable design-system kit — `src/components/admin/kit/`

| Primitive | Purpose |
|-----------|---------|
| `AdminPageHeader` | eyebrow + title + description + actions slot (page-owned) |
| `StatCard` | KPI value, label, delta (▲/▼ + %), optional sparkline, optional href/onClick |
| `DataTable` | column defs, sort, pagination, sticky dense header, row actions, RTL |
| `FilterBar` | search input + filter controls row, consistent spacing |
| `EmptyState` | icon + title + description + optional action |
| `LoadingState` | skeleton rows/cards |
| `ErrorState` | error message + retry |
| `DetailDrawer` | right-side (RTL: left) slide-over for record detail |
| `SectionCard` | replaces ad-hoc `DashboardPanel`; header + body, elevation-correct |
| `StatusBadge` | consistent status pills (pending/approved/failed/…), token-driven colors |

All theme-safe (semantic tokens), RTL-correct, demoed on a **`kit-preview`** page (replaces the
existing `sidebar-preview` page).

### D. Command palette (⌘K) + action registry

- **`src/components/admin/command/CommandPalette.tsx`** — HeroUI dialog + list; opens on ⌘K / Ctrl+K
  and via the sidebar trigger; focus-trapped; keyboard navigable; closes on Esc/select.
- **`src/components/admin/command/command-registry.ts`** —
  `registerCommands(commands: AdminCommand[])` / `getCommands()`. `AdminCommand = { id, label,
  group, icon?, keywords?, run: (ctx) => void | Promise<void>, enabled?: (ctx) => boolean }`.
- **Foundation ships:** navigate-to-section (derived from `ADMIN_NAV`), global search (users/content
  via existing `GlobalSearch` data sources), theme toggle, and safe cross-cutting actions
  ("Open website", "Go to Console", "Copy current URL").
- **Extensibility contract:** each section wave calls `registerCommands([...])` for its domain
  actions (e.g. "Approve refund…", "Suspend user…"). Foundation delivers the engine + contract;
  domain wiring ships with the owning section.

### E. New dashboard + metrics

Rebuilt `app/(i18n)/_shared/admin/(dashboard)/page.tsx` on the kit:
- **Hero KPI row** (`StatCard`s with deltas): Revenue (SAR), Active users, New signups,
  Pending refunds, Pending payouts, Pending certifications. The "pending" cards are **triage** —
  click → section (and exposed as ⌘K actions).
- **Revenue trend** (Recharts, existing data) + **gateway/health** panel.
- **Operations triage** panel — counts of items needing admin attention (refunds, payouts, cert
  applications, taken-down events).
- Existing 8 panels' **data wiring preserved**; panels recomposed into the new layout using
  `SectionCard`/`StatCard`.
- **Backend (only backend surface in this slice):** new metrics lacking a query get small
  **read-only** aggregation queries under `src/lib/admin/` (CQRS-style), admin-guarded. The
  implementation plan must **enumerate each new query** and confirm whether an existing
  query/endpoint already covers it before adding one.

## i18n / RTL / a11y

- All new copy via `next-intl` with `en` + `ar` + `es` keys; **no hardcoded strings** (no English
  in Arabic surfaces or vice versa).
- RTL: sidebar side flips, breadcrumb chevrons rotate, palette + drawer mirror, table alignment.
- a11y: ⌘K focus trap + roles, `DataTable` keyboard navigation, visible focus rings, color
  contrast verified in **both** light and dark themes.

## Error handling & edge cases

- Dashboard query failure → `ErrorState` per panel (one panel failing must not blank the page).
- Empty data (e.g. zero pending refunds) → `EmptyState`, and triage KPI shows `0` (not an error).
- Non-admin reaching `/admin` → unchanged: existing `layout.tsx` guard returns `AccessDenied`.
- Palette with no matching command → empty result row, not a crash.
- Hydration: preserve the existing sidebar open/closed `localStorage` persistence behavior.

## Testing strategy

- **Primitives:** render + interaction tests for `StatCard`, `DataTable` (sort/paginate/row action),
  `DetailDrawer` (open/close/focus), `StatusBadge` variants.
- **Palette:** ⌘K open, keyboard nav, search filter, action `run` invoked, Esc closes, registry
  `registerCommands`/`getCommands`.
- **Breadcrumb:** derivation from representative pathnames incl. locale prefix + RTL.
- **Shell:** RTL snapshot; sidebar persistence; account cluster renders session profile.
- **Dashboard queries:** unit tests per new query (correct aggregation, admin-only).
- Gate: `pnpm typecheck:touched -- <files>` during dev; full `pnpm experts:check` before any commit.

## Files

**New**
- `src/components/admin/admin-nav.ts`
- `src/components/admin/kit/{AdminPageHeader,StatCard,DataTable,FilterBar,EmptyState,LoadingState,ErrorState,DetailDrawer,SectionCard,StatusBadge}.tsx`
- `src/components/admin/command/{CommandPalette,command-registry}.ts(x)`
- `src/lib/admin/*` read-only dashboard queries (exact list enumerated in the plan)
- `app/(i18n)/_shared/admin/kit-preview/page.tsx` (replaces `sidebar-preview`)
- i18n message keys for new admin copy (en/ar/es)

**Rebuilt**
- `src/components/admin/AdminWorkspaceShell.tsx` (layers, real breadcrumb, page-owned header, ⌘K)
- `src/components/admin/AdminShell.tsx` (consume `admin-nav.ts`; drop own list)
- `src/components/admin/admin-sidebar.tsx` (consume `admin-nav.ts`; remove commented block; real user)
- `app/(i18n)/_shared/admin/(dashboard)/page.tsx` + `(sections)/*` (recompose on kit; preserve data)

**Deleted / retired**
- `src/components/admin/admin-navbar.tsx` (~555 lines) and `navbar/*` if orphaned
- quick-link `Tabs` block + dead Cancel/Save buttons + commented dead code in shell/sidebar
- `src/components/admin/admin-header.tsx` if unused after rebuild
- `app/(i18n)/_shared/admin/sidebar-preview/page.tsx`
- (verify each deletion with `tsc` + caller grep before removing)

## Risks

| Risk | Mitigation |
|------|------------|
| Deleting navbar/tabs orphans imports | grep callers + `tsc` before delete; delete in same diff as caller updates |
| New dashboard queries touch real data | read-only, admin-guarded, unit-tested |
| HeroUI v3 beta component gaps (palette/table) | check `heroui-react` MCP docs; fall back to React-Aria primitives already in `components/ui` |
| Dark-mode regressions | semantic tokens only; contrast pass both themes; RTL+theme snapshot |
| Scope creep from "full actions" | registry contract bounds foundation to engine + starter actions |

## Decomposition recap (program)

- **Spec 1 (this):** shell + kit + palette engine + dashboard.
- **Wave 2 — Operations:** Users, Certifications (+ Storage). Apply kit, register ⌘K actions, add drawers.
- **Wave 3 — Finance:** Payments, Revenue, Refunds, Payouts, Affiliates.
- **Wave 4 — Insights & Platform:** Analytics/Views, Health, + Tools utility pages.

Each later wave is mostly "apply the kit to this page's data + register actions" → fast.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
