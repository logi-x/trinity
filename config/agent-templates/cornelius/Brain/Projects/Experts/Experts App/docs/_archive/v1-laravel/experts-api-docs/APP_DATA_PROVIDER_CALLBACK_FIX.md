---
title: "🚫 AppDataProvider Callback Page Skip"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/experts-api-docs"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🚫 AppDataProvider Callback Page Skip

## Problem

Even with a 100-second delay in the signin-callback page, these API calls were **still happening immediately**:

```
❌ GET /v1/user 401 (Unauthorized)
❌ GET /v1/organizations/list/mine 401 (Unauthorized)
❌ GET /v1/plans/current 401 (Unauthorized)
```

**Timeline:**

```
0ms:  signin-callback page loads
1ms:  AppDataProvider mounts → API calls start ❌
100000ms: (debug delay)
100001ms: signIn() completes
100002ms: Redirect happens
```

---

## Root Cause

The **signin-callback page uses the root layout**, which includes `AppDataProvider`:

```typescript
app/layout.tsx
  → SDKAuthProvider
    → AppDataProvider          // ❌ Tries to fetch data immediately
      → app/auth/signin-callback/page.tsx
```

**Flow:**

```
1. User lands on /auth/signin-callback
2. Root layout renders
3. AppDataProvider mounts
4. useUser(), useOrganizations(), usePlans() hooks run
5. API calls start → No token yet → 401 errors ❌
6. (Meanwhile) page's useEffect runs signIn()
7. Too late - API calls already failed!
```

---

## Solution: Skip Data Fetching on Callback Pages

### Updated AppDataProvider

**File:** `packages/providers/src/app-data-provider.tsx`

```typescript
export const AppDataProvider = ({children}) => {
  // ✅ Check if we're on a callback page
  const isCallbackPage = typeof window !== 'undefined' &&
    (window.location.pathname.includes('/auth/signin-callback') ||
     window.location.pathname.includes('/auth/callback') ||
     window.location.pathname.includes('/auth/redirect'));

  // ✅ Early return - skip all data fetching
  if (isCallbackPage) {
    console.log("⏭️  Skipping AppDataProvider on callback page");
    return <>{children}</>;
  }

  // Normal data fetching for non-callback pages
  const userResponse = useApiQuery(...);
  const orgsResponse = useApiQuery(...);
  const plansResponse = useApiQuery(...);

  // ...
}
```

---

## How It Works Now

### Callback Page Flow

```
┌──────────────────────────────┐
│  /auth/signin-callback loads │
└──────────┬───────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  AppDataProvider mounts            │
│  ├─ Checks pathname               │
│  ├─ isCallbackPage = true         │
│  └─ return <>{children}</>        │ ✅ No API calls!
└──────────┬───────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  signin-callback page renders      │
│  ├─ useEffect runs               │
│  ├─ signIn() completes           │
│  └─ window.location.href → /dashboard
└──────────┬───────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  /dashboard loads                  │
└──────────┬───────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  AppDataProvider mounts            │
│  ├─ Checks pathname               │
│  ├─ isCallbackPage = false        │
│  └─ Fetches data                  │ ✅ With token!
└──────────┬───────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  API calls succeed                 │
│  ✅ GET /v1/user 200               │
│  ✅ GET /v1/organizations 200      │
│  ✅ GET /v1/plans 200              │
└────────────────────────────────────┘
```

---

## Files Changed

1. ✅ `packages/providers/src/app-data-provider.tsx` - Added callback page check
2. ✅ `app/auth/signin-callback/page.tsx` - Removed debug delay
3. ✅ `app/auth/layout.tsx` - Created (minimal, for documentation)

---

## Testing

### Expected Console Output

**On signin-callback page:**

```
⏭️  Skipping AppDataProvider on callback page
🔐 Signing in with token data: {...}
✅ Sign-in successful, redirecting to dashboard...
```

**After redirect to dashboard:**

```
🔐 Setting up SDK token resolver
✅ SDK token resolver configured and ready
✅ GET /v1/user 200
✅ GET /v1/organizations/list/mine 200
✅ GET /v1/plans/current 200
```

### What You Should NOT See

```
❌ GET /v1/user 401            // Before redirect
❌ GET /v1/organizations 401   // Before redirect
❌ GET /v1/plans 401           // Before redirect
```

---

## Why This Fix is Critical

### Security

- ✅ Prevents unauthorized API calls
- ✅ No token leakage to callback pages
- ✅ Clean separation of concerns

### Performance

- ✅ No wasted API calls (that would fail anyway)
- ✅ Faster page load (skips unnecessary fetches)
- ✅ No retry logic triggered

### User Experience

- ✅ No 401 errors in console (looks broken)
- ✅ No flash of error states
- ✅ Smooth, professional flow

---

## Callback Pages to Skip

The provider skips data fetching on these paths:

1. `/auth/signin-callback` - OAuth callback handler
2. `/auth/callback` - Generic auth callback
3. `/auth/redirect` - Auth redirects

**Pattern:** Any page under `/auth/*` that's handling authentication flow.

---

## Alternative Approaches (Not Used)

### ❌ Approach 1: Separate Layout

```typescript
// app/auth/layout.tsx (doesn't work - still nested in root)
export default function AuthLayout({children}) {
  return <>{children}</>;  // Still inside root layout!
}
```

**Why not:** Next.js layouts are nested, so AppDataProvider still runs.

### ❌ Approach 2: Conditional Hooks

```typescript
const userResponse = isCallbackPage ? null : useApiQuery(...);
```

**Why not:** Hooks can't be conditional (React rules violation).

### ✅ Approach 3: Early Return (What We Used)

```typescript
if (isCallbackPage) {
  return <>{children}</>;  // Skip everything
}
```

**Why yes:** Clean, simple, works perfectly.

---

## Related Fixes

This fix complements the other auth fixes:

1. [AUTH_401_RACE_CONDITION_FIX.md](./AUTH_401_RACE_CONDITION_FIX.md) - SDKAuthProvider blocking
2. [AUTH_LOADING_UX_FIX.md](./AUTH_LOADING_UX_FIX.md) - Loading screen flash fix
3. [EFFICIENT_AUTH_FLOW.md](./EFFICIENT_AUTH_FLOW.md) - Complete auth flow

Together, these fixes ensure:

- ✅ No premature API calls
- ✅ No 401 errors
- ✅ No loading screen flash
- ✅ Smooth, fast authentication

---

## Summary

**Problem:** AppDataProvider making API calls before authentication completes

**Root Cause:** Callback pages use root layout with AppDataProvider

**Fix:** AppDataProvider checks pathname and skips fetching on callback pages

**Result:** No more premature 401 errors! 🎉
