---
title: "Course Form Layout Component"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/course"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Course Form Layout Component

## Overview

The `CourseFormLayout` component provides a modern, flexible layout for course creation and editing forms with a smooth, responsive design. It features an innovative vertical accordion toggle for the live preview panel and a separate full preview modal.

## Key Features

### 🎨 Modern Flexbox Design

- **Flexible layout** with smooth transitions (300ms ease-in-out)
- **Dynamic width calculations** that adapt to content and preview visibility
- **Vertical accordion button** on the right edge of the form for intuitive preview toggling

### 📱 Responsive Behavior

**Mobile (< 1024px)**

- Stacked layout: Form on top, preview below
- Full-width form for better mobile editing experience
- Preview panel collapses to full width when visible
- Accordion button hidden on mobile

**Desktop (≥ 1024px)**

- Side-by-side layout with smooth resizing
- Form panel: Flexible width (`flex-1`) when preview is visible
- Preview panel: Fixed width (400px on lg, 480px on xl screens)
- Vertical accordion button visible on right edge of form

### 🔄 Two Independent Preview Controls

#### 1. **Live Preview Toggle** (Vertical Accordion Button)

- **Location**: Right edge of form panel (vertical accordion style)
- **Design**: Tall pill-shaped button (h-24 w-6) with rounded corners
- **States**:
  - **Preview Shown**: Primary colored background, ChevronRight icon (→)
  - **Preview Hidden**: Neutral background, ChevronLeft icon (←)
- **Animation**: Preview expands/collapses from right side with smooth width and opacity transitions
- **Tooltip**: Positioned at top, shows "Hide/Show live preview"
- **Desktop only**: Hidden on mobile devices

#### 2. **Full Preview Button** (Toolbar Button)

- **Location**: Top toolbar (Maximize2 icon)
- **Behavior**: Opens full preview in modal dialog
- **Independent**: Works regardless of live preview panel state
- **Modal**: Fullscreen with max-width of 1400px

## Visual Enhancements

### Vertical Accordion Button

```tsx
<button className="flex h-24 w-6 items-center justify-center rounded-lg border shadow-md">
  {showLivePreview ? <ChevronRight /> : <ChevronLeft />}
</button>
```

**Active State (Preview Shown)**:

- Background: `bg-primary/10`
- Border: `border-primary/20`
- Text: `text-primary`
- Hover: `hover:bg-primary/20`
- Icon: ChevronRight (→) indicates you can hide it

**Inactive State (Preview Hidden)**:

- Background: `bg-white` / `dark:bg-zinc-800`
- Border: `border-zinc-200` / `dark:border-zinc-700`
- Text: `text-zinc-500` / `dark:text-zinc-400`
- Hover: `hover:bg-zinc-50` / `dark:hover:bg-zinc-700`
- Icon: ChevronLeft (←) indicates you can show it

### Preview Header

```tsx
<div className="flex items-center justify-between rounded-lg bg-gradient-to-r from-primary-50 to-secondary-50 p-4">
  <div className="flex items-center gap-2">
    <Eye className="h-5 w-5 text-primary" />
    <span className="font-semibold">Live Preview</span>
  </div>
  <Chip size="sm" variant="flat" color="primary">
    Updates in real-time
  </Chip>
</div>
```

Features:

- Gradient background (primary → secondary)
- Eye icon for visual clarity
- "Live Preview" title
- Real-time update indicator chip

### Full Preview Modal

```tsx
<Modal
  size="5xl"
  scrollBehavior="inside"
  classNames={{ base: "max-w-[1400px]" }}
>
  <ModalHeader>
    <Maximize2 className="h-5 w-5 text-primary" />
    <span>Full Course Preview</span>
  </ModalHeader>
  <ModalBody className="p-6">{renderExpandedPreview()}</ModalBody>
</Modal>
```

### Sticky Preview Panel

- Uses `sticky top-0` positioning
- Stays visible while scrolling through long forms
- Inner content has fixed width (400px/480px) to maintain size during animations

## Layout Structure

### Flexbox-based Layout

