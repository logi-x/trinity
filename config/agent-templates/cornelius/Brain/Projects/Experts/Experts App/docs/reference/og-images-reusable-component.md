---
title: "OG images reusable component"
date: "2026-04-11"
tags: ["project/experts", "docs/v4", "topic/seo", "topic/og"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

## Reusable OpenGraph Image Component

## Overview

The Experts platform uses a centralized, reusable component for generating OpenGraph (OG) images across all pages. This ensures consistent branding, reduces code duplication, and makes it easy to create new OG images.

## Architecture

### Core Components

1. **Generator Function** (`src/components/og/generate-og-image.tsx`)
   - Main function that generates OG images
   - Handles font loading, styling, and layout
   - Fully configurable via parameters

2. **Presets** (`src/components/og/og-presets.ts`)
   - Predefined configurations for common pages
   - Ensures consistent branding
   - Easy to customize

3. **Page-Specific Files** (`app/*/opengraph-image.tsx`)
   - Minimal files that use the generator
   - Just configuration, no implementation

## File Structure

```
src/components/og/
├── generate-og-image.tsx    # Core generator function
└── og-presets.ts             # Predefined configurations

app/
├── courses/
│   └── opengraph-image.tsx   # Uses generator with courses preset
├── events/
│   └── opengraph-image.tsx   # Uses generator with events preset
└── community/
    └── opengraph-image.tsx   # Uses generator with community preset
```

## Usage

### Method 1: Use a Preset (Recommended)

For standard pages, use predefined presets:

```typescript
// app/pricing/opengraph-image.tsx
import {
  generateOGImage,
  generateAltText,
  OG_IMAGE_SIZE,
} from "@/components/og/generate-og-image";
import { getOGPreset } from "@/components/og/og-presets";

export const alt = generateAltText(
  "Pricing",
  "Flexible Pricing Plans",
  "Experts",
);
export const size = OG_IMAGE_SIZE;
export const contentType = "image/png";

export default async function Image() {
  return generateOGImage(getOGPreset("pricing"));
}
```

**Available Presets**:

- `courses` - Blue gradient, learning-focused
- `events` - Cyan gradient, event-focused
- `community` - Pink gradient, community-focused
- `pricing` - Green gradient, pricing-focused
- `instructors` - Orange gradient, instructor-focused
- `about` - Blue gradient, about-focused
- `certificates` - Violet gradient, certificate-focused
- `affiliate` - Green gradient, affiliate-focused

### Method 2: Customize a Preset

Modify a preset for specific needs:

```typescript
// app/special-courses/opengraph-image.tsx
import {
  generateOGImage,
  generateAltText,
  OG_IMAGE_SIZE,
} from "@/components/og/generate-og-image";
import { customizePreset } from "@/components/og/og-presets";

export const alt = "Special Courses | Experts";
export const size = OG_IMAGE_SIZE;
export const contentType = "image/png";

export default async function Image() {
  return generateOGImage(
    customizePreset("courses", {
      headlineTop: "Limited Time Offer",
      headlineBottom: "Premium Courses",
      badgeText: "Enroll Now",
    }),
  );
}
```

### Method 3: Full Custom Configuration

For unique pages, provide a complete configuration:

```typescript
// app/custom-page/opengraph-image.tsx
import {
  generateOGImage,
  generateAltText,
  OG_IMAGE_SIZE,
} from "@/components/og/generate-og-image";

export const alt = "Custom Page | Experts";
export const size = OG_IMAGE_SIZE;
export const contentType = "image/png";

export default async function Image() {
  return generateOGImage({
    eyebrow: "Custom Badge",
    headlineTop: "Your Custom",
    headlineBottom: "Headline Here",
    descriptionEn: "Your English description here",
    descriptionAr: "الوصف العربي هنا", // Optional
    badgeText: "Custom CTA",
    gradientColors: ["#ff0000", "#00ff00", "#0000ff"], // Optional
    eyebrowColor: "#ff0000", // Optional
  });
}
```

## Configuration Options

### OGImageConfig Interface

```typescript
interface OGImageConfig {
  eyebrow: string; // Small chip at top (e.g., "Expert-Led Learning")
  headlineTop: string; // First line of headline (regular text)
  headlineBottom: string; // Second line of headline (gradient text)
  descriptionEn: string; // English description
  descriptionAr?: string; // Arabic description (optional)
  badgeText: string; // Bottom badge CTA text
  gradientColors?: [string, string, string]; // RGB color array (default: blue-violet-pink)
  eyebrowColor?: string; // Eyebrow badge color (default: blue)
}
```

### Default Values

```typescript
const defaults = {
  gradientColors: ["#3b82f6", "#8b5cf6", "#ec4899"], // Blue → Violet → Pink
  eyebrowColor: "#3b82f6", // Blue
};
```

## Design Guidelines

### Headline Best Practices

**Top Line (Regular)**:

- 2-3 words max
- Action-oriented
- Sets context

**Bottom Line (Gradient)**:

- 2-3 words max
- Key value proposition
- Eye-catching

**Examples**:

```
✅ GOOD:
  Top: "Discover Your Next"
  Bottom: "Learning Journey"

✅ GOOD:
  Top: "Join Live"
  Bottom: "Expert Events"

❌ BAD (too long):
  Top: "Discover All the Amazing Courses"
  Bottom: "That We Have Available For You"
```

### Description Best Practices

**English Description**:

- 8-12 words
- Specific and concrete
- Mentions key benefits or numbers

**Arabic Description**:

- Mirror English meaning
- Similar length
- Right-to-left compatible

**Examples**:

```
✅ GOOD:
  EN: "100+ courses in technology, business, design and more"
  AR: "أكثر من 100 دورة في التكنولوجيا والأعمال والتصميم"

❌ BAD (too vague):
  EN: "Many great courses available"
  AR: "دورات رائعة متاحة"
```

### Badge Text Best Practices

- 2-4 words max
- Strong CTA
- Action verb

**Examples**:

```
✅ GOOD:
  - "Start Learning Today"
  - "Register Now"
  - "Join the Discussion"
  - "View Plans"

❌ BAD:
  - "Click Here"
  - "Learn More About This"
```

## Color Schemes

### Brand Colors

Each content type has a signature color:

| Type         | Primary Color | Hex       | Gradient               |
| ------------ | ------------- | --------- | ---------------------- |
| Courses      | Blue          | `#3b82f6` | Blue → Violet → Pink   |
| Events       | Cyan          | `#06b6d4` | Blue → Cyan → Violet   |
| Community    | Pink          | `#ec4899` | Pink → Violet → Blue   |
| Pricing      | Green         | `#10b981` | Green → Blue → Violet  |
| Instructors  | Orange        | `#f59e0b` | Orange → Pink → Violet |
| Certificates | Violet        | `#8b5cf6` | Violet → Pink → Orange |
| Affiliate    | Green         | `#10b981` | Green → Cyan → Blue    |

### Custom Gradients

When creating custom gradients, use 3 colors that:

1. Have good contrast with white background
2. Transition smoothly (adjacent on color wheel works best)
3. Match your brand guidelines

**Good Gradient Examples**:

```typescript
// Warm gradient
gradientColors: ["#f59e0b", "#ec4899", "#8b5cf6"]; // Orange → Pink → Violet

// Cool gradient
gradientColors: ["#3b82f6", "#06b6d4", "#10b981"]; // Blue → Cyan → Green

// Monochromatic
gradientColors: ["#3b82f6", "#6366f1", "#8b5cf6"]; // Blue → Indigo → Violet
```

## Adding a New Preset

To add a new preset configuration:

1. Open `src/components/og/og-presets.ts`
2. Add a new entry to the `OG_PRESETS` object:

```typescript
export const OG_PRESETS: Record<string, OGImageConfig> = {
  // ... existing presets ...

  yourNewPreset: {
    eyebrow: "Your Badge Text",
    headlineTop: "Your First",
    headlineBottom: "Headline Text",
    descriptionEn: "Your English description here",
    descriptionAr: "الوصف العربي هنا",
    badgeText: "Your CTA",
    gradientColors: ["#color1", "#color2", "#color3"],
    eyebrowColor: "#color1",
  },
};
```

3. Use it in your page:

```typescript
// app/your-page/opengraph-image.tsx
export default async function Image() {
  return generateOGImage(getOGPreset("yourNewPreset"));
}
```

## Live Preview Tool

### Design with Hot Module Replacement

Visit `/og-live` for a real-time preview tool with HMR:

```
http://localhost:3025/og-live
```

**Features**:

- ✅ Live preview at exact 1200x630 size
- ✅ Hot reload - see changes instantly
- ✅ Preset selector - switch between courses, events, community, etc.
- ✅ Full configuration editor - modify all fields
- ✅ Color pickers for gradients and accent colors
- ✅ Copy-paste code snippet - ready to use in your page
- ✅ Same design as static generation - what you see is what you get

**How it works**:

1. The preview page uses the same `OGImageContent` component used for static generation
2. Changes to `src/components/og/og-image-content.tsx` appear instantly in the preview
3. All presets from `og-presets.ts` are available in the dropdown
4. Copy the generated config to your page's `opengraph-image.tsx`

**Workflow**:

1. Open `http://localhost:3025/og-live` in your browser
2. Select a preset or customize from scratch
3. Adjust text, colors, and gradient
4. See changes in real-time
5. Copy the configuration code
6. Paste into your page's `opengraph-image.tsx`

## Testing OG Images

### Local Testing

Visit the OG image route directly:

```
http://localhost:3025/courses/opengraph-image
http://localhost:3025/events/opengraph-image
http://localhost:3025/community/opengraph-image
```

### Social Media Debuggers

Test how images appear on social platforms:

1. **Facebook**: [Sharing Debugger](https://developers.facebook.com/tools/debug/)
2. **Twitter**: [Card Validator](https://cards-dev.twitter.com/validator)
3. **LinkedIn**: [Post Inspector](https://www.linkedin.com/post-inspector/)
4. **Generic**: [OpenGraph.xyz](https://www.opengraph.xyz/)

**Note**: Social platforms cache OG images aggressively. Use debugger tools to force refresh.

## Migration Guide

### Converting Existing OG Images

If you have an existing custom OG image file, convert it to use the generator:

**Before** (custom implementation):

```typescript
// app/my-page/opengraph-image.tsx (200+ lines)
import {ImageResponse} from "next/og";
import {readFile} from "node:fs/promises";
// ... lots of code ...

export default async function Image() {
  const fonts = await Promise.all([...]);
  return new ImageResponse(
    <div style={{...}}>
      {/* Custom JSX */}
    </div>,
    {fonts: [...]}
  );
}
```

**After** (using generator):

```typescript
// app/my-page/opengraph-image.tsx (15 lines)
import {
  generateOGImage,
  generateAltText,
  OG_IMAGE_SIZE,
} from "@/components/og/generate-og-image";

export const alt = generateAltText("MyPage", "My Page Title", "Experts");
export const size = OG_IMAGE_SIZE;
export const contentType = "image/png";

export default async function Image() {
  return generateOGImage({
    eyebrow: "...",
    headlineTop: "...",
    headlineBottom: "...",
    descriptionEn: "...",
    descriptionAr: "...",
    badgeText: "...",
  });
}
```

**Benefits**:

- ✅ 90% less code
- ✅ Consistent branding
- ✅ Easier to maintain
- ✅ Automatic font loading
- ✅ Bilingual support built-in

## Performance

### Build Time

- Font loading: ~50ms per image
- Image generation: ~100-200ms per image
- Total: ~150-250ms per page

**Note**: OG images are generated at build time (not runtime), so there's no performance impact on page loads.

### Caching

OG images are:

- Generated once at build time
- Cached as static assets
- Served with long-lived cache headers
- No runtime overhead

## Troubleshooting

### Fonts Not Loading

**Problem**: OG image shows system fonts instead of Poppins/Cairo

**Solution**: Ensure fonts exist in `public/fonts/`:

```bash
ls public/fonts/Poppins-*
ls public/fonts/Cairo-*
```

### Arabic Text Not Showing

**Problem**: Arabic text appears as boxes or missing

**Solution**:

1. Verify Cairo fonts are loaded
2. Check that `descriptionAr` is provided
3. Ensure proper Arabic text encoding

### Gradient Not Showing

**Problem**: Headline appears as solid color

**Solution**: Verify gradient colors are valid hex codes:

```typescript
// ✅ GOOD
gradientColors: ["#3b82f6", "#8b5cf6", "#ec4899"];

// ❌ BAD
gradientColors: ["blue", "violet", "pink"];
```

### Image Too Large

**Problem**: OG image file size > 1MB

**Solution**: OG images should be ~50-200KB. If larger, contact the development team to optimize the generator.

## Best Practices

### ✅ DO

- Use presets when possible for consistency
- Keep headlines short and punchy
- Include both English and Arabic descriptions
- Test on multiple social platforms
- Use brand colors from the presets
- Keep badge text action-oriented

### ❌ DON'T

- Don't create custom implementations (use the generator)
- Don't make headlines longer than 3 words per line
- Don't use non-brand colors without approval
- Don't skip Arabic translations
- Don't use images or icons (not supported by Satori)
- Don't modify the core generator without team approval

## Examples

### Courses Page

```typescript
return generateOGImage({
  eyebrow: "Expert-Led Learning",
  headlineTop: "Discover Your Next",
  headlineBottom: "Learning Journey",
  descriptionEn: "100+ courses in technology, business, design and more",
  descriptionAr: "أكثر من 100 دورة في التكنولوجيا والأعمال والتصميم",
  badgeText: "Start Learning Today",
});
```

### Events Page

```typescript
return generateOGImage({
  eyebrow: "Live Expert Events",
  headlineTop: "Join Live Sessions",
  headlineBottom: "With Industry Leaders",
  descriptionEn: "Workshops, webinars, and networking events with top experts",
  descriptionAr: "ورش عمل وندوات وفعاليات للتواصل مع كبار الخبراء",
  badgeText: "Register Now",
  gradientColors: ["#3b82f6", "#06b6d4", "#8b5cf6"],
  eyebrowColor: "#06b6d4",
});
```

### Community Page

```typescript
return generateOGImage({
  eyebrow: "Community Insights",
  headlineTop: "Connect & Learn",
  headlineBottom: "With Our Community",
  descriptionEn:
    "Join discussions, share knowledge, and grow with fellow learners",
  descriptionAr: "انضم إلى المناقشات وشارك المعرفة واكتسب الخبرات مع زملائك",
  badgeText: "Join the Discussion",
  gradientColors: ["#ec4899", "#8b5cf6", "#3b82f6"],
  eyebrowColor: "#ec4899",
});
```

## Conclusion

The reusable OG image component provides:

- ✅ **Consistency** - Same look across all pages
- ✅ **Maintainability** - One place to update design
- ✅ **Simplicity** - ~15 lines of code per page
- ✅ **Flexibility** - Easy to customize when needed
- ✅ **Performance** - Build-time generation, no runtime cost

Use it for all new pages and migrate existing pages gradually!
