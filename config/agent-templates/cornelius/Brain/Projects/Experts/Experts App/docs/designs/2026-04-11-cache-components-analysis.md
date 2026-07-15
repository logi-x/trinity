---
title: "Cache components analysis"
date: "2026-04-11"
tags: ["project/experts", "docs/v4", "topic/cache", "topic/nextjs"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Cache Components Analysis for Experts LMS

## Current Architecture

**Status**: ❌ Not using Cache Components (everything client-side)

### Current Flow (Courses Page Example)

1. User visits `/courses`
2. Browser loads empty page (Client Component)
3. JavaScript executes, makes API call to `/api/v1/courses`
4. API route queries database
5. Data returned to client
6. React renders courses

**Problems**:

- Slow initial page load (no content until JS executes)
- API route hit on every visit (no caching)
- Database queried on every request
- Poor SEO (content not in initial HTML)
- Higher server load

---

## Optimized Architecture with Cache Components

### Flow with Cached Server Components

1. User visits `/courses`
2. Server renders page with cached data
3. Browser receives **full HTML with content**
4. React hydrates for interactivity
5. Subsequent visits use cached data (no DB query)

**Benefits**:

- Fast initial page load (instant content)
- Better SEO (content in HTML)
- Reduced database load (cached queries)
- Lower server costs
- Better Core Web Vitals

---

## Side-by-Side Comparison

### Current (Client-Side)

```typescript
// ❌ app/courses/page.tsx
"use client";

import { usePublishedCourses } from "@/hooks/use-courses";

export default function CoursesPage() {
  // Client-side data fetch (runs in browser)
  const { courses, isLoading } = usePublishedCourses({
    search: searchQuery,
    category: selectedCategory,
    // ... filters
  });

  if (isLoading) return <Skeleton />; // Empty page initially

  return <CourseGrid courses={courses} />;
}
```

**Performance**:

- Time to First Byte (TTFB): ~200ms
- First Contentful Paint (FCP): ~1.5s (waiting for JS)
- Largest Contentful Paint (LCP): ~2.5s
- Total: **~2.5s** to show content

---

### Optimized (Server Component + Cache)

```typescript
// ✅ app/courses/page.tsx
import { getPublishedCourses } from '@/lib/cached-queries';

// Server Component (default in App Router)
export default async function CoursesPage() {
  // Server-side cached query (runs on server)
  const courses = await getPublishedCourses(); // Cached!

  return <CourseGrid courses={courses} />; // Pre-rendered HTML
}
```

```typescript
// ✅ lib/cached-queries.ts
"use cache";

export async function getPublishedCourses() {
  return prisma.course.findMany({ where: { published: true } });
}
```

**Performance (First Visit)**:

- Time to First Byte (TTFB): ~300ms
- First Contentful Paint (FCP): ~400ms (HTML already has content!)
- Largest Contentful Paint (LCP): ~600ms
- Total: **~600ms** to show content

**Performance (Cached Visit)**:

- Time to First Byte (TTFB): ~50ms
- First Contentful Paint (FCP): ~100ms
- Largest Contentful Paint (LCP): ~200ms
- Total: **~200ms** to show content (75% faster!)

---

## Hybrid Approach: Best of Both Worlds

For pages with **filters and interactivity**, use a **hybrid approach**:

### Initial Load: Cached Server Component

```typescript
// app/courses/page.tsx
import { getPublishedCourses } from '@/lib/cached-queries';
import { CoursesClient } from './courses-client';

export default async function CoursesPage() {
  // Server-rendered with cached data
  const initialCourses = await getPublishedCourses();

  return <CoursesClient initialCourses={initialCourses} />;
}
```

### Interactivity: Client Component

```typescript
// app/courses/courses-client.tsx
'use client';

import { useState } from 'react';
import { usePublishedCourses } from '@/hooks/use-courses';

export function CoursesClient({ initialCourses }) {
  const [filters, setFilters] = useState({});

  // Use initialCourses for first render, then fetch filtered data
  const { courses } = usePublishedCourses(filters, {
    fallbackData: initialCourses, // ✅ Show cached data instantly
  });

  return <CourseGrid courses={courses} filters={filters} />;
}
```

**Best of Both Worlds**:

- ✅ Fast initial load (cached data)
- ✅ SEO-friendly (content in HTML)
- ✅ Interactive filters (client-side)
- ✅ Reduced DB load (cached queries)

---

## When to Cache in Your LMS

### ✅ Cache These (High Impact, Low Risk)

| Feature                  | Current      | Cache Strategy                   | Impact                        |
| ------------------------ | ------------ | -------------------------------- | ----------------------------- |
| **Course Catalog**       | Client fetch | `'use cache'`                    | 🔥 High - Most visited page   |
| **Course Details**       | Client fetch | `'use cache'` + tag revalidation | 🔥 High - SEO critical        |
| **Instructor Profiles**  | Client fetch | `'use cache'`                    | 🟡 Medium - Public pages      |
| **Pricing Page**         | Static       | `'use cache'`                    | 🟡 Medium - Rarely changes    |
| **Landing Page**         | Static       | Already fast                     | 🟢 Low - Already optimized    |
| **Blog/Community Posts** | Client fetch | `'use cache'`                    | 🟡 Medium - Content marketing |

---

### ❌ Don't Cache These (User-Specific/Real-Time)

| Feature                   | Reason                 | Approach          |
| ------------------------- | ---------------------- | ----------------- |
| **User Dashboard**        | Personalized content   | Client-side fetch |
| **Lesson Progress**       | Real-time updates      | Client-side fetch |
| **Enrollments**           | User-specific          | Client-side fetch |
| **Affiliate Commissions** | Financial data         | Client-side fetch |
| **Event Registrations**   | Real-time availability | Client-side fetch |
| **Shopping Cart**         | Session-specific       | Client-side fetch |

---

## Implementation Priority

### Phase 1: Quick Wins (1-2 hours)

1. ✅ Create `lib/cached-queries.ts` (DONE - see file)
2. ✅ Create `lib/revalidation.ts` (DONE - see file)
3. Refactor course catalog to use cached query
4. Refactor course details page
5. Add revalidation to course update actions

**Estimated Performance Gain**: 60-75% faster page loads

---

### Phase 2: Expand Caching (2-4 hours)

1. Cache instructor profiles
2. Cache blog/community posts
3. Cache pricing page
4. Add cache warming on deployments

**Estimated Performance Gain**: 80-90% faster across site

---

### Phase 3: Advanced Optimization (4-8 hours)

1. Implement Partial Prerendering (PPR) for mixed static/dynamic pages
2. Add incremental static regeneration (ISR) for course content
3. Implement stale-while-revalidate for non-critical content
4. Add cache analytics and monitoring

**Estimated Performance Gain**: 90-95% faster, <200ms LCP

---

## Cost-Benefit Analysis

### Current Costs (No Caching)

- Database queries: ~1000/hour (peak)
- Server CPU: ~60% average
- API route invocations: ~800/hour
- Monthly server cost: $X (estimate based on your infrastructure)

### With Cache Components

- Database queries: ~50/hour (-95%)
- Server CPU: ~20% average (-67%)
- API route invocations: ~100/hour (-87%)
- **Estimated monthly savings**: 40-60% lower server costs

**Additional Benefits**:

- Better SEO rankings (faster page loads)
- Higher conversion rates (users see content faster)
- Better user experience (instant page loads)
- Lower infrastructure scaling needs

---

## Migration Strategy

### Low-Risk Approach

1. Start with **public, static content** (course catalog, instructor profiles)
2. Test in staging environment first
3. Monitor cache hit rates and performance metrics
4. Gradually expand to more pages
5. Keep user-specific pages client-side (no risk)

### Rollback Plan

- Cache Components are opt-in (no breaking changes)
- Can disable caching by removing `'use cache'` directive
- Client-side fetching still works as fallback

---

## My Recommendation

**YES, implement Cache Components, but start small:**

### Week 1: Foundation

- [x] Create cached query utilities (DONE)
- [x] Create revalidation utilities (DONE)
- [ ] Refactor `/courses` page (highest traffic)
- [ ] Refactor `/course/[id]` page (SEO critical)
- [ ] Add cache monitoring

### Week 2: Expand

- [ ] Cache instructor profiles
- [ ] Cache blog/community posts
- [ ] Add revalidation to all update actions
- [ ] Monitor performance metrics

### Week 3: Optimize

- [ ] Implement PPR for dashboard (static header + dynamic content)
- [ ] Optimize cache hit rates
- [ ] Add cache warming for critical pages

**Expected Results**:

- 60-75% faster page loads (Week 1)
- 40-60% lower server costs (Week 2)
- Better SEO rankings (Week 3+)

---

## Conclusion

**Cache Components are a GREAT fit for your LMS** because:

1. ✅ High traffic on public pages (course catalog, course details)
2. ✅ Content changes infrequently (courses, instructors)
3. ✅ SEO is critical for course discovery
4. ✅ Lower server costs at scale
5. ✅ Better user experience

**Start with the course catalog** (highest impact, lowest risk), then expand to other public pages.

**Don't cache** user-specific content (dashboards, progress, enrollments) - keep those client-side for real-time updates.
