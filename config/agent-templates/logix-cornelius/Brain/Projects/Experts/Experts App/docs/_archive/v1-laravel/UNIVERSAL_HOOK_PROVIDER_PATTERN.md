---
title: "Universal Hook & Provider Pattern"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/universal-hook-provider-pattern"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Universal Hook & Provider Pattern

This document defines the standard patterns for creating hooks and providers across the Experts platform, ensuring consistency and best practices.

## Table of Contents

1. [Universal Hook Pattern](#universal-hook-pattern)
2. [Universal Provider Pattern](#universal-provider-pattern)
3. [Best Practices](#best-practices)
4. [Examples](#examples)

---

## Universal Hook Pattern

### Basic Hook Structure

All data-fetching hooks should follow this pattern:

```typescript
"use client";

import { useApiQuery } from "./use-api-query";
import { YourRepository } from "@experts/models";
import type { YourType } from "@experts/models";
import { useSkeleton } from "@experts/providers";
import { useEffect } from "react";

export function useYourHook<T = YourType>() {
  const { setLoading } = useSkeleton("your-skeleton-key");

  const response = useApiQuery<YourType>(
    "your-cache-key",
    () => YourRepository.yourMethod(),
    undefined,
    { requireAuth: true }, // or false for public endpoints
  );

  useEffect(() => {
    setLoading(response.isLoading);
  }, [response.isLoading, setLoading]);

  return {
    data: response.data as T | undefined,
    raw: response,
    error: response.error,
    isLoading: response.isLoading,
    mutate: response.mutate,
  };
}
```

### Hook Naming Conventions

- **Prefix with `use`**: All hooks must start with `use`
- **Descriptive names**: `useProfile`, `useCourses`, `useOrganization`
- **Singular vs Plural**:
  - Singular for single item: `useProfile`, `useOrganization`
  - Plural for collections: `useCourses`, `useUsers`

### Cache Key Conventions

```typescript
// ✅ Good - Static, descriptive keys
"user-profile";
"current-plan";
"courses-list";
"organization-details";

// ❌ Bad - Dynamic or unclear keys
isAuthenticated ? "profile" : "public"`user-${id}`; // Use array format instead
("data");
```

For parameterized queries, use array format:

```typescript
const response = useApiQuery<Course>(
  ["course-details", courseId],
  () => CourseRepository.getCourse(courseId),
  undefined,
  { requireAuth: true },
);
```

### Authentication Options

```typescript
// For authenticated-only endpoints
{
  requireAuth: true;
}

// For public endpoints (accessible without auth)
{
  requireAuth: false;
}

// Default is false if not specified
```

### Key Rules

1. ✅ **DO** use `useApiQuery` for all data fetching
2. ✅ **DO** set `requireAuth` explicitly
3. ✅ **DO** integrate with skeleton provider
4. ✅ **DO** use static cache keys when possible
5. ❌ **DON'T** call `useSession()` directly in hooks
6. ❌ **DON'T** manually check authentication status
7. ❌ **DON'T** use dynamic cache keys based on auth state

---

## Universal Provider Pattern

### Basic Provider Structure

All context providers should follow this pattern:

```typescript
"use client";

import React, {createContext, useContext, useEffect, useMemo} from "react";
import type {YourType} from "@experts/types";
import {useSkeleton} from "./skeleton-provider";
import {useApiQuery} from "@experts/hooks";
import {YourService} from "@experts/sdk";

interface YourContextType {
  yourData: YourType | null;
  isLoading: boolean;
  error: Error | null;
}

const YourContext = createContext<YourContextType | undefined>(undefined);

export const useYourContext = (): YourContextType => {
  const context = useContext(YourContext);
  if (context === undefined) {
    throw new Error("useYourContext must be used within a YourProvider");
  }
  return context;
};

export const YourProvider = ({children}: {children: React.ReactNode}): React.ReactNode => {
  const {setLoading} = useSkeleton("your-skeleton-key");

  const response = useApiQuery(
    "your-cache-key",
    () => YourService.yourMethod(),
    undefined,
    {requireAuth: true},
  );

  useEffect(() => {
    setLoading(response.isLoading);
  }, [response.isLoading, setLoading]);

  const value = useMemo(
    () => ({
      yourData: response.data ?? null,
      isLoading: response.isLoading,
      error: response.error ?? null,
    }),
    [response.data, response.isLoading, response.error],
  );

  return <YourContext.Provider value={value}>{children}</YourContext.Provider>;
};
```

### Provider Naming Conventions

- **Suffix with `Provider`**: `CurrentPlanProvider`, `OrganizationProvider`
- **Export hook with `use` prefix**: `useCurrentPlan`, `useOrganization`
- **Context name with `Context` suffix**: `CurrentPlanContext`

### Key Rules

1. ✅ **DO** create a custom hook for consuming context
2. ✅ **DO** throw error if hook used outside provider
3. ✅ **DO** use `useMemo` for context value
4. ✅ **DO** integrate with skeleton provider
5. ✅ **DO** use `useApiQuery` for data fetching
6. ❌ **DON'T** call `useSession()` in providers
7. ❌ **DON'T** manually manage authentication state
8. ❌ **DON'T** use dynamic cache keys based on auth

---

## Best Practices

### 1. Skeleton Integration

Always integrate with the skeleton provider for consistent loading states:

```typescript
const { setLoading } = useSkeleton("your-unique-key");

useEffect(() => {
  setLoading(response.isLoading);
}, [response.isLoading, setLoading]);
```

### 2. Error Handling

Return errors from hooks and providers:

```typescript
return {
  data: response.data,
  error: response.error,
  isLoading: response.isLoading,
};
```

### 3. Type Safety

Use generics for flexible typing:

```typescript
export function useYourHook<T = DefaultType>() {
  // ...
  return {
    data: response.data as T | undefined,
    // ...
  };
}
```

### 4. Mutation Support

Always expose the `mutate` function for manual refetching:

```typescript
return {
  data: response.data,
  mutate: response.mutate, // For manual cache updates
};
```

### 5. Avoid Re-renders

Use `useMemo` in providers to prevent unnecessary re-renders:

```typescript
const value = useMemo(
  () => ({
    yourData: response.data ?? null,
    isLoading: response.isLoading,
  }),
  [response.data, response.isLoading],
);
```

---

## Examples

### Example 1: Simple Data Hook

```typescript
"use client";

import { useApiQuery } from "./use-api-query";
import { UserRepository } from "@experts/models";
import type { User } from "@experts/models";
import { useSkeleton } from "@experts/providers";
import { useEffect } from "react";

export function useProfile<T = User>() {
  const { setLoading } = useSkeleton("user-profile");

  const response = useApiQuery<User>(
    "user-profile",
    () => UserRepository.getProfile(),
    undefined,
    { requireAuth: true },
  );

  useEffect(() => {
    setLoading(response.isLoading);
  }, [response.isLoading, setLoading]);

  return {
    data: response.data as T | undefined,
    raw: response,
    error: response.error,
    isLoading: response.isLoading,
    mutate: response.mutate,
  };
}
```

### Example 2: Parameterized Hook

```typescript
"use client";

import { useApiQuery } from "./use-api-query";
import { CourseRepository } from "@experts/models";
import type { Course } from "@experts/models";
import { useSkeleton } from "@experts/providers";
import { useEffect } from "react";

export function useCourse(courseId: string) {
  const { setLoading } = useSkeleton("course-details");

  const response = useApiQuery<Course>(
    ["course-details", courseId],
    () => CourseRepository.getCourse(courseId),
    undefined,
    { requireAuth: true },
  );

  useEffect(() => {
    setLoading(response.isLoading);
  }, [response.isLoading, setLoading]);

  return {
    data: response.data,
    error: response.error,
    isLoading: response.isLoading,
    mutate: response.mutate,
  };
}
```

### Example 3: Public Endpoint Hook

```typescript
"use client";

import { useApiQuery } from "./use-api-query";
import { CourseRepository } from "@experts/models";
import type { Course } from "@experts/models";
import { useSkeleton } from "@experts/providers";
import { useEffect } from "react";

export function usePublicCourses() {
  const { setLoading } = useSkeleton("public-courses");

  const response = useApiQuery<Course[]>(
    "public-courses-list",
    () => CourseRepository.getPublicCourses(),
    undefined,
    { requireAuth: false }, // Public endpoint
  );

  useEffect(() => {
    setLoading(response.isLoading);
  }, [response.isLoading, setLoading]);

  return {
    data: response.data ?? [],
    error: response.error,
    isLoading: response.isLoading,
    mutate: response.mutate,
  };
}
```

### Example 4: Provider with Context

```typescript
"use client";

import React, {createContext, useContext, useEffect, useMemo} from "react";
import type {Plan} from "@experts/types";
import {useSkeleton} from "./skeleton-provider";
import {useApiQuery} from "@experts/hooks";
import {PlansService} from "@experts/sdk";

interface CurrentPlanContextType {
  currentPlan: Plan | null;
  isLoading: boolean;
}

const CurrentPlanContext = createContext<CurrentPlanContextType | undefined>(undefined);

export const useCurrentPlan = (): CurrentPlanContextType => {
  const context = useContext(CurrentPlanContext);
  if (context === undefined) {
    throw new Error("useCurrentPlan must be used within a CurrentPlanProvider");
  }
  return context;
};

export const CurrentPlanProvider = ({children}: {children: React.ReactNode}): React.ReactNode => {
  const {setLoading} = useSkeleton("current-plan");

  const response = useApiQuery(
    "current-plan",
    () => PlansService.getCurrentUsersPlan(),
    undefined,
    {requireAuth: true},
  );

  useEffect(() => {
    setLoading(response.isLoading);
  }, [response.isLoading, setLoading]);

  const value = useMemo(
    () => ({
      currentPlan: response.data ?? null,
      isLoading: response.isLoading,
    }),
    [response.data, response.isLoading],
  );

  return <CurrentPlanContext.Provider value={value}>{children}</CurrentPlanContext.Provider>;
};
```

### Example 5: Hook with Filters

```typescript
"use client";

import { useApiQuery } from "./use-api-query";
import { CourseRepository } from "@experts/models";
import type { Course, CourseFilters } from "@experts/models";
import { useSkeleton } from "@experts/providers";
import { useEffect } from "react";

export function useCourses(filters?: CourseFilters) {
  const { setLoading } = useSkeleton("courses-list");

  const cacheKey = filters
    ? ["courses-list", JSON.stringify(filters)]
    : "courses-list";

  const response = useApiQuery<Course[]>(
    cacheKey,
    () => CourseRepository.getCourses(filters),
    undefined,
    { requireAuth: true },
  );

  useEffect(() => {
    setLoading(response.isLoading);
  }, [response.isLoading, setLoading]);

  return {
    data: response.data ?? [],
    error: response.error,
    isLoading: response.isLoading,
    mutate: response.mutate,
  };
}
```

---

## Migration Checklist

When updating existing hooks/providers to this pattern:

- [ ] Remove `useSession()` imports and calls
- [ ] Remove manual authentication checks
- [ ] Change dynamic cache keys to static keys
- [ ] Set `requireAuth` explicitly in `useApiQuery`
- [ ] Integrate with skeleton provider
- [ ] Use `useMemo` for context values (providers only)
- [ ] Add proper TypeScript types
- [ ] Export `mutate` function
- [ ] Test on page refresh (not just HMR)

---

## Common Pitfalls

### ❌ Don't Do This

```typescript
// Calling useSession directly
const { status } = useSession();
const isAuthenticated = status === "authenticated";

// Dynamic cache keys based on auth
const key = isAuthenticated ? "data" : "public";

// Dynamic requireAuth based on session
{
  requireAuth: isAuthenticated;
}

// Using useRef in auth logic
const isInitialized = useRef(false); // Won't trigger re-renders!
```

### ✅ Do This Instead

```typescript
// Let useApiQuery handle auth via useSDKAuth
const response = useApiQuery(
  "your-cache-key",
  () => YourRepository.yourMethod(),
  undefined,
  { requireAuth: true },
);

// Static cache keys
"user-profile"[("course-details", courseId)];

// Use useState for auth state that needs re-renders
const [isInitialized, setIsInitialized] = useState(false);
```

---

## Related Documentation

- [SDK Authentication Pattern](./UNIVERSAL_CLIENT_PATTERN.md)
- [Cursor Rules](./COURSE/CURSOR_RULES_UPDATED.md)
