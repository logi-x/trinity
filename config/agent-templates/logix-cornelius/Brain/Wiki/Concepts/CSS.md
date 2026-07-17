---
title: "CSS"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "topic/css", "styles"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/CSS.md"
---

# CSS

CSS in this vault usually means UI implementation quality in the Experts frontend: layout behavior, responsive fixes, design-system consistency, and the gap between intended design and actual rendered behavior.

## Where it shows up most

- component styling in the Experts app
- layout and spacing bugs
- modal, overlay, and stacking issues
- responsive behavior across admin and public surfaces
- design-token use with Tailwind and component libraries

## Practical themes from conversations

- fighting visual regressions after component changes
- aligning raw utility classes with reusable design patterns
- fixing overlay/z-index issues in modal-heavy flows
- keeping RTL support sane when styles become brittle

## Vault context

When a conversation links to this page, it usually is not about CSS as theory. It is about visual correctness, maintainability, and how styling decisions interact with [[Wiki/Concepts/HeroUI]], [[Wiki/Concepts/Tailwind CSS]], or custom component work.

## Rule of thumb

Treat CSS problems as product problems, not just polish. Spacing, hierarchy, and interaction feedback change trust, conversion, and admin usability.

## Related

- [[Wiki/Concepts/Tailwind CSS]]
- [[Wiki/Concepts/HeroUI]]
- [[Wiki/Concepts/ui-ux-pro-max]]
- [[Wiki/Concepts/i18n]]
