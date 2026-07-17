---
title: "2026 06 05 admin orbit foundation 1a nav and shell"
date: "2026-06-05"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/plans/2026-06-05-admin-orbit-foundation-1a-nav-and-shell.md"
---
# Admin Orbit Foundation — Plan 1a: Navigation Source of Truth + Shell

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Collapse the three competing admin nav systems into one source of truth and rebuild the admin shell as clean layers with a real breadcrumb and real page header — removing all placeholder/dead chrome.

**Architecture:** A single `admin-nav.ts` module defines every admin destination and its group. The rebuilt `AdminSidebar` (flat base rail, grouped) and `AdminWorkspaceShell` (raised workspace card, quiet top bar) both consume it. A pure `deriveAdminBreadcrumb()` function maps the locale-stripped pathname to breadcrumb segments. The 555-line `admin-navbar.tsx`, the quick-link tabs, the fake breadcrumb, and the dead "Cancel/Save" buttons are deleted.

**Tech Stack:** Next.js 16 (App Router, `_shared` canonical routes), React 19, HeroUI v3 (beta) + Tailwind v4, `next-intl`, the in-repo `components/ui/sidebar` (shadcn-style) primitive, Vitest + Testing Library, lucide-react icons.

**Scope note:** This is plan **1a of 4** for the Orbit Foundation slice (see spec `docs/superpowers/specs/2026-06-05-admin-orbit-foundation-design.md`). Plans 1b (kit primitives), 1c (⌘K command palette), 1d (dashboard + queries) follow. The reusable `AdminPageHeader` arrives in 1b; until then the shell renders a correct title block derived from `ADMIN_NAV` (real data, not a placeholder), so 1a ships a coherent shell on its own. The ⌘K trigger button is added in 1c to avoid shipping a dead control here.

---

## File Structure

| File | Responsibility |
|------|----------------|
| `src/components/admin/admin-nav.ts` (new) | The only definition of admin sections, groups, and group order. Consumed by sidebar, breadcrumb, and (later) the palette. |
| `src/components/admin/admin-breadcrumb.ts` (new) | Pure `deriveAdminBreadcrumb(pathname, locale)` → segments. No React, fully unit-testable. |
| `src/components/admin/admin-sidebar.tsx` (rebuild) | Flat grouped base rail driven by `ADMIN_NAV`; real account cluster; commented dead block removed. |
| `src/components/admin/AdminWorkspaceShell.tsx` (rebuild) | Layered shell: raised workspace card, quiet top bar with real breadcrumb + derived title block. No navbar/tabs/fake-breadcrumb/dead-buttons. |
| `src/components/admin/AdminShell.tsx` (modify) | Stop defining its own nav list; pass `profile` through. |
| `src/i18n/messages/{en,ar,es}/admin.json` (modify) | New `admin.nav.*` (group + section labels) and `admin.shell.*` keys. |
| `src/components/admin/admin-navbar.tsx` + `navbar/*` (delete if orphaned) | Removed redundant nav system. |
| `src/components/admin/admin-header.tsx` (delete if unused) | Removed dead chrome. |
| `app/(i18n)/_shared/admin/sidebar-preview/page.tsx` (delete) | Dead preview page (replaced by `kit-preview` in 1b). |
| `src/components/admin/__tests__/*` (new) | Unit tests for nav + breadcrumb + shell render. |

---

## Task 1: Single navigation source of truth (`admin-nav.ts`)

**Files:**
- Create: `apps/experts-app/src/components/admin/admin-nav.ts`
- Test: `apps/experts-app/src/components/admin/__tests__/admin-nav.test.ts`

- [ ] **Step 1: Write the failing test**

```ts
// apps/experts-app/src/components/admin/__tests__/admin-nav.test.ts
import {describe, it, expect} from "vitest";
import {ADMIN_NAV, ADMIN_NAV_GROUPS, findActiveNavItem} from "../admin-nav";

describe("ADMIN_NAV", () => {
  it("has a unique id and href per item", () => {
    const ids = ADMIN_NAV.map((i) => i.id);
    const hrefs = ADMIN_NAV.map((i) => i.href);
    expect(new Set(ids).size).toBe(ids.length);
    expect(new Set(hrefs).size).toBe(hrefs.length);
  });

  it("only uses declared groups, and every group is represented", () => {
    const used = new Set(ADMIN_NAV.map((i) => i.group));
    for (const item of ADMIN_NAV) {
      expect(ADMIN_NAV_GROUPS).toContain(item.group);
    }
    for (const group of ADMIN_NAV_GROUPS) {
      expect(used.has(group)).toBe(true);
    }
  });

  it("includes every real admin destination", () => {
    const hrefs = ADMIN_NAV.map((i) => i.href);
    for (const href of [
      "/admin",
      "/admin/users",
      "/admin/certifications",
      "/admin/storage",
      "/admin/payments",
      "/admin/revenue",
      "/admin/refunds",
      "/admin/payouts",
      "/admin/affiliates",
      "/admin/views",
      "/admin/events",
      "/admin/health",
    ]) {
      expect(hrefs).toContain(href);
    }
  });

  it("matches the dashboard only on exact /admin", () => {
    expect(findActiveNavItem("/admin")?.id).toBe("dashboard");
    expect(findActiveNavItem("/admin/users")?.id).toBe("users");
    expect(findActiveNavItem("/admin/users/123")?.id).toBe("users");
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/__tests__/admin-nav.test.ts`
Expected: FAIL — cannot resolve `../admin-nav`.

