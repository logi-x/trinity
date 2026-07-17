---
title: "2026 06 05 admin orbit foundation 1d dashboard"
date: "2026-06-05"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/plans/2026-06-05-admin-orbit-foundation-1d-dashboard.md"
---
# Admin Orbit Foundation — Plan 1d: Dashboard Rebuild + Triage Queries

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the admin dashboard on the kit (plan 1b) with a scannable hero KPI row and an operations-triage panel ("what needs me now"), backed by one new read-only admin query, while preserving the existing data-wired panels.

**Architecture:** A new read-only `admin-triage.query.ts` returns counts of items awaiting admin action (pending refunds, pending payouts, pending certifications), exposed through a `GET /api/v1/admin/triage` route guarded by `requireAdmin()` and consumed via `useApiQuery`. The dashboard page is recomposed on `SectionCard`/`StatCard` from the kit; existing section components (`RevenueChart`, `UsersPanel`, etc.) keep their data wiring and are placed inside the new layout. The triage counts are also registered as ⌘K actions (plan 1c).

**Tech Stack:** Prisma (`RefundRequest`, `CertificationApplication`, `AffiliatePayout`), Next.js route handlers with `requireAdmin()` + zod, `useApiQuery(key, fetcher, swrConfig?, options?)`, the admin kit (1b), the command registry (1c), recharts, Vitest.

**Scope note:** Plan **1d of 4** — completes the Orbit Foundation. The dashboard's existing 8 panel components are **recomposed, not rewritten internally**; only the page layout, the hero KPI row, and the triage panel are new. This is the only plan in the foundation that adds backend (one read-only query + one route).

---

## File Structure

| File | Responsibility |
|------|----------------|
| `src/lib/admin/dto/admin-triage.dto.ts` | `AdminTriageDTO` shape. |
| `src/lib/admin/queries/admin-triage.query.ts` | `getAdminTriage()` — read-only counts via prisma. |
| `src/lib/admin/queries/__tests__/admin-triage.query.test.ts` | Unit test (mocked prisma). |
| `app/api/v1/admin/triage/route.ts` | `GET` handler, `requireAdmin()`-guarded. |
| `app/api/v1/admin/triage/__tests__/route.test.ts` | Auth + happy-path test. |
| `app/(i18n)/_shared/admin/(dashboard)/(sections)/TriagePanel.tsx` | Triage UI consuming `/api/v1/admin/triage`. |
| `app/(i18n)/_shared/admin/(dashboard)/(sections)/HeroKpis.tsx` | Hero KPI row (StatCards) from overview + triage. |
| `app/(i18n)/_shared/admin/(dashboard)/page.tsx` (rebuild) | New layout composing HeroKpis + TriagePanel + existing panels in `SectionCard`s. |
| `src/components/admin/command/dashboard-commands.ts` | Triage ⌘K actions registered from the dashboard. |
| i18n `admin.dashboard.*` keys (en/ar/es) | Dashboard copy. |

---

## Task 1: `AdminTriageDTO` + i18n keys

**Files:**
- Create: `src/lib/admin/dto/admin-triage.dto.ts`
- Modify: `src/i18n/messages/{en,ar,es}/admin.json`

- [ ] **Step 1: Create the DTO**

```ts
// src/lib/admin/dto/admin-triage.dto.ts
export interface AdminTriageDTO {
  pendingRefunds: number;
  pendingPayouts: number;
  pendingCertifications: number;
}
```

- [ ] **Step 2: Add `dashboard` block to `en/admin.json`**

```json
"dashboard": {
  "heroEyebrow": "Overview",
  "heroTitle": "Dashboard",
  "kpiRevenue": "Revenue",
  "kpiUsers": "Active users",
  "kpiSignups": "New signups",
  "kpiPendingRefunds": "Pending refunds",
  "kpiPendingPayouts": "Pending payouts",
  "kpiPendingCertifications": "Pending certifications",
  "triageTitle": "Needs your attention",
  "triageDescription": "Items awaiting an admin decision",
  "triageEmpty": "All clear — nothing pending",
  "viewAll": "View all"
}
```

- [ ] **Step 3: Add `dashboard` block to `ar/admin.json`**

