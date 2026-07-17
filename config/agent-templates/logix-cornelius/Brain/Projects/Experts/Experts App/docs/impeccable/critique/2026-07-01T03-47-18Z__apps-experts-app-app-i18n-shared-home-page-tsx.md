---
target: landing
total_score: 23
p0_count: 1
p1_count: 2
timestamp: 2026-07-01T03-47-18Z
slug: apps-experts-app-app-i18n-shared-home-page-tsx
title: "2026 07 01T03 47 18Z apps experts app app i18n shared home page tsx"
date: "2026-07-01"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
---

Method: dual-agent (A: design review · B: detector + browser evidence) — both isolated, both verified against the live dev server at http://localhost:3025 (/en + /ar, desktop 1440px + mobile 390px).

# Critique — Landing / Home page

Target: `apps/experts-app/app/(i18n)/_shared/(home)/page.tsx` + its 10 `(sections)/`.

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 2 | Stats render literal "0 Courses / 0% completion" with no state distinguishing "loading" from "genuinely zero". |
| 2 | Match System / Real World | 3 | Copy is plain and task-appropriate; the gallery repeating one "Dental Occlusion" thumbnail ×6 reads as a data bug. |
| 3 | User Control and Freedom | 3 | Hero auto-rotates every 6s; desktop pauses on hover, but mobile has no pause and only 2px dots as controls. |
| 4 | Consistency and Standards | 1 | The hero — the highest-visibility button on the platform — abandons the pill-shape + single-blue system every other button follows. |
| 5 | Error Prevention | 3 | No destructive actions on this page; low risk. |
| 6 | Recognition Rather Than Recall | 3 | Icon+label nav, clear section headers. |
| 7 | Flexibility and Efficiency | 2 | Hero carousel dots are bare `<button>`s with no "slide 2 of 3" affordance; no keyboard path. |
| 8 | Aesthetic and Minimalist Design | 1 | Directly contradicts the platform's own "Control Room" north star: glow-blur, 3-color rotating hero, 5-hue stat icons, stacked hero-metric cards, marquee, scroll-velocity gallery. |
| 9 | Error Recovery | 2 | Empty states exist but "No reviews yet" sits under "What Our Learners Say — Join thousands of satisfied students". |
| 10 | Help and Documentation | 3 | FAQ section is genuinely well done, with a contact-support escape hatch. |
| **Total** | | **23/40** | **Acceptable band — significant improvements needed** |

## Anti-Patterns Verdict

**Does it look AI-generated? Yes — inside ~3 seconds.** The tells compound rather than being singular: a hero whose badge/underline/CTA/dot cycle through violet→blue→amber every 6s, a pulsing `blur-2xl` glow behind the hero image, 5 drifting blurred background shapes, three stacked floating "hero-metric" cards, and a 5-hue rainbow stat-icon row. This is a dense cluster of the exact anti-patterns the project's own DESIGN.md spends 200+ lines rejecting by name ("generic AI-SaaS template… gradient hero-metric cards… identical icon-card grids").

**Deterministic scan** (`detect.mjs`, exit 2): **1 finding** — `ai-color-palette` (warning) at `hero-section.tsx:69`, the `from-violet-500 to-purple-600` hero variant. The detector is a substring matcher and massively *under*-reports here: Assessment A independently caught the same violet as the tip of a systemic **One Voice Rule** violation spanning the badge, underline (`#8d54ff`/`#2778db`/`#f99c00`), CTA fill, dot indicator, and the whole `stats-section` rainbow row. Where the two assessments agree, they agree hard; the LLM review is the load-bearing signal, the detector merely corroborates one anchor point.

**Browser evidence refutes one worry and confirms the worst one:**
- *Refuted:* the fragile `bg-${...}-500` interpolated Tailwind dot-color class **does compile and render** in all three states, and every image (`cdn.experts.com.sa`, `i.pravatar.cc`, `howa.edu.sa`) returned HTTP 200 — nothing is visually broken by uncompiled CSS. Flag it as fragile, not broken.
- *Confirmed:* the empty/duplicate/zero content is real (a backend aggregation vs. listing disagreement — stats say "0 Courses" while the carousel above renders 6 live course cards and "Featured Courses" says "No featured courses found"), and Arabic pages leak untranslated English course/event strings inside RTL sentence flow.

**Visual overlays:** none available. Overlay injection was attempted (live-server started on :8400, `/detect.js` reachable) but the app's CSP `script-src` allowlist silently blocked the cross-origin script, so no `[Human]` overlay tab exists. The CLI scan is the authoritative deterministic signal.

## Overall Impression

The page opens on an unstable high and then sags through four consecutive trust sections that visibly contradict their own promises, recovering only at FAQ/CTA. What works: the team clearly *can* execute the documented system — FAQ and CTA are clean, restrained, single-blue, flat-at-rest. What doesn't: the "creative" sections (hero, stats, display-cards, gallery) treat the design system as optional and reach for a different decorative gimmick each. The single biggest opportunity is to bring those sections up to the discipline FAQ/CTA already prove is achievable — that one move kills most of the AI-slop read *and* most of the trust damage at once.

## What's Working

1. **RTL execution is real, verified craft.** Both agents confirmed `/ar`: mirrored nav, hero layout, CTA arrow direction, reversed marquee/stat order, no LTR leakage in chrome. Arabic-first is not an afterthought.
2. **FAQ is the best-executed section** — correct flat-at-rest cards (border + tone, no shadow), single blue accent, honest "still have questions → contact support" fallback. Proof the system works when followed.
3. **CTA section** restrains to one blue field + one white pill button — no rainbow, no glow, no floating shapes. The strongest peak-end moment on the page.

