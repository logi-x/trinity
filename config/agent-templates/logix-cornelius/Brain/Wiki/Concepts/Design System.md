---
title: "Design System"
date: "2026-07-01"
updated: "2026-07-01"
tags: ["entity", "topic", "design-system", "ui", "frontend"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Design System.md"
---

# Design System

The shared **UI foundation** of the Experts platform: the tokens, primitives,
and composition rules that keep the web app (and its native counterpart)
visually consistent, accessible, and bidirectional (LTR/RTL).

## In the Experts app (web)

- **HeroUI v3** is the primary component library, on **Tailwind CSS v4**;
  shadcn/Radix are used as fallbacks where a primitive is missing.
- Motion/animation via [[Wiki/Concepts/Motion]]; all surfaces must work in
  both **en/es (LTR)** and **ar (RTL)** — see [[Wiki/Concepts/i18n]].
- Design intent and taste guidance are captured under
  [[Wiki/Concepts/ui-ux-pro-max]].

## Native

- The SwiftUI client has its own tokens/components — see
  [[Projects/Experts/Experts OS/docs/reference/Glossary — Experts OS|Experts OS docs]]
  ("Design system — Experts OS").

## Related

- [[Wiki/Concepts/HeroUI]] · [[Wiki/Concepts/Tailwind CSS]] · [[Wiki/Concepts/shadcn-ui]]
- [[Wiki/Concepts/CSS]] · [[Wiki/Concepts/Motion]] · [[Wiki/Concepts/ui-ux-pro-max]]