```json
"dashboard": {
  "heroEyebrow": "نظرة عامة",
  "heroTitle": "اللوحة الرئيسية",
  "kpiRevenue": "الإيرادات",
  "kpiUsers": "المستخدمون النشطون",
  "kpiSignups": "تسجيلات جديدة",
  "kpiPendingRefunds": "مبالغ مستردة معلّقة",
  "kpiPendingPayouts": "مدفوعات معلّقة",
  "kpiPendingCertifications": "اعتمادات معلّقة",
  "triageTitle": "يحتاج انتباهك",
  "triageDescription": "عناصر بانتظار قرار المشرف",
  "triageEmpty": "كل شيء على ما يرام — لا يوجد معلّق",
  "viewAll": "عرض الكل"
}
```

- [ ] **Step 4: Add `dashboard` block to `es/admin.json`**

```json
"dashboard": {
  "heroEyebrow": "Resumen",
  "heroTitle": "Panel",
  "kpiRevenue": "Ingresos",
  "kpiUsers": "Usuarios activos",
  "kpiSignups": "Nuevos registros",
  "kpiPendingRefunds": "Reembolsos pendientes",
  "kpiPendingPayouts": "Pagos pendientes",
  "kpiPendingCertifications": "Certificaciones pendientes",
  "triageTitle": "Requiere tu atención",
  "triageDescription": "Elementos a la espera de una decisión",
  "triageEmpty": "Todo en orden, nada pendiente",
  "viewAll": "Ver todo"
}
```

- [ ] **Step 5: Verify + commit**

Run: `cd apps/experts-app && node -e "['en','ar','es'].forEach(l=>{const m=require('./src/i18n/messages/'+l+'/admin.json'); if(!m.dashboard?.triageTitle) throw new Error('missing in '+l)}); console.log('ok')"`
Expected: `ok`.

```bash
git add src/lib/admin/dto/admin-triage.dto.ts src/i18n/messages/en/admin.json src/i18n/messages/ar/admin.json src/i18n/messages/es/admin.json
git commit -m "feat(admin/dashboard): triage DTO + dashboard i18n keys"
```

---

## Task 2: `getAdminTriage()` read-only query

**Files:**
- Create: `src/lib/admin/queries/admin-triage.query.ts`
- Test: `src/lib/admin/queries/__tests__/admin-triage.query.test.ts`

**Context (verified against schema):**
- `RefundRequest.status` is `RefundStatus` with values `requested | approved | rejected | processed`. **Pending = `requested`**.
- `CertificationApplication.status` is `CertificationApplicationStatus`; values needing admin review = **`SUBMITTED`, `RESUBMITTED`, `NEEDS_INFO`**. (Use `SUBMITTED` + `RESUBMITTED` as the actionable set.)
- Payouts: the `AffiliatePayout` model exists. **Verify its pending status field/value** against `prisma/schema.prisma` (the `AffiliatePayout` block) and the existing affiliates payout query before finalizing the `where`. The template below uses `status: "pending"`; correct it to the real enum value if different.

- [ ] **Step 1: Write the failing test**

```ts
// src/lib/admin/queries/__tests__/admin-triage.query.test.ts
import {describe, it, expect, vi, beforeEach} from "vitest";

const count = vi.fn();
vi.mock("@/lib/prisma", () => ({
  default: {
    refundRequest: {count: (...a: unknown[]) => count("refund", ...a)},
    certificationApplication: {count: (...a: unknown[]) => count("cert", ...a)},
    affiliatePayout: {count: (...a: unknown[]) => count("payout", ...a)},
  },
}));

import {getAdminTriage} from "../admin-triage.query";

describe("getAdminTriage", () => {
  beforeEach(() => count.mockReset());

  it("returns counts for the three pending buckets", async () => {
    count.mockImplementation((kind: string) =>
      Promise.resolve(kind === "refund" ? 3 : kind === "cert" ? 5 : 2),
    );
    const result = await getAdminTriage();
    expect(result).toEqual({pendingRefunds: 3, pendingCertifications: 5, pendingPayouts: 2});
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/lib/admin/queries/__tests__/admin-triage.query.test.ts`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement**

