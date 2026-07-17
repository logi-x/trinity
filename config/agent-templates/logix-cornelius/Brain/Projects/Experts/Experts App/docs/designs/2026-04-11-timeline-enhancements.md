---
title: "Timeline Enhancements - User Profile Activity Feed"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/timeline-enhancements"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Timeline Enhancements - User Profile Activity Feed

**Date**: December 22, 2025
**Status**: ✅ Complete

## Overview

Enhanced the user profile timeline with a visual timeline drawing, smaller compact cards, and more data display. The new design provides a modern, Twitter/GitHub-style activity feed with better visual hierarchy and information density.

---

## Key Features

### 1. Visual Timeline Drawing

**Vertical Timeline Line**:

- Gradient line running from top to bottom (`from-violet-500/20 via-violet-500/40 to-violet-500/20`)
- Positioned absolutely on the left side
- Creates a visual connection between activities
- Subtle gradient effect for depth

**Timeline Nodes**:

- 48px circular nodes with activity type icons
- Color-coded by activity type (post, comment, like, follow, etc.)
- Semi-transparent background matching activity color
- Border ring for depth effect
- Icons clearly indicate activity type at a glance

### 2. Smaller, Compact Cards

**Before**: Full-width cards with large padding
**After**: Compact cards with:

- Reduced padding (p-4 instead of default)
- Smaller avatar (32px instead of 40px)
- Condensed text sizes
- Line clamping for descriptions (2 lines max)
- Better space utilization

### 3. More Data Display

**Enhanced Information**:

1. **Activity Type Badge**: Color-coded badge showing activity type (Posted, Commented, Liked, etc.)
2. **Relative Timestamps**: Human-readable time (e.g., "2h ago", "3d ago", "Just now")
3. **Absolute Timestamp**: Hover tooltip shows full date/time
4. **Metadata Display**: Shows additional context (reaction type, entity type, followed user)
5. **Activity Icons**: 12+ activity types with unique icons and colors

**Activity Types Supported**:

- 📄 Posts (FileText - blue)
- 💬 Comments (MessageSquare - green)
- ❤️ Likes/Reactions (Heart - pink)
- 👤 Follows (UserPlus - purple)
- 📚 Courses (BookOpen - orange)
- ✅ Enrollments (CheckCircle2 - teal)
- 📅 Events (Calendar - indigo)
- 🏆 Certificates (Award - amber)
- 👁️ Views (Eye - slate)
- 🔗 Shares (Share2 - cyan)
- ⭐ Reviews/Ratings (Star - yellow)
- ✨ Generic Activity (Sparkles - violet)

### 4. Better Visual Hierarchy

**Layout Structure**:

```
┌─────────────────────────────────────────┐
│  Timeline Line (gradient)               │
│     │                                   │
│     ●───┬─ Icon Node (circular)         │
│     │   │  ┌─────────────────────┐      │
│     │   └──│ Compact Card        │      │
│     │      │  • Avatar + Name    │      │
│     │      │  • Badge + Time     │      │
│     │      │  • Title (1 line)   │      │
│     │      │  • Description (2)  │      │
│     │      │  • Metadata         │      │
│     │      └─────────────────────┘      │
│     │                                   │
│     ●───┬─ Next Activity                │
│     │   └──...                          │
└─────────────────────────────────────────┘
```

**Visual Improvements**:

- Clear separation between timeline nodes and content
- Consistent spacing (4-unit gap between items)
- Cards offset from timeline (ml-12) for alignment
- Hover effects (shadow-md, bg-accent/50)
- Smooth transitions (duration-200)

---

## Files Modified

### `/home/logix/experts/apps/experts-app/src/components/profile/activity-feed.tsx`

**Changes**:

- Added absolute-positioned vertical timeline line
- Switched from `ActivityItem` to `TimelineActivityItem`
- Added `isFirst` and `isLast` props for future customization
- Maintained loading and empty states

**Key Code**:

