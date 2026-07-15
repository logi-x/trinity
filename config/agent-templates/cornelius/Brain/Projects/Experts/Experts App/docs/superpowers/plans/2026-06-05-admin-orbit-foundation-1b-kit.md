---
title: "2026 06 05 admin orbit foundation 1b kit"
date: "2026-06-05"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/plans/2026-06-05-admin-orbit-foundation-1b-kit.md"
---
# Admin Orbit Foundation — Plan 1b: Design-System Kit

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a small, reusable `components/admin/kit/` set (page header, section card, stat card, status badge, empty/loading/error states, filter bar, data table, detail drawer) plus the real account cluster in the shell footer — every later section reuses these.

**Architecture:** The kit is mostly **opinionated composition of existing `components/ui` primitives** (`Table*`, `Badge`, `Skeleton`, `EmptyState`, `Drawer*`, `Card`, `pagination`) — not new low-level UI. Each kit component is theme-safe (semantic tokens), RTL-correct, and demonstrated on a `kit-preview` page. Depends on plan 1a (`admin-nav.ts`, rebuilt shell).

**Tech Stack:** React 19, HeroUI v3 + Tailwind v4, in-repo `components/ui/*` (shadcn-style: `table.tsx`, `badge.tsx` exporting `Badge`+`badgeVariants`, `skeleton.tsx` exporting `Skeleton`, `empty-state.tsx` exporting `EmptyState({icon,title,description,action})`, `drawer.tsx` exporting `Drawer/DrawerContent/DrawerHeader/DrawerTitle/DrawerDescription/DrawerClose`, `card.tsx`, `pagination.tsx`, `avatar.tsx`, `dropdown-menu.tsx`), recharts (installed), lucide-react, Vitest + Testing Library.

**Scope note:** Plan **1b of 4**. The kit primitives here are consumed by the dashboard (1d) and all later section waves. This plan does **not** restyle the 11 section pages — only builds + demos the kit and adds the account cluster.

---

## File Structure

| File | Responsibility |
|------|----------------|
| `src/components/admin/kit/index.ts` | Barrel export for the kit. |
| `src/components/admin/kit/AdminPageHeader.tsx` | eyebrow + title + description + actions slot (page-owned header). |
| `src/components/admin/kit/SectionCard.tsx` | Standard elevated content card (header + body). Replaces ad-hoc `DashboardPanel`. |
| `src/components/admin/kit/StatCard.tsx` | KPI: value, label, optional delta + sparkline + href/onClick. |
| `src/components/admin/kit/StatusBadge.tsx` | Status → token-colored pill (pending/approved/rejected/failed/processing/neutral). |
| `src/components/admin/kit/AdminEmptyState.tsx` | Thin admin wrapper over `ui/empty-state`. |
| `src/components/admin/kit/LoadingState.tsx` | `TableSkeleton`, `CardsSkeleton` built from `Skeleton`. |
| `src/components/admin/kit/ErrorState.tsx` | Error message + retry action. |
| `src/components/admin/kit/FilterBar.tsx` | Search input + arbitrary filter controls row. |
| `src/components/admin/kit/DataTable.tsx` | Column-driven table: sort, pagination, row actions, sticky dense header; renders loading/empty/error. |
| `src/components/admin/kit/DetailDrawer.tsx` | Side slide-over for record detail (wraps `ui/drawer`). |
| `src/components/admin/AdminAccount.tsx` | Account cluster (avatar + name/email + menu) for the shell footer. |
| `app/(i18n)/_shared/admin/kit-preview/page.tsx` | Live demo of every kit component (replaces deleted `sidebar-preview`). |
| `src/components/admin/kit/__tests__/*` | Unit tests per component. |

**i18n:** add `admin.kit.*` keys (`retry`, `noResults`, `noResultsDescription`, `loading`, `errorTitle`, `errorDescription`, `previous`, `next`, `page`) to `src/i18n/messages/{en,ar,es}/admin.json`. Concrete values in Task 1.

---

## Task 1: Kit i18n keys + barrel

**Files:**
- Modify: `src/i18n/messages/{en,ar,es}/admin.json`
- Create: `src/components/admin/kit/index.ts`

- [ ] **Step 1: Add `kit` block to `en/admin.json`**

```json
"kit": {
  "retry": "Retry",
  "loading": "Loading…",
  "noResults": "No results",
  "noResultsDescription": "Nothing to show here yet.",
  "errorTitle": "Something went wrong",
  "errorDescription": "We couldn't load this data. Try again.",
  "previous": "Previous",
  "next": "Next",
  "pageOf": "Page {page} of {total}"
}
```

- [ ] **Step 2: Add `kit` block to `ar/admin.json`**

```json
"kit": {
  "retry": "إعادة المحاولة",
  "loading": "جارٍ التحميل…",
  "noResults": "لا توجد نتائج",
  "noResultsDescription": "لا يوجد شيء لعرضه بعد.",
  "errorTitle": "حدث خطأ ما",
  "errorDescription": "تعذّر تحميل البيانات. حاول مرة أخرى.",
  "previous": "السابق",
  "next": "التالي",
  "pageOf": "صفحة {page} من {total}"
}
```

- [ ] **Step 3: Add `kit` block to `es/admin.json`**

```json
"kit": {
  "retry": "Reintentar",
  "loading": "Cargando…",
  "noResults": "Sin resultados",
  "noResultsDescription": "Aún no hay nada que mostrar.",
  "errorTitle": "Algo salió mal",
  "errorDescription": "No pudimos cargar los datos. Inténtalo de nuevo.",
  "previous": "Anterior",
  "next": "Siguiente",
  "pageOf": "Página {page} de {total}"
}
```

