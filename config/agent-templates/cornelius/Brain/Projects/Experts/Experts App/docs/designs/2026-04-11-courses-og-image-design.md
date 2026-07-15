---
title: "Courses OG image design"
date: "2026-04-11"
tags: ["project/experts", "docs/v4", "topic/seo", "topic/og", "topic/courses"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Courses Page OpenGraph Image Design

## Visual Design Specification

### Dimensions

- **Width**: 1200px
- **Height**: 630px
- **Aspect Ratio**: 1.91:1 (optimal for social media)

### Layout Breakdown

```
┌────────────────────────────────────────────────────────────────┐
│  Padding: 80px                                                 │
│                                                                │
│  ┌──────────────────┐                                         │
│  │ • Expert-Led     │  ← Eyebrow chip (blue pill badge)      │
│  │   Learning       │                                         │
│  └──────────────────┘                                         │
│                                                                │
│  Discover Your Next                  ← Main headline          │
│  Learning Journey                    ← Gradient text          │
│                                                                │
│  100+ courses in technology,         ← English subheadline    │
│  business, design and more                                    │
│  أكثر من 100 دورة في التكنولوجيا     ← Arabic subheadline     │
│  والأعمال والتصميم                                           │
│                                                                │
│                                    ┌────────────────────────┐ │
│                                    │ ✓ Start Learning Today │ │
│                                    └────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

## Component Specifications

### 1. Eyebrow Chip (Top Badge)

**Purpose**: Quick context indicator for the page type

**Styling**:

- Background: `rgba(59, 130, 246, 0.08)` (subtle blue tint)
- Border: `2px solid rgba(59, 130, 246, 0.2)` (blue outline)
- Border Radius: `9999px` (fully rounded pill)
- Padding: `12px 24px`
- Font: Poppins SemiBold, 20px
- Color: `#1e40af` (blue-800)
- Letter Spacing: `0.025em`

**Content**:

- Blue dot indicator (10px circle, `#3b82f6`)
- Text: "Expert-Led Learning"

### 2. Main Headline

**Purpose**: Primary message - what the page offers

**Line 1** (Regular):

- Text: "Discover Your Next"
- Font: Poppins Bold, 72px
- Color: `#0a0a0a` (near-black)
- Line Height: 1.1
- Letter Spacing: `-0.02em`

**Line 2** (Gradient):

- Text: "Learning Journey"
- Font: Poppins Bold, 72px
- Gradient: `linear-gradient(to right, #3b82f6, #8b5cf6, #ec4899)`
  - Blue → Violet → Pink
- Background Clip: text
- Line Height: 1.1

### 3. Subheadline (Bilingual)

**Purpose**: Additional context and course information

**English Line**:

- Text: "100+ courses in technology, business, design and more"
- Font: Poppins Regular, 26px
- Color: `rgba(10, 10, 10, 0.7)` (70% opacity)
- Line Height: 1.5

**Arabic Line**:

- Text: "أكثر من 100 دورة في التكنولوجيا والأعمال والتصميم"
- Font: Cairo Regular, 24px
- Color: `rgba(10, 10, 10, 0.6)` (60% opacity)
- Line Height: 1.5

### 4. Bottom CTA Badge

**Purpose**: Call-to-action indicator

**Position**: `bottom: 60px`, `right: 80px`

**Styling**:

- Background: `#0a0a0a` (black)
- Border Radius: `12px`
- Padding: `16px 28px`

**Content**:

- Checkmark icon: Blue circle (32px) with white ✓
  - Background: `#3b82f6`
  - Border Radius: 50%
- Text: "Start Learning Today"
  - Font: Poppins SemiBold, 20px
  - Color: `#ffffff`
  - Letter Spacing: `0.01em`

### 5. Background

**Base**:

- Color: `#ffffff` (white)

**Pattern**:

- Subtle dot grid pattern using `radial-gradient`
- Two overlapping gradients:
  - Blue dots: `rgba(59, 130, 246, 0.05)` at 25px intervals
  - Purple dots: `rgba(139, 92, 246, 0.05)` at 75px intervals
- Grid Size: `100px × 100px`

### 6. Decorative Elements (Blur Orbs)

**Top-Right Orb**:

- Size: 120px × 120px
- Position: `top: 40px`, `right: 80px`
- Gradient: `linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(139, 92, 246, 0.15))`
- Blur: `40px`

**Bottom-Left Orb**:

- Size: 80px × 80px
- Position: `bottom: 150px`, `left: 80px`
- Gradient: `linear-gradient(135deg, rgba(236, 72, 153, 0.15), rgba(139, 92, 246, 0.15))`
- Blur: `30px`

## Color Palette Reference

| Name       | Hex Code  | Usage                          |
| ---------- | --------- | ------------------------------ |
| White      | `#ffffff` | Background base                |
| Near Black | `#0a0a0a` | Primary text, CTA background   |
| Blue 500   | `#3b82f6` | Primary accent, gradient start |
| Blue 800   | `#1e40af` | Eyebrow text                   |
| Violet 500 | `#8b5cf6` | Gradient middle                |
| Pink 500   | `#ec4899` | Gradient end                   |

### Opacity Variants

| Color       | Opacity | Usage                 |
| ----------- | ------- | --------------------- |
| Blue        | 8%      | Chip background       |
| Blue        | 20%     | Chip border           |
| Black       | 70%     | Subheadline (English) |
| Black       | 60%     | Subheadline (Arabic)  |
| Blue        | 5%      | Background pattern    |
| Blue/Violet | 15%     | Blur orbs             |

## Typography Stack

### Primary (Latin Script)

- **Family**: Poppins
- **Weights**:
  - Regular (400) - Body text
  - SemiBold (600) - Eyebrow, badges
  - Bold (700) - Headlines

### Secondary (Arabic Script)

- **Family**: Cairo
- **Weights**:
  - Regular (400) - Body text
  - Bold (700) - Headlines

## Responsive Considerations

While OG images are fixed at 1200×630, the design is optimized for:

- **Desktop sharing**: Full detail visible
- **Mobile sharing**: Headline readable even when scaled down
- **Thumbnail previews**: High contrast ensures readability

## Accessibility

- ✅ High contrast ratios (4.5:1 minimum)
- ✅ Clear visual hierarchy
- ✅ Alt text provided: "Online Courses | Experts Learning Platform"
- ✅ Bilingual content for diverse audiences

## Design Principles

1. **Clarity First**: Headline is immediately readable
2. **Brand Consistency**: Uses Experts brand colors and typography
3. **Visual Interest**: Gradients and blur effects add depth without clutter
4. **Bilingual**: Respects both English and Arabic audiences
5. **Modern**: Contemporary design with glassmorphism influences
6. **Actionable**: CTA badge encourages engagement

## Implementation Notes

- Generated using Next.js `ImageResponse` API
- Uses Satori for server-side rendering
- Fonts loaded from `public/fonts/`
- All styles are inline (Satori requirement)
- No external dependencies required
- Build-time generation for optimal performance

## Social Media Preview Examples

### Facebook

- Shows full image with headline clearly visible
- Blue brand colors match Facebook's UI
- Bilingual text visible in preview

### Twitter

- Summary large image card format
- Headline and gradient stand out in feed
- CTA badge visible in thumbnail

### LinkedIn

- Professional appearance with clean design
- Course count adds credibility
- Brand colors create recognition

## Testing Checklist

- [ ] Image generates without errors
- [ ] Fonts load correctly (Poppins + Cairo)
- [ ] Gradient renders smoothly
- [ ] Arabic text displays properly (right-to-left aware)
- [ ] Colors match brand guidelines
- [ ] File size < 1MB (recommended for OG images)
- [ ] Tested on Facebook debugger
- [ ] Tested on Twitter card validator
- [ ] Tested on LinkedIn post inspector

## Version History

- **v1.0** (2026-01-31): Initial design with bilingual support, gradient headline, and modern blur effects
