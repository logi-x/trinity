---
title: "shadcn/ui to HeroUI Migration & Primary Color Tokens — outcome"
date: "2026-03-20"
tags: ["project/experts", "topic/heroui-migration", "outcome"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

# shadcn/ui to HeroUI Migration & Primary Color Tokens

**Outcome:** Migrated the primary shadcn/ui component set to HeroUI across the app and replaced all hardcoded violet/purple color classes with primary design tokens, enabling automatic dark mode and theme consistency. Core objective complete; a small tail of lower-traffic components was deferred to a future cleanup phase.

## What shipped
- 484 hardcoded violet/purple references across 83 files replaced with primary tokens (`text-primary`, `bg-primary/10`, `border-primary/20`); redundant `dark:` violet overrides removed since the CSS variable handles dark mode.
- `BRAND_PRIMARY_HEX` (`#4f6ef7`) constant added for OG image / canvas / Recharts contexts where CSS variables are unavailable.
- Button migrated to HeroUI across 68 files with prop API adjustments (`isDisabled`, `isIconOnly`, `color="danger"`, `as={Link}`).
- Badge migrated to HeroUI Chip across ~45 files; Card migrated to HeroUI Card compound components across 39 files.
- Form components (Input, Label, Textarea→TextArea, Checkbox, RadioGroup) and Select (via Select+ListBox compound pattern) migrated across 29 consumer files.
- Overlays migrated across 23 files: Dialog→Modal, AlertDialog→HeroUI AlertDialog, Sheet→Drawer, DropdownMenu→Dropdown — all using compound component patterns.
- Zero shadcn imports for the migrated components remain outside `src/components/ui/`.

## Key decisions
- `#4f6ef7` chosen as hex approximation of `oklch(0.58 0.17 255.97)` for non-CSS-variable contexts.
- Console categorical violet colors treated as brand colors (replaced), not semantic category colors.
- shadcn source files in `src/components/ui/` left untouched — retained for remaining internal ui/ dependencies (calendar, pagination, sidebar).
- HeroUI Badge is a notification dot, so Chip is used for all label/tag patterns; Card uses dot-notation sub-components (`Card.Header`, not `CardHeader`).
- `asChild` replaced with `as={Link} href=...`; `variant="destructive"` mapped to `color="danger"`; `disabled`→`isDisabled`, `size="icon"`→`isIconOnly`, `checked`→`isSelected`, `onCheckedChange`/`onValueChange`→`onChange`.
- Controlled modals use `useOverlayState`; nested AlertDialog-inside-DropdownMenuItem simplified to direct `onPress` handlers.

## Patterns established
- Brand color: always use primary tokens, never hardcoded violet/purple; charts use `BRAND_PRIMARY_HEX` or CSS variable accessor.
- HeroUI Select compound: `Select > Select.Trigger > Select.Value + Select.Indicator`, `Select.Popover > ListBox > ListBox.Item` (with `id`, `aria-label`, `textValue`).
- HeroUI overlay compounds: Modal (Backdrop/Container/Dialog/Header/Heading/Body/Footer), AlertDialog (trigger-based and controlled), Drawer (placement mapping: side→placement), Dropdown (Trigger/Popover/Menu/Item/Section/Separator).
- HeroUI form prop mapping conventions standardized across consumers.

## Key files
- `src/components/og/og-presets.ts`, `src/components/og/generate-og-image.tsx` — brand hex constant and OG defaults.
- Broad consumer surface across `app/(i18n)/_shared/**`, `src/components/**`, `src/lib/events/**`, `src/lib/courses/**` (navbars, profile, creator pages, event/course forms, dialogs).

## Deferred
- ~38 remaining shadcn imports for lower-traffic components (Tabs, Avatar, Progress→ProgressBar, Switch, Separator, Tooltip, Skeleton) across ~50 files deferred to a dedicated UI cleanup phase.
- Accessibility debt: ~90 `isIconOnly` Button instances lack `aria-label` (flagged in UI-REVIEW.md).