## Priority Issues

**[P0] The marketing homepage ships live "0" / empty / duplicate content in its trust-building sections.** A first-time visitor's first real data points are "0 Courses", "0% completion", a gallery of 6 identical thumbnails, "No featured courses found", near-duplicate event cards, and "No reviews yet" directly under "What Our Learners Say". Both agents confirmed this live; B traced it to a backend stats-aggregation vs. listing disagreement.
- *Why it matters:* this is a credibility failure at the exact moment the page is converting skepticism into trust — and for a creator-economy platform, it signals "low traction" to the very creators the growth loop depends on.
- *Fix:* gate these sections behind a minimum-content threshold — don't render 0-value stats as headline numbers (show a calmer "growing" state under a floor), replace empty Featured/Testimonials with editorial placeholders rather than bare "no results" lines, and dedupe `shuffledImages` in `page.tsx` so the gallery never repeats a thumbnail. Backend follow-up on the stats/listing mismatch.
- *Suggested command:* `$impeccable harden`

**[P1] The hero abandons the design system's own single-accent and pill-button rules on the highest-visibility element of the platform.** `hero-section.tsx` hardcodes violet/blue/amber across badge, underline, CTA fill, and progress dot, and squares the CTA to `rounded-xl` instead of the house full pill — while every *other* CTA on the page (CTA section, FAQ) correctly renders as a blue pill.
- *Why it matters:* it's the loudest, most checkable DESIGN.md violation and the biggest single driver of the "AI made this" read.
- *Fix:* collapse hero variant color to the one Signal Blue token across all three variants (vary imagery/copy/icon, not hue); restore the CTA to `buttonVariants({variant: "primary"})` full pill.
- *Suggested command:* `$impeccable quieter`

**[P1] Hero decorative motion creates high extraneous cognitive load and contradicts the "Control Room" north star.** Six-plus independently-animating elements (glow blur + 5 floating shapes + 3 stacked metric cards) compete before the user reads the headline; the 6s auto-rotation swaps color, headline, CTA target, and card contents under a reader mid-sentence — worse on mobile where there's no pause.
- *Why it matters:* this is the "generic AI-SaaS hero-metric template" the DESIGN.md rejects by name, and it actively impedes comprehension of the one message that matters.
- *Fix:* remove `floatingShapes` and the pulsing `blur-2xl` glow; reduce three floating cards to at most one purposeful proof-point; add a real pause/label affordance (and honor `prefers-reduced-motion`).
- *Suggested command:* `$impeccable distill`

**[P2] Rainbow 5-hue stat icons break the Charts-Only Rule.** `stats-section.tsx` applies `text-primary`/`amber-500`/`emerald-500`/`purple-500`/`rose-500` to five sibling icon chips — the chart palette leaking into chrome, fragmenting a row that should read as one coherent metric block.
- *Fix:* one tonal treatment for all five icons; differentiate by icon shape/label, not hue.
- *Suggested command:* `$impeccable colorize` (to correct usage, not add color)

**[P3] Hero and testimonial cards carry resting-state shadows the DESIGN.md prohibits.** `shadow-2xl`/`shadow-xl` on at-rest cards violates the "Flat-At-Rest Rule"; depth should come from the tonal ladder + hairline borders.
- *Fix:* drop to border + tone at rest; reserve shadow for genuine overlays (modals/popovers/toasts).
- *Suggested command:* `$impeccable polish`

## Persona Red Flags

**Jordan (first-time visitor, takes labels literally):** hero is confident, but the stats row reads "0 Courses / 0% completion", and "Featured Courses" says "No featured courses found" directly under "Hand-picked by our experts". Copy and empty-state contradict each other; Jordan reads it as broken, not early-stage, and abandons before the page recovers at FAQ/CTA.

**Saudi mobile-first learner on Arabic/RTL (project-specific):** RTL mirroring is solid, but the hero auto-rotates every 6s with no mobile pause (`onMouseEnter` is desktop-only), so the entire hero — color, headline, CTA target — swaps under an Arabic reader mid-sentence. The 2px dots have no `aria-label` ("go to slide 2 of 3"). Comprehension + a11y gap for the primary audience. Plus: course/event strings stay English inside Arabic flow.

**Alex (busy creator evaluating whether to publish here):** scrolls for proof of platform activity, finds duplicate gallery thumbnails (×6), near-identical event cards, and empty testimonials. Reads as "low actual usage" — the single most damaging failure, because the creator growth loop depends on projecting real traction.

## Minor Observations

- Dead code in shipped files: commented-out secondary CTA (hero + display-cards) and the fully commented-out `CreatorStudioSection` in `page.tsx`.
- Loading skeleton renders the "Get Started" button as a plain rectangle, not a pill — the loading silhouette doesn't match the resolved button.
- `expertInstructors` headlines as "3" on a floating card — a very small number to feature.
- Partner logos render small/low-contrast in the marquee; the `SAMAYA` SVG shows overlapping letterforms in both locales (vendor asset issue, not CSS).
- The fragile `bg-${...}-500` interpolated Tailwind class works today but is one Tailwind config change from silently breaking.

## Questions to Consider

- If the "Control Room" north star says color should be rare and always mean "here", what is the hero's 3-color rotation actually pointing at — and would the page lose anything if all three variants were the same Signal Blue?
- Is the empty/zero state of Stats, Featured Courses, and Testimonials a dev-seed artifact or a real production gap — and should the page even render those sections below a content-volume threshold?
- FAQ and CTA already prove the team can execute the documented system cleanly. What would it take to hold the hero, stats, and display-cards to that same discipline rather than treating them as the sections where the rules don't apply?
