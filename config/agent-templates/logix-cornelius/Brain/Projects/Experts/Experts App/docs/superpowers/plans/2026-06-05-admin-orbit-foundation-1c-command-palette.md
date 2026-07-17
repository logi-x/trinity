---
title: "2026 06 05 admin orbit foundation 1c command palette"
date: "2026-06-05"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/plans/2026-06-05-admin-orbit-foundation-1c-command-palette.md"
---
# Admin Orbit Foundation — Plan 1c: ⌘K Command Palette

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a ⌘K command palette for the admin shell with an extensible action registry — foundation provides the engine, navigation commands, theme toggle, and a starter set of cross-cutting actions; later section waves register their own domain actions into the same registry.

**Architecture:** A module-level `command-registry` (pure, testable) holds `AdminCommand`s. `CommandPalette` reuses the in-repo `ui/command` `CommandDialog` (cmdk), binds the ⌘K / Ctrl+K hotkey, groups commands, and runs the selected command with a small context (`navigate`, `toggleTheme`, `closePalette`). Navigation commands derive from `admin-nav.ts` (plan 1a). Depends on plans 1a (nav + shell) and benefits from 1b but does not require the kit.

**Tech Stack:** React 19, `cmdk` via `@/components/ui/command` (`Command, CommandDialog, CommandInput, CommandList, CommandEmpty, CommandGroup, CommandItem, CommandShortcut`), `next-themes` (theme toggle), `@/i18n/routing` `useRouter`, `next-intl`, lucide-react, Vitest + Testing Library.

**Scope note:** Plan **1c of 4**. Domain actions (approve refund, suspend user, …) are **not** added here — they ship with their owning section in waves 2–4 via `registerCommands`. The existing `GlobalSearch` (content search) remains the top-bar/sidebar search; this plan ensures the two don't both bind ⌘K.

---

## File Structure

| File | Responsibility |
|------|----------------|
| `src/components/admin/command/command-registry.ts` | Pure registry: `registerCommands`, `getCommands`, `clearCommands`, types. No React. |
| `src/components/admin/command/nav-commands.ts` | Builds navigation `AdminCommand`s from `ADMIN_NAV`. |
| `src/components/admin/command/starter-commands.ts` | Cross-cutting starter actions (theme toggle, open website, go to console, copy URL). |
| `src/components/admin/command/CommandPalette.tsx` | The dialog + hotkey + grouped rendering + run. |
| `src/components/admin/command/use-command-palette.ts` | Open-state context/hook so the sidebar trigger and shell share one palette. |
| `src/components/admin/AdminWorkspaceShell.tsx` (modify) | Mount `<CommandPaletteProvider>` + `<CommandPalette/>`. |
| `src/components/admin/admin-sidebar.tsx` (modify) | Add a ⌘K trigger button in the header. |
| i18n `admin.command.*` keys (en/ar/es) | Palette copy. |

---

## Task 1: Command registry (pure)

**Files:**
- Create: `src/components/admin/command/command-registry.ts`
- Test: `src/components/admin/command/__tests__/command-registry.test.ts`

- [ ] **Step 1: Write the failing test**

```ts
import {describe, it, expect, beforeEach} from "vitest";
import {registerCommands, getCommands, clearCommands, type AdminCommand} from "../command-registry";

const cmd = (id: string): AdminCommand => ({
  id, group: "Test", label: id, run: () => {},
});

describe("command-registry", () => {
  beforeEach(() => clearCommands());

  it("registers and returns commands", () => {
    registerCommands([cmd("a"), cmd("b")]);
    expect(getCommands().map((c) => c.id)).toEqual(["a", "b"]);
  });

  it("dedupes by id (last write wins)", () => {
    registerCommands([cmd("a")]);
    registerCommands([{...cmd("a"), label: "updated"}]);
    expect(getCommands().filter((c) => c.id === "a")).toHaveLength(1);
    expect(getCommands().find((c) => c.id === "a")?.label).toBe("updated");
  });

  it("returns an unregister function", () => {
    const off = registerCommands([cmd("temp")]);
    off();
    expect(getCommands().find((c) => c.id === "temp")).toBeUndefined();
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/command/__tests__/command-registry.test.ts`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement**

