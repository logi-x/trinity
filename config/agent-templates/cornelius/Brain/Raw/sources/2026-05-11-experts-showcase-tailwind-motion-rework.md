---
title: "Experts Showcase — Tailwind/Motion Rework"
date: "2026-05-11"
tags: ["project/experts", "session", "project/experts-app", "tailwind", "motion", "company-profile", "showcase", "rtl", "i18n"]
category: "session"
source: "session"
source_id: "Raw/sources/2026-05-11-experts-showcase-tailwind-motion-rework.md"
---

# Experts Showcase — Tailwind/Motion Rework

Date: 2026-05-11
Branch: `enhance/company-profile-showcase`
Scope: `apps/experts-app/app/(i18n)/_shared/company-profile/showcase/**`, `_shared/company-profile/print/**`, `_shared/company/collateral/letterhead/**`

## Summary

Migrated the entire company-profile print/collateral surface from CSS Modules → Tailwind v4 utility classes, added light/dark theme awareness, fixed RTL throughout, then progressively redesigned the showcase board page: typographic backdrop, motion-driven hero card stack, motion-driven business-card fan with paper texture, focused carousel for spreads, and section reorder so Typography leads as the system foundation.

---

## Files Affected

### Converted CSS Modules → Tailwind (modules deleted)

| Module deleted                                                     | Component(s) updated                                               |
| ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| `showcase/showcase.module.css`                                     | `showcase/page.tsx` (later decomposed into multiple section files) |
| `print/print.module.css` (~856 lines)                              | `print/page.tsx` (~1327 lines, decomposed)                         |
| `company/collateral/letterhead/letterhead.module.css` (~343 lines) | `Letterhead.tsx`, `LetterheadGenerator.tsx`                        |

### New / restructured showcase files

```
showcase/
  page.tsx                          # server, composes sections + plumbs isRtl
  data.ts                           # SHOWCASE_CARD_SLOTS, ShowcaseCardEntry, fetchers
  previews.tsx                      # SpreadPreview, BusinessCard*Preview, Letterhead/Invoice previews
  spreads.tsx                       # ShowcaseSpread type + spreads[] data
  chrome.tsx                        # SectionLabel, SplitSection, CopyColumn primitives
  sections/
    hero.tsx                        # server shell, imports CardStack
    CardStack.tsx                   # client, motion deck for hero
    BackdropLetters.tsx             # server, huge bilingual glyphs as page backdrop
    ticker-strip.tsx
    typography-section.tsx
    spreads-section.tsx             # server shell, imports SpreadsCarousel
    SpreadsCarousel.tsx             # client, focused carousel with blur neighbors
    letterhead-section.tsx
    invoice-section.tsx
    business-cards-section.tsx      # server shell, imports BusinessCardFan
    BusinessCardFan.tsx             # client, motion fan with paper texture
    site-footer.tsx
```

Decomposition of `page.tsx` into the `sections/*` files happened during the user's iterative edits, not by my hand — the final shape preserves the server/client island pattern.

---

## Conventions Established

### Tailwind v4 token mapping

| CSS-module token            | Tailwind replacement                        | Notes                          |
| --------------------------- | ------------------------------------------- | ------------------------------ |
| `--ink` (page bg)           | `bg-background`                             | Theme-adaptive                 |
| `--muted` / `--muted-light` | `text-muted-foreground`                     |                                |
| `--line` (subtle border)    | `border-border`                             |                                |
| `--sheet` (subtle surface)  | `bg-card/50`                                |                                |
| Brand bluish accent         | `text-accent`, `bg-accent`, `border-accent` | Maps to `--color-accent` token |

### Print sub-brand vs theme-adaptive chrome

**Critical distinction** (came up across letterhead, print profile, and showcase):

- **Print artifact** (the page being printed): keep colors hardcoded (`bg-[#fff]`, `text-[#1a1718]`, `text-[#c8a96e]` gold). Do **not** use theme tokens — those flip in dark mode and would invert the printed page.
- **Workspace chrome** (generator forms, preview frames, surrounding UI): use theme tokens (`bg-card`, `text-foreground`, `border-border`).
- Gold `#c8a96e` is the **print sub-brand accent**, not the product brand. Product brand is the bluish `--accent` token. They coexist: print artifacts wear gold, the showcase board wrapping them wears the product's blue.