- [ ] **Step 4: Create the barrel (filled in as components land)**

```ts
// src/components/admin/kit/index.ts
export {AdminPageHeader} from "./AdminPageHeader";
export {SectionCard} from "./SectionCard";
export {StatCard} from "./StatCard";
export {StatusBadge, type AdminStatus} from "./StatusBadge";
export {AdminEmptyState} from "./AdminEmptyState";
export {TableSkeleton, CardsSkeleton} from "./LoadingState";
export {ErrorState} from "./ErrorState";
export {FilterBar} from "./FilterBar";
export {DataTable, type DataTableColumn} from "./DataTable";
export {DetailDrawer} from "./DetailDrawer";
```

> The barrel references files created in later tasks. Expect `pnpm typecheck` to fail until Task 10; do **not** run a full typecheck after this task. Commit the barrel last if your executor prefers — but keeping it here documents the kit's public surface.

- [ ] **Step 5: Commit**

```bash
git add src/components/admin/kit/index.ts src/i18n/messages/en/admin.json src/i18n/messages/ar/admin.json src/i18n/messages/es/admin.json
git commit -m "feat(admin/kit): i18n keys + kit barrel"
```

---

## Task 2: `AdminPageHeader`

**Files:**
- Create: `src/components/admin/kit/AdminPageHeader.tsx`
- Test: `src/components/admin/kit/__tests__/AdminPageHeader.test.tsx`

- [ ] **Step 1: Write the failing test**

```tsx
import {describe, it, expect} from "vitest";
import {render, screen} from "@testing-library/react";
import {AdminPageHeader} from "../AdminPageHeader";

describe("AdminPageHeader", () => {
  it("renders eyebrow, title, description and actions", () => {
    render(
      <AdminPageHeader
        eyebrow="Finance"
        title="Refunds"
        description="Manage pending refunds"
        actions={<button>Export</button>}
      />,
    );
    expect(screen.getByRole("heading", {name: "Refunds"})).toBeInTheDocument();
    expect(screen.getByText("Finance")).toBeInTheDocument();
    expect(screen.getByText("Manage pending refunds")).toBeInTheDocument();
    expect(screen.getByRole("button", {name: "Export"})).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/AdminPageHeader.test.tsx`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement**

```tsx
// src/components/admin/kit/AdminPageHeader.tsx
import type {ReactNode} from "react";
import {cn} from "@/lib/utils";

export interface AdminPageHeaderProps {
  eyebrow?: string;
  title: string;
  description?: string;
  actions?: ReactNode;
  className?: string;
}

export function AdminPageHeader({eyebrow, title, description, actions, className}: AdminPageHeaderProps) {
  return (
    <div className={cn("flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between", className)}>
      <div className="min-w-0 space-y-1">
        {eyebrow && (
          <p className="text-muted-foreground text-[11px] font-semibold tracking-[0.18em] uppercase">
            {eyebrow}
          </p>
        )}
        <h1 className="text-foreground truncate text-2xl font-semibold tracking-tight">{title}</h1>
        {description && (
          <p className="text-muted-foreground max-w-2xl text-sm leading-6">{description}</p>
        )}
      </div>
      {actions && <div className="flex shrink-0 items-center gap-2">{actions}</div>}
    </div>
  );
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/AdminPageHeader.test.tsx`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/components/admin/kit/AdminPageHeader.tsx src/components/admin/kit/__tests__/AdminPageHeader.test.tsx
git commit -m "feat(admin/kit): AdminPageHeader"
```

---

## Task 3: `SectionCard`

**Files:**
- Create: `src/components/admin/kit/SectionCard.tsx`
- Test: `src/components/admin/kit/__tests__/SectionCard.test.tsx`

- [ ] **Step 1: Write the failing test**

```tsx
import {describe, it, expect} from "vitest";
import {render, screen} from "@testing-library/react";
import {SectionCard} from "../SectionCard";