```tsx
<div className="relative" role="feed">
  {/* Timeline vertical line */}
  <div className="absolute left-6 top-8 bottom-8 w-0.5 bg-gradient-to-b from-violet-500/20 via-violet-500/40 to-violet-500/20" />

  {/* Activity items */}
  <div className="space-y-4">
    {activities.map((activity, index) => (
      <TimelineActivityItem
        key={activity.id}
        activity={activity}
        isFirst={index === 0}
        isLast={index === activities.length - 1}
      />
    ))}
  </div>
</div>
```

### `/home/logix/experts/apps/experts-app/src/components/profile/timeline-activity-item.tsx` (NEW)

**Features**:

1. **Activity Icon Mapping** (`getActivityIcon` function):
   - Maps 20+ activity types to icons
   - Returns icon component, colors, and label
   - Consistent color scheme across app

2. **Relative Time Formatting** (`formatRelativeTime` function):
   - Converts timestamps to human-readable format
   - Handles: "Just now", "2m ago", "3h ago", "4d ago", "2w ago", "Jan 15"
   - Smart year display (hides current year)

3. **Compact Layout**:
   - Header row: Avatar (32px) + Name + Badge + Time
   - Title row: Single line with ellipsis
   - Description: 2 lines max with line-clamp
   - Metadata: Flexible tags for additional context

4. **Interactive Elements**:
   - Clickable avatar (navigates to profile)
   - Clickable card (if activity has link)
   - Keyboard navigation support (Enter/Space)
   - Hover states for better UX

5. **Accessibility**:
   - ARIA labels for screen readers
   - Semantic HTML (time element with datetime)
   - Role="button" for interactive elements
   - Keyboard navigation support

---

## Technical Details

### Tailwind Classes Used

**Timeline Line**:

```css
absolute left-6 top-8 bottom-8 w-0.5
bg-gradient-to-b from-violet-500/20 via-violet-500/40 to-violet-500/20
```

**Timeline Node**:

```css
h-12 w-12 rounded-full border-2 border-background
flex items-center justify-center shadow-sm
[bgColor] /* Dynamic: bg-blue-500/10, bg-green-500/10, etc. */
```

**Card**:

```css
ml-12 /* Offset from timeline */
border-border/50 bg-card/50
hover:bg-accent/50 hover:shadow-md
transition-all duration-200
```

**Avatar**:

```css
h-8 w-8 rounded-full
ring-2 ring-violet-500/20
cursor-pointer hover:opacity-80
```

**Badge**:

```css
text-xs border-0
[bgColor] [color] /* Dynamic colors */
```

### Component Props

```typescript
interface TimelineActivityItemProps {
  activity: Activity; // Activity data from API
  isFirst?: boolean; // First item in timeline
  isLast?: boolean; // Last item in timeline
}
```

### Activity Type Interface

```typescript
interface Activity {
  id: string;
  type: string; // Activity type key
  entityType: string; // Entity being acted upon
  entityId: string; // Entity ID
  title: string | null; // Activity title
  description: string | null; // Activity description
  metadata: Record<string, unknown> | null; // Additional data
  link: string | null; // Optional link
  createdAt: string; // ISO timestamp
  user: {
    id: string;
    username: string | null;
    fullName: string;
    avatar: string | null;
  };
  followedUser?: {
    // For follow activities
    username: string | null;
    fullName: string | null;
  } | null;
}
```

---

## Responsive Design

The timeline is fully responsive:

**Desktop** (default):

- Timeline line on left
- Cards offset with ml-12
- Full metadata display

**Tablet** (no changes needed):

- Layout scales naturally
- Text remains readable

**Mobile** (future enhancement):

- Could reduce timeline line offset
- Could stack elements vertically
- Could reduce icon sizes

---

## Performance Optimizations

1. **Component Memoization**: Each item renders independently
2. **Image Optimization**: Next.js Image component with width/height
3. **Line Clamping**: CSS-only text truncation (no JS)
4. **Conditional Rendering**: Metadata only shown if present
5. **Event Delegation**: Minimal event handlers per item

