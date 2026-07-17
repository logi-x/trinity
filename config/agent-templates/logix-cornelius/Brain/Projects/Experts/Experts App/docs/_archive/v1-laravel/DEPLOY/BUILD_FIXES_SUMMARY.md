---
title: "Build Fixes Summary - SDK Migration Complete"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/deploy"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Build Fixes Summary - SDK Migration Complete

**Date:** 2025-11-19
**Build Status:** ✅ SUCCESS

## 🎯 Build Errors Fixed

### Error: "Export OpenAPI doesn't exist in target module"

**Files Fixed (3 files):**

1. **`packages/hooks/src/use-api-mutation.ts`**
   - **Issue:** Importing and using `OpenAPI.TOKEN` which doesn't exist in new SDK
   - **Fix:** Removed `OpenAPI` import and `OpenAPI.TOKEN` check
   - **Change:**

     ```typescript
     // Before:
     import { OpenAPI } from "@experts/sdk";
     const tokenReady =
       isAuthenticated && !!session?.user?.accessToken && !!OpenAPI.TOKEN;

     // After:
     const tokenReady = isAuthenticated && !!session?.user?.accessToken;
     ```

2. **`apps/experts-app/src/app/(console)/console/categories/hooks/use-api-mutation.ts`**
   - **Issue:** Same as above - using `OpenAPI.TOKEN`
   - **Fix:** Removed `OpenAPI` import and check
   - **Change:** Same pattern as file #1

3. **`apps/experts-app/src/app/(console)/console/categories/hooks/use-api-query.ts`**
   - **Issue:** Same as above - using `OpenAPI.TOKEN`
   - **Fix:** Removed `OpenAPI` import and check
   - **Change:** Same pattern as file #1

## 📋 Why These Fixes Work

### Old SDK Pattern (openapi-typescript-codegen)

The old SDK exposed an `OpenAPI` configuration object:

```typescript
import { OpenAPI } from "@experts/sdk";

// Setting token globally
OpenAPI.TOKEN = "my-token";

// Checking if token was set
if (OpenAPI.TOKEN) {
  /* ... */
}
```

### New SDK Pattern (@hey-api/openapi-ts)

The new SDK uses a different approach with our custom config module:

```typescript
import { configureSdk, setAuthToken } from "@experts/sdk/config";

// Setting token via configureSdk (persistent)
configureSdk(undefined, async () => session?.user?.accessToken);

// Setting token via setAuthToken (one-time)
setAuthToken(token);

// Checking token: Just check the session directly
if (session?.user?.accessToken) {
  /* ... */
}
```

**Why we don't need `OpenAPI.TOKEN` anymore:**

- The new SDK handles token management internally through our `config.ts` module
- Token is automatically injected via the `configureSdk()` function in `use-sdk-auth.ts`
- We only need to verify the session has a token, not check the SDK's internal state
- This is cleaner and follows the React/NextAuth pattern better

## 🔧 Technical Details

### Token Flow in New Architecture

1. **User logs in** → NextAuth creates session with `accessToken`
2. **`use-sdk-auth.ts` hook** → Calls `configureSdk()` with token resolver
3. **Token resolver** → Returns `session?.user?.accessToken`
4. **SDK config** → Caches token for 1 minute, auto-refreshes
5. **API calls** → Automatically include cached token in Authorization header

### What Changed in Hooks

**Before (Old Pattern):**

```typescript
// Had to check both session AND OpenAPI.TOKEN
const tokenReady =
  isAuthenticated && !!session?.user?.accessToken && !!OpenAPI.TOKEN;
```

**After (New Pattern):**

```typescript
// Only check session token (SDK handles the rest)
const tokenReady = isAuthenticated && !!session?.user?.accessToken;
```

This simplification is possible because:

- `configureSdk()` is called globally in `use-sdk-auth.ts`
- Token is automatically managed by our config module
- We don't need to manually set/check `OpenAPI.TOKEN`

## ✅ Verification Steps Performed

1. ✅ Removed all `OpenAPI` imports from `@experts/sdk`
2. ✅ Updated all `OpenAPI.TOKEN` checks to use session token
3. ✅ Verified no remaining `Service` class imports
4. ✅ Ran full production build successfully
5. ✅ Confirmed all 123 routes compiled without errors

## 📊 Build Results

```
✓ Compiled successfully in 44s
✓ Generating static pages using 23 workers (123/123) in 3.4s

Total Routes: 123
Build Time: ~47 seconds
Status: SUCCESS ✅
```

## 🎉 Final Status

**Migration Complete!** All build errors have been resolved.

### Summary of All Changes Made

**Total Files Updated:** 21 files

- 4 SDK core files (created/updated)
- 8 repository files
- 3 auth/validation files
- 3 app-specific files
- 3 hook files (build fixes)

**Zero Errors:** No TypeScript errors, no build errors, no import errors

**Ready for:** Testing and deployment

## 🚀 Next Steps

1. **Test the application** in development mode
2. **Verify authentication flows** (login, logout, token refresh)
3. **Test API calls** through the UI
4. **Monitor console** for any runtime warnings
5. **Deploy to staging** for integration testing

---

**Build Fixed By:** Claude Code
**Completion Time:** 2025-11-19
**Build Status:** ✅ PASSING
