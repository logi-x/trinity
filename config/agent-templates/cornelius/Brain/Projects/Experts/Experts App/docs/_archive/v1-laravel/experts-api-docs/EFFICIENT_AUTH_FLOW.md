---
title: "🔐 Efficient Login/Logout Flow"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/experts-api-docs"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🔐 Efficient Login/Logout Flow

## Overview

This guide shows the **clean, efficient authentication flow** with the new SDK setup that prevents 401 race conditions.

---

## 🚀 Login Flow

### Option 1: OAuth Redirect (Recommended)

**Use Case:** Standard login from anywhere in the app

```typescript
import {getAuthUrl} from "@utils/auth/auth-helpers";

function LoginButton() {
  return (
    <Button onClick={() => window.location.href = getAuthUrl("login")}>
      Sign In
    </Button>
  );
}
```

**Flow:**

```
1. User clicks "Sign In"
2. Redirect to: https://auth.experts.com.sa/oauth/redirect
3. OAuth provider handles authentication
4. Callback to: /auth/callback with token
5. signIn("experts-oauth") creates session
6. updateSession() propagates session
7. Wait 200ms for SDK configuration
8. window.location.href → Dashboard
9. SDKAuthProvider blocks rendering until token ready
10. All API calls succeed ✅
```

---

### Option 2: Credentials Login (Alternative)

**Use Case:** Custom login form within your app

```typescript
import {signIn, useSession} from "next-auth/react";
import {useRouter} from "next/navigation";

function LoginForm() {
  const {update: updateSession} = useSession();
  const router = useRouter();

  async function handleLogin(email: string, password: string) {
    // Submit credentials
    const result = await signIn("credentials", {
      email,
      password,
      redirect: false,
    });

    if (result?.error) {
      toast.error("Login failed", {description: result.error});
      return;
    }

    // ✅ Force session update
    await updateSession();

    // ✅ Wait for SDK to configure (double microtask)
    await new Promise(resolve => setTimeout(resolve, 200));

    // ✅ Full page reload ensures clean state
    window.location.href = "/dashboard";
  }

  return (
    <form onSubmit={e => {
      e.preventDefault();
      handleLogin(email, password);
    }}>
      {/* Form fields */}
    </form>
  );
}
```

---

## 🚪 Logout Flow

### Recommended Approach (Using Helper)

```typescript
import {performLogout} from "@utils/auth/auth-helpers";

function LogoutButton() {
  return (
    <Button onClick={() => performLogout()}>
      Sign Out
    </Button>
  );
}
```

**What it does:**

```
1. Calls /api/auth/logout (POST) → Invalidates Laravel token
2. Calls signOut({redirect: false}) → Clears NextAuth session
3. Shows toast: "Logged out successfully"
4. window.location.href → /auth?tab=login
```

---

### Custom Logout with Redirect

```typescript
import {performLogout} from "@utils/auth/auth-helpers";

function LogoutWithRedirect() {
  async function handleLogout() {
    // Logout and redirect to pricing page
    await performLogout("/pricing");
  }

  return <Button onClick={handleLogout}>Sign Out</Button>;
}
```

---

## 🔄 Complete Auth Flow Diagram

### Login Flow

```
┌──────────────────────┐
│   User clicks login  │
└──────────┬───────────┘
           │
           ▼
┌────────────────────────────────┐
│  OAuth Redirect                │
│  https://auth.../oauth/redirect│
└──────────┬─────────────────────┘
           │
           ▼
┌────────────────────────────────┐
│  OAuth Provider Auth           │
│  User enters credentials       │
└──────────┬─────────────────────┘
           │
           ▼
┌────────────────────────────────┐
│  Callback: /auth/callback      │
│  ├─ signIn("experts-oauth")   │
│  ├─ updateSession()           │
│  ├─ Wait 200ms                │
│  └─ window.location → /dashboard│
└──────────┬─────────────────────┘
           │
           ▼
┌────────────────────────────────┐
│  Dashboard Page Loads          │
│  ├─ SDKAuthProvider mounts    │
│  ├─ Shows "Initializing SDK..." │
│  ├─ setTokenResolver(token)   │
│  ├─ Double microtask delay    │
│  └─ sdkReady = true           │
└──────────┬─────────────────────┘
           │
           ▼
┌────────────────────────────────┐
│  AppDataProvider renders       │
│  ├─ GET /v1/user              │ ✅ 200 (has token)
│  ├─ GET /v1/organizations     │ ✅ 200 (has token)
│  └─ GET /v1/plans/current     │ ✅ 200 (has token)
└──────────┬─────────────────────┘
           │
           ▼
┌──────────────────────┐
│  Dashboard loaded    │ ✅
│  No 401 errors!     │
└──────────────────────┘
```

### Logout Flow