---

## Future Enhancements

### Short-term

- [ ] Add "Load More" pagination
- [ ] Add activity filtering (posts only, comments only, etc.)
- [ ] Add date separators ("Today", "Yesterday", "Last Week")
- [ ] Add skeleton loading states
- [ ] Add animations for new activities

### Medium-term

- [ ] Add activity grouping (e.g., "John liked 3 posts")
- [ ] Add inline reactions to activities
- [ ] Add activity search/filter
- [ ] Add export timeline feature
- [ ] Add year markers on timeline line

### Long-term

- [ ] Real-time activity updates via polling
- [ ] Infinite scroll with virtual list
- [ ] Activity detail modal
- [ ] Activity notifications integration
- [ ] Timeline customization (hide certain types)

---

## Usage Example

```tsx
// In user profile page
import { ActivityFeed } from "@/components/profile/activity-feed";

export default function UserProfilePage() {
  const profile = useProfile();

  return (
    <Tabs defaultValue="timeline">
      <TabsContent value="timeline">
        <ActivityFeed userId={profile.id} />
      </TabsContent>
    </Tabs>
  );
}
```

---

## Testing Checklist

### Visual Testing

- ✅ Timeline line renders correctly
- ✅ Nodes align with timeline line
- ✅ Cards are properly offset
- ✅ Hover effects work smoothly
- ✅ Icons and colors match activity types
- ✅ Text truncation works (line-clamp)

### Functional Testing

- ✅ Click avatar → navigate to profile
- ✅ Click card with link → navigate to content
- ✅ Keyboard navigation works (Tab, Enter, Space)
- ✅ Relative time updates are accurate
- ✅ Tooltip shows full timestamp on hover
- ✅ Metadata displays correctly

### Edge Cases

- ✅ Empty timeline shows "No activities" message
- ✅ Loading state shows spinner
- ✅ Long usernames truncate properly
- ✅ Long descriptions clamp to 2 lines
- ✅ Activities without links are non-clickable
- ✅ Missing avatars show initials

### Accessibility

- ✅ Screen reader announces timeline correctly
- ✅ Time elements have proper datetime attribute
- ✅ Interactive elements have ARIA labels
- ✅ Focus indicators are visible
- ✅ Keyboard navigation works throughout

---

## Design Inspiration

Inspired by:

- **Twitter**: Compact cards with avatars and timestamps
- **GitHub**: Activity feed with timeline and icons
- **LinkedIn**: Professional activity feed layout
- **Notion**: Clean, minimal card design

---

## Color Palette

Activity type colors follow a semantic pattern:

| Activity Type | Color        | Usage                |
| ------------- | ------------ | -------------------- |
| Posts         | Blue (600)   | Content creation     |
| Comments      | Green (600)  | Engagement           |
| Likes         | Pink (600)   | Reactions            |
| Follows       | Purple (600) | Social connections   |
| Courses       | Orange (600) | Learning content     |
| Enrollments   | Teal (600)   | Learning progress    |
| Events        | Indigo (600) | Scheduled activities |
| Certificates  | Amber (600)  | Achievements         |
| Views         | Slate (600)  | Passive engagement   |
| Shares        | Cyan (600)   | Content distribution |
| Reviews       | Yellow (600) | Feedback             |
| Generic       | Violet (600) | Default fallback     |

All colors use `/10` opacity for backgrounds and full strength for text/icons.

---

## Conclusion

The enhanced timeline provides a modern, information-dense activity feed that:

- **Improves UX**: Visual timeline makes chronology clear
- **Increases Data Density**: More information in less space
- **Enhances Scannability**: Icons and colors enable quick recognition
- **Maintains Performance**: Lightweight, optimized components
- **Supports Accessibility**: Full keyboard and screen reader support

The new design significantly improves the user profile experience and aligns with modern social platform design patterns.