```tsx
<div className="relative flex flex-col gap-6 lg:flex-row">
  {/* Form Panel with Accordion Button */}
  <div className="relative w-full lg:flex-1 transition-all duration-300">
    <Card>{/* Form content */}</Card>

    {/* Vertical Accordion Button */}
    <div className="absolute top-1/2 -right-3 z-10 hidden lg:block">
      <button>{/* Toggle button */}</button>
    </div>
  </div>

  {/* Live Preview Panel - Expands/collapses from right */}
  <div className="origin-right overflow-hidden transition-all duration-300">
    {/* Preview content */}
  </div>
</div>
```

Benefits:

- ✅ Simple, intuitive layout logic
- ✅ Smooth 300ms transitions
- ✅ Easy to customize widths
- ✅ Better responsive behavior
- ✅ Form automatically fills available space
- ✅ Accordion button clearly indicates expand/collapse direction

## Width Calculations

### Form Panel

| Preview State | Mobile | Desktop (lg) | Desktop (xl) |
| ------------- | ------ | ------------ | ------------ |
| Hidden        | 100%   | 100%         | 100%         |
| Visible       | 100%   | flex-1\*     | flex-1\*     |

\*flex-1 = `calc(100% - 400px - 24px)` on lg, `calc(100% - 480px - 24px)` on xl

### Preview Panel

| Preview State | Mobile | Desktop (lg) | Desktop (xl) |
| ------------- | ------ | ------------ | ------------ |
| Hidden        | w-0    | w-0          | w-0          |
| Visible       | 100%   | 400px        | 480px        |

Animation: `w-0 scale-x-0 opacity-0` → `w-full scale-x-100 opacity-100`

### Full Preview Modal

- Opens as fullscreen modal overlay
- Max width: 1400px
- Centered on screen
- Scrollable content
- Independent of live preview state

## Usage Example

```tsx
import { CourseFormLayout } from "@experts/ui";
import { useState } from "react";

export default function CreateCoursePage() {
  const [showLivePreview, setShowLivePreview] = useState(true);

  return (
    <CourseFormLayout
      title="Create New Course"
      totalSteps={4}
      activeStep={1}
      stepTitles={["Information", "Details", "Curriculum", "Review"]}
      // Live preview control (vertical accordion button)
      showLivePreview={showLivePreview}
      setShowLivePreview={setShowLivePreview}
      // State indicators
      hasUnsavedChanges={isDirty}
      isAutoSaving={isAutoSaving}
      lastAutoSave={lastSaveTime}
      isOnline={isOnline}
      // Navigation
      onNext={handleNext}
      onPrevious={handlePrevious}
      onSubmit={handlePublish}
      goToStep={setStep}
      // Actions
      onBack={() => router.push("/courses")}
      onSaveDraft={handleSaveDraft}
      onCopyLink={handleCopyLink}
      // Compact preview for sidebar
      previewContent={
        <CoursePreviewContent
          formData={formData}
          previewMode="partial"
          {...previewProps}
        />
      }
      // Full preview for modal (optional)
      renderExpandedPreview={() => (
        <LiveCoursePreview
          formData={formData}
          previewMode="expanded"
          {...previewProps}
        />
      )}
    >
      {/* Your form content */}
      <CourseStepRenderer activeStep={activeStep} steps={courseSteps} />
    </CourseFormLayout>
  );
}
```

## Control Elements

### 1. Vertical Accordion Button (Right Edge)

**Appearance:**

- Pill-shaped vertical button (24 pixels wide, 96 pixels tall)
- Positioned on right edge of form panel
- Centered vertically (`top-1/2 -translate-y-1/2`)
- Slightly overlaps right edge (`-right-3`) for better visual connection
- Rounded corners with shadow for depth

**Behavior:**

- Click to toggle live preview panel
- Icon changes direction based on state:
  - ChevronRight (→) when preview is shown = "hide preview"
  - ChevronLeft (←) when preview is hidden = "show preview"
- Color changes to indicate active/inactive state
- Smooth transition on hover

**Desktop only**: Hidden on mobile (`hidden lg:block`)

### 2. Full Preview Button (Toolbar - Maximize2)

- Opens full preview in modal
- Tooltip: "Open full preview"
- Best for final review before publishing
- **Only shown if** `renderExpandedPreview` prop is provided

### 3. Save Draft Button (Toolbar - Optional)

- Saves current progress
- Tooltip: "Save draft" or "No changes to save"
- Disabled when no changes present

## Two Preview Content Slots