```ts
// src/lib/admin/queries/admin-triage.query.ts
import prisma from "@/lib/prisma";
import type {AdminTriageDTO} from "../dto/admin-triage.dto";

export async function getAdminTriage(): Promise<AdminTriageDTO> {
  const [pendingRefunds, pendingCertifications, pendingPayouts] = await Promise.all([
    prisma.refundRequest.count({where: {status: "requested"}}),
    prisma.certificationApplication.count({where: {status: {in: ["SUBMITTED", "RESUBMITTED"]}}}),
    // VERIFY: AffiliatePayout pending status value against prisma/schema.prisma.
    prisma.affiliatePayout.count({where: {status: "pending"}}),
  ]);

  return {pendingRefunds, pendingPayouts, pendingCertifications};
}
```

> Run `cd apps/experts-app && awk '/model AffiliatePayout/{f=1} f{print} /^}/{if(f)f=0}' prisma/schema.prisma` to read the payout status field/enum, and adjust the third `count` `where` accordingly. If `AffiliatePayout` has no `status`, use the field that represents "not yet paid" (e.g. `paidAt: null`) and update the test's `payout` branch to match.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/lib/admin/queries/__tests__/admin-triage.query.test.ts`
Expected: PASS.

- [ ] **Step 5: Typecheck against the real Prisma client**

Run: `cd apps/experts-app && pnpm typecheck:touched -- src/lib/admin/queries/admin-triage.query.ts`
Expected: no errors. If a `where.status` value is not assignable, that means the enum value is wrong — fix it to the real value (this is the verification gate).

- [ ] **Step 6: Commit**

```bash
git add src/lib/admin/queries/admin-triage.query.ts src/lib/admin/queries/__tests__/admin-triage.query.test.ts
git commit -m "feat(admin/dashboard): read-only triage counts query"
```

---

## Task 3: `GET /api/v1/admin/triage` route

**Files:**
- Create: `app/api/v1/admin/triage/route.ts`
- Test: `app/api/v1/admin/triage/__tests__/route.test.ts`

**Context:** Mirror the existing admin route pattern (`app/api/v1/admin/events/route.ts`): `requireAdmin()` from `@/lib/permissions`, `NextResponse.json`, try/catch → 500 with a generic message (no internal detail leaked).

- [ ] **Step 1: Write the failing test**

```ts
// app/api/v1/admin/triage/__tests__/route.test.ts
import {describe, it, expect, vi, beforeEach} from "vitest";

const requireAdmin = vi.fn();
const getAdminTriage = vi.fn();
vi.mock("@/lib/permissions", () => ({requireAdmin: () => requireAdmin()}));
vi.mock("@/lib/admin/queries/admin-triage.query", () => ({getAdminTriage: () => getAdminTriage()}));

import {GET} from "../route";

describe("GET /api/v1/admin/triage", () => {
  beforeEach(() => {
    requireAdmin.mockReset();
    getAdminTriage.mockReset();
  });

  it("returns 403 for non-admins", async () => {
    requireAdmin.mockResolvedValue({authorized: false, error: "Forbidden"});
    const res = await GET();
    expect(res.status).toBe(403);
  });

  it("returns triage counts for admins", async () => {
    requireAdmin.mockResolvedValue({authorized: true});
    getAdminTriage.mockResolvedValue({pendingRefunds: 3, pendingPayouts: 2, pendingCertifications: 5});
    const res = await GET();
    expect(res.status).toBe(200);
    await expect(res.json()).resolves.toEqual({pendingRefunds: 3, pendingPayouts: 2, pendingCertifications: 5});
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run "app/api/v1/admin/triage/__tests__/route.test.ts"`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement**

```ts
// app/api/v1/admin/triage/route.ts
import {NextResponse} from "next/server";
import {requireAdmin} from "@/lib/permissions";
import {getAdminTriage} from "@/lib/admin/queries/admin-triage.query";

export async function GET() {
  const {authorized, error: authError} = await requireAdmin();
  if (!authorized) {
    return NextResponse.json(
      {error: authError || "Forbidden"},
      {status: authError?.includes("Unauthorized") ? 401 : 403},
    );
  }

  try {
    const result = await getAdminTriage();
    return NextResponse.json(result);
  } catch (error) {
    console.error("[admin/triage] query failed", error);
    return NextResponse.json({error: "Internal server error"}, {status: 500});
  }
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run "app/api/v1/admin/triage/__tests__/route.test.ts"`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add "app/api/v1/admin/triage/route.ts" "app/api/v1/admin/triage/__tests__/route.test.ts"
git commit -m "feat(admin/dashboard): triage API route (admin-guarded)"
```

---

## Task 4: `TriagePanel` section

**Files:**
- Create: `app/(i18n)/_shared/admin/(dashboard)/(sections)/TriagePanel.tsx`
- Test: `app/(i18n)/_shared/admin/(dashboard)/(sections)/__tests__/TriagePanel.test.tsx`

**Context:** Client component using `useApiQuery<AdminTriageDTO>` against `/api/v1/admin/triage`, rendered inside a kit `SectionCard`, with `StatCard` links to the relevant sections; shows the kit loading/error states.

- [ ] **Step 1: Write the failing test**

```tsx
import {describe, it, expect, vi} from "vitest";
import {render, screen} from "@testing-library/react";
import {NextIntlClientProvider} from "next-intl";
import enAdmin from "@/i18n/messages/en/admin.json";
import {TriagePanel} from "../TriagePanel";