- [ ] **Step 3: Write minimal implementation**

```ts
// apps/experts-app/src/components/admin/admin-nav.ts
import type {LucideIcon} from "lucide-react";
import {
  BadgeCheck,
  BarChart3,
  CalendarClock,
  CreditCard,
  HandCoins,
  HardDrive,
  LayoutDashboard,
  Plug,
  Receipt,
  Share2,
  ShieldAlert,
  TrendingUp,
  Users,
  Wallet,
} from "lucide-react";

export type AdminNavGroup =
  | "Overview"
  | "Operations"
  | "Finance"
  | "Insights"
  | "Trust & Safety"
  | "Tools";

export const ADMIN_NAV_GROUPS: readonly AdminNavGroup[] = [
  "Overview",
  "Operations",
  "Finance",
  "Insights",
  "Trust & Safety",
  "Tools",
] as const;

export interface AdminNavItem {
  id: string;
  /** i18n key under `admin.nav.items`, e.g. "dashboard" → admin.nav.items.dashboard */
  labelKey: string;
  href: string;
  icon: LucideIcon;
  group: AdminNavGroup;
  /** Optional custom active matcher; defaults to exact-or-prefix on href. */
  match?: (pathname: string) => boolean;
}

export const ADMIN_NAV: readonly AdminNavItem[] = [
  {id: "dashboard", labelKey: "dashboard", href: "/admin", icon: LayoutDashboard, group: "Overview", match: (p) => p === "/admin"},

  {id: "users", labelKey: "users", href: "/admin/users", icon: Users, group: "Operations"},
  {id: "certifications", labelKey: "certifications", href: "/admin/certifications", icon: BadgeCheck, group: "Operations"},
  {id: "storage", labelKey: "storage", href: "/admin/storage", icon: HardDrive, group: "Operations"},

  {id: "payments", labelKey: "payments", href: "/admin/payments", icon: CreditCard, group: "Finance"},
  {id: "revenue", labelKey: "revenue", href: "/admin/revenue", icon: TrendingUp, group: "Finance"},
  {id: "refunds", labelKey: "refunds", href: "/admin/refunds", icon: HandCoins, group: "Finance"},
  {id: "payouts", labelKey: "payouts", href: "/admin/payouts", icon: Wallet, group: "Finance"},
  {id: "affiliates", labelKey: "affiliates", href: "/admin/affiliates", icon: Share2, group: "Finance"},

  {id: "views", labelKey: "views", href: "/admin/views", icon: BarChart3, group: "Insights"},

  {id: "events", labelKey: "events", href: "/admin/events", icon: CalendarClock, group: "Trust & Safety"},
  {id: "health", labelKey: "health", href: "/admin/health", icon: ShieldAlert, group: "Trust & Safety"},

  {id: "processing-fee", labelKey: "processingFee", href: "/admin/processing-fee-calculator", icon: Receipt, group: "Tools"},
  {id: "noon-webhook", labelKey: "noonWebhook", href: "/admin/noon-webhook-test", icon: Plug, group: "Tools"},
] as const;

function isActive(item: AdminNavItem, pathname: string): boolean {
  if (item.match) return item.match(pathname);
  return pathname === item.href || pathname.startsWith(`${item.href}/`);
}

/** Find the active nav item for a locale-stripped pathname (e.g. "/admin/users"). */
export function findActiveNavItem(pathname: string): AdminNavItem | undefined {
  // Prefer the most specific (longest href) match so /admin doesn't shadow /admin/users.
  return [...ADMIN_NAV]
    .filter((item) => isActive(item, pathname))
    .sort((a, b) => b.href.length - a.href.length)[0];
}

/** Items grouped in `ADMIN_NAV_GROUPS` order, omitting empty groups. */
export function groupedAdminNav(): {group: AdminNavGroup; items: AdminNavItem[]}[] {
  return ADMIN_NAV_GROUPS.map((group) => ({
    group,
    items: ADMIN_NAV.filter((item) => item.group === group),
  })).filter((g) => g.items.length > 0);
}
```

> Note: `Receipt` and `Plug` are valid lucide-react icons. If `pnpm typecheck` reports either is missing in the installed lucide-react version, substitute `Calculator` (processing-fee) and `Webhook` (noon-webhook), which are also valid.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/__tests__/admin-nav.test.ts`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add apps/experts-app/src/components/admin/admin-nav.ts apps/experts-app/src/components/admin/__tests__/admin-nav.test.ts
git commit -m "feat(admin): single nav source of truth (admin-nav.ts)"
```

---

## Task 2: Breadcrumb derivation (`admin-breadcrumb.ts`)

**Files:**
- Create: `apps/experts-app/src/components/admin/admin-breadcrumb.ts`
- Test: `apps/experts-app/src/components/admin/__tests__/admin-breadcrumb.test.ts`

- [ ] **Step 1: Write the failing test**

