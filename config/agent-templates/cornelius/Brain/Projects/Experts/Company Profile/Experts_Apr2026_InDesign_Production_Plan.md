---
title: "Experts Company Profile InDesign Production Plan — 22 April 2026"
date: "2026-04-22"
tags: ["project/experts", "company-profile", "indesign", "production-plan"]
category: "project/experts"
source: "draft"
source_id: "Projects/Experts/Company Profile/Experts_Apr2026_InDesign_Production_Plan.md"
updated: "2026-07-15"
---

# Experts Company Profile InDesign Production Plan

InDesign-first production plan for `Experts_Apr2026_Company Profile3.indd`

## Links

- [Experts Company Profile Source](/Projects/Experts/Company Profile/Experts_Apr2026_Company_Profile_Source.md)
- [Experts Company Profile Bilingual Spreads](/Projects/Experts/Company Profile/Experts_Apr2026_Company_Profile_Bilingual_Spreads.md)
- [Experts Company Profile Asset Brief](/Projects/Experts/Company Profile/Experts_Apr2026_Company_Profile_Asset_Brief.md)

## Recommendation

Build the final company profile in InDesign.

Use the existing HTML deck and bilingual spread draft as creative and copy references, but treat InDesign as the source of truth for:

- page setup
- bilingual spread structure
- paragraph styles
- image placement
- export-ready PDF output

## Working model

Each spread should be a bilingual pair:

- left page = English
- right page = Arabic

The two pages should feel like mirrored editorial twins, not one page translated into a cramped second page.

## Document setup

## Size

Use one of these depending on delivery goal:

- `A4 landscape` if this is mainly a PDF company profile
- `1920x1080 proportion` if you want it to visually align with the slide system and also repurpose pages for presentation

For a premium company profile PDF, my recommendation is:

- `A4 landscape`
- facing pages enabled
- 3 mm bleed

## Margins

Recommended starting margins:

- top: 18 mm
- bottom: 18 mm
- inside: 20 mm
- outside: 20 mm

If the spreads feel too dense, increase inside/outside to 22 to 24 mm.

## Grid

Use a simple editorial grid:

- 12-column grid on each page
- 4 mm gutter
- baseline grid optional

This gives enough flexibility for:

- large hero headings
- screenshot blocks
- card layouts
- quote blocks

## Master pages

Create these master pages first.

## `A-Master / Light Content`

Use for most interior light spreads.

Contains:

- page number
- subtle header/logo placement
- optional faint grid background
- standard margins and guides

## `B-Master / Dark Content`

Use for darker narrative or premium spreads.

Contains:

- white/light page number
- logo treatment for dark background
- optional radial glow anchor areas

## `C-Master / Cover`

Use for first spread and final spread.

Contains:

- reduced chrome
- larger image-safe zones
- no standard interior header

## `D-Master / Image Heavy`

Use for spreads where screenshots or editorial visuals dominate.

Contains:

- minimal page furniture
- generous safe zones
- optional caption position

## Page plan

Recommended 12 spreads, matching the HTML deck:

1. Cover
2. Who we are
3. Vision and mission
4. Platform overview
5. For learners
6. For experts
7. Commerce and monetization
8. Regional readiness
9. Community and engagement
10. Product experience
11. Why Experts / use cases
12. Closing / back cover

If the current InDesign file has more pages, you can split these:

- separate vision and mission
- separate community and engagement
- split why Experts and use cases

## Spread structure rules

Each spread should follow these rules:

- English page on left
- Arabic page on right
- same visual weight on both pages
- same section title level on both pages
- same approximate text volume on both pages
- do not let one side feel empty while the other side is overloaded

When a page needs imagery:

- either give both pages their own visual block
- or use one shared visual across the spread only if it has no text dependency

Avoid:

- paragraphs crossing the gutter
- tiny bilingual captions under the same image
- squeezing both languages into one page

## Style system

Create paragraph styles before placing content.

## English paragraph styles

- `EN_Display_H1`
- `EN_Display_H2`
- `EN_Eyebrow`
- `EN_Body`
- `EN_Body_Small`
- `EN_Card_Title`
- `EN_Card_Body`
- `EN_Quote`
- `EN_Footer`

## Arabic paragraph styles

- `AR_Display_H1`
- `AR_Display_H2`
- `AR_Eyebrow`
- `AR_Body`
- `AR_Body_Small`
- `AR_Card_Title`
- `AR_Card_Body`
- `AR_Quote`
- `AR_Footer`

## Character styles

- `Accent_Primary`
- `Muted_Text`
- `Caps_Label`
- `Numeric_Stat`

## Suggested type settings

These are starting points, not rigid rules.

## English

- `EN_Display_H1`: DM Sans Bold, 42 to 54 pt, tight leading, tracking slightly negative
- `EN_Display_H2`: DM Sans Bold, 28 to 36 pt
- `EN_Eyebrow`: Inter SemiBold, 9 to 11 pt, all caps, increased tracking
- `EN_Body`: Inter Regular, 11.5 to 13 pt, 150% leading
- `EN_Card_Title`: DM Sans Bold, 16 to 20 pt
- `EN_Card_Body`: Inter Regular, 10.5 to 11.5 pt

## Arabic