vi.mock("@/hooks/use-api-query", () => ({
  useApiQuery: () => ({
    data: {pendingRefunds: 3, pendingPayouts: 2, pendingCertifications: 5},
    isLoading: false,
    error: undefined,
    tokenReady: true,
    isAuthLoading: false,
  }),
}));

describe("TriagePanel", () => {
  it("renders the three triage counts", () => {
    render(
      <NextIntlClientProvider locale="en" messages={{admin: enAdmin}}>
        <TriagePanel />
      </NextIntlClientProvider>,
    );
    expect(screen.getByText("Pending refunds")).toBeInTheDocument();
    expect(screen.getByText("3")).toBeInTheDocument();
    expect(screen.getByText("5")).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run "app/(i18n)/_shared/admin/(dashboard)/(sections)/__tests__/TriagePanel.test.tsx"`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement**

```tsx
// app/(i18n)/_shared/admin/(dashboard)/(sections)/TriagePanel.tsx
"use client";

import {useTranslations} from "next-intl";
import type {AdminTriageDTO} from "@/lib/admin/dto/admin-triage.dto";
import {useApiQuery} from "@/hooks/use-api-query";
import {SectionCard, StatCard, CardsSkeleton, ErrorState} from "@/components/admin/kit";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export function TriagePanel() {
  const t = useTranslations("admin.dashboard");
  const {data, isLoading, error} = useApiQuery<AdminTriageDTO>(
    "/api/v1/admin/triage",
    fetcher,
    {revalidateOnFocus: false},
    {requireAuth: true},
  );

  return (
    <SectionCard title={t("triageTitle")} description={t("triageDescription")}>
      {isLoading ? (
        <CardsSkeleton count={3} />
      ) : error ? (
        <ErrorState />
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <StatCard label={t("kpiPendingRefunds")} value={data?.pendingRefunds ?? 0} href="/admin/refunds" />
          <StatCard label={t("kpiPendingPayouts")} value={data?.pendingPayouts ?? 0} href="/admin/payouts" />
          <StatCard label={t("kpiPendingCertifications")} value={data?.pendingCertifications ?? 0} href="/admin/certifications" />
        </div>
      )}
    </SectionCard>
  );
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run "app/(i18n)/_shared/admin/(dashboard)/(sections)/__tests__/TriagePanel.test.tsx"`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add "app/(i18n)/_shared/admin/(dashboard)/(sections)/TriagePanel.tsx" "app/(i18n)/_shared/admin/(dashboard)/(sections)/__tests__/TriagePanel.test.tsx"
git commit -m "feat(admin/dashboard): triage panel"
```

---

## Task 5: `HeroKpis` row

**Files:**
- Create: `app/(i18n)/_shared/admin/(dashboard)/(sections)/HeroKpis.tsx`
- Test: `app/(i18n)/_shared/admin/(dashboard)/(sections)/__tests__/HeroKpis.test.tsx`

**Context:** Reuse the existing overview data source. Read `app/(i18n)/_shared/admin/(dashboard)/(sections)/OverviewCards.tsx` to find the exact hook/DTO it uses (`AdminOverviewDTO` via `useApiQuery`) and the field names for revenue / users / signups; reuse the **same** endpoint so no new query is needed for these three. Render them as kit `StatCard`s with deltas if the DTO provides them.

- [ ] **Step 1: Inspect the overview data source**

Run: `cd apps/experts-app && sed -n '40,176p' "app/(i18n)/_shared/admin/(dashboard)/(sections)/OverviewCards.tsx"`
Note the endpoint string, the `AdminOverviewDTO` import path, and the property names for revenue, users, and new signups (and any `*Change`/delta fields).

- [ ] **Step 2: Write the failing test**

```tsx
import {describe, it, expect, vi} from "vitest";
import {render, screen} from "@testing-library/react";
import {NextIntlClientProvider} from "next-intl";
import enAdmin from "@/i18n/messages/en/admin.json";
import {HeroKpis} from "../HeroKpis";

// Match the real AdminOverviewDTO field names discovered in Step 1.
vi.mock("@/hooks/use-api-query", () => ({
  useApiQuery: () => ({
    data: {totalRevenue: 482000, totalUsers: 18204, newSignups: 320},
    isLoading: false,
    error: undefined,
    tokenReady: true,
    isAuthLoading: false,
  }),
}));

describe("HeroKpis", () => {
  it("renders the revenue, users and signups KPIs", () => {
    render(
      <NextIntlClientProvider locale="en" messages={{admin: enAdmin}}>
        <HeroKpis />
      </NextIntlClientProvider>,
    );
    expect(screen.getByText("Revenue")).toBeInTheDocument();
    expect(screen.getByText("Active users")).toBeInTheDocument();
    expect(screen.getByText("New signups")).toBeInTheDocument();
  });
});
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run "app/(i18n)/_shared/admin/(dashboard)/(sections)/__tests__/HeroKpis.test.tsx"`
Expected: FAIL — module not found.

- [ ] **Step 4: Implement (adjust field names to match Step 1)**

```tsx
// app/(i18n)/_shared/admin/(dashboard)/(sections)/HeroKpis.tsx
"use client";

import {useTranslations} from "next-intl";
import {Wallet, Users, UserPlus} from "lucide-react";
import type {AdminOverviewDTO} from "@/lib/admin/dto/admin-overview.dto";
import {useApiQuery} from "@/hooks/use-api-query";
import {StatCard, CardsSkeleton} from "@/components/admin/kit";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

export function HeroKpis() {
  const t = useTranslations("admin.dashboard");
  // Use the SAME endpoint OverviewCards uses (confirmed in Step 1).
  const {data, isLoading} = useApiQuery<AdminOverviewDTO>(
    "/api/v1/admin/overview",
    fetcher,
    {revalidateOnFocus: false},
    {requireAuth: true},
  );

  if (isLoading) return <CardsSkeleton count={3} />;

  // Replace the property accesses below with the real AdminOverviewDTO fields from Step 1.
  const revenue = (data as {totalRevenue?: number})?.totalRevenue ?? 0;
  const users = (data as {totalUsers?: number})?.totalUsers ?? 0;
  const signups = (data as {newSignups?: number})?.newSignups ?? 0;

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
      <StatCard label={t("kpiRevenue")} value={`SAR ${revenue.toLocaleString()}`} icon={Wallet} />
      <StatCard label={t("kpiUsers")} value={users.toLocaleString()} icon={Users} />
      <StatCard label={t("kpiSignups")} value={signups.toLocaleString()} icon={UserPlus} />
    </div>
  );
}
```

> If the overview endpoint string or `AdminOverviewDTO` field names differ from the placeholders, fix both the implementation and the test mock to the real names. The `as {…}` casts are a deliberate bridge so the file typechecks before you finalize the real field names; replace them with direct `data?.field` access once confirmed (do not leave the casts in the committed version if the real fields are known).

- [ ] **Step 5: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run "app/(i18n)/_shared/admin/(dashboard)/(sections)/__tests__/HeroKpis.test.tsx"`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add "app/(i18n)/_shared/admin/(dashboard)/(sections)/HeroKpis.tsx" "app/(i18n)/_shared/admin/(dashboard)/(sections)/__tests__/HeroKpis.test.tsx"
git commit -m "feat(admin/dashboard): hero KPI row reusing overview data"
```

---

## Task 6: Rebuild the dashboard page layout

**Files:**
- Modify (rebuild): `app/(i18n)/_shared/admin/(dashboard)/page.tsx`

**Context:** Compose the new sections + the existing panels into the kit layout. The existing panel components (`RevenueChart`, `OperationsPanel`, `UsersPanel`, `RecentActivity`, `PerformancePanel`, `CategoriesPanel`, `ContentStats`) keep their own data wiring; they are placed inside the new grid. The old `OverviewCards` is superseded by `HeroKpis` (remove its usage from the page but keep the file for now — a later wave may delete it).

- [ ] **Step 1: Replace the page body**

```tsx
// app/(i18n)/_shared/admin/(dashboard)/page.tsx
"use client";

import {HeroKpis} from "./(sections)/HeroKpis";
import {TriagePanel} from "./(sections)/TriagePanel";
import {ContentStats} from "./(sections)/ContentStats";
import {RevenueChart} from "./(sections)/RevenueChart";
import {UsersPanel} from "./(sections)/UsersPanel";
import {OperationsPanel} from "./(sections)/OperationsPanel";
import {CategoriesPanel} from "./(sections)/CategoriesPanel";
import {PerformancePanel} from "./(sections)/PerformancePanel";
import {RecentActivity} from "./(sections)/RecentActivity";

export default function AdminDashboardPage() {
  return (
    <div className="space-y-6 pb-8" dir="ltr">
      <HeroKpis />
      <TriagePanel />

      <ContentStats variant="panel" />

      <div className="grid gap-6 lg:grid-cols-3">
        <RevenueChart variant="panel" className="lg:col-span-2" />
        <OperationsPanel variant="panel" />
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <UsersPanel variant="panel" className="lg:col-span-2" />
        <RecentActivity variant="panel" />
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <PerformancePanel variant="panel" className="lg:col-span-2" />
        <CategoriesPanel variant="panel" />
      </div>
    </div>
  );
}
```

> The `dir="ltr"` wrapper is preserved from the original (charts/numbers read LTR even in Arabic). If the existing panels already render their own card chrome, leave them as-is — do not double-wrap them in `SectionCard`. Only `HeroKpis`/`TriagePanel` use the kit directly.

- [ ] **Step 2: Run the dashboard section tests**

Run: `cd apps/experts-app && pnpm vitest run "app/(i18n)/_shared/admin/(dashboard)"`
Expected: PASS.

- [ ] **Step 3: Typecheck the dashboard tree**

Run: `cd apps/experts-app && pnpm typecheck:touched -- "app/(i18n)/_shared/admin/(dashboard)/page.tsx" "app/(i18n)/_shared/admin/(dashboard)/(sections)/HeroKpis.tsx" "app/(i18n)/_shared/admin/(dashboard)/(sections)/TriagePanel.tsx"`
Expected: no errors.

- [ ] **Step 4: Commit**

```bash
git add "app/(i18n)/_shared/admin/(dashboard)/page.tsx"
git commit -m "feat(admin/dashboard): recompose dashboard on kit with hero KPIs + triage"
```

---

## Task 7: Register triage ⌘K actions from the dashboard

**Files:**
- Create: `src/components/admin/command/dashboard-commands.ts`
- Modify: `app/(i18n)/_shared/admin/(dashboard)/page.tsx` (register on mount)
- Test: `src/components/admin/command/__tests__/dashboard-commands.test.ts`

**Context:** Demonstrates the registry-extensibility contract from plan 1c — the dashboard registers "view pending …" navigation actions so they appear in ⌘K.

- [ ] **Step 1: Write the failing test**

```ts
import {describe, it, expect, vi} from "vitest";
import {buildDashboardCommands} from "../dashboard-commands";

describe("buildDashboardCommands", () => {
  it("creates triage navigation actions", () => {
    const cmds = buildDashboardCommands((k) => k);
    const ids = cmds.map((c) => c.id);
    expect(ids).toContain("dashboard:view-refunds");
    expect(ids).toContain("dashboard:view-certifications");
  });

  it("navigates on run", () => {
    const navigate = vi.fn();
    const closePalette = vi.fn();
    const cmd = buildDashboardCommands((k) => k).find((c) => c.id === "dashboard:view-refunds")!;
    cmd.run({navigate, toggleTheme: () => {}, closePalette});
    expect(navigate).toHaveBeenCalledWith("/admin/refunds");
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/command/__tests__/dashboard-commands.test.ts`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement the commands builder**

```ts
// src/components/admin/command/dashboard-commands.ts
import {HandCoins, BadgeCheck, Wallet} from "lucide-react";
import type {AdminCommand} from "./command-registry";

export function buildDashboardCommands(translate: (key: string) => string): AdminCommand[] {
  const group = translate("command.groups.navigate");
  const mk = (id: string, labelKey: string, href: string, icon: AdminCommand["icon"]): AdminCommand => ({
    id,
    group,
    label: translate(labelKey),
    icon,
    run: ({navigate, closePalette}) => {
      navigate(href);
      closePalette();
    },
  });
  return [
    mk("dashboard:view-refunds", "dashboard.kpiPendingRefunds", "/admin/refunds", HandCoins),
    mk("dashboard:view-payouts", "dashboard.kpiPendingPayouts", "/admin/payouts", Wallet),
    mk("dashboard:view-certifications", "dashboard.kpiPendingCertifications", "/admin/certifications", BadgeCheck),
  ];
}
```

- [ ] **Step 4: Register them on the dashboard**

Add to `app/(i18n)/_shared/admin/(dashboard)/page.tsx` (it is already `"use client"`):

```tsx
import {useEffect} from "react";
import {useTranslations} from "next-intl";
import {registerCommands} from "@/components/admin/command/command-registry";
import {buildDashboardCommands} from "@/components/admin/command/dashboard-commands";

// inside AdminDashboardPage, before the return:
const t = useTranslations("admin");
useEffect(() => {
  const off = registerCommands(buildDashboardCommands((k) => t(k)));
  return off;
}, [t]);
```

- [ ] **Step 5: Run tests**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/command/__tests__/dashboard-commands.test.ts "app/(i18n)/_shared/admin/(dashboard)"`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/components/admin/command/dashboard-commands.ts "app/(i18n)/_shared/admin/(dashboard)/page.tsx" src/components/admin/command/__tests__/dashboard-commands.test.ts
git commit -m "feat(admin/dashboard): register triage actions into ⌘K"
```

---

## Task 8: Full gate + manual verification + foundation wrap-up

**Files:** none (verification)

- [ ] **Step 1: Run the full admin + api test scope**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin src/lib/admin "app/(i18n)/_shared/admin" "app/api/v1/admin/triage"`
Expected: all PASS.

- [ ] **Step 2: Repo gate**

Run: `pnpm experts:check` (then `pnpm experts:check:fix` if needed, re-run).
Expected: FORMAT/LINT/TYPECHECK pass.

- [ ] **Step 3: Manual dashboard verification**

Run the app, visit `/admin`:
- Hero KPI row shows Revenue / Active users / New signups.
- Triage panel shows the three pending counts (or the empty/loading/error state); each card links to its section.
- Existing panels (revenue chart, users, activity, performance, categories) still render with data.
- ⌘K → type "pending" → the dashboard triage actions appear and navigate.
- Toggle `ar` (numbers/charts stay LTR inside the panels) and dark mode (legible).

- [ ] **Step 4: Final foundation commit (if fixes applied)**

```bash
git add -A && git commit -m "chore(admin): format/lint fixes for dashboard rebuild" || echo "nothing to commit"
```

---

## Self-Review

- **Spec coverage (dashboard portion):** hero KPI row ✓(T5); operations triage ✓(T2–T4); pending refunds/payouts/certifications as triage + ⌘K actions ✓(T4, T7); existing 8 panels' data wiring preserved ✓(T6); one read-only admin query + route, the only backend surface ✓(T2–T3); admin-guarded ✓(T3); i18n en/ar/es ✓(T1). New metric queries are enumerated (exactly one: `getAdminTriage`) per the spec's requirement to list them.
- **Placeholder scan:** every code step is complete; the two genuine unknowns (AffiliatePayout pending status; AdminOverviewDTO field names) are gated by explicit inspect-then-fix steps with the exact command to run, plus a typecheck gate that fails loudly if the guess is wrong — not silent placeholders.
- **Type consistency:** `AdminTriageDTO` used identically across query (T2), route (T3), and panel (T4). `buildDashboardCommands` returns `AdminCommand[]` matching the registry (1c). `useApiQuery` call shape matches the verified 4-arg signature.

---

## Foundation complete

After plans 1a–1d: one nav source of truth, layered shell with real breadcrumb + account cluster, a reusable kit, a ⌘K palette with an extensible registry, and a rebuilt dashboard with triage — all theme-safe and RTL-correct, with the placeholder/dead chrome gone. Waves 2–4 (Operations / Finance / Insights & Platform) then apply the kit and register domain ⌘K actions per section.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
