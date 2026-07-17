---
title: "Content Scaling in Device Frames"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/ui"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Content Scaling in Device Frames

## Overview

The iPhone and iPad components now support **content scaling** to make embedded page builder elements appear more realistic within device frames. Instead of scaling the device itself, we scale the content inside to simulate how real content would appear on actual devices.

## How It Works

### The Problem

When embedding full desktop-sized content into device frames, it looks unrealistic because:

- Desktop content is designed for larger screens (1920px+)
- Mobile content should appear smaller and optimized for ~390px width
- Tablet content should be optimized for ~800px width

### The Solution

We use CSS `transform: scale()` on the content container:

```tsx
<div
  style={{
    width: `${100 / contentScale}%`, // Expand container
    height: `${100 / contentScale}%`, // Expand container
    transform: `scale(${contentScale})`, // Scale down content
    transformOrigin: "top left", // Scale from top-left
  }}
>
  {children}
</div>
```

This creates a larger canvas that gets scaled down, making desktop content appear realistically sized on mobile/tablet frames.

## Usage

### iPhone Component

**Default Scale: 0.35 (35%)**
This makes desktop content appear as if it were designed for mobile.

```tsx
// Use default scaling (recommended)
<Iphone enableScroll={true} screenBackground="transparent">
  {pageBuilderContent}
</Iphone>

// Custom scaling
<Iphone contentScale={0.4}>  {/* 40% size */}
  {pageBuilderContent}
</Iphone>

// No scaling (full size)
<Iphone contentScale={1}>
  {mobileOptimizedContent}
</Iphone>
```

### iPad Component

**Default Scale: 0.5 (50%)**
This makes desktop content appear as if it were designed for tablet.

```tsx
// Use default scaling (recommended)
<Ipad orientation="portrait" enableScroll={true} screenBackground="transparent">
  {pageBuilderContent}
</Ipad>

// Custom scaling
<Ipad contentScale={0.6}>  {/* 60% size */}
  {pageBuilderContent}
</Ipad>

// No scaling (full size)
<Ipad contentScale={1}>
  {tabletOptimizedContent}
</Ipad>
```

## Scale Factor Guide

| contentScale | Use Case                  | Example                        |
| ------------ | ------------------------- | ------------------------------ |
| 0.3 - 0.35   | Desktop → Mobile          | Page builder content in iPhone |
| 0.4 - 0.5    | Desktop → Tablet          | Page builder content in iPad   |
| 0.6 - 0.8    | Large mobile/Small tablet | Responsive content             |
| 1.0          | No scaling                | Already optimized for device   |

## Page Builder Integration

The page-builder-editor automatically uses optimal scaling:

```tsx
// Mobile viewport
<Iphone contentScale={0.35}>
  <Frame data={pageBuilderData}>{defaultContent}</Frame>
</Iphone>

// Tablet viewport
<Ipad contentScale={0.5}>
  <Frame data={pageBuilderData}>{defaultContent}</Frame>
</Ipad>
```

## Visual Examples

### Before (No Scaling)

```
┌─────────────────┐
│ ┌─────────────┐ │  Desktop content fills entire
│ │ HUGE TEXT   │ │  mobile screen - unrealistic
│ │             │ │
│ │ BIG BUTTON  │ │
│ └─────────────┘ │
└─────────────────┘
```

### After (contentScale={0.35})

```
┌─────────────────┐
│ Small text      │  Desktop content scaled to 35%
│ Normal Button   │  Looks like real mobile content
│ Another section │
│ Footer content  │
│ [scrollable...] │
└─────────────────┘
```

## Technical Details

### Transform Origin

We use `transformOrigin: "top left"` so content scales from the top-left corner, maintaining proper alignment with the device screen.

### Container Expansion

The container is expanded to `100 / contentScale %` to create a larger canvas before scaling:

- If `contentScale = 0.35`, container = 285.71% (100/0.35)
- If `contentScale = 0.5`, container = 200% (100/0.5)

This ensures the content has proper dimensions before being scaled down.

### Scrolling

Scrolling works correctly because:

1. The outer container has `overflow: auto`
2. The inner container is expanded
3. Content is scaled but maintains its scroll behavior

## Best Practices

### 1. Use Default Scales

The default values are optimized for most use cases:

- iPhone: `0.35` for realistic mobile appearance
- iPad: `0.5` for realistic tablet appearance

### 2. Adjust for Content Type

- **Page builders**: Use defaults (0.35 for mobile, 0.5 for tablet)
- **Mobile-first designs**: Use higher scales (0.6-0.8)
- **Already responsive**: Use `1` (no scaling)

### 3. Test Scrolling

With smaller scales, ensure:

- Content doesn't get too small to read
- Interactive elements remain clickable
- Scroll behavior feels natural

### 4. Consider Text Readability

Very small scales (< 0.3) may make text hard to read:

```tsx
// Too small - text may be unreadable
<Iphone contentScale={0.2}>...</Iphone>

// Good balance
<Iphone contentScale={0.35}>...</Iphone>
```

## Troubleshooting

**Content appears too small?**

- Increase `contentScale` value
- Check if content is already mobile-optimized

**Content appears too large?**

- Decrease `contentScale` value
- Verify content dimensions

**Scrolling not working?**

- Ensure `enableScroll={true}` is set
- Check that content height exceeds screen height

**Blurry text?**

- Use appropriate scale factors (avoid very small values)
- Ensure content has proper font sizes

## Migration from Old Pattern

**Before (manual scaling):**

```tsx
<div className="scale-[0.35] origin-top-left">{content}</div>
```

**After (built-in scaling):**

```tsx
<Iphone contentScale={0.35}>{content}</Iphone>
```

## Future Enhancements

Potential improvements:

- Automatic scale detection based on content dimensions
- Responsive scaling based on container size
- Per-breakpoint scaling configurations
- Visual scale slider for live preview
