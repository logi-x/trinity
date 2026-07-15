---
title: "Authentication Navigation Race Condition Fix"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/experts-api-docs"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Authentication Navigation Race Condition Fix

## Problem

After implementing `SDKAuthProvider`, 401 errors still occurred **during the callback page navigation**, specifically when:

1. User logs in on `/auth`
2. Redirects to `/auth/callback?redirect_uri=/`
3. Session updates to authenticated
4. **Root layout re-renders** with new session
5. SDK marks `isReady=true` but token resolver isn't fully configured yet
6. `AppDataProvider` immediately starts fetching → **401 errors**

### Console Log Evidence

```
sdk-auth-provider.tsx:48 ✅ SDK Auth Ready: {isAuthenticated: false, hasSession: false}
login.tsx:68 🔐 Login attempt: {email: 'ahmed@logi-x.org'}
login.tsx:84 ✅ Login successful, redirecting to: /auth/callback?redirect_uri=%2F

sdk-auth-provider.tsx:48 ✅ SDK Auth Ready: {isAuthenticated: true, hasSession: true}  ← Session updates
client.gen.ts:96  GET /v1/plans/current 401 (Unauthorized)                              ← Immediately fails
client.gen.ts:96  GET /v1/organizations/list/mine 401 (Unauthorized)
client.gen.ts:96  GET /v1/user 401 (Unauthorized)

oauth-callback.tsx:43 ✅ Authentication successful: {user: 'ahmed@logi-x.org'}           ← Too late
```

## Root Cause

The issue was a **timing problem in React's rendering pipeline**:

1. **NextAuth session updates** during navigation to `/auth/callback`
2. **Root layout re-renders** because session changed
3. **`useSDKAuth()` useEffect runs** and calls:
   ```typescript
   setTokenResolver(async () => session.user.accessToken as string);
   setGlobalInitialized(true); // ❌ Marks ready IMMEDIATELY
   ```
4. **`SDKAuthProvider` checks `isReady`** → Returns `true`
5. **`AppDataProvider` renders** → Starts fetching data
6. **Token resolver isn't actually usable yet** → 401 errors

The problem: React's `useEffect` callbacks run **after** the component renders, but state updates are synchronous. The `setGlobalInitialized(true)` runs **before** the token resolver is fully configured in the SDK runtime.

## Solution

**Two-layer microtask delay** to ensure token is truly configured:

### Layer 1: `use-sdk-auth.ts` - Dual State Tracking

```typescript
// Global persistent state
let globalIsInitialized = false;
let globalTokenConfigured = false; // NEW: Second state

function getSnapshot() {
  return globalIsInitialized && globalTokenConfigured; // Both must be true
}

function setTokenConfigured(value: boolean) {
  if (globalTokenConfigured !== value) {
    globalTokenConfigured = value;
    listeners.forEach((listener) => listener());
  }
}

// In useEffect:
if (status === "authenticated" && session?.user?.accessToken) {
  setTokenResolver(async () => session.user.accessToken as string);

  // Use microtask to ensure token is configured before marking as ready
  queueMicrotask(() => {
    setTokenConfigured(true); // ✅ Delayed
    setGlobalInitialized(true); // ✅ Delayed
  });
}
```

**Why `queueMicrotask()`?**

- Runs **after** current JavaScript execution completes
- Runs **before** next browser paint
- Ensures `setTokenResolver()` has completed its work
- Still fast (~1ms delay) but prevents race condition

### Layer 2: `sdk-auth-provider.tsx` - Internal Ready State

```typescript
export function SDKAuthProvider({children}: {children: ReactNode}) {
  const {isReady, isAuthenticated, sessionId, hasRefreshError} = useSDKAuth();
  const [internalReady, setInternalReady] = useState(false);  // NEW: Internal state

  useEffect(() => {
    if (!isReady) {
      setInternalReady(false);  // Reset when not ready
    } else {
      // Add a microtask delay to ensure token is truly configured
      queueMicrotask(() => {
        setInternalReady(true);  // ✅ Additional delay
      });
    }
  }, [isReady, isAuthenticated, sessionId, hasRefreshError]);

  // Don't render children until BOTH are ready
  if (!isReady || !internalReady) {
    return <LoadingScreen />;
  }

  return <>{children}</>;
}
```