### RTL conventions

- Prefer logical properties (`ms`/`me`/`ps`/`pe`/`start`/`end`/`border-s`/`border-e`/`text-start`/`text-end`) over physical equivalents.
- Use `rtl:` variant only where logical utilities don't apply: transforms, decorative-only positioning, rotation flips.
- For motion-driven components: pass `isRtl: boolean` prop (sourced from `getLocale() === "ar"` in the server parent) and flip sign of `rotate` / `x` translations inline rather than via CSS.
- Arrow icons in carousel/buttons: `className="rtl:rotate-180"`.

### Motion library usage (`motion/react`, v12)

The project has both `motion` and `framer-motion` installed (v12). Standardized on **`motion/react`** (the modern import).

Wrap each interactive cluster in `<MotionConfig reducedMotion="user">` — motion does **not** auto-respect `prefers-reduced-motion`; explicit opt-in is required.

**Critical gotcha:** motion writes transforms to inline style. Tailwind transform utilities (`hover:scale-X`, `hover:rotate-0`) also write transform. They **fight each other**. Choose one:

- Motion controls transform → Tailwind handles only non-transform props (shadow, brightness via `filter`, opacity via CSS hover).
- Tailwind controls transform → no motion needed, simpler.

For motion-driven components, hover/focus/tap all use motion props (`whileHover`, `whileFocus`, `whileTap`) not CSS variants.

---

## Three Distinct Motion Treatments

Designed to feel related but not identical across the page:

### 1. Hero card stack (`CardStack.tsx`)

- 4-card centered stage (`580×540` aspect ratio, percent positions).
- **Entrance**: spring up from below (`y: 40 → 0`, `opacity: 0 → 1`), staggered `0.08s * i + 0.12s`.
- **Hover**: spring lift (`y: -14`, `rotate: 0`, `scale: 1.06`, `zIndex: 30`). Spring `stiffness: 320, damping: 22` — tight and responsive.
- Feels like: picking up paper from a stack.

### 2. Business cards (`BusinessCardFan.tsx`)

- "Dealt-in from the wings" entrance: each card flies in from the edge it lands nearest (`fromStart` flag → `x: ±220px`). Initial rotation exaggerated `* 2.4` then settles.
- Triggered via `whileInView` with `once: true, margin: "-15%"` — fires when section enters viewport (below the fold).
- **Hover**: 3D perspective tilt — parent `[perspective:1200px]`, child `[transform-style:preserve-3d]`. `rotateX: -10°` (tips top-back toward viewer), `y: -16`, `z: 60` (real 3D translation, not just up), `scale: 1.10`.
- Heavier mass (`0.95`) than hero (`0.7`) — cards land with weight.
- **Surface texture overlay** (per card): combined linen-weave (crosshatch `repeating-linear-gradient` at warm low-alpha) + paper-fiber SVG (`feTurbulence` with asymmetric `baseFrequency='0.55 0.9'` for fiber-like stretched noise, `feColorMatrix` sepia tint) + `mix-blend-multiply opacity-[0.35]`. Mimics premium uncoated/linen card stock without darkening the white card. Far better than plain SVG noise (which reads as digital artifact rather than fiber).
- Feels like: a real card deck.

### 3. Spreads carousel (`SpreadsCarousel.tsx`)

- Replaces a 3-col grid showing all 6 spreads. Saves ~2 viewport heights.
- One row, active card centered with two **blurred** neighbors (`filter: blur(8px)`, `scale: 0.78`, `opacity: 0.55`, `x: ±64%`). Cards beyond ±1 from active return `null`.
- **4 ways to navigate**: (1) click a blurred neighbor → it becomes center; (2) prev/next round buttons with rtl:rotate-180 arrows; (3) dot indicators (`bg-border w-2` → `bg-accent w-8` for active); (4) drag/swipe on active card via `drag="x"` with `dragElastic: 0.18`, threshold ±60px.
- Keyboard: `ArrowLeft`/`ArrowRight` (RTL-swapped semantics), `Home`/`End`. Region `role="region" aria-roledescription="carousel"`, dots `role="tab" aria-selected`, `sr-only aria-live="polite"` announcement on change.
- Feels like: a confident editorial display.

