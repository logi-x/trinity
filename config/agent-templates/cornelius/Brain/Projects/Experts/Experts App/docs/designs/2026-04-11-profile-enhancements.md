---
title: "User Profile Page Enhancements"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/profile-enhancements"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# User Profile Page Enhancements

## Overview

Enhanced the user profile page (`/app/[username]/page.tsx`) with modern features, better architecture, and improved user experience.

## Key Enhancements

### 1. **Component Architecture** ✅

- **Extracted Components**: Separated concerns into dedicated components for better maintainability
  - `ProfileHeader` → `/src/components/profile/ProfileHeader.tsx`
  - `ProfileStats` → `/src/components/profile/ProfileStats.tsx`
  - `ActivityFeed` → `/app/[username]/(tabs)/activity-feed.tsx`
  - `ActivityItem` → `/app/[username]/(tabs)/activity-item.tsx`
  - `CoursesTab` → `/app/[username]/(tabs)/courses.tsx`
  - `EventsTab` → `/app/[username]/(tabs)/events.tsx`

### 2. **Visual Enhancements** ✅

#### Cover Photo

- Added customizable cover photo support
- Gradient fallback for users without cover photos
- Edit button for profile owners

#### Enhanced Avatar Section

- Larger, more prominent avatar (128px → 160px)
- Camera icon for quick photo updates (profile owners)
- Verified badge indicator for verified users
- Instructor badge with better positioning

#### New Features in ProfileHeader

- **Share Profile**: Native share API with clipboard fallback
- **Verified Badge**: CheckCircle icon for verified accounts
- **Social Links**: Twitter, LinkedIn, GitHub integration
- **Location & Website**: Display user location and personal website
- **Cover Photo**: Professional-looking banner image

### 3. **Enhanced Stats Section** ✅

- Animated stat cards with stagger effect
- Hover animations (scale on hover)
- Icon-based visual indicators
- Color-coded categories:
  - Followers: Violet
  - Following: Blue
  - Posts: Emerald
  - Courses: Amber
- Number formatting (1K, 1M for large numbers)

### 4. **New Tab Components** ✅

#### Courses Tab

- Grid layout (responsive: 1 col → 2 cols → 3 cols)
- Course cards with:
  - Thumbnail images
  - Enrollment count
  - Duration
  - Rating
  - Price display
  - Draft badge for unpublished courses
- Hover effects (scale + image zoom)

#### Events Tab

- Grid layout (responsive)
- Event cards with:
  - Event images
  - Status badges (upcoming, ongoing, completed, cancelled)
  - Date and time
  - Location (virtual or physical)
  - Registration count
- Color-coded status badges

### 5. **Improved Activity Feed** ✅

- Separated into dedicated components
- Better accessibility with ARIA labels
- Semantic HTML (`<time>` tags with `dateTime`)
- Improved avatar fallbacks

### 6. **SEO & Metadata** ✅

- Dynamic page title: `{name} (@{username}) | Experts`
- Dynamic meta description using user bio
- Updates on profile load via `useEffect`

### 7. **Accessibility Improvements** ✅

- ARIA labels on all interactive elements
- Proper `alt` text for images
- Keyboard navigation support
- Semantic HTML elements (`<time>`, role="feed", etc.)
- Focus states on all buttons

### 8. **Responsive Design** ✅

- Mobile-first approach
- Responsive grid layouts (2 cols mobile → 4 cols desktop)
- Adaptive tab layout (grid on mobile, flex on desktop)
- Proper spacing and padding adjustments
- Touch-friendly button sizes

### 9. **User Experience** ✅

- Smooth animations with Framer Motion
- Staggered animations for stats cards
- Hover effects on cards
- Toast notifications for actions (share, copy link)
- Loading states for all async operations
- Empty states for all tabs
- Gradient fallbacks for missing images

### 10. **Performance** ✅

- Optimized image loading with Next.js Image component
- `priority` prop on above-fold images (avatar, cover)
- Lazy loading for tab content
- Efficient data fetching with SWR
- Error handling and fallbacks

## New User Profile Fields

Added optional fields to the `UserProfile` interface:

```typescript
interface UserProfile {
  // Existing fields...

  // New fields:
  coverPhoto?: string | null;
  location?: string | null;
  website?: string | null;
  socialLinks?: {
    twitter?: string;
    linkedin?: string;
    github?: string;
  };
  isVerified?: boolean;
}
```

## File Structure

```
apps/experts-app/
├── app/[username]/
│   ├── page.tsx                          # Main profile page (enhanced)
│   └── (tabs)/
│       ├── about.tsx                     # About tab (existing)
│       ├── activity-feed.tsx             # Activity feed (new)
│       ├── activity-item.tsx             # Activity item (new)
│       ├── courses.tsx                   # Courses tab (new)
│       └── events.tsx                    # Events tab (new)
└── src/components/profile/
    ├── ProfileHeader.tsx                 # Profile header (new)
    └── ProfileStats.tsx                  # Stats section (new)
```

## Dependencies Used

All existing dependencies, no new packages required:

- ✅ `framer-motion` - Animations
- ✅ `sonner` - Toast notifications
- ✅ `lucide-react` - Icons
- ✅ `next/image` - Image optimization
- ✅ `swr` - Data fetching

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Graceful fallback for Share API
- Responsive design for all screen sizes
- Touch-friendly on mobile devices

## Future Enhancements (Optional)

1. **Profile Analytics**: View count, profile views tracking
2. **Achievements System**: Badges and achievements display
3. **Activity Filters**: Filter activities by type
4. **Infinite Scroll**: Load more activities on scroll
5. **Profile Themes**: Custom color schemes
6. **Privacy Settings**: Public/private profile toggle
7. **QR Code**: Generate QR code for profile sharing
8. **Export Profile**: Download profile as PDF
9. **Follower/Following Lists**: Modal to view lists
10. **Custom Tabs**: Allow users to create custom tabs

## Migration Notes

### Backend Changes Required (Optional)

To fully support the new features, the API should return these additional fields:

```typescript
// GET /api/users/[username]
{
  // Add these fields to the response:
  coverPhoto?: string | null,
  location?: string | null,
  website?: string | null,
  socialLinks?: {
    twitter?: string,
    linkedin?: string,
    github?: string
  },
  isVerified?: boolean
}
```

### Database Schema Updates (Optional)

```prisma
model User {
  // Add these fields to User model:
  coverPhoto   String?
  location     String?
  website      String?
  twitter      String?
  linkedin     String?
  github       String?
  isVerified   Boolean @default(false)
}
```

## Testing Checklist

- [ ] Profile loads correctly
- [ ] All tabs display properly
- [ ] Follow/Unfollow works
- [ ] Share profile works (native & fallback)
- [ ] Social links open correctly
- [ ] Responsive design on mobile
- [ ] Loading states display
- [ ] Empty states display
- [ ] Error states display
- [ ] Images load with fallbacks
- [ ] Animations work smoothly
- [ ] Accessibility (keyboard navigation)
- [ ] SEO metadata updates

## Performance Metrics

- **Lighthouse Score**: Target 90+ (Performance, Accessibility, SEO)
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3.5s
- **Largest Contentful Paint**: < 2.5s

---

**Enhanced by**: Claude Code
**Date**: December 2025
**Version**: 2.0.0