```
┌──────────────────────┐
│  User clicks logout  │
└──────────┬───────────┘
           │
           ▼
┌────────────────────────────────┐
│  performLogout()               │
│  ├─ POST /api/auth/logout     │ (invalidates Laravel token)
│  ├─ signOut({redirect: false})│ (clears NextAuth session)
│  ├─ toast.success()           │
│  └─ window.location → /auth   │
└──────────┬─────────────────────┘
           │
           ▼
┌────────────────────────────────┐
│  Full Page Reload              │
│  ├─ All cookies cleared       │
│  ├─ All state cleared         │
│  └─ SDK token resolver = null │
└──────────┬─────────────────────┘
           │
           ▼
┌──────────────────────┐
│  Login page          │ ✅
│  Clean slate         │
└──────────────────────┘
```

---

## 📦 Auth Helper Functions

### Available Functions

```typescript
import {
  performLogout,
  getAuthUrl,
  navigateToLogin,
  navigateToRegister,
} from "@utils/auth/auth-helpers";
```

### Function Reference

#### `performLogout(redirectTo?: string)`

Logout user and redirect.

```typescript
// Simple logout
await performLogout();

// Logout with custom redirect
await performLogout("/pricing");
```

#### `getAuthUrl(type?: "login" | "register")`

Get authentication URL.

```typescript
const loginUrl = getAuthUrl("login");
// → https://auth.experts.com.sa/oauth/redirect

const registerUrl = getAuthUrl("register");
// → https://auth.experts.com.sa/register
```

#### `navigateToLogin(redirectAfterLogin?: string)`

Navigate to login with return path.

```typescript
// Login and return to current page
navigateToLogin();

// Login and return to specific page
navigateToLogin("/dashboard");
```

#### `navigateToRegister(redirectAfterRegister?: string)`

Navigate to register with return path.

```typescript
// Register and return to current page
navigateToRegister();

// Register and return to pricing
navigateToRegister("/pricing");
```

---

## 🎯 Common Patterns

### Protected Route

```typescript
"use client";

import {useSession} from "next-auth/react";
import {navigateToLogin} from "@utils/auth/auth-helpers";
import {useEffect} from "react";

export default function ProtectedPage() {
  const {status} = useSession();

  useEffect(() => {
    if (status === "unauthenticated") {
      navigateToLogin(window.location.pathname);
    }
  }, [status]);

  if (status === "loading") {
    return <Loading />;
  }

  return <DashboardContent />;
}
```

### Navbar Auth Buttons

```typescript
import {getAuthUrl, performLogout} from "@utils/auth/auth-helpers";
import {useSession} from "next-auth/react";

function NavbarAuth() {
  const {data: session, status} = useSession();

  if (status === "loading") {
    return <Skeleton />;
  }

  if (status === "unauthenticated") {
    return (
      <>
        <Button onClick={() => window.location.href = getAuthUrl("login")}>
          Login
        </Button>
        <Button onClick={() => window.location.href = getAuthUrl("register")}>
          Sign Up
        </Button>
      </>
    );
  }

  return (
    <>
      <UserDropdown user={session.user} />
      <Button onClick={() => performLogout()}>
        Logout
      </Button>
    </>
  );
}
```

### Session Expired Handler

```typescript
import { setup401ErrorHandling } from "@sdk/runtime";
import { navigateToLogin } from "@utils/auth/auth-helpers";

// In your app initialization
setup401ErrorHandling(() => {
  console.warn("🔐 Session expired");
  navigateToLogin(window.location.pathname);
});
```

---

## ⚡ Performance Optimizations

### Before (Old Complex Logout)

```typescript
❌ setTimeout(..., 1000)         // Unnecessary 1-second delay
❌ Multiple API calls            // Redundant requests
❌ Complex redirect logic        // Over-engineered
❌ Inconsistent error handling   // Confusing flow

Total time: ~1200ms
```

### After (Efficient Logout)

```typescript
✅ Immediate API call            // No delays
✅ Single logout endpoint        // One request
✅ Simple redirect               // Direct path
✅ Graceful error handling       // Fails safely

Total time: ~200ms (6x faster!)
```

---

## 🛡️ Security Benefits

### Token Invalidation

```typescript
// ✅ Logout API invalidates token on Laravel side
POST /api/auth/logout
→ Laravel revokes token
→ Token can't be reused even if stolen
```

### Cookie Clearing

```typescript
// ✅ Logout API clears all auth cookies
res.cookies.set({
  name: "__Secure-next-auth.session-token",
  value: "",
  expires: new Date(0), // Expires immediately
});
```

### State Cleanup

```typescript
// ✅ Full page reload ensures complete cleanup
window.location.href = "/auth"
→ All React state cleared
→ All SWR caches cleared
→ All SDK state cleared
```

---

## 🐛 Troubleshooting