---

## Editorial Backdrop

`BackdropLetters.tsx` — 7 huge bilingual glyphs (`A B C D` DM Sans 900 + `ب أ ت` Readex Pro 700) scattered down the page at `text-foreground/[0.07]` light / `/0.06` dark. Theme-adaptive (uses `text-foreground`, not gold or rose). Each clamped `text-[clamp(220px,38vw,640px)]` with mild rotation (-6° to +8°), positioned at `top: Xvh` (~110vh apart), alternating `start`/`end` edges. Page `overflow-x-clip` clips edge bleed without scrollbar.

---

## Showcase Section Reorder (numbering changed)

| Position | Section         | Was    | Now    |
| -------- | --------------- | ------ | ------ |
| 1        | Hero            | —      | —      |
| 2        | Ticker          | —      | —      |
| 3        | **Typography**  | **05** | **01** |
| 4        | Profile spreads | 01     | **02** |
| 5        | Letterhead      | 02     | **03** |
| 6        | Tax invoice     | 03     | **04** |
| 7        | Business cards  | 04     | **05** |
| 8        | Footer          | —      | —      |

**Rationale**: Typography is the system foundation (atoms); spreads/letterhead/invoice/cards are artifacts built on it. Reading flow goes atoms → applied artifacts.

---

## Showcase `printStyles.profile` Migration

Old: `showcase/page.tsx` imported the `print.module.css` and concatenated `printStyles.profile + " ..."` onto the spread preview wrapper.

New: print/page.tsx exports a `profileClass` constant. Showcase imports it: `import { profileClass } from "../print/page"` (now from `print/profile-root.ts` after decomposition). Same concatenation shape; no module needed.

---

## Letterhead Print-vs-Chrome Split

`Letterhead.tsx` is the print artifact — kept literal hex colors (`#1a1718`, `#e0dcd8`, `#888`, etc.), gold `#c8a96e`, sub-pixel A4 dimensions (`793.7px`, `1122.5px`, `75.6px`, `49.6px`, etc.) via arbitrary Tailwind values. `@page { size: A4; margin: 0 }` survives as an inline `<style>` const at top of the file (Tailwind has no `@page` equivalent).

`LetterheadGenerator.tsx` is the workspace — uses theme tokens (`bg-card`, `border-border`, `text-foreground`).

---

## Known Gotchas Captured

1. **Motion transforms fight Tailwind transforms.** Pick one source of truth per element.
2. **`prefers-reduced-motion` is opt-in for motion**, not automatic — wrap with `<MotionConfig reducedMotion="user">`.
3. **`overflow-x-auto` + huge decorative backdrop letters → horizontal scrollbar.** Switch to `overflow-x-clip` on the main wrapper.
4. **`mix-blend-multiply` on white surface darkens visibly** even at low opacity if texture colors aren't very light. For "keep card white" effect: lighten texture RGB (e.g. warm cream `150,120,80` at alpha `0.025`) and lower wrapper opacity to ~`0.35`. Or switch to `mix-blend-overlay` which has near-zero darkening effect on near-white.
5. **`getLocale()` from `next-intl/server`** is the established RTL-detection pattern in `_shared/` pages — propagate `isRtl` via prop into client islands rather than re-detecting client-side.
6. **`useRef` not needed for carousel drag** — motion handles drag state internally; just provide `dragConstraints` and `onDragEnd`.
7. **The print sub-brand has its own accent (gold).** Don't mass-replace gold occurrences with `text-accent` — the printed artifacts are designed around gold and would need a full redesign to switch.

---

## Open Threads

- The product app's actual brand color (`--accent`, bluish) is now used on the showcase wrapper while the print artifacts inside keep gold. If product brand ever changes, only the showcase chrome needs updating; print artifacts stay independent.
- Eventually an `/ar/company-profile/showcase` route may want to exist (currently only `/en/`). The `_shared/` component is ready — `isRtl` propagates correctly, logical properties work end-to-end.
- The motion library import is `motion/react` (v12); if the team decides to consolidate, `framer-motion` could be removed from package.json since both ship the same code.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
