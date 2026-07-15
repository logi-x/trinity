---
title: "Motion"
date: "2026-05-11"
updated: "2026-05-11"
tags: ["entity", "topic", "tech/motion", "tech/framer-motion"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Motion.md"
---

# Motion

`motion` is the v12 successor to `framer-motion` — same library, new package name (`motion/react` for the React entrypoint). The Experts app has both `motion` and `framer-motion` installed at `^12.38.0`. Standardize on `motion/react` imports.

## Where used (so far)

- `apps/experts-app/app/(i18n)/_shared/company-profile/showcase/sections/CardStack.tsx` — hero card stack (spring lift on hover, staggered entrance).
- `.../BusinessCardFan.tsx` — 3D perspective tilt on hover, "dealt-in from the wings" entrance via `whileInView`.
- `.../SpreadsCarousel.tsx` — focused carousel with blurred neighbors, drag-to-swipe via `drag="x"`.

## Conventions

- **Reduced motion is opt-in.** Wrap clusters in `<MotionConfig reducedMotion="user">`. Motion does **not** automatically respect `prefers-reduced-motion` without this.
- **Transforms are owned by motion or by Tailwind — not both.** Motion's `whileHover` / `animate` writes inline transform; Tailwind's `hover:scale-X` / `hover:rotate-0` writes its own. They overwrite each other. Pick one source per element. Non-transform CSS hover (`hover:shadow-X`, `hover:brightness-X`) is safe to combine.
- **For `whileInView` entrance animations**, use `viewport={{once: true, margin: "-15% 0% -15% 0%"}}` for "fire once when section enters fold from below."
- **Spring config gives the feel.** Tight UI feedback uses `stiffness: 280-320, damping: 20-22`; weighty paper-like motion uses `stiffness: 110-140, damping: 16-18, mass: 0.7-0.95`.
- **RTL with motion.** Motion writes transforms inline; CSS `rtl:` variants don't intercept them. Pass `isRtl: boolean` as a prop and flip the sign of `rotate` / `x` translations programmatically. The `isRtl` value comes from `getLocale() === "ar"` in the server parent (next-intl).
- **Drag carousel pattern.** `drag="x"` + `dragConstraints={{left: 0, right: 0}}` + `dragElastic: 0.18` + `onDragEnd` reading `info.offset.x` past a threshold (~60px) for direction change.

## Related

- [[Wiki/Concepts/Tailwind CSS]]
- [[Wiki/Concepts/i18n]]
- [[Raw/sources/2026-05-11-experts-showcase-tailwind-motion-rework]]
