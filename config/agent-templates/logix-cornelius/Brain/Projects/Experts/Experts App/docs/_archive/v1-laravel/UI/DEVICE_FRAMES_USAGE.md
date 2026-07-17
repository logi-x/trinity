---
title: "Device Frame Components - Enhanced Usage Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/ui"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Device Frame Components - Enhanced Usage Guide

## Overview

The iPhone and iPad components have been enhanced to support embedding custom React content (like page builder elements) directly within the device frames. These components now support three rendering modes:

1. **Children Content** (highest priority) - Render custom React components
2. **Video Content** - Display video with auto-play
3. **Image Content** - Display static images

## Components

### iPhone Component

Display content in an iPhone frame with realistic device proportions.

#### Props

```typescript
interface IphoneProps extends HTMLAttributes<HTMLDivElement> {
  src?: string; // Image source URL
  videoSrc?: string; // Video source URL
  children?: ReactNode; // React content (highest priority)
  enableScroll?: boolean; // Enable scrolling (default: true)
  screenBackground?: string; // Background color (default: "white")
  className?: string; // Additional CSS classes
  style?: CSSProperties; // Additional inline styles
}
```

#### Usage Examples

**1. Embedding Page Builder Content**

```tsx
import { Iphone } from "@experts/ui";
import { Frame } from "@craftjs/core";

function PagePreview() {
  return (
    <Iphone enableScroll={true} screenBackground="transparent">
      <Frame data={pageBuilderData}>{/* Your page builder content */}</Frame>
    </Iphone>
  );
}
```

**2. Displaying Custom React Components**

```tsx
import { Iphone } from "@experts/ui";

function AppPreview() {
  return (
    <Iphone enableScroll={true} screenBackground="#f5f5f5">
      <div className="p-4">
        <h1>Welcome to My App</h1>
        <p>This is custom content inside the iPhone frame</p>
        <button>Click Me</button>
      </div>
    </Iphone>
  );
}
```

**3. Video Display (fallback when no children)**

```tsx
<Iphone videoSrc="https://example.com/demo-video.mp4" className="max-w-md" />
```

**4. Image Display (fallback when no children or video)**

```tsx
<Iphone src="https://example.com/screenshot.png" className="max-w-md" />
```

---

### iPad Component

Display content in an iPad frame with support for both portrait and landscape orientations.

#### Props

```typescript
interface IpadProps extends HTMLAttributes<HTMLDivElement> {
  src?: string; // Image source URL
  videoSrc?: string; // Video source URL
  orientation?: "portrait" | "landscape"; // Device orientation (default: "portrait")
  children?: ReactNode; // React content (highest priority)
  enableScroll?: boolean; // Enable scrolling (default: true)
  screenBackground?: string; // Background color (default: "white")
  className?: string; // Additional CSS classes
  style?: CSSProperties; // Additional inline styles
}
```

#### Usage Examples

**1. Embedding Page Builder Content**

```tsx
import { Ipad } from "@experts/ui";
import { Frame } from "@craftjs/core";

function PagePreview() {
  return (
    <Ipad
      orientation="portrait"
      enableScroll={true}
      screenBackground="transparent"
    >
      <Frame data={pageBuilderData}>{/* Your page builder content */}</Frame>
    </Ipad>
  );
}
```

**2. Landscape Orientation**

```tsx
<Ipad orientation="landscape" enableScroll={true} screenBackground="#ffffff">
  <div className="p-8">
    <h1>Landscape View</h1>
    <p>Perfect for wide content layouts</p>
  </div>
</Ipad>
```

**3. Dashboard Preview**

```tsx
<Ipad orientation="landscape" enableScroll={true}>
  <Dashboard />
</Ipad>
```

---

## Integration with Page Builder

The page-builder-editor component now uses the enhanced device frames seamlessly:

```tsx
// In page-builder-editor.tsx
const renderCanvas = () => {
  const frameContent = <Frame data={frameData}>{defaultContent}</Frame>;

  if (viewport === "mobile") {
    return (
      <Iphone enableScroll={true} screenBackground="transparent">
        {frameContent}
      </Iphone>
    );
  }

  if (viewport === "tablet") {
    return (
      <Ipad
        orientation="portrait"
        enableScroll={true}
        screenBackground="transparent"
      >
        {frameContent}
      </Ipad>
    );
  }

  return frameContent; // Desktop - no frame
};
```

