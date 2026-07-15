---
title: "Tailwind CSS"
date: "2026-04-10"
updated: "2026-05-11"
tags: ["entity", "topic", "tech/tailwind-css"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Tailwind CSS.md"
---

# Tailwind CSS

Tailwind CSS is the styling utility layer behind much of the Experts frontend. In this vault it usually means fast UI iteration, token discipline, and the tradeoff between utility speed and long-term readability.

## Common conversation themes

- utility-heavy component styling
- keeping spacing and typography consistent
- mixing Tailwind with HeroUI or shadcn-ui
- avoiding unreadable class soup in complex components

## Gotchas captured in practice

- **Print artifacts vs theme-adaptive chrome must use different color sources.** A component that renders a printed page (letterhead, business card, invoice document, print profile spreads) keeps colors hardcoded as literal hex via arbitrary values (`bg-[#fff]`, `text-[#1a1718]`, gold `#c8a96e`). The surrounding workspace (generators, preview frames, showcase board) uses theme tokens (`bg-background`, `border-border`, `text-foreground`, `text-accent`) and flips with `.dark`. Decide per file which side it belongs to. (Captured 2026-05-11 during company-profile collateral migration.)
- **`@page`, `@media print`, and other irreducible print CSS** cannot be expressed in Tailwind utilities. Keep them in a tiny inline `<style>` const at the top of the file rather than maintaining a separate `.module.css` just for those rules.
- **`overflow-x-auto` + huge decorative absolute children (e.g. typographic backdrops) → unwanted horizontal scrollbar.** Use `overflow-x-clip` on the wrapper instead.
- **Motion (`motion/react`) transforms fight Tailwind transform utilities.** If a component uses `motion`'s `whileHover` / `animate` for transform, do not also apply `hover:scale-X` / `hover:rotate-0` Tailwind variants — they overwrite each other. Pick one source of truth per element. (Non-transform CSS hover like `hover:shadow-X`, `hover:brightness-X` is safe to combine.)
- **CSS Module → Tailwind migration approach** that worked across `showcase`, `print/page.tsx` (1327 lines), and `letterhead`: extract repeated class strings to module-top `const FOO_CLASS = "..."` only when a string appears 3+ times. Below that threshold, inline is more readable. Avoid pulling in `cn`/`clsx` deps just for concatenation — `+ " "` is fine.
- **Container queries (`container-type: inline-size`, `100cqw` math)** for print-preview scaling are best preserved exactly as arbitrary Tailwind values (`[container-type:inline-size]` + `[transform:scale(calc(100cqw/1123px))]`) rather than approximating with media queries.
- **Tailwind v4 logical properties (`ms`, `me`, `ps`, `pe`, `start`, `end`, `border-s`, `border-e`, `text-start`, `text-end`)** should be the default for any RTL-capable surface; `rtl:` variant overrides are reserved for transforms and decorative positioning that logical properties cannot express.

## Related

- [[Wiki/Concepts/CSS]]
- [[Wiki/Concepts/HeroUI]]
- [[Wiki/Concepts/shadcn-ui]]
- [[Wiki/Concepts/i18n]]
- [[Wiki/Concepts/Motion]]
- [[Raw/sources/2026-05-11-experts-showcase-tailwind-motion-rework]]