- `AR_Display_H1`: Readex Pro SemiBold/Bold, 40 to 50 pt
- `AR_Display_H2`: Readex Pro SemiBold, 26 to 34 pt
- `AR_Eyebrow`: Almarai Bold, 10 to 12 pt
- `AR_Body`: Almarai Regular, 12 to 14 pt, slightly more leading than English
- `AR_Card_Title`: Readex Pro SemiBold, 17 to 21 pt
- `AR_Card_Body`: Almarai Regular, 11 to 12 pt

Arabic usually needs a little more vertical room. Plan for that from the start.

## Color system

Use the current Experts design tokens.

- primary accent: `oklch(0.58 0.17 255.97)`
- light background: `oklch(0.98 0 0)`
- dark background: `oklch(0.08 0 0)`
- muted foreground: `oklch(0.72 0.01 270)`
- destructive red only as rare accent: `oklch(0.7 0.19 22.23)`

In InDesign, build swatches for:

- `Experts Primary`
- `Experts Background Light`
- `Experts Background Dark`
- `Experts Text Dark`
- `Experts Text Light`
- `Experts Muted`
- `Experts Border`

## Shape system

Match the product language:

- cards: 20 px equivalent radius
- media frames: 24 px equivalent radius
- chips/pills: 999 px

Avoid sharp-cornered corporate boxes unless used intentionally for contrast.

## Image placement system

Create object styles:

- `Image_Rounded_24`
- `Card_Rounded_20`
- `Dark_Screen_Frame`
- `Light_Screen_Frame`
- `Caption_Small`

## Screenshot handling

When placing screenshots:

- crop tightly
- avoid browser chrome where possible
- make the screenshot itself the graphic object, not a tiny full-page capture
- use consistent corner radius and shadow treatment

Best screenshot categories:

- home page EN
- home page AR
- course catalog
- learner dashboard
- course player
- creator dashboard
- pricing/checkout
- community feed

## Spread-by-spread layout notes

## 1. Cover

Master:

- `C-Master / Cover`

Layout:

- dark full-spread background
- large bilingual headlines, each page owning its own side
- shared product visual cluster across lower or outer side

Use:

- `og-home-en.png`
- `og-home-ar.png`

## 2. Who we are

Master:

- `A-Master / Light Content`

Layout:

- large headline top
- body copy mid
- two supporting cards at bottom

## 3. Vision and mission

Master:

- `B-Master / Dark Content`

Layout:

- statement-led page
- two cards or blocks below for vision/mission

## 4. Platform overview

Master:

- `A-Master / Light Content`

Layout:

- headline and short intro
- 4-module or 6-module card grid

## 5. For learners

Master:

- `D-Master / Image Heavy`

Layout:

- copy at top or left
- strong screenshots below or opposite

## 6. For experts

Master:

- `A-Master / Light Content`

Layout:

- feature cards or quote cards
- optional single dashboard crop

## 7. Commerce and monetization

Master:

- `B-Master / Dark Content`

Layout:

- pricing/checkout visual
- supporting stat or payment cards

## 8. Regional readiness

Master:

- `A-Master / Light Content`

Layout:

- mirror Arabic UI and English UI
- small supporting compliance/payment blocks

## 9. Community and engagement

Master:

- `B-Master / Dark Content`

Layout:

- one large community visual
- smaller interaction/value cards

## 10. Product experience

Master:

- `A-Master / Light Content`

Layout:

- system/quality spread
- dark mode vs light mode callouts
- component or theme cards

## 11. Why Experts / use cases

Master:

- `B-Master / Dark Content`

Layout:

- pillar cards on English page
- use-case cards on Arabic page

## 12. Closing / back cover

Master:

- `C-Master / Cover`

Layout:

- large concluding statement
- contact block
- quiet premium finish

## Bilingual layout rules

Arabic side should not be a literal geometry copy of the English side.

Mirror these:

- alignment
- icon direction
- card reading order
- visual anchoring
- pull-quote direction

Keep these consistent:

- block heights
- image sizes
- section hierarchy
- spacing rhythm

## Workflow inside InDesign

Recommended sequence:

1. duplicate the existing `.indd` file before touching anything
2. remove irrelevant placeholder copy and unrelated styles
3. set up document grid and master pages
4. build paragraph, character, color, and object styles
5. lay out all English pages first
6. build Arabic pages as mirrored companions
7. place screenshots and crop consistently
8. adjust for balance spread by spread
9. export draft PDF
10. review typography, Arabic spacing, and image consistency

## What to import from the current files

Use as source material:

- bilingual spread copy:
  - `Experts_Apr2026_Company_Profile_Bilingual_Spreads.md`
- asset planning:
  - `Experts_Apr2026_Company_Profile_Asset_Brief.md`
- visual reference:
  - `company-profile-bilingual.html`

## What to avoid

- reusing outdated client styles from the current `.indd`
- mixing too many fonts
- using generic stock business photos as the dominant visual language
- making Arabic text smaller just to force matching heights
- overly dense paragraphs
- over-decorating with too many gradients on every spread

## Final export

For review PDF:

- export optimized interactive/viewing PDF

For final print-ready PDF:

- include bleed
- embed fonts
- check Arabic rendering carefully
- package links and fonts if handing off

## Best next step

Open the current InDesign file and do only this first:

1. duplicate the file
2. strip old placeholder copy
3. create masters and styles
4. lay out spreads 1 to 3 fully before touching the rest

If those first three spreads look right, the rest of the document will move much faster.