## Key Features

### 1. **Automatic Content Prioritization**

The components intelligently choose what to render:

```tsx
// Priority order:
// 1. children (if provided)
// 2. videoSrc (if provided and no children)
// 3. src (if provided and no children or videoSrc)
```

### 2. **Scroll Management**

Control whether content should scroll within the device frame:

```tsx
// Enable scrolling for long content
<Iphone enableScroll={true}>
  <LongPageContent />
</Iphone>

// Disable scrolling for fixed layouts
<Iphone enableScroll={false}>
  <SplashScreen />
</Iphone>
```

### 3. **Theme Integration**

Use transparent backgrounds to inherit theme colors:

```tsx
<Iphone screenBackground="transparent">
  <ThemedContent /> {/* Inherits page theme */}
</Iphone>

<Iphone screenBackground="#1a1a1a">
  <DarkContent /> {/* Force dark background */}
</Iphone>
```

### 4. **Responsive Sizing**

Device frames scale proportionally:

```tsx
<div className="max-w-[434px]">
  <Iphone>{content}</Iphone>
</div>

<div className="max-w-[900px]">
  <Ipad>{content}</Ipad>
</div>
```

## Advanced Examples

### Multi-Device Preview

```tsx
function MultiDevicePreview({ content }) {
  return (
    <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
      {/* Mobile View */}
      <div>
        <h3>Mobile</h3>
        <Iphone enableScroll={true}>{content}</Iphone>
      </div>

      {/* Tablet View */}
      <div>
        <h3>Tablet</h3>
        <Ipad orientation="portrait" enableScroll={true}>
          {content}
        </Ipad>
      </div>
    </div>
  );
}
```

### Interactive Preview

```tsx
function InteractivePreview() {
  const [viewport, setViewport] = useState("mobile");

  return (
    <>
      <select onChange={(e) => setViewport(e.target.value)}>
        <option value="mobile">Mobile</option>
        <option value="tablet">Tablet</option>
      </select>

      {viewport === "mobile" ? (
        <Iphone enableScroll={true}>
          <YourApp />
        </Iphone>
      ) : (
        <Ipad orientation="portrait" enableScroll={true}>
          <YourApp />
        </Ipad>
      )}
    </>
  );
}
```

### Dark Mode Support

```tsx
function ThemedPreview() {
  const { theme } = useTheme();

  return (
    <Iphone
      enableScroll={true}
      screenBackground={theme === "dark" ? "#1a1a1a" : "#ffffff"}
    >
      <YourApp />
    </Iphone>
  );
}
```

## Best Practices

1. **Use transparent backgrounds** when you want the content to inherit page theme
2. **Enable scrolling** for page builder content and long-form content
3. **Disable scrolling** for splash screens, modals, or fixed-height content
4. **Choose appropriate max-width** to control device frame size
5. **Test in both orientations** for iPad to ensure content looks good
6. **Consider performance** when embedding complex page builder content

## Technical Details

### Screen Dimensions

**iPhone:**

- Device: 433 × 882px
- Screen: 389.5 × 843.5px
- Screen Position: 21.25px from left, 19.25px from top
- Border Radius: 55.75px

**iPad:**

- Device: 834 × 1194px (portrait)
- Screen: 794 × 1154px
- Screen Position: 20px from all sides
- Border Radius: 20px

### Z-Index Layering

```
z-10: Children content (interactive)
z-0:  Video/Image content (non-interactive)
SVG:  Device frame (overlay)
```

## Migration Guide

If you were using the old pattern with manual positioning:

**Before:**

```tsx
<div className="relative">
  <Iphone />
  <div className="absolute" style={{left: "4.9%", top: "2.2%", ...}}>
    {content}
  </div>
</div>
```

**After:**

```tsx
<Iphone enableScroll={true} screenBackground="transparent">
  {content}
</Iphone>
```

## Troubleshooting

**Content not visible?**

- Check if `screenBackground` is set (default is "white")
- Ensure content has proper dimensions
- Verify z-index conflicts aren't hiding content

**Scrolling not working?**

- Verify `enableScroll={true}` is set
- Ensure content height exceeds screen height
- Check for overflow CSS conflicts

**Frame looks distorted?**

- Use proper container with max-width
- Maintain aspect ratio constraints
- Avoid conflicting transform styles
