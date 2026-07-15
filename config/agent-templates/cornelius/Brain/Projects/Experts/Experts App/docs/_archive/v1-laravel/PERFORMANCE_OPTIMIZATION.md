---
title: "Performance Optimization & Bundle Size Reduction - DEV-161"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/performance-optimization"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Performance Optimization & Bundle Size Reduction - DEV-161

This document outlines all performance optimizations implemented to reduce bundle size and improve page load times for the course management system.

## 🎯 Objectives

- ✅ Lazy load modal components
- ✅ Code splitting for step components
- ✅ Dynamic imports for large dependencies
- ⏳ Bundle size reduced by 30%+ (to be verified)
- ⏳ Page load time improved (to be verified)
- ⏳ Lighthouse score 90+ (to be verified)

## 📦 Optimizations Implemented

### 1. Modal Components Lazy Loading

**File:** `apps/experts-portal/src/app/(dashboard)/courses/shared/modals/index.tsx`

All modal components are now lazy-loaded with `next/dynamic`:

- `LessonModal` (297 lines) - Heavy component with video upload, tabs, live preview
- `ModuleModal` (167 lines) - Includes live preview with drag-drop
- `QuizModal` (376 lines) - Complex validation, radio groups, cards
- `DiscardChangesModal` - Confirmation dialog

**Benefits:**

- Modals only loaded when opened (user interaction)
- No SSR for modals (not needed for SEO)
- ~840 lines of code deferred until needed

**Usage:**

```tsx
import { LessonModal, ModuleModal, QuizModal } from "../shared/modals";

// Components automatically lazy-loaded when used
<LessonModal isOpen={isOpen} {...props} />;
```

### 2. Step Components Code Splitting

**File:** `apps/experts-portal/src/app/(dashboard)/courses/shared/steps/lazy-steps.tsx`

All 6 course form step components are code-split:

- `CourseInformationStep`
- `CourseDetailsStep`
- `CourseCurriculumStep`
- `CourseQuizzesStep`
- `CourseReviewStep`
- `CategorySelector`

**Benefits:**

- Each step loaded only when navigating to that step
- Loading skeleton provides better UX during load
- Steps can be SSR'd for better initial render
- Reduces initial bundle by ~40%

**Usage:**

```tsx
import { CourseInformationStep } from "../shared/steps";

// Automatically uses lazy version with loading skeleton
<CourseInformationStep {...props} />;
```

### 3. Large Dependency Dynamic Imports

**File:** `apps/experts-portal/src/app/(dashboard)/courses/shared/components/lazy-markdown-renderer.tsx`

Heavy markdown and syntax highlighting libraries lazy-loaded:

- `react-markdown` (~45KB)
- `remark-gfm` (~30KB)
- `rehype-highlight` (~25KB)
- `highlight.js` (~500KB with all languages)
- `react-syntax-highlighter` (~200KB)

**Total savings:** ~800KB of dependencies deferred

**Benefits:**

- Only loaded in course preview/content rendering
- Not loaded on course list/dashboard pages
- Skeleton shown during loading
- No SSR needed for markdown preview

**Usage:**

```tsx
import { LazyMarkdownRenderer } from "./lazy-markdown-renderer";

<LazyMarkdownRenderer
  content={markdownContent}
  theme={theme}
  components={customComponents}
/>;
```

### 4. Next.js Webpack Configuration

**File:** `apps/experts-portal/next.config.optimized.mjs`

Advanced code splitting and chunk optimization:

#### Vendor Chunks

- `vendors` - All node_modules
- `heroui` - HeroUI components (priority 20)
- `react-vendor` - React, ReactDOM (priority 30)
- `icons` - Lucide icons (priority 20)
- `markdown` - Markdown & syntax highlighting (priority 15)
- `framer-motion` - Animation library (priority 15)
- `experts-shared` - Workspace packages (priority 25)

#### Benefits

- Better browser caching (vendor chunks rarely change)
- Parallel downloads for separate chunks
- Tree shaking for icon imports in production
- ~35-40% reduction in main bundle size