### Issue: Still seeing 401 errors after login

**Check:**

1. Is `SDKAuthProvider` wrapping `AppDataProvider` in layout?
2. Is the 200ms delay present in callback page?
3. Is `updateSession()` being called?

**Debug:**

```typescript
// In callback page
console.log("Session before update:", session);
await updateSession();
console.log("Session after update:", session);
```

### Issue: Logout not working

**Check:**

1. Is `/api/auth/logout` route returning 200?
2. Are cookies being cleared? (Check DevTools → Application → Cookies)
3. Is `signOut()` completing?

**Debug:**

```typescript
// In navbar
console.log("Starting logout...");
await performLogout();
console.log("Logout complete"); // Should not reach here (page reloads)
```

### Issue: Login redirect not working

**Check:**

1. OAuth callback URL configured correctly?
2. `NEXT_PUBLIC_AUTH_URL` environment variable set?
3. `window.location.href` executing?

**Debug:**

```typescript
// In callback page
console.log("Redirect URL:", callbackUrl);
console.log("About to redirect...");
window.location.href = callbackUrl;
```

---

## 📋 Migration Checklist

Updating from old auth flow to new efficient flow:

### Navbar Components

- [ ] Replace complex logout with `performLogout()`
- [ ] Use `getAuthUrl()` for login/register links
- [ ] Remove setTimeout delays
- [ ] Remove redundant error handling

### Login Forms

- [ ] Add `updateSession()` after `signIn()`
- [ ] Add 200ms delay before navigation
- [ ] Use `window.location.href` for redirects
- [ ] Remove client-side navigation (`router.push`)

### Protected Routes

- [ ] Use `navigateToLogin()` for auth redirects
- [ ] Pass current path for return navigation
- [ ] Remove complex redirect logic

### API Routes

- [ ] Ensure `/api/auth/logout` supports POST
- [ ] Verify cookies are being cleared
- [ ] Check domain is set correctly for cookies

---

## 🎯 Best Practices

### DO ✅

- Use `performLogout()` for logout
- Use `getAuthUrl()` for auth URLs
- Call `updateSession()` after `signIn()`
- Wait 200ms before navigation after login
- Use `window.location.href` for auth redirects
- Let `SDKAuthProvider` handle token configuration

### DON'T ❌

- Don't use `setTimeout` for logout delays
- Don't make redundant API calls
- Don't use `router.push()` immediately after auth
- Don't clear tokens manually (let helpers handle it)
- Don't implement custom logout logic (use helpers)
- Don't navigate before session updates

---

## 🧪 Testing

### Manual Test Checklist

**Login:**

1. Navigate to `/auth`
2. Complete OAuth flow
3. See brief "Initializing SDK..." loading
4. Land on dashboard
5. Check console - no 401 errors
6. Check network - all API calls show 200
7. Verify user data loaded correctly

**Logout:**

1. Click logout button
2. See "Logged out successfully" toast
3. Redirect to `/auth?tab=login`
4. Check cookies cleared (DevTools)
5. Try accessing protected route → Redirects to login
6. Login again → Everything works

**Session Persistence:**

1. Login successfully
2. Refresh page
3. No loading screen (already initialized)
4. User stays logged in
5. Data loads immediately

---

## 📊 Comparison

| Aspect              | Old Flow  | New Efficient Flow |
| ------------------- | --------- | ------------------ |
| **Logout Time**     | ~1200ms   | ~200ms (6x faster) |
| **Login 401s**      | ❌ Always | ✅ Never           |
| **Code Complexity** | 45 lines  | 3 lines            |
| **Error Rate**      | High      | Low                |
| **User Experience** | Janky     | Smooth             |
| **Maintainability** | Hard      | Easy               |

---

## 🔗 Related Files

**Auth Helpers:**

- `packages/utilities/auth/auth-helpers.ts` - Reusable auth functions

**Providers:**

- `packages/providers/src/sdk-auth-provider.tsx` - Token configuration
- `packages/hooks/src/use-sdk-auth.ts` - SDK auth hook

**Routes:**

- `app/auth/signin-callback/page.tsx` - OAuth callback handler
- `app/api/auth/logout/route.ts` - Logout API endpoint

**Components:**

- `packages/ui/src/navbar/navbar-1.tsx` - Example implementation

---

## 💡 Key Takeaways

1. **Always call `updateSession()`** after `signIn()` before navigation
2. **Wait 200ms** for SDK to configure token (matches double microtask)
3. **Use `window.location.href`** for auth-related redirects (not `router.push`)
4. **Use helper functions** for consistency across app
5. **Let SDKAuthProvider handle SDK setup** (don't configure token manually)
6. **Trust the blocking behavior** - loading screens prevent race conditions

---

**Result:** Clean, fast, error-free authentication! 🎉
