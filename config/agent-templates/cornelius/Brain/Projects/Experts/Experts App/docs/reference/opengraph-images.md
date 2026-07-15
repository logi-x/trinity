---
title: "Open Graph images"
date: "2026-04-11"
tags: ["project/experts", "docs/v4", "topic/seo", "topic/og"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# OpenGraph Images

## Overview

This document describes the OpenGraph (OG) image implementation for the Experts platform. OG images are social media preview images that appear when sharing links on platforms like Facebook, Twitter, LinkedIn, etc.

## Implementation

### Courses Page OG Image

**Location**: `app/courses/opengraph-image.tsx`

The courses page uses a dynamic OpenGraph image generated using Next.js's `ImageResponse` API. This approach provides:

- ✅ Dynamic generation at build time
- ✅ Consistent branding across social platforms
- ✅ Bilingual content (English + Arabic)
- ✅ Custom fonts (Poppins + Cairo)
- ✅ Modern gradient design

### Design Features

#### Layout Structure

```
┌──────────────────────────────────────────────┐
│  [Expert-Led Learning]  (eyebrow chip)       │
│                                              │
│  Discover Your Next                          │
│  Learning Journey    (gradient headline)     │
│                                              │
│  100+ courses in technology...               │
│  أكثر من 100 دورة في التكنولوجيا...          │
│                                              │
│                    [✓ Start Learning Today]  │
└──────────────────────────────────────────────┘
```

#### Color Palette

| Element         | Color                      | Usage                        |
| --------------- | -------------------------- | ---------------------------- |
| Background      | `#ffffff`                  | Clean white base             |
| Primary text    | `#0a0a0a`                  | Near-black for readability   |
| Secondary text  | `rgba(10, 10, 10, 0.7)`    | Muted for subheadlines       |
| Primary blue    | `#3b82f6`                  | Brand accent (blue-500)      |
| Purple          | `#8b5cf6`                  | Gradient accent (violet-500) |
| Pink            | `#ec4899`                  | Gradient accent (pink-500)   |
| Chip background | `rgba(59, 130, 246, 0.08)` | Subtle blue tint             |
| Chip border     | `rgba(59, 130, 246, 0.2)`  | Blue border                  |

#### Typography

- **Headlines**: Poppins Bold (700) @ 72px
- **Body**: Poppins Regular (400) @ 26px
- **Arabic text**: Cairo Regular (400) @ 24px
- **Eyebrow**: Poppins SemiBold (600) @ 20px

### File Structure

```
app/courses/
├── layout.tsx                 # Metadata configuration (removed hardcoded OG image)
├── page.tsx                   # Courses page
└── opengraph-image.tsx        # Dynamic OG image generator
```

## Testing OG Images

### Local Development

Visit the OG image route directly in your browser:

```
http://localhost:3025/courses/opengraph-image
```

This will display the generated PNG image.

### Social Media Debuggers

Test how the image appears on different platforms:

1. **Facebook**: [Sharing Debugger](https://developers.facebook.com/tools/debug/)
2. **Twitter**: [Card Validator](https://cards-dev.twitter.com/validator)
3. **LinkedIn**: [Post Inspector](https://www.linkedin.com/post-inspector/)
4. **Generic**: [OpenGraph.xyz](https://www.opengraph.xyz/)

**Important**: Social platforms cache OG images aggressively. Use their debugger tools to force a refresh when testing.

## How Next.js Generates OG Images

1. **At Build Time**: Next.js detects `opengraph-image.tsx` and generates the image
2. **Route Creation**: Automatically creates `/courses/opengraph-image` route
3. **Metadata Integration**: Next.js automatically adds the OG image to metadata
4. **Caching**: Images are cached and served as static assets

## Adding OG Images to Other Pages

To add an OG image to another page:

1. Create `opengraph-image.tsx` in the page directory
2. Export the required constants and component:

```typescript
import { ImageResponse } from "next/og";

export const alt = "Page Title";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image() {
  return new ImageResponse(
    // JSX content here
    <div style={{...}}>Your content</div>,
    { ...size }
  );
}
```

3. Next.js will automatically handle the rest!

## Important Constraints

The `ImageResponse` API uses [Satori](https://github.com/vercel/satori) for rendering, which has limitations:

- ❌ **No CSS classes** - Use inline `style` objects only
- ❌ **No CSS Grid** - Use Flexbox instead
- ❌ **No external images** - Must use base64 or absolute URLs
- ✅ **Flexbox supported** - Most flexbox properties work
- ✅ **Font loading** - Must load `.ttf` files explicitly

## Font Loading

Fonts are loaded from `public/fonts/` directory:

```typescript
const [fontRegular, fontBold] = await Promise.all([
  readFile(join(process.cwd(), "public/fonts/Font-Regular.ttf")),
  readFile(join(process.cwd(), "public/fonts/Font-Bold.ttf")),
]);

return new ImageResponse(content, {
  ...size,
  fonts: [
    { name: "Font", data: fontRegular, style: "normal", weight: 400 },
    { name: "Font", data: fontBold, style: "normal", weight: 700 },
  ],
});
```

## Bilingual Support

The courses OG image includes both English and Arabic text:

- **English**: Poppins font (Latin script)
- **Arabic**: Cairo font (Arabic script)
- **Layout**: Stacked vertically with proper spacing

This ensures the image is accessible and appealing to both audiences.

## Future Enhancements

Potential improvements for OG images:

1. **Dynamic data**: Pull course count, featured courses from database
2. **Personalization**: User-specific OG images for profiles
3. **Localized versions**: Separate images per locale
4. **A/B testing**: Test different designs for better engagement
5. **Course-specific**: Individual OG images for each course page

## References

- [Next.js OG Image Generation](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image)
- [Satori Documentation](https://github.com/vercel/satori)
- [Open Graph Protocol](https://ogp.me/)
- [Twitter Cards](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards)