```ts
// apps/experts-app/src/components/admin/__tests__/admin-breadcrumb.test.ts
import {describe, it, expect} from "vitest";
import {deriveAdminBreadcrumb} from "../admin-breadcrumb";

describe("deriveAdminBreadcrumb", () => {
  it("returns Admin > group > section for a known section", () => {
    const crumbs = deriveAdminBreadcrumb("/en/admin/users", "en");
    expect(crumbs).toEqual([
      {labelKey: "admin.nav.root", href: "/admin"},
      {groupLabelKey: "admin.nav.groups.Operations"},
      {labelKey: "admin.nav.items.users", href: "/admin/users", current: true},
    ]);
  });

  it("returns only the root crumb on the dashboard", () => {
    const crumbs = deriveAdminBreadcrumb("/en/admin", "en");
    expect(crumbs).toEqual([{labelKey: "admin.nav.root", href: "/admin", current: true}]);
  });

  it("strips any locale prefix (ar, es)", () => {
    expect(deriveAdminBreadcrumb("/ar/admin/refunds", "ar").at(-1)).toMatchObject({
      labelKey: "admin.nav.items.refunds",
      current: true,
    });
  });

  it("falls back to the root crumb for an unknown admin path", () => {
    expect(deriveAdminBreadcrumb("/en/admin/does-not-exist", "en")).toEqual([
      {labelKey: "admin.nav.root", href: "/admin", current: true},
    ]);
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/__tests__/admin-breadcrumb.test.ts`
Expected: FAIL — cannot resolve `../admin-breadcrumb`.

- [ ] **Step 3: Write minimal implementation**

```ts
// apps/experts-app/src/components/admin/admin-breadcrumb.ts
import {findActiveNavItem} from "./admin-nav";

export type AdminBreadcrumb =
  | {labelKey: string; href: string; current?: boolean}
  | {groupLabelKey: string};

/** Remove a leading "/<locale>" segment so paths match ADMIN_NAV hrefs. */
function stripLocale(pathname: string, locale: string): string {
  const prefix = `/${locale}`;
  if (pathname === prefix) return "/";
  if (pathname.startsWith(`${prefix}/`)) return pathname.slice(prefix.length) || "/";
  return pathname;
}

export function deriveAdminBreadcrumb(pathname: string, locale: string): AdminBreadcrumb[] {
  const path = stripLocale(pathname, locale);
  const item = findActiveNavItem(path);

  if (!item || item.href === "/admin") {
    return [{labelKey: "admin.nav.root", href: "/admin", current: true}];
  }

  return [
    {labelKey: "admin.nav.root", href: "/admin"},
    {groupLabelKey: `admin.nav.groups.${item.group}`},
    {labelKey: `admin.nav.items.${item.labelKey}`, href: item.href, current: true},
  ];
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/__tests__/admin-breadcrumb.test.ts`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add apps/experts-app/src/components/admin/admin-breadcrumb.ts apps/experts-app/src/components/admin/__tests__/admin-breadcrumb.test.ts
git commit -m "feat(admin): pure breadcrumb derivation from admin-nav"
```

---

## Task 3: i18n keys for nav + shell (en, ar, es)

**Files:**
- Modify: `apps/experts-app/src/i18n/messages/en/admin.json`
- Modify: `apps/experts-app/src/i18n/messages/ar/admin.json`
- Modify: `apps/experts-app/src/i18n/messages/es/admin.json`

- [ ] **Step 1: Add the `nav` and `shell` blocks to `en/admin.json`**

Add these two top-level keys inside the root object of `src/i18n/messages/en/admin.json` (alongside `metadata`, `affiliates`, …):

```json
"nav": {
  "root": "Admin",
  "groups": {
    "Overview": "Overview",
    "Operations": "Operations",
    "Finance": "Finance",
    "Insights": "Insights",
    "Trust & Safety": "Trust & Safety",
    "Tools": "Tools"
  },
  "items": {
    "dashboard": "Dashboard",
    "users": "Users",
    "certifications": "Certifications",
    "storage": "Storage",
    "payments": "Payments",
    "revenue": "Revenue",
    "refunds": "Refunds",
    "payouts": "Payouts",
    "affiliates": "Affiliates",
    "views": "Analytics",
    "events": "Events",
    "health": "Health",
    "processingFee": "Processing-fee calculator",
    "noonWebhook": "Noon webhook test"
  }
},
"shell": {
  "brand": "Experts",
  "openWebsite": "Open website",
  "toggleSidebar": "Toggle sidebar",
  "searchPlaceholder": "Search…",
  "account": "Account"
}
```

- [ ] **Step 2: Add the Arabic translations to `ar/admin.json`**

```json
"nav": {
  "root": "لوحة التحكم",
  "groups": {
    "Overview": "نظرة عامة",
    "Operations": "العمليات",
    "Finance": "المالية",
    "Insights": "التحليلات",
    "Trust & Safety": "الأمان والموثوقية",
    "Tools": "الأدوات"
  },
  "items": {
    "dashboard": "اللوحة الرئيسية",
    "users": "المستخدمون",
    "certifications": "الاعتمادات",
    "storage": "التخزين",
    "payments": "المدفوعات",
    "revenue": "الإيرادات",
    "refunds": "المبالغ المستردة",
    "payouts": "المدفوعات للمنشئين",
    "affiliates": "المسوّقون",
    "views": "الإحصاءات",
    "events": "الفعاليات",
    "health": "الحالة",
    "processingFee": "حاسبة رسوم المعالجة",
    "noonWebhook": "اختبار Noon webhook"
  }
},
"shell": {
  "brand": "Experts",
  "openWebsite": "فتح الموقع",
  "toggleSidebar": "تبديل الشريط الجانبي",
  "searchPlaceholder": "بحث…",
  "account": "الحساب"
}
```

- [ ] **Step 3: Add the Spanish translations to `es/admin.json`**

```json
"nav": {
  "root": "Administración",
  "groups": {
    "Overview": "Resumen",
    "Operations": "Operaciones",
    "Finance": "Finanzas",
    "Insights": "Analíticas",
    "Trust & Safety": "Confianza y seguridad",
    "Tools": "Herramientas"
  },
  "items": {
    "dashboard": "Panel",
    "users": "Usuarios",
    "certifications": "Certificaciones",
    "storage": "Almacenamiento",
    "payments": "Pagos",
    "revenue": "Ingresos",
    "refunds": "Reembolsos",
    "payouts": "Pagos a creadores",
    "affiliates": "Afiliados",
    "views": "Analíticas",
    "events": "Eventos",
    "health": "Estado",
    "processingFee": "Calculadora de comisiones",
    "noonWebhook": "Prueba de webhook Noon"
  }
},
"shell": {
  "brand": "Experts",
  "openWebsite": "Abrir sitio web",
  "toggleSidebar": "Alternar barra lateral",
  "searchPlaceholder": "Buscar…",
  "account": "Cuenta"
}
```

- [ ] **Step 4: Verify JSON validity**

Run: `cd apps/experts-app && node -e "['en','ar','es'].forEach(l=>{const m=require('./src/i18n/messages/'+l+'/admin.json'); if(!m.nav?.items?.dashboard||!m.shell?.brand) throw new Error('missing keys in '+l); }); console.log('ok')"`
Expected: prints `ok`.

- [ ] **Step 5: Commit**

```bash
git add apps/experts-app/src/i18n/messages/en/admin.json apps/experts-app/src/i18n/messages/ar/admin.json apps/experts-app/src/i18n/messages/es/admin.json
git commit -m "i18n(admin): nav + shell keys (en/ar/es)"
```

---

## Task 4: Rebuild `AdminSidebar` on `ADMIN_NAV`

**Files:**
- Modify (rebuild): `apps/experts-app/src/components/admin/admin-sidebar.tsx`
- Test: `apps/experts-app/src/components/admin/__tests__/admin-sidebar.test.tsx`

**Context:** The current sidebar hardcodes `data.navMain` (out of sync with the tabs), keeps a large commented-out `ADMIN_NAV_ITEMS` block, and a fake `John Doe` user. It uses the in-repo `components/ui/sidebar` primitive (exports `Sidebar`, `SidebarContent`, `SidebarHeader`, `SidebarFooter`, `SidebarGroup`, `SidebarGroupLabel`, `SidebarMenu`, `SidebarMenuItem`, `SidebarMenuButton`). Keep the `/console` sub-nav (`AdminNavConsole` from `./navbar/console`) — Console is a separate destination still in use.

- [ ] **Step 1: Write the failing test**

```tsx
// apps/experts-app/src/components/admin/__tests__/admin-sidebar.test.tsx
import {describe, it, expect, vi} from "vitest";
import {render, screen} from "@testing-library/react";
import {NextIntlClientProvider} from "next-intl";
import {AdminSidebar} from "../admin-sidebar";
import {SidebarProvider} from "@/components/ui/sidebar";
import enAdmin from "@/i18n/messages/en/admin.json";

