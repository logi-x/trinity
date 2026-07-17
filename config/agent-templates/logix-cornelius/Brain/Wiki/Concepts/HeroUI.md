---
title: "HeroUI"
date: "2026-04-10"
updated: "2026-07-13"
tags: ["entity", "topic", "tech/heroui"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/HeroUI.md"
---

# HeroUI

HeroUI is one of the main component-library reference points in Experts frontend work. Conversations usually bring it up when dealing with modal behavior, tables, form controls, overlays, and theming friction.

## Common pain points

- modal overlay and stacking issues
- component styling that fights custom design needs
- accessibility and keyboard behavior
- combining library defaults with Tailwind-heavy customization

## Vault context

HeroUI is less important as a brand choice than as a recurring implementation constraint. When it shows up, the real topic is often how much the product should conform to the library versus how much the library should be bent to the product.

## Experts theme boundary

Experts preserves the standard shadcn meaning of `--muted` as a background and `--muted-foreground` as subdued text. HeroUI v3 expects `--muted` to be subdued text and also couples `--default` to both structural fills and interaction states.

Do not patch or modify HeroUI packages to reconcile this mismatch. Keep the adaptation in an app-owned integration boundary, preserve shadcn compatibility, and use role-specific tokens only where one HeroUI token spans genuinely different visual roles.

The validated boundary in `apps/experts-app` has two parts:

- `postcss-semantic-color-bridge.cjs` runs after Tailwind expansion and rewrites `var(--muted)` only inside CSS `color` declarations to `var(--muted-foreground)`. Background declarations keep shadcn's `--muted` semantics, so upstream shadcn component updates need no local edits.
- `app/heroui-bridge.css` owns the narrow HeroUI role exceptions that cannot be inferred from the property alone. Tabs use `--control-track`; menu and listbox hover states use `--interaction-hover`. Theme values live in `globals.css` rather than in component or package source.

This boundary was verified against the production Turbopack output: no `color` declaration retained `var(--muted)`, while background declarations using it remained present.

## Related

- [[Wiki/Concepts/CSS]]
- [[Wiki/Concepts/Tailwind CSS]]
- [[Wiki/Concepts/React]]
- [[Wiki/Concepts/ui-ux-pro-max]]