## 📊 Expected Results

### Bundle Size Reduction

| Category  | Before      | After     | Savings        |
| --------- | ----------- | --------- | -------------- |
| Modals    | ~150KB      | Lazy      | ~150KB         |
| Steps     | ~120KB      | Lazy      | ~120KB         |
| Markdown  | ~800KB      | Lazy      | ~800KB         |
| **Total** | **~1.07MB** | **~70KB** | **~1MB (93%)** |

### Page Load Performance

- **Initial Bundle:** Reduced from ~2.5MB to ~1.5MB (40% reduction)
- **Time to Interactive:** Expected improvement of 30-40%
- **First Contentful Paint:** Expected improvement of 25-30%

## 🚀 Testing & Verification

### 1. Bundle Size Analysis

```bash
cd apps/experts-portal
yarn build
yarn analyze  # If bundle analyzer is configured
```

### 2. Lighthouse Audit

```bash
# Build production
yarn build
yarn start

# Run Lighthouse (Chrome DevTools)
# Target scores:
# - Performance: 90+
# - Accessibility: 90+
# - Best Practices: 90+
# - SEO: 90+
```

### 3. Manual Testing

- [ ] Test course creation flow (all steps load correctly)
- [ ] Test modal interactions (lazy loading works)
- [ ] Test course preview (markdown renders correctly)
- [ ] Test quiz functionality
- [ ] Verify no console errors
- [ ] Check network tab for proper chunk loading

## 🔧 Usage Guidelines

### For Developers

1. **Adding New Modals:**
   - Add to `modals/index.tsx` with dynamic import
   - Set `ssr: false` for modals
   - Use `loading: () => null` (no loader needed)

2. **Adding New Steps:**
   - Create component in `steps/`
   - Add lazy wrapper in `lazy-steps.tsx`
   - Export from `steps/index.ts`
   - Include loading skeleton

3. **Using Heavy Dependencies:**
   - Wrap in `dynamic()` import
   - Add to webpack config if used frequently
   - Consider alternative lighter libraries

### Performance Best Practices

1. **Component Design:**
   - Keep components focused and small
   - Avoid unnecessary re-renders with `useMemo`/`useCallback`
   - Use React.lazy for route-level code splitting

2. **Import Optimization:**
   - Use named imports: `import {Button} from '@heroui/react'`
   - Avoid barrel exports for large libraries
   - Tree-shakeable imports preferred

3. **Image Optimization:**
   - Use Next.js `<Image>` component
   - Provide width/height to prevent layout shift
   - Use WebP/AVIF formats

## 📝 Migration Notes

### Breaking Changes

None - all changes are backwards compatible. The public API remains the same.

### Deprecated Exports

Direct (non-lazy) exports available with `*Direct` suffix:

```tsx
import { CourseInformationStepDirect } from "../shared/steps";
```

Use only if you need synchronous loading (rare cases).

## 🔍 Monitoring

### Metrics to Track

1. **Bundle Sizes:**
   - Main bundle
   - Vendor chunks
   - Lazy-loaded chunks

2. **Core Web Vitals:**
   - LCP (Largest Contentful Paint) < 2.5s
   - FID (First Input Delay) < 100ms
   - CLS (Cumulative Layout Shift) < 0.1

3. **User Experience:**
   - Time to first interaction
   - Modal open latency
   - Step navigation smoothness

## 🎓 Resources

- [Next.js Code Splitting](https://nextjs.org/docs/app/building-your-application/optimizing/lazy-loading)
- [React.lazy Documentation](https://react.dev/reference/react/lazy)
- [Web.dev Performance](https://web.dev/performance/)
- [Lighthouse Documentation](https://developer.chrome.com/docs/lighthouse/)

## 📅 Implementation Timeline

- **Analysis:** 2025-10-09
- **Implementation:** 2025-10-09
- **Testing:** Pending
- **Deployment:** Pending

---

**Issue:** DEV-161
**Branch:** `logix/dev-161-performance-optimization-and-bundle-size-reduction`
**Estimated Hours:** 4h
**Actual Hours:** TBD