describe("SectionCard", () => {
  it("renders title, optional action, and children", () => {
    render(
      <SectionCard title="Revenue" action={<button>View all</button>}>
        <p>body</p>
      </SectionCard>,
    );
    expect(screen.getByText("Revenue")).toBeInTheDocument();
    expect(screen.getByRole("button", {name: "View all"})).toBeInTheDocument();
    expect(screen.getByText("body")).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/SectionCard.test.tsx`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement**

```tsx
// src/components/admin/kit/SectionCard.tsx
import type {ReactNode} from "react";
import {cn} from "@/lib/utils";

export interface SectionCardProps {
  title?: string;
  description?: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
  bodyClassName?: string;
}

export function SectionCard({title, description, action, children, className, bodyClassName}: SectionCardProps) {
  return (
    <section
      className={cn(
        "bg-card border-border/70 overflow-hidden rounded-2xl border shadow-[0_20px_48px_-40px_rgba(15,23,42,0.35)]",
        className,
      )}
    >
      {(title || action) && (
        <header className="border-border/60 flex items-start justify-between gap-4 border-b px-5 py-4">
          <div className="min-w-0 space-y-0.5">
            {title && (
              <h2 className="text-foreground text-base font-semibold tracking-tight">{title}</h2>
            )}
            {description && <p className="text-muted-foreground text-xs leading-relaxed">{description}</p>}
          </div>
          {action && <div className="shrink-0">{action}</div>}
        </header>
      )}
      <div className={cn("p-5", bodyClassName)}>{children}</div>
    </section>
  );
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/SectionCard.test.tsx`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/components/admin/kit/SectionCard.tsx src/components/admin/kit/__tests__/SectionCard.test.tsx
git commit -m "feat(admin/kit): SectionCard"
```

---

## Task 4: `StatusBadge`

**Files:**
- Create: `src/components/admin/kit/StatusBadge.tsx`
- Test: `src/components/admin/kit/__tests__/StatusBadge.test.tsx`

**Context:** Reuse `ui/badge` (`Badge`). Map a small status vocabulary to token-driven classes that work in light + dark.

- [ ] **Step 1: Write the failing test**

```tsx
import {describe, it, expect} from "vitest";
import {render, screen} from "@testing-library/react";
import {StatusBadge} from "../StatusBadge";

describe("StatusBadge", () => {
  it("renders the provided label", () => {
    render(<StatusBadge status="pending" label="Pending" />);
    expect(screen.getByText("Pending")).toBeInTheDocument();
  });

  it("applies a distinct class per status", () => {
    const {rerender} = render(<StatusBadge status="approved" label="Approved" />);
    const approved = screen.getByText("Approved").className;
    rerender(<StatusBadge status="rejected" label="Rejected" />);
    const rejected = screen.getByText("Rejected").className;
    expect(approved).not.toBe(rejected);
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/StatusBadge.test.tsx`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement**

```tsx
// src/components/admin/kit/StatusBadge.tsx
import {cn} from "@/lib/utils";

export type AdminStatus = "pending" | "approved" | "rejected" | "processing" | "failed" | "neutral";

const STATUS_CLASS: Record<AdminStatus, string> = {
  pending: "bg-amber-500/10 text-amber-700 dark:text-amber-400 border-amber-500/20",
  approved: "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/20",
  rejected: "bg-red-500/10 text-red-700 dark:text-red-400 border-red-500/20",
  processing: "bg-blue-500/10 text-blue-700 dark:text-blue-400 border-blue-500/20",
  failed: "bg-red-500/10 text-red-700 dark:text-red-400 border-red-500/20",
  neutral: "bg-muted text-muted-foreground border-border",
};

export interface StatusBadgeProps {
  status: AdminStatus;
  label: string;
  className?: string;
}

export function StatusBadge({status, label, className}: StatusBadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium",
        STATUS_CLASS[status],
        className,
      )}
    >
      {label}
    </span>
  );
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/StatusBadge.test.tsx`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/components/admin/kit/StatusBadge.tsx src/components/admin/kit/__tests__/StatusBadge.test.tsx
git commit -m "feat(admin/kit): StatusBadge"
```

---

## Task 5: `StatCard`

**Files:**
- Create: `src/components/admin/kit/StatCard.tsx`
- Test: `src/components/admin/kit/__tests__/StatCard.test.tsx`

**Context:** KPI card with value, label, optional delta (▲/▼ + percent, green/red), optional sparkline (recharts), optional `href` (whole card becomes a link via `@/i18n/routing` `Link`).

- [ ] **Step 1: Write the failing test**

```tsx
import {describe, it, expect} from "vitest";
import {render, screen} from "@testing-library/react";
import {Wallet} from "lucide-react";
import {StatCard} from "../StatCard";

describe("StatCard", () => {
  it("renders label, value and a positive delta", () => {
    render(<StatCard label="Revenue" value="SAR 482K" delta={12} icon={Wallet} />);
    expect(screen.getByText("Revenue")).toBeInTheDocument();
    expect(screen.getByText("SAR 482K")).toBeInTheDocument();
    expect(screen.getByText(/12%/)).toBeInTheDocument();
  });

  it("renders as a link when href is provided", () => {
    render(<StatCard label="Pending refunds" value="23" href="/admin/refunds" />);
    expect(screen.getByRole("link")).toHaveAttribute("href", expect.stringContaining("/admin/refunds"));
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/StatCard.test.tsx`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement**

```tsx
// src/components/admin/kit/StatCard.tsx
import type {ReactNode} from "react";
import type {LucideIcon} from "lucide-react";
import {ArrowDownRight, ArrowUpRight} from "lucide-react";
import {Line, LineChart, ResponsiveContainer} from "recharts";
import {Link} from "@/i18n/routing";
import {cn} from "@/lib/utils";

export interface StatCardProps {
  label: string;
  value: ReactNode;
  delta?: number; // percent; positive = up/green, negative = down/red
  icon?: LucideIcon;
  spark?: number[];
  href?: string;
  className?: string;
}

function Inner({label, value, delta, icon: Icon, spark}: StatCardProps) {
  const series = spark?.map((y, i) => ({i, y}));
  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <p className="text-muted-foreground text-xs font-medium">{label}</p>
        {Icon && <Icon className="text-muted-foreground h-4 w-4" />}
      </div>
      <div className="flex items-end justify-between gap-2">
        <p className="text-foreground text-2xl font-semibold tracking-tight">{value}</p>
        {typeof delta === "number" && (
          <span
            className={cn(
              "inline-flex items-center gap-0.5 text-xs font-medium",
              delta >= 0 ? "text-emerald-600 dark:text-emerald-400" : "text-red-600 dark:text-red-400",
            )}
          >
            {delta >= 0 ? <ArrowUpRight className="h-3.5 w-3.5" /> : <ArrowDownRight className="h-3.5 w-3.5" />}
            {Math.abs(delta)}%
          </span>
        )}
      </div>
      {series && series.length > 1 && (
        <div className="h-10">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={series}>
              <Line type="monotone" dataKey="y" stroke="var(--primary)" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

export function StatCard(props: StatCardProps) {
  const base = "bg-card border-border/70 rounded-2xl border p-4 shadow-[0_16px_40px_-36px_rgba(15,23,42,0.35)]";
  if (props.href) {
    return (
      <Link href={props.href} className={cn(base, "hover:border-border transition-colors", props.className)}>
        <Inner {...props} />
      </Link>
    );
  }
  return (
    <div className={cn(base, props.className)}>
      <Inner {...props} />
    </div>
  );
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/StatCard.test.tsx`
Expected: PASS. (recharts renders inside jsdom; if `ResponsiveContainer` warns about zero width, that's a known jsdom noise — the test does not assert on the chart.)

- [ ] **Step 5: Commit**

```bash
git add src/components/admin/kit/StatCard.tsx src/components/admin/kit/__tests__/StatCard.test.tsx
git commit -m "feat(admin/kit): StatCard with delta + sparkline + optional link"
```

---

## Task 6: `AdminEmptyState`, `ErrorState`, `LoadingState`

**Files:**
- Create: `src/components/admin/kit/AdminEmptyState.tsx`
- Create: `src/components/admin/kit/ErrorState.tsx`
- Create: `src/components/admin/kit/LoadingState.tsx`
- Test: `src/components/admin/kit/__tests__/states.test.tsx`

- [ ] **Step 1: Write the failing test**

```tsx
import {describe, it, expect, vi} from "vitest";
import {render, screen, fireEvent} from "@testing-library/react";
import {NextIntlClientProvider} from "next-intl";
import enAdmin from "@/i18n/messages/en/admin.json";
import {AdminEmptyState} from "../AdminEmptyState";
import {ErrorState} from "../ErrorState";
import {TableSkeleton} from "../LoadingState";

function wrap(ui: React.ReactNode) {
  return render(<NextIntlClientProvider locale="en" messages={{admin: enAdmin}}>{ui}</NextIntlClientProvider>);
}

describe("kit states", () => {
  it("AdminEmptyState renders title + description", () => {
    wrap(<AdminEmptyState title="No refunds" description="Nothing pending" />);
    expect(screen.getByText("No refunds")).toBeInTheDocument();
  });

  it("ErrorState calls onRetry", () => {
    const onRetry = vi.fn();
    wrap(<ErrorState onRetry={onRetry} />);
    fireEvent.click(screen.getByRole("button", {name: "Retry"}));
    expect(onRetry).toHaveBeenCalledOnce();
  });

  it("TableSkeleton renders the requested number of rows", () => {
    const {container} = wrap(<TableSkeleton rows={5} columns={3} />);
    expect(container.querySelectorAll("[data-skeleton-row]").length).toBe(5);
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/states.test.tsx`
Expected: FAIL — modules not found.

- [ ] **Step 3: Implement the three files**

```tsx
// src/components/admin/kit/AdminEmptyState.tsx
import type {ElementType, ReactNode} from "react";
import {Inbox} from "lucide-react";
import {EmptyState} from "@/components/ui/empty-state";

export interface AdminEmptyStateProps {
  icon?: ElementType;
  title: string;
  description?: string;
  action?: ReactNode;
}

export function AdminEmptyState({icon = Inbox, title, description, action}: AdminEmptyStateProps) {
  return <EmptyState icon={icon} title={title} description={description ?? ""} action={action} />;
}
```

```tsx
// src/components/admin/kit/ErrorState.tsx
import {useTranslations} from "next-intl";
import {AlertTriangle} from "lucide-react";
import {Button} from "@heroui/react";

export interface ErrorStateProps {
  title?: string;
  description?: string;
  onRetry?: () => void;
}

export function ErrorState({title, description, onRetry}: ErrorStateProps) {
  const t = useTranslations("admin.kit");
  return (
    <div className="flex flex-col items-center justify-center gap-3 px-6 py-12 text-center">
      <div className="bg-red-500/10 text-red-600 dark:text-red-400 flex h-12 w-12 items-center justify-center rounded-2xl">
        <AlertTriangle className="h-6 w-6" />
      </div>
      <div className="space-y-1">
        <p className="text-foreground text-sm font-semibold">{title ?? t("errorTitle")}</p>
        <p className="text-muted-foreground text-sm">{description ?? t("errorDescription")}</p>
      </div>
      {onRetry && (
        <Button variant="secondary" onClick={onRetry} className="h-9 rounded-xl px-4 text-sm">
          {t("retry")}
        </Button>
      )}
    </div>
  );
}
```

```tsx
// src/components/admin/kit/LoadingState.tsx
import {Skeleton} from "@/components/ui/skeleton";

export function TableSkeleton({rows = 6, columns = 4}: {rows?: number; columns?: number}) {
  return (
    <div className="space-y-2">
      {Array.from({length: rows}).map((_, r) => (
        <div key={r} data-skeleton-row className="flex items-center gap-3">
          {Array.from({length: columns}).map((_, c) => (
            <Skeleton key={c} className="h-8 flex-1 rounded-lg" />
          ))}
        </div>
      ))}
    </div>
  );
}

export function CardsSkeleton({count = 4}: {count?: number}) {
  return (
    <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
      {Array.from({length: count}).map((_, i) => (
        <Skeleton key={i} className="h-28 rounded-2xl" />
      ))}
    </div>
  );
}
```

> Verify `EmptyState`'s prop names against `src/components/ui/empty-state.tsx` (Task confirmed: `{icon, iconClassName, title, description, action}`). If `Button`'s `onClick` is named `onPress` in this HeroUI v3 build, use `onPress`; check `src/components/ui/button.tsx` or an existing `@heroui/react` `Button` usage.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/states.test.tsx`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add src/components/admin/kit/AdminEmptyState.tsx src/components/admin/kit/ErrorState.tsx src/components/admin/kit/LoadingState.tsx src/components/admin/kit/__tests__/states.test.tsx
git commit -m "feat(admin/kit): empty / error / loading states"
```

---

## Task 7: `FilterBar`

**Files:**
- Create: `src/components/admin/kit/FilterBar.tsx`
- Test: `src/components/admin/kit/__tests__/FilterBar.test.tsx`

- [ ] **Step 1: Write the failing test**

```tsx
import {describe, it, expect, vi} from "vitest";
import {render, screen, fireEvent} from "@testing-library/react";
import {FilterBar} from "../FilterBar";

describe("FilterBar", () => {
  it("fires onSearchChange when typing", () => {
    const onSearchChange = vi.fn();
    render(<FilterBar searchValue="" onSearchChange={onSearchChange} searchPlaceholder="Search users" />);
    fireEvent.change(screen.getByPlaceholderText("Search users"), {target: {value: "ali"}});
    expect(onSearchChange).toHaveBeenCalledWith("ali");
  });

  it("renders extra controls", () => {
    render(
      <FilterBar searchValue="" onSearchChange={() => {}} searchPlaceholder="x">
        <button>Status</button>
      </FilterBar>,
    );
    expect(screen.getByRole("button", {name: "Status"})).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/FilterBar.test.tsx`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement**

```tsx
// src/components/admin/kit/FilterBar.tsx
import type {ReactNode} from "react";
import {Search} from "lucide-react";
import {cn} from "@/lib/utils";

export interface FilterBarProps {
  searchValue: string;
  onSearchChange: (value: string) => void;
  searchPlaceholder: string;
  children?: ReactNode;
  className?: string;
}

export function FilterBar({searchValue, onSearchChange, searchPlaceholder, children, className}: FilterBarProps) {
  return (
    <div className={cn("flex flex-wrap items-center gap-2", className)}>
      <div className="relative min-w-[200px] flex-1">
        <Search className="text-muted-foreground pointer-events-none absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 rtl:right-3 rtl:left-auto" />
        <input
          value={searchValue}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder={searchPlaceholder}
          className="bg-background border-border focus-visible:ring-ring h-9 w-full rounded-xl border pl-9 pr-3 text-sm outline-none focus-visible:ring-2 rtl:pr-9 rtl:pl-3"
        />
      </div>
      {children}
    </div>
  );
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/FilterBar.test.tsx`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/components/admin/kit/FilterBar.tsx src/components/admin/kit/__tests__/FilterBar.test.tsx
git commit -m "feat(admin/kit): FilterBar"
```

---

## Task 8: `DataTable`

**Files:**
- Create: `src/components/admin/kit/DataTable.tsx`
- Test: `src/components/admin/kit/__tests__/DataTable.test.tsx`

**Context:** Column-driven wrapper over `ui/table` (`Table/TableHeader/TableBody/TableRow/TableHead/TableCell`). Renders `TableSkeleton` while loading, `ErrorState` on error, `AdminEmptyState` when empty, and an optional pager. Sorting is controlled (caller owns sort state) to keep it simple and server-friendly.

- [ ] **Step 1: Write the failing test**

```tsx
import {describe, it, expect, vi} from "vitest";
import {render, screen, fireEvent} from "@testing-library/react";
import {NextIntlClientProvider} from "next-intl";
import enAdmin from "@/i18n/messages/en/admin.json";
import {DataTable, type DataTableColumn} from "../DataTable";

interface Row {id: string; name: string; amount: number}
const columns: DataTableColumn<Row>[] = [
  {id: "name", header: "Name", cell: (r) => r.name, sortable: true},
  {id: "amount", header: "Amount", cell: (r) => `SAR ${r.amount}`},
];
const rows: Row[] = [{id: "1", name: "Ali", amount: 100}, {id: "2", name: "Sara", amount: 200}];

function wrap(ui: React.ReactNode) {
  return render(<NextIntlClientProvider locale="en" messages={{admin: enAdmin}}>{ui}</NextIntlClientProvider>);
}

describe("DataTable", () => {
  it("renders headers and rows", () => {
    wrap(<DataTable columns={columns} rows={rows} getRowId={(r) => r.id} />);
    expect(screen.getByText("Name")).toBeInTheDocument();
    expect(screen.getByText("Ali")).toBeInTheDocument();
    expect(screen.getByText("SAR 200")).toBeInTheDocument();
  });

  it("shows empty state when no rows", () => {
    wrap(<DataTable columns={columns} rows={[]} getRowId={(r) => r.id} />);
    expect(screen.getByText("No results")).toBeInTheDocument();
  });

  it("shows the skeleton when loading", () => {
    const {container} = wrap(<DataTable columns={columns} rows={[]} getRowId={(r) => r.id} isLoading />);
    expect(container.querySelector("[data-skeleton-row]")).toBeTruthy();
  });

  it("fires onSortChange when a sortable header is clicked", () => {
    const onSortChange = vi.fn();
    wrap(<DataTable columns={columns} rows={rows} getRowId={(r) => r.id} onSortChange={onSortChange} />);
    fireEvent.click(screen.getByRole("button", {name: /Name/}));
    expect(onSortChange).toHaveBeenCalledWith("name");
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/DataTable.test.tsx`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement**

```tsx
// src/components/admin/kit/DataTable.tsx
import type {ReactNode} from "react";
import {ArrowDown, ArrowUp, ChevronsUpDown} from "lucide-react";
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow} from "@/components/ui/table";
import {cn} from "@/lib/utils";
import {AdminEmptyState} from "./AdminEmptyState";
import {ErrorState} from "./ErrorState";
import {TableSkeleton} from "./LoadingState";
import {useTranslations} from "next-intl";

export interface DataTableColumn<T> {
  id: string;
  header: ReactNode;
  cell: (row: T) => ReactNode;
  sortable?: boolean;
  className?: string;
}

export interface DataTableProps<T> {
  columns: DataTableColumn<T>[];
  rows: T[];
  getRowId: (row: T) => string;
  isLoading?: boolean;
  error?: unknown;
  onRetry?: () => void;
  onRowClick?: (row: T) => void;
  sortBy?: string;
  sortDir?: "asc" | "desc";
  onSortChange?: (columnId: string) => void;
  emptyTitle?: string;
  emptyDescription?: string;
}

export function DataTable<T>(props: DataTableProps<T>) {
  const {
    columns, rows, getRowId, isLoading, error, onRetry, onRowClick,
    sortBy, sortDir, onSortChange, emptyTitle, emptyDescription,
  } = props;
  const t = useTranslations("admin.kit");

  if (isLoading) return <TableSkeleton rows={6} columns={columns.length} />;
  if (error) return <ErrorState onRetry={onRetry} />;
  if (rows.length === 0) {
    return <AdminEmptyState title={emptyTitle ?? t("noResults")} description={emptyDescription ?? t("noResultsDescription")} />;
  }

  return (
    <div className="border-border/60 overflow-hidden rounded-xl border">
      <Table>
        <TableHeader className="bg-muted/40 sticky top-0">
          <TableRow>
            {columns.map((col) => (
              <TableHead key={col.id} className={cn("text-xs", col.className)}>
                {col.sortable && onSortChange ? (
                  <button
                    type="button"
                    onClick={() => onSortChange(col.id)}
                    className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1"
                  >
                    {col.header}
                    {sortBy === col.id ? (
                      sortDir === "asc" ? <ArrowUp className="h-3 w-3" /> : <ArrowDown className="h-3 w-3" />
                    ) : (
                      <ChevronsUpDown className="h-3 w-3 opacity-50" />
                    )}
                  </button>
                ) : (
                  col.header
                )}
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={getRowId(row)}
              onClick={onRowClick ? () => onRowClick(row) : undefined}
              className={cn(onRowClick && "hover:bg-muted/40 cursor-pointer")}
            >
              {columns.map((col) => (
                <TableCell key={col.id} className={cn("text-sm", col.className)}>
                  {col.cell(row)}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/DataTable.test.tsx`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add src/components/admin/kit/DataTable.tsx src/components/admin/kit/__tests__/DataTable.test.tsx
git commit -m "feat(admin/kit): DataTable (sort/loading/error/empty)"
```

---

## Task 9: `DetailDrawer`

**Files:**
- Create: `src/components/admin/kit/DetailDrawer.tsx`
- Test: `src/components/admin/kit/__tests__/DetailDrawer.test.tsx`

**Context:** Wrap `ui/drawer` (`Drawer/DrawerContent/DrawerHeader/DrawerTitle/DrawerDescription`). Controlled via `open`/`onOpenChange`.

- [ ] **Step 1: Write the failing test**

```tsx
import {describe, it, expect} from "vitest";
import {render, screen} from "@testing-library/react";
import {DetailDrawer} from "../DetailDrawer";

describe("DetailDrawer", () => {
  it("renders title + content when open", () => {
    render(
      <DetailDrawer open onOpenChange={() => {}} title="Refund #123" description="Details">
        <p>body</p>
      </DetailDrawer>,
    );
    expect(screen.getByText("Refund #123")).toBeInTheDocument();
    expect(screen.getByText("body")).toBeInTheDocument();
  });

  it("renders nothing visible when closed", () => {
    render(
      <DetailDrawer open={false} onOpenChange={() => {}} title="Hidden">
        <p>secret</p>
      </DetailDrawer>,
    );
    expect(screen.queryByText("secret")).not.toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/DetailDrawer.test.tsx`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement**

```tsx
// src/components/admin/kit/DetailDrawer.tsx
import type {ReactNode} from "react";
import {
  Drawer,
  DrawerContent,
  DrawerDescription,
  DrawerHeader,
  DrawerTitle,
} from "@/components/ui/drawer";

export interface DetailDrawerProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description?: string;
  children: ReactNode;
  footer?: ReactNode;
}

export function DetailDrawer({open, onOpenChange, title, description, children, footer}: DetailDrawerProps) {
  return (
    <Drawer open={open} onOpenChange={onOpenChange} direction="right">
      <DrawerContent className="ml-auto h-full w-full max-w-md rounded-l-2xl rounded-r-none">
        <DrawerHeader>
          <DrawerTitle>{title}</DrawerTitle>
          {description && <DrawerDescription>{description}</DrawerDescription>}
        </DrawerHeader>
        <div className="flex-1 overflow-y-auto px-4 pb-4">{children}</div>
        {footer && <div className="border-border/60 border-t p-4">{footer}</div>}
      </DrawerContent>
    </Drawer>
  );
}
```

> Verify `Drawer` accepts a `direction` prop in this build (vaul does). If `ui/drawer` is a custom wrapper without `direction`, drop the prop and rely on the wrapper's default side; check `src/components/ui/drawer.tsx`. The test does not assert on side, so it passes either way.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit/__tests__/DetailDrawer.test.tsx`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add src/components/admin/kit/DetailDrawer.tsx src/components/admin/kit/__tests__/DetailDrawer.test.tsx
git commit -m "feat(admin/kit): DetailDrawer"
```

---

## Task 10: Account cluster in the shell footer

**Files:**
- Create: `src/components/admin/AdminAccount.tsx`
- Modify: `src/components/admin/admin-sidebar.tsx` (render `AdminAccount` in footer; accept `profile` prop)
- Modify: `src/components/admin/AdminWorkspaceShell.tsx` (pass `profile` to `AdminSidebar`; remove the `void profile` line from plan 1a)
- Test: `src/components/admin/__tests__/admin-account.test.tsx`

- [ ] **Step 1: Write the failing test**

```tsx
import {describe, it, expect} from "vitest";
import {render, screen} from "@testing-library/react";
import {NextIntlClientProvider} from "next-intl";
import enAdmin from "@/i18n/messages/en/admin.json";
import {AdminAccount} from "../AdminAccount";

describe("AdminAccount", () => {
  it("renders the profile name and email", () => {
    render(
      <NextIntlClientProvider locale="en" messages={{admin: enAdmin}}>
        <AdminAccount profile={{fullName: "Ahmed S", email: "a@x.com", avatarUrl: null}} />
      </NextIntlClientProvider>,
    );
    expect(screen.getByText("Ahmed S")).toBeInTheDocument();
    expect(screen.getByText("a@x.com")).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/__tests__/admin-account.test.tsx`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement `AdminAccount`**

```tsx
// src/components/admin/AdminAccount.tsx
import {Avatar} from "@/components/ui/avatar";

export interface AdminAccountProfile {
  fullName?: string | null;
  email?: string | null;
  avatarUrl?: string | null;
}

function initials(name?: string | null): string {
  if (!name) return "?";
  return name.split(" ").map((p) => p[0]).filter(Boolean).slice(0, 2).join("").toUpperCase();
}

export function AdminAccount({profile}: {profile?: AdminAccountProfile}) {
  return (
    <div className="flex items-center gap-3">
      <Avatar className="h-8 w-8">
        {/* Avatar internals (Image/Fallback) follow the existing ui/avatar API; render the URL when present. */}
        {profile?.avatarUrl ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={profile.avatarUrl} alt="" className="h-full w-full rounded-full object-cover" />
        ) : (
          <span className="bg-muted text-muted-foreground flex h-full w-full items-center justify-center rounded-full text-xs font-medium">
            {initials(profile?.fullName)}
          </span>
        )}
      </Avatar>
      <div className="min-w-0">
        <p className="text-foreground truncate text-sm font-medium">{profile?.fullName ?? "—"}</p>
        {profile?.email && <p className="text-muted-foreground truncate text-xs">{profile.email}</p>}
      </div>
    </div>
  );
}
```

> Check `src/components/ui/avatar.tsx` exports. If it exposes `AvatarImage`/`AvatarFallback`, use those instead of the raw `<img>`/`<span>` to match house style. The test only asserts on the name/email text, so either approach passes.

- [ ] **Step 4: Wire `AdminAccount` into the sidebar footer**

In `src/components/admin/admin-sidebar.tsx`: add `profile?: AdminAccountProfile` to the component props, import `AdminAccount`, and render it in `SidebarFooter` above the "Open website" link:

```tsx
// add import
import {AdminAccount, type AdminAccountProfile} from "./AdminAccount";

// change signature
export function AdminSidebar({profile, ...props}: React.ComponentProps<typeof Sidebar> & {profile?: AdminAccountProfile}) {

// in SidebarFooter, before the <Link href="/"> … </Link>:
        <AdminAccount profile={profile} />
```

In `src/components/admin/AdminWorkspaceShell.tsx`: replace the `void profile;` line (added in plan 1a) with passing it down — change `<AdminSidebar />` to `<AdminSidebar profile={profile} />`.

- [ ] **Step 5: Run tests**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/__tests__/admin-account.test.tsx src/components/admin/__tests__/admin-sidebar.test.tsx src/components/admin/__tests__/admin-workspace-shell.test.tsx`
Expected: PASS (account test + the 1a sidebar/shell tests still green).

- [ ] **Step 6: Typecheck touched files**

Run: `cd apps/experts-app && pnpm typecheck:touched -- src/components/admin/AdminAccount.tsx src/components/admin/admin-sidebar.tsx src/components/admin/AdminWorkspaceShell.tsx`
Expected: no errors.

- [ ] **Step 7: Commit**

```bash
git add src/components/admin/AdminAccount.tsx src/components/admin/admin-sidebar.tsx src/components/admin/AdminWorkspaceShell.tsx src/components/admin/__tests__/admin-account.test.tsx
git commit -m "feat(admin): real account cluster in shell footer"
```

---

## Task 11: `kit-preview` page + full gate

**Files:**
- Create: `app/(i18n)/_shared/admin/kit-preview/page.tsx`
- Create locale mirrors: `app/(i18n)/{en,ar,es}/admin/kit-preview/page.tsx`

- [ ] **Step 1: Create the shared preview page**

```tsx
// app/(i18n)/_shared/admin/kit-preview/page.tsx
"use client";

import {useState} from "react";
import {Wallet, Users} from "lucide-react";
import {
  AdminPageHeader, SectionCard, StatCard, StatusBadge, AdminEmptyState,
  TableSkeleton, ErrorState, FilterBar, DataTable, DetailDrawer, type DataTableColumn,
} from "@/components/admin/kit";

interface Row {id: string; name: string; status: "pending" | "approved"}
const rows: Row[] = [
  {id: "1", name: "Ali", status: "pending"},
  {id: "2", name: "Sara", status: "approved"},
];
const columns: DataTableColumn<Row>[] = [
  {id: "name", header: "Name", cell: (r) => r.name, sortable: true},
  {id: "status", header: "Status", cell: (r) => <StatusBadge status={r.status} label={r.status} />},
];

export default function KitPreviewPage() {
  const [search, setSearch] = useState("");
  const [open, setOpen] = useState(false);
  return (
    <div className="space-y-6">
      <AdminPageHeader eyebrow="Internal" title="Kit preview" description="Every admin kit primitive in one place." />
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard label="Revenue" value="SAR 482K" delta={12} icon={Wallet} spark={[3, 5, 4, 6, 5, 7, 8]} />
        <StatCard label="Users" value="18,204" delta={4} icon={Users} />
        <StatCard label="Pending refunds" value="23" href="/admin/refunds" />
        <StatCard label="Failures" value="2" delta={-50} />
      </div>
      <SectionCard title="Records" action={<button onClick={() => setOpen(true)}>Open drawer</button>}>
        <FilterBar searchValue={search} onSearchChange={setSearch} searchPlaceholder="Search records" />
        <div className="mt-4">
          <DataTable columns={columns} rows={rows} getRowId={(r) => r.id} onRowClick={() => setOpen(true)} />
        </div>
      </SectionCard>
      <SectionCard title="States">
        <div className="grid gap-4 lg:grid-cols-3">
          <AdminEmptyState title="Empty" description="Nothing here" />
          <ErrorState onRetry={() => {}} />
          <TableSkeleton rows={4} columns={2} />
        </div>
      </SectionCard>
      <DetailDrawer open={open} onOpenChange={setOpen} title="Record detail" description="Demo drawer">
        <p className="text-sm">Drawer body content.</p>
      </DetailDrawer>
    </div>
  );
}
```

- [ ] **Step 2: Create the three locale mirrors**

Each mirror re-exports the shared page (match the existing mirror pattern):

```tsx
// app/(i18n)/en/admin/kit-preview/page.tsx
import KitPreviewPage from "@/app/(i18n)/_shared/admin/kit-preview/page";
export default function EnglishKitPreviewPage() {
  return <KitPreviewPage />;
}
```

Repeat for `ar` (`ArabicKitPreviewPage`) and `es` (`SpanishKitPreviewPage`), identical body.

- [ ] **Step 3: Run the full kit test suite**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/kit`
Expected: all kit tests PASS.

- [ ] **Step 4: Full repo gate**

Run: `pnpm experts:check`
Expected: FORMAT/LINT/TYPECHECK pass. If failing, `pnpm experts:check:fix` then re-run.

- [ ] **Step 5: Manual check**

Run the app, visit `/admin/kit-preview`. Confirm every primitive renders; toggle `ar` (RTL: search icon flips side, drawer mirrors) and dark mode (all surfaces legible).

- [ ] **Step 6: Commit**

```bash
git add "app/(i18n)/_shared/admin/kit-preview/page.tsx" "app/(i18n)/en/admin/kit-preview/page.tsx" "app/(i18n)/ar/admin/kit-preview/page.tsx" "app/(i18n)/es/admin/kit-preview/page.tsx"
git commit -m "feat(admin/kit): kit-preview demo page (replaces sidebar-preview)"
```

---

## Self-Review

- **Spec coverage (kit portion):** AdminPageHeader ✓(T2) · StatCard ✓(T5) · DataTable ✓(T8) · FilterBar ✓(T7) · EmptyState ✓(T6) · LoadingState ✓(T6) · ErrorState ✓(T6) · DetailDrawer ✓(T9) · SectionCard ✓(T3) · StatusBadge ✓(T4) · real account cluster ✓(T10) · kit-preview ✓(T11). All theme-safe (semantic tokens), RTL-considered, i18n via `admin.kit.*`.
- **Placeholder scan:** every step has complete code; primitive-API assumptions (`EmptyState` props, `Button` `onClick`/`onPress`, `Drawer` `direction`, `Avatar` subcomponents) are flagged for one-line verification against the real `ui/*` file, not left vague.
- **Type consistency:** `DataTableColumn`/`DataTable`, `AdminStatus`/`StatusBadge`, `AdminAccountProfile` used consistently across tasks and the barrel (T1). Barrel names match each component's exported symbol.

---

## Next plans

- **1c — ⌘K command palette** (reuses `ui/command` `CommandDialog`; sidebar ⌘K trigger; `command-registry`; starter actions).
- **1d — Dashboard rebuild** on this kit + new read-only triage queries.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