```ts
// src/components/admin/command/command-registry.ts
import type {LucideIcon} from "lucide-react";

export interface AdminCommandContext {
  navigate: (href: string) => void;
  toggleTheme: () => void;
  closePalette: () => void;
}

export interface AdminCommand {
  id: string;
  /** Display group label (already localized by the caller). */
  group: string;
  /** Either a literal label or an i18n key resolved by the palette. */
  label?: string;
  labelKey?: string;
  icon?: LucideIcon;
  keywords?: string[];
  shortcut?: string;
  run: (ctx: AdminCommandContext) => void | Promise<void>;
  enabled?: () => boolean;
}

const registry = new Map<string, AdminCommand>();

/** Register commands; returns an unregister function for the same ids. */
export function registerCommands(commands: AdminCommand[]): () => void {
  for (const c of commands) registry.set(c.id, c);
  const ids = commands.map((c) => c.id);
  return () => {
    for (const id of ids) registry.delete(id);
  };
}

export function getCommands(): AdminCommand[] {
  return Array.from(registry.values()).filter((c) => c.enabled?.() ?? true);
}

export function clearCommands(): void {
  registry.clear();
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/command/__tests__/command-registry.test.ts`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add src/components/admin/command/command-registry.ts src/components/admin/command/__tests__/command-registry.test.ts
git commit -m "feat(admin/command): pure command registry"
```

---

## Task 2: Navigation + starter commands

**Files:**
- Create: `src/components/admin/command/nav-commands.ts`
- Create: `src/components/admin/command/starter-commands.ts`
- Test: `src/components/admin/command/__tests__/nav-commands.test.ts`

- [ ] **Step 1: Write the failing test**

```ts
import {describe, it, expect, vi} from "vitest";
import {buildNavCommands} from "../nav-commands";
import {ADMIN_NAV} from "../../admin-nav";