vi.mock("next/navigation", () => ({usePathname: () => "/en/admin/users"}));

function renderSidebar() {
  return render(
    <NextIntlClientProvider locale="en" messages={{admin: enAdmin}}>
      <SidebarProvider>
        <AdminSidebar />
      </SidebarProvider>
    </NextIntlClientProvider>,
  );
}

describe("AdminSidebar", () => {
  it("renders every nav group label", () => {
    renderSidebar();
    for (const label of ["Operations", "Finance", "Insights", "Trust & Safety"]) {
      expect(screen.getByText(label)).toBeInTheDocument();
    }
  });

  it("renders the active section (Users) link", () => {
    renderSidebar();
    expect(screen.getByRole("link", {name: /Users/})).toHaveAttribute("href", expect.stringContaining("/admin/users"));
  });

  it("does not render the hardcoded placeholder user", () => {
    renderSidebar();
    expect(screen.queryByText("John Doe")).not.toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/__tests__/admin-sidebar.test.tsx`
Expected: FAIL — current sidebar renders `data.navMain` group labels but not grouped via `groupedAdminNav`, and "John Doe" exists in the file (the test asserting its absence fails) / group labels like "Insights" missing.

- [ ] **Step 3: Rebuild the implementation**

```tsx
// apps/experts-app/src/components/admin/admin-sidebar.tsx
"use client";

import * as React from "react";
import {ExternalLink, Sparkles} from "lucide-react";
import {usePathname} from "next/navigation";
import {useTranslations} from "next-intl";
import {Link} from "@/i18n/routing";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import {GlobalSearch} from "../GlobalSearch";
import {useIsRTL} from "@/hooks/use-is-rtl";
import {cn} from "@/lib/utils";
import {groupedAdminNav, findActiveNavItem} from "./admin-nav";
import {AdminNavConsole} from "./navbar/console";

const CONSOLE_NAV = [
  {
    id: "console-main",
    title: "Console",
    url: "/console",
    items: [
      {id: "console-diagnostics-stream", title: "Diagnostics Stream", url: "/console"},
      {id: "console-system-status", title: "System Status", url: "/console/status"},
      {id: "console-changelog", title: "Changelog", url: "/console/changelog"},
    ],
  },
];

function stripLocale(pathname: string, locale: string): string {
  const prefix = `/${locale}`;
  if (pathname === prefix) return "/";
  if (pathname.startsWith(`${prefix}/`)) return pathname.slice(prefix.length) || "/";
  return pathname;
}

export function AdminSidebar({...props}: React.ComponentProps<typeof Sidebar>) {
  const {dir, isRTL} = useIsRTL();
  const t = useTranslations("admin");
  const pathname = usePathname();
  // next-intl Link strips locale; usePathname includes it. Strip the first segment.
  const locale = pathname.split("/").filter(Boolean)[0] ?? "en";
  const activePath = stripLocale(pathname, locale);
  const activeId = findActiveNavItem(activePath)?.id;
  const groups = groupedAdminNav();

  return (
    <Sidebar
      dir={dir}
      side={isRTL ? "right" : "left"}
      variant="inset"
      {...props}
      className="bg-background max-h-screen overflow-hidden"
    >
      <SidebarHeader className="gap-4 px-4 pt-6 pb-3">
        <Link href="/admin" className="flex items-center gap-3">
          <div className="bg-foreground text-background flex h-9 w-9 items-center justify-center rounded-xl shadow-sm">
            <Sparkles className="h-4 w-4" />
          </div>
          <p className="text-foreground truncate text-base font-semibold tracking-tight">
            {t("shell.brand")}
          </p>
        </Link>
        <GlobalSearch />
      </SidebarHeader>

      <SidebarContent className="px-3 pb-4">
        {groups.map(({group, items}) => (
          <SidebarGroup key={group}>
            <SidebarGroupLabel>{t(`nav.groups.${group}`)}</SidebarGroupLabel>
            <SidebarMenu>
              {items.map((item) => {
                const Icon = item.icon;
                const isActive = item.id === activeId;
                return (
                  <SidebarMenuItem key={item.id}>
                    <SidebarMenuButton asChild isActive={isActive} tooltip={t(`nav.items.${item.labelKey}`)}>
                      <Link href={item.href} className={cn("flex items-center gap-2.5")}>
                        <Icon className="h-4 w-4 shrink-0" />
                        <span className="truncate">{t(`nav.items.${item.labelKey}`)}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroup>
        ))}
        <AdminNavConsole items={CONSOLE_NAV} />
      </SidebarContent>

      <SidebarFooter className="border-border/60 space-y-3 border-t px-4 py-4">
        <Link
          href="/"
          className="text-muted-foreground hover:text-foreground flex h-9 items-center gap-2.5 rounded-xl px-2 text-sm font-medium transition"
        >
          <ExternalLink className="h-4 w-4 shrink-0" />
          {t("shell.openWebsite")}
        </Link>
      </SidebarFooter>
    </Sidebar>
  );
}
```

> If `AdminNavConsole`'s prop type does not match `CONSOLE_NAV` (check `./navbar/console.tsx` for its exact `items` shape — it currently accepts `{id,title,url,icon?,items?}`), add an `icon: Terminal` field from `lucide-react` to the console entry to satisfy the type. Run `pnpm typecheck:touched -- src/components/admin/admin-sidebar.tsx` to confirm.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/__tests__/admin-sidebar.test.tsx`
Expected: PASS (3 tests). If `SidebarMenuButton`'s `isActive`/`tooltip`/`asChild` props differ, read `src/components/ui/sidebar.tsx` around the `SidebarMenuButton` definition and adjust prop names to match.

- [ ] **Step 5: Typecheck the touched file**

Run: `cd apps/experts-app && pnpm typecheck:touched -- src/components/admin/admin-sidebar.tsx`
Expected: no errors.

- [ ] **Step 6: Commit**

```bash
git add apps/experts-app/src/components/admin/admin-sidebar.tsx apps/experts-app/src/components/admin/__tests__/admin-sidebar.test.tsx
git commit -m "feat(admin): grouped sidebar driven by admin-nav, drop placeholder user"
```

---

## Task 5: Rebuild `AdminWorkspaceShell` (layers, real breadcrumb, real header)

**Files:**
- Modify (rebuild): `apps/experts-app/src/components/admin/AdminWorkspaceShell.tsx`
- Test: `apps/experts-app/src/components/admin/__tests__/admin-workspace-shell.test.tsx`

**Context:** Remove `AdminNavbar`, the quick-link `Tabs`, the fake "Build Your Application / Data Fetching" breadcrumb, and the dead "Cancel / Save changes" buttons. Render a real breadcrumb from `deriveAdminBreadcrumb` and a title block from the active `ADMIN_NAV` item (label + group; descriptions move to i18n later — for 1a use the group + label only, no invented copy). Keep `SidebarProvider`/`SidebarInset` layering and the existing `localStorage` open/close persistence.

- [ ] **Step 1: Write the failing test**

```tsx
// apps/experts-app/src/components/admin/__tests__/admin-workspace-shell.test.tsx
import {describe, it, expect, vi} from "vitest";
import {render, screen} from "@testing-library/react";
import {NextIntlClientProvider} from "next-intl";
import {AdminWorkspaceShell} from "../AdminWorkspaceShell";
import enAdmin from "@/i18n/messages/en/admin.json";

vi.mock("next/navigation", () => ({
  usePathname: () => "/en/admin/users",
  useRouter: () => ({push: vi.fn()}),
}));

function renderShell() {
  return render(
    <NextIntlClientProvider locale="en" messages={{admin: enAdmin}}>
      <AdminWorkspaceShell>
        <div data-testid="page-content">Hello</div>
      </AdminWorkspaceShell>
    </NextIntlClientProvider>,
  );
}

describe("AdminWorkspaceShell", () => {
  it("renders the page content", () => {
    renderShell();
    expect(screen.getByTestId("page-content")).toBeInTheDocument();
  });

  it("renders a real breadcrumb, not the placeholder", () => {
    renderShell();
    expect(screen.queryByText("Build Your Application")).not.toBeInTheDocument();
    expect(screen.queryByText("Data Fetching")).not.toBeInTheDocument();
    expect(screen.getByText("Users")).toBeInTheDocument(); // current crumb / title
  });

  it("does not render dead Cancel/Save buttons", () => {
    renderShell();
    expect(screen.queryByRole("button", {name: /Save changes/i})).not.toBeInTheDocument();
    expect(screen.queryByRole("button", {name: /^Cancel$/i})).not.toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/__tests__/admin-workspace-shell.test.tsx`
Expected: FAIL — current shell renders "Build Your Application" and "Save changes".

- [ ] **Step 3: Rebuild the implementation**

```tsx
// apps/experts-app/src/components/admin/AdminWorkspaceShell.tsx
"use client";

import {type ReactNode, startTransition, useLayoutEffect, useState} from "react";
import {usePathname} from "next/navigation";
import {useLocale, useTranslations} from "next-intl";
import {Separator} from "@heroui/react";
import {ChevronRight} from "lucide-react";
import {cn} from "@/lib/utils";
import {SidebarInset, SidebarProvider, SidebarTrigger} from "@/components/ui/sidebar";
import {AdminSidebar} from "./admin-sidebar";
import {GlobalSearch} from "../GlobalSearch";
import {Link} from "@/i18n/routing";
import {deriveAdminBreadcrumb} from "./admin-breadcrumb";
import {findActiveNavItem} from "./admin-nav";

interface AdminWorkspaceShellProps {
  children: ReactNode;
  profile?: {fullName?: string | null; email?: string | null; avatarUrl?: string | null};
}

function stripLocale(pathname: string, locale: string): string {
  const prefix = `/${locale}`;
  if (pathname === prefix) return "/";
  if (pathname.startsWith(`${prefix}/`)) return pathname.slice(prefix.length) || "/";
  return pathname;
}

export function AdminWorkspaceShell({children, profile}: AdminWorkspaceShellProps) {
  const locale = useLocale();
  const t = useTranslations("admin");
  const fullPathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [hydrated, setHydrated] = useState(false);

  useLayoutEffect(() => {
    const stored = window.localStorage.getItem("admin-sidebar:open");
    if (stored !== null) {
      const next = stored === "true";
      startTransition(() => setSidebarOpen(next));
    }
    startTransition(() => setHydrated(true));
  }, []);

  function handleOpenChange(open: boolean) {
    startTransition(() => {
      setSidebarOpen(open);
      window.localStorage.setItem("admin-sidebar:open", String(open));
    });
  }

  const path = stripLocale(fullPathname, locale);
  const activeItem = findActiveNavItem(path);
  const crumbs = deriveAdminBreadcrumb(fullPathname, locale);
  void profile; // Account cluster wiring lands with the kit (plan 1b).

  if (!hydrated) {
    return <div className="bg-background min-h-screen" />;
  }

  return (
    <SidebarProvider
      open={sidebarOpen}
      onOpenChange={handleOpenChange}
      className={cn(
        "max-w-9xl mx-auto h-screen overflow-hidden rounded-3xl backdrop-blur",
        sidebarOpen &&
          "shadow-[-30px_0_75px_-75px_rgba(15,23,42,0.35)] backdrop-blur-sm transition-all duration-300",
      )}
      style={
        {
          "--sidebar-width": "calc(var(--spacing) * 72)",
          "--header-height": "calc(var(--spacing) * 12)",
        } as React.CSSProperties
      }
    >
      <AdminSidebar />

      <SidebarInset
        className={cn(
          "@container/sidebar-inset min-h-[calc(100svh-5rem)]",
          "bg-card border-border/70 m-2 h-full overflow-hidden rounded-2xl border shadow-[0_28px_60px_-42px_rgba(15,23,42,0.35)]",
        )}
      >
        {/* Quiet top bar */}
        <header className="border-border/60 bg-background/60 sticky top-0 z-40 flex h-16 w-full shrink-0 items-center justify-between gap-2 border-b backdrop-blur-sm">
          <div className="flex items-center gap-2 px-4">
            <SidebarTrigger className="-ml-1" aria-label={t("shell.toggleSidebar")} />
            <Separator orientation="vertical" className="mr-2 data-[orientation=vertical]:h-4" />
            <nav aria-label="Breadcrumb" className="flex items-center gap-1.5 text-sm">
              {crumbs.map((crumb, i) => {
                const isLast = i === crumbs.length - 1;
                if ("groupLabelKey" in crumb) {
                  return (
                    <span key={i} className="text-muted-foreground hidden items-center gap-1.5 md:flex">
                      {t(crumb.groupLabelKey.replace(/^admin\./, ""))}
                      {!isLast && <ChevronRight className="h-3.5 w-3.5 rtl:rotate-180" />}
                    </span>
                  );
                }
                const label = t(crumb.labelKey.replace(/^admin\./, ""));
                return (
                  <span key={i} className="flex items-center gap-1.5">
                    {crumb.current ? (
                      <span className="text-foreground font-medium">{label}</span>
                    ) : (
                      <Link href={crumb.href} className="text-muted-foreground hover:text-foreground">
                        {label}
                      </Link>
                    )}
                    {!isLast && <ChevronRight className="text-muted-foreground h-3.5 w-3.5 rtl:rotate-180" />}
                  </span>
                );
              })}
            </nav>
          </div>
          <div className="hidden max-w-sm min-w-fit flex-1 px-4 @2xl/sidebar-inset:flex @2xl/sidebar-inset:min-w-xs">
            <GlobalSearch />
          </div>
        </header>

        {/* Scroll region + page-derived title block + page content */}
        <div className="flex h-full flex-1 flex-col gap-4 overflow-y-auto p-4">
          {activeItem && (
            <div className="flex items-center gap-4">
              <div className="bg-background border-border/70 flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border shadow-sm">
                <activeItem.icon className="text-foreground h-6 w-6" />
              </div>
              <div className="min-w-0">
                <p className="text-muted-foreground text-xs">{t(`nav.groups.${activeItem.group}`)}</p>
                <h1 className="text-foreground truncate text-2xl font-semibold tracking-tight">
                  {t(`nav.items.${activeItem.labelKey}`)}
                </h1>
              </div>
            </div>
          )}
          {children}
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
```

> `t(crumb.labelKey.replace(/^admin\./, ""))` is needed because the breadcrumb keys are returned fully-qualified (`admin.nav.items.users`) but `t` is already scoped to `admin`. Verify in Step 4; if your `t` scope differs, adjust the prefix stripping.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/__tests__/admin-workspace-shell.test.tsx`
Expected: PASS (3 tests).

- [ ] **Step 5: Typecheck**

Run: `cd apps/experts-app && pnpm typecheck:touched -- src/components/admin/AdminWorkspaceShell.tsx`
Expected: no errors.

- [ ] **Step 6: Commit**

```bash
git add apps/experts-app/src/components/admin/AdminWorkspaceShell.tsx apps/experts-app/src/components/admin/__tests__/admin-workspace-shell.test.tsx
git commit -m "feat(admin): rebuild shell — layers, real breadcrumb, drop placeholder/dead chrome"
```

---

## Task 6: Simplify `AdminShell` to consume the nav module

**Files:**
- Modify: `apps/experts-app/src/components/admin/AdminShell.tsx`

**Context:** `AdminShell` currently defines its own `ADMIN_NAV_ITEMS` and passes them to `AdminWorkspaceShell`. The rebuilt shell reads nav from `admin-nav.ts` directly, so this list is now dead. Reduce `AdminShell` to a thin pass-through that forwards `profile`.

- [ ] **Step 1: Replace the file contents**

```tsx
// apps/experts-app/src/components/admin/AdminShell.tsx
import type {ReactNode} from "react";
import {AdminWorkspaceShell} from "@/components/admin/AdminWorkspaceShell";

interface AdminShellProps {
  children: ReactNode;
  profile?: {fullName?: string | null; email?: string | null; avatarUrl?: string | null};
}

export function AdminShell({children, profile}: AdminShellProps) {
  return <AdminWorkspaceShell profile={profile}>{children}</AdminWorkspaceShell>;
}
```

- [ ] **Step 2: Typecheck the layout that consumes it**

Run: `cd apps/experts-app && pnpm typecheck:touched -- src/components/admin/AdminShell.tsx "app/(i18n)/_shared/admin/layout.tsx"`
Expected: no errors (the `layout.tsx` already passes only `profile` + children).

- [ ] **Step 3: Commit**

```bash
git add apps/experts-app/src/components/admin/AdminShell.tsx
git commit -m "refactor(admin): AdminShell becomes thin pass-through to workspace shell"
```

---

## Task 7: Delete the redundant nav systems and dead chrome

**Files:**
- Delete: `apps/experts-app/src/components/admin/admin-navbar.tsx`
- Delete: `apps/experts-app/app/(i18n)/_shared/admin/sidebar-preview/page.tsx` and the locale mirrors `app/(i18n)/{en,ar,es}/admin/sidebar-preview/page.tsx`
- Conditionally delete: `apps/experts-app/src/components/admin/admin-header.tsx`, `src/components/admin/navbar/{main,projects,secondary,user}.tsx`

- [ ] **Step 1: Find remaining importers before deleting**

Run:
```bash
cd apps/experts-app && \
  echo "--- admin-navbar ---"; grep -rn "admin-navbar" src app --include=*.tsx --include=*.ts | grep -v "admin-navbar.tsx:" ; \
  echo "--- admin-header ---"; grep -rn "admin-header" src app --include=*.tsx --include=*.ts | grep -v "admin-header.tsx:" ; \
  echo "--- navbar/ subfiles ---"; for f in main projects secondary user; do echo "navbar/$f:"; grep -rn "navbar/$f" src app --include=*.tsx --include=*.ts; done
```
Expected: After Tasks 4–6, `admin-navbar` and `admin-header` have **no** importers (the shell no longer renders them). `navbar/console` is still imported by the sidebar (keep it). Any of `navbar/{main,projects,secondary,user}` with no importer is safe to delete.

- [ ] **Step 2: Delete the confirmed-orphan files**

Run (only for files that printed no importer in Step 1):
```bash
cd apps/experts-app && git rm \
  src/components/admin/admin-navbar.tsx \
  "app/(i18n)/_shared/admin/sidebar-preview/page.tsx" \
  "app/(i18n)/en/admin/sidebar-preview/page.tsx" \
  "app/(i18n)/ar/admin/sidebar-preview/page.tsx" \
  "app/(i18n)/es/admin/sidebar-preview/page.tsx"
# Add admin-header.tsx and navbar/{main,projects,secondary,user}.tsx to this list ONLY if Step 1 showed no importers.
```

- [ ] **Step 3: Verify nothing broke (full typecheck of the app)**

Run: `cd apps/experts-app && pnpm typecheck`
Expected: no errors. If an unexpected importer surfaces, restore that file with `git checkout -- <file>` and leave it — note it for a later wave rather than forcing the delete.

- [ ] **Step 4: Run the admin test suite**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin`
Expected: all admin tests PASS.

- [ ] **Step 5: Commit**

```bash
git add -A apps/experts-app/src/components/admin apps/experts-app/app
git commit -m "chore(admin): remove redundant navbar/tabs + dead chrome (sidebar-preview, admin-header)"
```

---

## Task 8: Full gate + manual shell verification

**Files:** none (verification only)

- [ ] **Step 1: Run the repo quality gate**

Run: `pnpm experts:check`
Expected: FORMAT, LINT, TYPECHECK all pass. If any fail, run `pnpm experts:check:fix`, then re-run `pnpm experts:check`.

- [ ] **Step 2: Manually verify the shell**

Run the app (see the `run` skill / project launch). Visit `/admin`, `/admin/users`, `/admin/refunds`:
- Exactly one sidebar; groups Overview/Operations/Finance/Insights/Trust & Safety/Tools render, with correct active highlight.
- Breadcrumb reads `Admin / <Group> / <Section>` (or just `Admin` on the dashboard) — **never** "Build Your Application".
- No "Cancel / Save changes" buttons; no top navbar; no quick-link tabs.
- Title block shows the real section name + group.
- Toggle `ar` locale: sidebar flips to the right, breadcrumb chevrons rotate, labels are Arabic.
- Toggle dark mode: surfaces, borders, and active states remain legible.

- [ ] **Step 3: Final commit (if `experts:check:fix` changed anything)**

```bash
git add -A && git commit -m "chore(admin): apply format/lint fixes for shell rebuild" || echo "nothing to commit"
```

---

## Self-Review

- **Spec coverage (1a portion):** single nav source of truth ✓ (T1); real breadcrumb ✓ (T2/T5); shell layers per orbit ✓ (T5); remove placeholder/dead chrome ✓ (T5/T7); i18n en/ar/es + RTL ✓ (T3/T5); real account cluster — **deferred to 1b** (noted in T5; `profile` is threaded but the account UI ships with the kit). Kit primitives, ⌘K palette, dashboard, new queries — out of scope for 1a, covered by plans 1b/1c/1d.
- **Placeholder scan:** no TBD/TODO; every code step shows complete code; deletions are guarded by import-grep + `tsc` rather than assumed.
- **Type consistency:** `findActiveNavItem`, `groupedAdminNav`, `deriveAdminBreadcrumb`, `AdminNavItem.labelKey`, and the `admin.nav.*`/`admin.shell.*` i18n keys are used consistently across T1–T6. `SidebarMenuButton`/`AdminNavConsole` prop shapes are flagged for verification against the real primitive files before relying on them.

---

## Next plans in this slice

- **1b — Kit primitives** (`AdminPageHeader`, `StatCard`, `DataTable`, `FilterBar`, `EmptyState`, `LoadingState`, `ErrorState`, `DetailDrawer`, `SectionCard`, `StatusBadge`) + `kit-preview` page + real account cluster in the shell footer.
- **1c — ⌘K command palette** + `command-registry` + sidebar ⌘K trigger + starter actions.
- **1d — Dashboard rebuild** on the kit + new read-only triage queries (pending refunds/payouts/certifications) following the `src/lib/admin/queries` → API route → `useApiQuery` pattern.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