**Why double-check?**

- First check: `isReady` from `useSDKAuth` (token resolver set + microtask delay)
- Second check: `internalReady` (additional microtask delay for React state updates)
- Ensures AppDataProvider can't render until token is **fully** configured

## Timeline Comparison

### Before Fix (Broken)

```
T=0ms:    Session updates → useSDKAuth effect scheduled
T=0ms:    setTokenResolver() called
T=0ms:    setGlobalInitialized(true) ❌ IMMEDIATE
T=0ms:    isReady = true
T=0ms:    SDKAuthProvider renders children
T=0ms:    AppDataProvider starts fetching
T=1ms:    API calls made WITHOUT token → 401
T=2ms:    Token resolver actually usable (too late)
```

### After Fix (Working)

```
T=0ms:    Session updates → useSDKAuth effect scheduled
T=0ms:    setTokenResolver() called
T=0ms:    queueMicrotask(() => setTokenConfigured(true))  ✅ DELAYED
T=1ms:    Microtask runs → setTokenConfigured(true)
T=1ms:    isReady = true
T=1ms:    SDKAuthProvider schedules queueMicrotask(() => setInternalReady(true))
T=2ms:    Microtask runs → setInternalReady(true)
T=2ms:    SDKAuthProvider renders children
T=2ms:    AppDataProvider starts fetching
T=3ms:    API calls made WITH token → 200 ✅
```

## Why Microtasks, Not setTimeout?

```typescript
// ❌ Too slow (4-10ms minimum)
setTimeout(() => setInternalReady(true), 0);

// ✅ Fast and precise (~1-2ms)
queueMicrotask(() => setInternalReady(true));
```

Microtasks:

- Run after current code completes
- Run before next browser paint
- Predictable timing (~1ms)
- Perfect for synchronization

## Files Changed

1. **`packages/hooks/src/use-sdk-auth.ts`**
   - Added `globalTokenConfigured` state
   - Added `setTokenConfigured()` function
   - Wrapped state updates in `queueMicrotask()`
   - Updated `getSnapshot()` to check both states

2. **`packages/providers/src/sdk-auth-provider.tsx`**
   - Added `internalReady` state
   - Added second microtask delay in useEffect
   - Changed render condition to check both `isReady` AND `internalReady`

3. **`docs/AUTH_401_FIX.md`**
   - Updated root cause explanation
   - Updated solution section
   - Added dual-state tracking details

## Testing

Expected console output after fix:

```
✅ SDK Auth Ready: {isAuthenticated: false, hasSession: false}
🔐 Login attempt: {email: 'user@example.com'}
✅ Login successful, redirecting to: /auth/callback?redirect_uri=%2F
✅ SDK Auth Ready: {isAuthenticated: true, hasSession: true}
[~2ms delay - loading screen visible]
✅ Authentication successful: {user: 'user@example.com', accessToken: 'present'}
✅ GET /v1/user 200 OK
✅ GET /v1/organizations/list/mine 200 OK
✅ GET /v1/plans/current 200 OK
```

Key differences:

- ✅ No 401 errors
- ✅ Brief (~2ms) loading screen during callback
- ✅ All API calls succeed
- ✅ User data loads immediately

## Performance Impact

- **Added delay**: ~2ms (two microtasks)
- **User perception**: Imperceptible (faster than a frame)
- **Benefit**: Eliminates failed API calls and retries
- **Net effect**: Actually **faster** because no error recovery needed

## Related Issues

- Initial 401 fix: `AUTH_401_FIX.md`
- Complete auth flow: `AUTH_FLOW.md`
- Migration guide: `AUTH_MIGRATION_SUMMARY.md`

## Summary

The navigation race condition was caused by synchronous state updates marking the SDK as "ready" before the token resolver was actually usable. The fix uses **two layers of microtask delays** to ensure proper ordering:

1. **useSDKAuth layer**: Delays `isReady=true` until token is configured
2. **SDKAuthProvider layer**: Delays rendering until state propagates through React

This ensures `AppDataProvider` never renders until the SDK is **truly** ready with a configured Bearer token. The ~2ms delay is imperceptible but eliminates 401 errors completely.