describe("buildNavCommands", () => {
  it("creates one navigate command per nav item", () => {
    const cmds = buildNavCommands((key) => key); // identity translator
    expect(cmds).toHaveLength(ADMIN_NAV.length);
    expect(cmds.every((c) => c.id.startsWith("nav:"))).toBe(true);
  });

  it("run() navigates to the item href", () => {
    const navigate = vi.fn();
    const closePalette = vi.fn();
    const cmds = buildNavCommands((key) => key);
    const dashboard = cmds.find((c) => c.id === "nav:dashboard")!;
    dashboard.run({navigate, toggleTheme: () => {}, closePalette});
    expect(navigate).toHaveBeenCalledWith("/admin");
    expect(closePalette).toHaveBeenCalledOnce();
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/command/__tests__/nav-commands.test.ts`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement both files**

```ts
// src/components/admin/command/nav-commands.ts
import {ADMIN_NAV} from "../admin-nav";
import type {AdminCommand} from "./command-registry";

/** translate: maps an i18n key to a localized string (the palette passes next-intl's `t`). */
export function buildNavCommands(translate: (key: string) => string): AdminCommand[] {
  return ADMIN_NAV.map((item) => ({
    id: `nav:${item.id}`,
    group: translate("command.groups.navigate"),
    label: translate(`nav.items.${item.labelKey}`),
    icon: item.icon,
    keywords: [item.href],
    run: ({navigate, closePalette}) => {
      navigate(item.href);
      closePalette();
    },
  }));
}
```

```ts
// src/components/admin/command/starter-commands.ts
import {ExternalLink, MoonStar, Terminal, Link2} from "lucide-react";
import type {AdminCommand} from "./command-registry";

export function buildStarterCommands(translate: (key: string) => string): AdminCommand[] {
  return [
    {
      id: "action:toggle-theme",
      group: translate("command.groups.actions"),
      label: translate("command.actions.toggleTheme"),
      icon: MoonStar,
      run: ({toggleTheme, closePalette}) => {
        toggleTheme();
        closePalette();
      },
    },
    {
      id: "action:open-website",
      group: translate("command.groups.actions"),
      label: translate("command.actions.openWebsite"),
      icon: ExternalLink,
      run: ({navigate, closePalette}) => {
        navigate("/");
        closePalette();
      },
    },
    {
      id: "action:go-console",
      group: translate("command.groups.actions"),
      label: translate("command.actions.goConsole"),
      icon: Terminal,
      run: ({navigate, closePalette}) => {
        navigate("/console");
        closePalette();
      },
    },
    {
      id: "action:copy-url",
      group: translate("command.groups.actions"),
      label: translate("command.actions.copyUrl"),
      icon: Link2,
      run: ({closePalette}) => {
        if (typeof window !== "undefined") void navigator.clipboard?.writeText(window.location.href);
        closePalette();
      },
    },
  ];
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/command/__tests__/nav-commands.test.ts`
Expected: PASS (2 tests).

- [ ] **Step 5: Commit**

```bash
git add src/components/admin/command/nav-commands.ts src/components/admin/command/starter-commands.ts src/components/admin/command/__tests__/nav-commands.test.ts
git commit -m "feat(admin/command): navigation + starter commands"
```

---

## Task 3: i18n keys for the palette

**Files:**
- Modify: `src/i18n/messages/{en,ar,es}/admin.json`

- [ ] **Step 1: Add `command` block to `en/admin.json`**

```json
"command": {
  "placeholder": "Type a command or search…",
  "empty": "No commands found",
  "trigger": "Command menu",
  "groups": {"navigate": "Navigate", "actions": "Actions"},
  "actions": {
    "toggleTheme": "Toggle theme",
    "openWebsite": "Open website",
    "goConsole": "Go to Console",
    "copyUrl": "Copy current URL"
  }
}
```

- [ ] **Step 2: Add `command` block to `ar/admin.json`**

```json
"command": {
  "placeholder": "اكتب أمرًا أو ابحث…",
  "empty": "لا توجد أوامر",
  "trigger": "قائمة الأوامر",
  "groups": {"navigate": "التنقل", "actions": "إجراءات"},
  "actions": {
    "toggleTheme": "تبديل السمة",
    "openWebsite": "فتح الموقع",
    "goConsole": "الذهاب إلى الكونسول",
    "copyUrl": "نسخ الرابط الحالي"
  }
}
```

- [ ] **Step 3: Add `command` block to `es/admin.json`**

```json
"command": {
  "placeholder": "Escribe un comando o busca…",
  "empty": "No se encontraron comandos",
  "trigger": "Menú de comandos",
  "groups": {"navigate": "Navegar", "actions": "Acciones"},
  "actions": {
    "toggleTheme": "Cambiar tema",
    "openWebsite": "Abrir sitio web",
    "goConsole": "Ir a la consola",
    "copyUrl": "Copiar URL actual"
  }
}
```

- [ ] **Step 4: Verify JSON validity**

Run: `cd apps/experts-app && node -e "['en','ar','es'].forEach(l=>{const m=require('./src/i18n/messages/'+l+'/admin.json'); if(!m.command?.actions?.toggleTheme) throw new Error('missing in '+l)}); console.log('ok')"`
Expected: prints `ok`.

- [ ] **Step 5: Commit**

```bash
git add src/i18n/messages/en/admin.json src/i18n/messages/ar/admin.json src/i18n/messages/es/admin.json
git commit -m "i18n(admin): command palette keys"
```

---

## Task 4: Palette open-state context (`use-command-palette`)

**Files:**
- Create: `src/components/admin/command/use-command-palette.ts`
- Test: `src/components/admin/command/__tests__/use-command-palette.test.tsx`

- [ ] **Step 1: Write the failing test**

```tsx
import {describe, it, expect} from "vitest";
import {renderHook, act} from "@testing-library/react";
import {CommandPaletteProvider, useCommandPalette} from "../use-command-palette";

describe("useCommandPalette", () => {
  it("toggles open state via context", () => {
    const {result} = renderHook(() => useCommandPalette(), {wrapper: CommandPaletteProvider});
    expect(result.current.open).toBe(false);
    act(() => result.current.setOpen(true));
    expect(result.current.open).toBe(true);
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/command/__tests__/use-command-palette.test.tsx`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement**

```tsx
// src/components/admin/command/use-command-palette.ts
"use client";

import {createContext, useContext, useState, type ReactNode} from "react";

interface CommandPaletteState {
  open: boolean;
  setOpen: (open: boolean) => void;
}

const Ctx = createContext<CommandPaletteState | null>(null);

export function CommandPaletteProvider({children}: {children: ReactNode}) {
  const [open, setOpen] = useState(false);
  return <Ctx.Provider value={{open, setOpen}}>{children}</Ctx.Provider>;
}

export function useCommandPalette(): CommandPaletteState {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useCommandPalette must be used within CommandPaletteProvider");
  return ctx;
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/command/__tests__/use-command-palette.test.tsx`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/components/admin/command/use-command-palette.ts src/components/admin/command/__tests__/use-command-palette.test.tsx
git commit -m "feat(admin/command): palette open-state context"
```

---

## Task 5: `CommandPalette` component

**Files:**
- Create: `src/components/admin/command/CommandPalette.tsx`
- Test: `src/components/admin/command/__tests__/command-palette.test.tsx`

**Context:** Registers nav + starter commands on mount, renders them grouped in the `CommandDialog`, binds ⌘K to toggle open, and runs a command on select. Uses `useRouter` from `@/i18n/routing` for `navigate` and `next-themes` `useTheme` for `toggleTheme`.

- [ ] **Step 1: Write the failing test**

```tsx
import {describe, it, expect, vi, beforeEach} from "vitest";
import {render, screen, fireEvent} from "@testing-library/react";
import {NextIntlClientProvider} from "next-intl";
import enAdmin from "@/i18n/messages/en/admin.json";
import {CommandPalette} from "../CommandPalette";
import {CommandPaletteProvider} from "../use-command-palette";
import {clearCommands} from "../command-registry";

const push = vi.fn();
vi.mock("@/i18n/routing", async (orig) => {
  const actual = await orig<typeof import("@/i18n/routing")>();
  return {...actual, useRouter: () => ({push})};
});
vi.mock("next-themes", () => ({useTheme: () => ({theme: "light", setTheme: vi.fn()})}));

function renderPalette() {
  return render(
    <NextIntlClientProvider locale="en" messages={{admin: enAdmin}}>
      <CommandPaletteProvider>
        <CommandPalette defaultOpen />
      </CommandPaletteProvider>
    </NextIntlClientProvider>,
  );
}

describe("CommandPalette", () => {
  beforeEach(() => {
    clearCommands();
    push.mockClear();
  });

  it("renders navigation commands when open", () => {
    renderPalette();
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
    expect(screen.getByText("Refunds")).toBeInTheDocument();
  });

  it("navigates when a nav command is selected", () => {
    renderPalette();
    fireEvent.click(screen.getByText("Users"));
    expect(push).toHaveBeenCalledWith("/admin/users");
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/command/__tests__/command-palette.test.tsx`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement**

```tsx
// src/components/admin/command/CommandPalette.tsx
"use client";

import {useEffect, useMemo} from "react";
import {useTranslations} from "next-intl";
import {useRouter} from "@/i18n/routing";
import {useTheme} from "next-themes";
import {
  CommandDialog,
  CommandInput,
  CommandList,
  CommandEmpty,
  CommandGroup,
  CommandItem,
} from "@/components/ui/command";
import {useCommandPalette} from "./use-command-palette";
import {registerCommands, getCommands, type AdminCommand, type AdminCommandContext} from "./command-registry";
import {buildNavCommands} from "./nav-commands";
import {buildStarterCommands} from "./starter-commands";

export function CommandPalette({defaultOpen = false}: {defaultOpen?: boolean}) {
  const t = useTranslations("admin");
  const router = useRouter();
  const {theme, setTheme} = useTheme();
  const {open, setOpen} = useCommandPalette();

  // Seed foundation commands once.
  useEffect(() => {
    const off = registerCommands([
      ...buildNavCommands((k) => t(k)),
      ...buildStarterCommands((k) => t(k)),
    ]);
    return off;
  }, [t]);

  // ⌘K / Ctrl+K toggles the palette.
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen(!open);
      }
    }
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open, setOpen]);

  useEffect(() => {
    if (defaultOpen) setOpen(true);
  }, [defaultOpen, setOpen]);

  const ctx: AdminCommandContext = useMemo(
    () => ({
      navigate: (href) => router.push(href),
      toggleTheme: () => setTheme(theme === "dark" ? "light" : "dark"),
      closePalette: () => setOpen(false),
    }),
    [router, theme, setTheme, setOpen],
  );

  // Group commands by their (already-localized) group label.
  const grouped = useMemo(() => {
    const map = new Map<string, AdminCommand[]>();
    for (const c of getCommands()) {
      const list = map.get(c.group) ?? [];
      list.push(c);
      map.set(c.group, list);
    }
    return Array.from(map.entries());
    // Recompute whenever the dialog opens so late-registered (section-wave) commands appear.
  }, [open]);

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder={t("command.placeholder")} />
      <CommandList>
        <CommandEmpty>{t("command.empty")}</CommandEmpty>
        {grouped.map(([group, commands]) => (
          <CommandGroup key={group} heading={group}>
            {commands.map((c) => {
              const Icon = c.icon;
              const label = c.label ?? (c.labelKey ? t(c.labelKey) : c.id);
              return (
                <CommandItem
                  key={c.id}
                  value={`${label} ${(c.keywords ?? []).join(" ")}`}
                  onSelect={() => void c.run(ctx)}
                >
                  {Icon && <Icon className="mr-2 h-4 w-4 rtl:mr-0 rtl:ml-2" />}
                  <span>{label}</span>
                </CommandItem>
              );
            })}
          </CommandGroup>
        ))}
      </CommandList>
    </CommandDialog>
  );
}
```

> `CommandItem`'s select handler is `onSelect` in cmdk. Confirm against `src/components/ui/command.tsx` (it re-exports cmdk's `Command.Item`). If `CommandDialog` does not accept `open`/`onOpenChange`, check the wrapper signature — the in-repo `CommandDialog` is used by `GlobalSearch` with open state, so the props exist.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin/command/__tests__/command-palette.test.tsx`
Expected: PASS (2 tests). cmdk filters by `value`; both Dashboard and Users render with no query.

- [ ] **Step 5: Commit**

```bash
git add src/components/admin/command/CommandPalette.tsx src/components/admin/command/__tests__/command-palette.test.tsx
git commit -m "feat(admin/command): CommandPalette (⌘K, grouped, runs commands)"
```

---

## Task 6: Mount the palette + sidebar trigger; reconcile ⌘K with GlobalSearch

**Files:**
- Modify: `src/components/admin/AdminWorkspaceShell.tsx`
- Modify: `src/components/admin/admin-sidebar.tsx`
- Check/Modify: `src/components/GlobalSearch.tsx`

- [ ] **Step 1: Check GlobalSearch's hotkey**

Run: `cd apps/experts-app && grep -nE "metaKey|ctrlKey|'k'|\"k\"|key === " src/components/GlobalSearch.tsx`
Expected: reveals whether `GlobalSearch` binds ⌘K. If it does, the admin palette and GlobalSearch would both open on ⌘K.

- [ ] **Step 2: Resolve the conflict (only if Step 1 found a ⌘K binding)**

`GlobalSearch` is content search; the admin palette owns ⌘K inside `/admin`. Give `GlobalSearch` an optional prop to disable its own hotkey, and pass it in admin:

In `src/components/GlobalSearch.tsx`, add a prop `disableHotkey?: boolean` and guard the keydown effect:
```tsx
export function GlobalSearch({disableHotkey = false}: {disableHotkey?: boolean} = {}) {
  // …inside the ⌘K keydown effect:
  useEffect(() => {
    if (disableHotkey) return;
    // …existing binding…
  }, [disableHotkey /*, …existing deps */]);
```
Then in `admin-sidebar.tsx` and the shell top bar, render `<GlobalSearch disableHotkey />`.

> If Step 1 shows GlobalSearch does **not** bind ⌘K, skip this step entirely and leave `GlobalSearch` untouched.

- [ ] **Step 3: Mount the provider + palette in the shell**

In `src/components/admin/AdminWorkspaceShell.tsx`:
- import `{CommandPaletteProvider}` and `{CommandPalette}` from `./command/use-command-palette` and `./command/CommandPalette`.
- Wrap the returned `SidebarProvider` tree in `<CommandPaletteProvider>` and render `<CommandPalette />` inside it (e.g. just before `</CommandPaletteProvider>`).

```tsx
// shape (only the wrapping shown):
return (
  <CommandPaletteProvider>
    <SidebarProvider /* …unchanged… */>
      {/* …unchanged shell… */}
    </SidebarProvider>
    <CommandPalette />
  </CommandPaletteProvider>
);
```

- [ ] **Step 4: Add the ⌘K trigger button to the sidebar header**

In `src/components/admin/admin-sidebar.tsx`, below the brand `Link` in `SidebarHeader`, add a button that opens the palette via `useCommandPalette`:

```tsx
import {useCommandPalette} from "./command/use-command-palette";
import {Kbd} from "@heroui/react";
import {Command as CommandIcon} from "lucide-react";

// inside the component:
const {setOpen} = useCommandPalette();

// in SidebarHeader, replacing or beside <GlobalSearch />:
<button
  type="button"
  onClick={() => setOpen(true)}
  aria-label={t("command.trigger")}
  className="border-border bg-background text-muted-foreground hover:text-foreground flex h-9 w-full items-center gap-2 rounded-xl border px-3 text-sm"
>
  <CommandIcon className="h-4 w-4" />
  <span className="flex-1 text-start">{t("command.placeholder")}</span>
  <Kbd>⌘K</Kbd>
</button>
```

> Because the sidebar now calls `useCommandPalette`, it must render inside `CommandPaletteProvider`. Step 3 wraps the whole shell (which contains `<AdminSidebar/>`) in the provider, so this is satisfied. Keep `<GlobalSearch disableHotkey />` if you still want content search in the header; otherwise the palette button can replace it.

- [ ] **Step 5: Run the admin + command suites**

Run: `cd apps/experts-app && pnpm vitest run src/components/admin`
Expected: all PASS. Update `admin-sidebar.test.tsx` / `admin-workspace-shell.test.tsx` to wrap rendered trees in `CommandPaletteProvider` if they now throw "must be used within CommandPaletteProvider".

- [ ] **Step 6: Typecheck**

Run: `cd apps/experts-app && pnpm typecheck:touched -- src/components/admin/AdminWorkspaceShell.tsx src/components/admin/admin-sidebar.tsx src/components/GlobalSearch.tsx`
Expected: no errors.

- [ ] **Step 7: Full gate + manual check**

Run: `pnpm experts:check` (fix with `pnpm experts:check:fix` if needed).
Manual: in `/admin`, press ⌘K → palette opens; type "ref" → Refunds; Enter navigates; click sidebar ⌘K button → opens; toggle theme action works; `ar` RTL: icon margins mirror; ensure GlobalSearch and palette don't both open on ⌘K.

- [ ] **Step 8: Commit**

```bash
git add src/components/admin/AdminWorkspaceShell.tsx src/components/admin/admin-sidebar.tsx src/components/GlobalSearch.tsx src/components/admin/__tests__
git commit -m "feat(admin/command): mount palette, sidebar ⌘K trigger, reconcile GlobalSearch hotkey"
```

---

## Self-Review

- **Spec coverage (palette portion):** engine + registry ✓(T1); nav commands ✓(T2); starter cross-cutting actions ✓(T2); ⌘K hotkey + grouped UI ✓(T5); extensibility contract for section waves (`registerCommands`) ✓(T1, used by T5); mounted in shell + sidebar trigger ✓(T6); i18n en/ar/es ✓(T3); RTL icon mirroring ✓(T5). Content search stays in `GlobalSearch`; hotkey conflict explicitly reconciled ✓(T6).
- **Placeholder scan:** complete code each step; cmdk prop names (`onSelect`, `CommandDialog` open/onOpenChange) flagged for one-line verification against the in-repo wrapper that `GlobalSearch` already uses.
- **Type consistency:** `AdminCommand`/`AdminCommandContext` from the registry are used identically in `nav-commands`, `starter-commands`, and `CommandPalette`. `useCommandPalette`/`CommandPaletteProvider` names match across T4/T6.

---

## Next plan

- **1d — Dashboard rebuild** on the kit (1b) with new read-only triage queries; the pending counts also get exposed as ⌘K actions registered from the dashboard.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
