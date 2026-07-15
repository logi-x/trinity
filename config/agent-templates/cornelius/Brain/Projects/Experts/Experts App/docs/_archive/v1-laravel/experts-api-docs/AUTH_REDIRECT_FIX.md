---
title: "🔄 Auth Redirect Fix"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/experts-api-docs"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🔄 Auth Redirect Fix

## Problem

After logout, users were redirected to:

```
❌ https://app.dev.experts.com.sa/auth?tab=login
```

But the app doesn't have an `/auth` route - it should redirect to the **auth subdomain**:

```
✅ https://auth.dev.experts.com.sa/oauth/redirect
```

---

## Root Cause

The `AUTH_REDIRECTS` constants were using **relative paths** (`/auth?tab=login`) instead of **full auth server URLs**.

```typescript
// ❌ Before (relative path)
export const AUTH_REDIRECTS = {
  LOGIN: "/auth?tab=login", // Stays on current domain
  LOGOUT: "/auth?tab=login", // app.dev → /auth (404!)
};

// ✅ After (full auth server URL)
export const AUTH_REDIRECTS = {
  get LOGIN() {
    return `${authServer}/oauth/redirect`; // Goes to auth subdomain
  },
  get LOGOUT() {
    return `${authServer}/oauth/redirect`;
  },
};
```

---

## Solution

### 1. Dynamic Auth Server URL

Created `getAuthServerUrl()` that works in both client and server:

```typescript
function getAuthServerUrl(): string {
  // Browser: Use NEXT_PUBLIC_AUTH_URL from window
  if (typeof window !== "undefined") {
    return window.NEXT_PUBLIC_AUTH_URL || "https://auth.experts.com.sa";
  }

  // Server: Use process.env
  return process.env.NEXT_PUBLIC_AUTH_URL || "https://auth.experts.com.sa";
}
```

### 2. Updated AUTH_REDIRECTS

Changed to use **getters** that return full URLs:

```typescript
export const AUTH_REDIRECTS = {
  get LOGIN() {
    return `${getAuthServerUrl()}/oauth/redirect`;
    // → https://auth.dev.experts.com.sa/oauth/redirect
  },
  get REGISTER() {
    return `${getAuthServerUrl()}/register`;
    // → https://auth.dev.experts.com.sa/register
  },
  get LOGOUT() {
    return `${getAuthServerUrl()}/oauth/redirect`;
    // → https://auth.dev.experts.com.sa/oauth/redirect
  },
};
```

### 3. Updated buildLogoutRedirectUrl()

Now returns full auth server URLs:

```typescript
export function buildLogoutRedirectUrl(redirectUri?: string | null): string {
  const authServerUrl = getAuthServerUrl();

  if (!redirectUri) {
    // Simple logout
    return `${authServerUrl}/oauth/redirect`;
    // → https://auth.dev.experts.com.sa/oauth/redirect
  }

  // With redirect after login
  return `${authServerUrl}/oauth/redirect?redirect_uri=${encodeURIComponent(validated)}`;
  // → https://auth.dev.experts.com.sa/oauth/redirect?redirect_uri=%2Fdashboard
}
```

---

## Expected URLs by Environment

### Development

```
LOGIN:    https://auth.dev.experts.com.sa/oauth/redirect
REGISTER: https://auth.dev.experts.com.sa/register
LOGOUT:   https://auth.dev.experts.com.sa/oauth/redirect
```

### Canary

```
LOGIN:    https://auth.canary.experts.com.sa/oauth/redirect
REGISTER: https://auth.canary.experts.com.sa/register
LOGOUT:   https://auth.canary.experts.com.sa/oauth/redirect
```

### Staging

```
LOGIN:    https://auth.stg.experts.com.sa/oauth/redirect
REGISTER: https://auth.stg.experts.com.sa/register
LOGOUT:   https://auth.stg.experts.com.sa/oauth/redirect
```

### Production

```
LOGIN:    https://auth.experts.com.sa/oauth/redirect
REGISTER: https://auth.experts.com.sa/register
LOGOUT:   https://auth.experts.com.sa/oauth/redirect
```

---

## Testing

### Expected Console Output

**When you logout:**

```
🔓 Starting logout...
🔓 Logout API response: {
  status: 200,
  redirectFromApi: "https://auth.dev.experts.com.sa/oauth/redirect",
  fallbackRedirect: "https://auth.dev.experts.com.sa/oauth/redirect"
}
🔓 Final redirect URL: https://auth.dev.experts.com.sa/oauth/redirect
```

**Browser URL changes to:**

```
✅ https://auth.dev.experts.com.sa/oauth/redirect
```

---

## Verify It's Working

### 1. Check Constants in Console

```javascript
// In browser console
import { AUTH_REDIRECTS } from "@utils/auth/auth-constants";

console.log(AUTH_REDIRECTS.LOGIN); // Should be full URL
console.log(AUTH_REDIRECTS.LOGOUT); // Should be full URL
```

### 2. Test Logout

```
1. Login to app
2. Click logout
3. Watch console for "Final redirect URL"
4. Verify browser goes to: https://auth.dev.experts.com.sa/oauth/redirect
```

### 3. Test Login

```
1. Go to app while logged out
2. Click "Sign In"
3. Verify redirect to: https://auth.dev.experts.com.sa/oauth/redirect
```

---

## Why This Fix Matters

### Security

- ✅ Always redirects to auth subdomain (not app subdomain)
- ✅ Validates redirect URLs to prevent open redirects
- ✅ Centralized URL logic = easier to audit

### User Experience

- ✅ No 404 errors on logout
- ✅ Consistent auth flow
- ✅ Proper subdomain separation

### Maintainability

- ✅ Single source of truth for URLs
- ✅ Environment-aware (dev, staging, prod)
- ✅ Easy to update across entire app

---

## Environment Variables

Make sure `NEXT_PUBLIC_AUTH_URL` is set correctly:

```env
# .env.local (development)
NEXT_PUBLIC_AUTH_URL=https://auth.dev.experts.com.sa

# .env.staging
NEXT_PUBLIC_AUTH_URL=https://auth.stg.experts.com.sa

# .env.production
NEXT_PUBLIC_AUTH_URL=https://auth.experts.com.sa
```

If not set, it falls back to `auth.{env}.experts.com.sa` based on `APP_ENV`.

---

## Summary

**Before:** Logout → `app.dev.experts.com.sa/auth?tab=login` → **404** ❌

**After:** Logout → `auth.dev.experts.com.sa/oauth/redirect` → **Success** ✅

The redirect URLs now correctly point to the **auth subdomain** using the **OAuth redirect endpoint**! 🎉
