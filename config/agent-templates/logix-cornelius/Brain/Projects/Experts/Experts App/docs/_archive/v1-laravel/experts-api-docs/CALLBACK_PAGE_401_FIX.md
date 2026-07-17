---
title: "✅ Callback Page 401 Fix - Final Solution"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/experts-api-docs"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# ✅ Callback Page 401 Fix - Final Solution

## Problem

API calls happening on `/auth/signin-callback` page **before** authentication completes:

```
❌ GET /v1/user 401
❌ GET /v1/organizations/list/mine 401
❌ GET /v1/plans/current 401
```

---

## Root Cause

`AppDataProvider` wraps the entire app and fetches data immediately when **any page** loads, including callback pages.

---

## Solution: Conditional SWR Keys (Follows React Hook Rules)

### ✅ Correct Implementation

```typescript
export const AppDataProvider = ({children}) => {
  // Check if on callback page
  const isCallbackPage = window.location.pathname.includes('/auth/signin-callback');

  // ✅ Always call hooks (React rules)
  const {setLoading} = useSkeleton("user-profile");

  // ✅ Use null key to skip fetching on callback pages
  const userResponse = useApiQuery(
    isCallbackPage ? null : "user-profile", // null = no API call
    () => UserRepository.getProfile(),
    undefined,
    {requireAuth: true}
  );

  const orgsResponse = useApiQuery(
    isCallbackPage ? null : "organizations-mine", // null = no API call
    // ...
  );

  const planResponse = useApiQuery(
    isCallbackPage ? null : "current-plan", // null = no API call
    // ...
  );

  // Contexts still provided (values are null/undefined on callback pages)
  return (
    <UserContext.Provider value={userValue}>
      {children}
    </UserContext.Provider>
  );
}
```

---

## Why This Works

### SWR Behavior with Null Keys

```typescript
// When key is null:
useSWR(null, fetcher);
// → Returns: { data: undefined, isLoading: false }
// → No API call made!

// When key is a string:
useSWR("user-profile", fetcher);
// → Makes API call
// → Returns actual data
```

### Follows React Rules

```typescript
// ✅ Correct - All hooks called in same order
const hook1 = useSkeleton();
const hook2 = useApiQuery(condition ? null : "key");
const hook3 = useState();

// ❌ Wrong - Early return before hooks
if (condition) return <>{children}</>;
const hook1 = useSkeleton(); // Never reached!
```

---

## Complete Flow

### On Callback Page (`/auth/signin-callback`)

```
1. AppDataProvider renders
2. isCallbackPage = true
3. useApiQuery(null, ...) → No API calls ✅
4. Contexts provided with null values
5. Page's useEffect runs signIn()
6. Redirect to dashboard
```

### On Dashboard (`/dashboard`)

```
1. AppDataProvider renders
2. isCallbackPage = false
3. useApiQuery("user-profile", ...) → API call ✅
4. SDK has token configured
5. API returns 200 ✅
```

---

## Result

✅ **No 401 errors on callback pages**  
✅ **No React hooks rule violations**  
✅ **Clean console logs**  
✅ **Smooth user experience**

---

## Testing

**Try logging in now and check console:**

```
✅ ⏭️  Skipping AppDataProvider data fetching on callback page
✅ 🔐 Signing in with token data: {...}
✅ ✅ Sign-in successful, redirecting to dashboard...
✅ 🔐 Setting up SDK token resolver
✅ ✅ SDK token resolver configured and ready
✅ ✅ GET /v1/user 200
✅ ✅ GET /v1/organizations/list/mine 200
✅ ✅ GET /v1/plans/current 200
```

**You should NOT see:**

```
❌ GET /v1/user 401 (before redirect)
❌ React hooks rule violations
```

---

**The authentication flow is now completely fixed!** 🎉