### `previewContent` (Sidebar Preview)

- **Purpose**: Compact, real-time preview shown in the sidebar
- **Width**: 400px (lg) / 480px (xl)
- **Updates**: Live as user types
- **Recommendation**: Use `LiveCoursePreview` with `previewMode="partial"`

### `renderExpandedPreview()` (Modal Preview - Optional)

- **Purpose**: Full, interactive preview shown in modal
- **Width**: Max 1400px
- **Updates**: When modal is opened
- **Recommendation**: Use `LiveCoursePreview` with `previewMode="expanded"`
- **Note**: If not provided, Full Preview button won't appear in toolbar

## Animation Details

### Live Preview Panel Animation

**Expand Animation (showing preview):**

```css
/* From */
w-0 scale-x-0 opacity-0

/* To */
w-full lg:w-[400px] xl:w-[480px]
scale-x-100
opacity-100

/* Properties */
origin-right              /* Scale from right edge */
transition-all            /* Animate all properties */
duration-300              /* 300ms duration */
ease-in-out              /* Smooth easing */
```

**Visual Effect:**

- Panel expands from right to left (grows from its position)
- Width increases from 0 to full size
- Opacity fades in simultaneously
- Form panel smoothly adjusts width

**Collapse Animation (hiding preview):**

- Panel collapses from right to left (shrinks toward its position)
- Width decreases to 0
- Opacity fades out
- Form panel smoothly expands to full width

### Transition Properties

```css
transition-all duration-300 ease-in-out
```

Animates:

- Width changes (w-0 ↔ w-full/w-[400px]/w-[480px])
- Scale transforms (scale-x-0 ↔ scale-x-100)
- Opacity (opacity-0 ↔ opacity-100)
- Form panel width adjustments

### Performance

- Uses GPU-accelerated transitions (transform, opacity)
- `origin-right` ensures scale animation originates from right edge
- `overflow-hidden` prevents content overflow during animation
- No layout thrashing
- Smooth 60fps animations on modern browsers

## Accessibility

✅ Semantic HTML structure
✅ ARIA labels on interactive elements
✅ Keyboard navigation support
✅ Focus management during transitions
✅ Screen reader friendly status updates
✅ Modal with proper focus trap
✅ ESC key closes modal
✅ Tooltip provides context for accordion button
✅ Clear visual feedback for button states

## Best Practices

### Do's ✅

- Keep `showLivePreview={true}` as default for balanced editing/preview experience
- Provide clear preview content that updates in real-time
- Use status indicators (hasUnsavedChanges, isAutoSaving) for user confidence
- Implement smooth form validation with visual feedback
- Use the full preview modal for final review before publishing
- Use the vertical accordion button for quick preview toggling during editing

### Don'ts ❌

- Don't put critical form controls in preview panel
- Don't skip transition animations (feels janky)
- Don't make preview panel wider than 600px (form becomes cramped)
- Don't rely solely on modal preview - side panel is for real-time updates
- Don't change accordion button position or size (UX consistency)

## Migration Guide

### Update Props API

```diff
- previewMode={previewMode}
- setPreviewMode={setPreviewMode}
+ showLivePreview={showLivePreview}
+ setShowLivePreview={setShowLivePreview}
```

### Component State Management

Before:

```tsx
const [previewMode, setPreviewMode] = useState<
  "hidden" | "partial" | "expanded"
>("partial");
```

After:

```tsx
const [showLivePreview, setShowLivePreview] = useState(true); // Simple boolean!
// Full preview is now handled independently via modal
```

### Preview Content Updates

Before:

```tsx
<LiveCoursePreview previewMode={previewMode} {...props} />
```

After:

```tsx
// For sidebar (always partial)
previewContent={
  <CoursePreviewContent
    previewMode="partial"
    {...props}
  />
}

// For modal (always expanded)
renderExpandedPreview={() => (
  <LiveCoursePreview
    previewMode="expanded"
    {...props}
  />
)}
```

## Browser Support

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari 14+, Chrome Android)

## Related Components

- `CourseStepIndicator` - Step progress visualization
- `CoursePreviewContent` - Wrapper for compact preview
- `LiveCoursePreview` - Live course preview with dual modes
- `useExpandedPreviewRenderer` - Hook for modal preview
