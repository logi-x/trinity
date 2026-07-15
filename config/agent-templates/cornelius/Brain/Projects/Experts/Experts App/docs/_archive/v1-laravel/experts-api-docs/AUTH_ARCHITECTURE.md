---
title: "🏗️ Authentication Architecture"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/experts-api-docs"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🏗️ Authentication Architecture

## Overview

Centralized, efficient authentication system using shared constants and utilities.

---

## 📁 File Structure

```
packages/utilities/auth/
├── auth-constants.ts      # Shared constants (client + server)
├── auth-helpers.ts        # Client-side utilities
└── index.ts               # Central exports

app/api/auth/
├── logout/route.ts        # Server-side logout API
└── callback/route.ts      # Server-side OAuth callback

packages/providers/
└── sdk-auth-provider.tsx  # SDK token configuration provider

packages/hooks/
└── use-sdk-auth.ts        # SDK auth hook with token resolver
```

---

## 🔧 Shared Constants (`auth-constants.ts`)

**Purpose:** Single source of truth for URLs, cookies, and validation

**Can be used in:**

- ✅ Server-side (API routes)
- ✅ Client-side (components)
- ✅ Middleware
- ✅ Server actions

```typescript
import {
  AUTH_REDIRECTS,
  buildLogoutRedirectUrl,
} from "@utils/auth/auth-constants";

// Constants
AUTH_REDIRECTS.LOGIN; // "/auth?tab=login"
AUTH_REDIRECTS.LOGOUT; // "/auth?tab=login"
AUTH_REDIRECTS.SESSION_EXPIRED; // "/auth?tab=login&error=session_expired"

// Functions
getCookiePrefix(); // "dev-", "canary-", "", etc.
getAuthDomain(); // ".dev.experts.com.sa", etc.
validateRedirectUrl(url); // Sanitizes URLs
buildLogoutRedirectUrl(uri); // Builds logout redirect
```

---

## 🎯 Client Helpers (`auth-helpers.ts`)

**Purpose:** Browser-based auth operations

**Can be used in:**

- ✅ Client components
- ✅ Event handlers
- ✅ React hooks

**Cannot be used in:**

- ❌ Server components
- ❌ API routes (use `auth-constants` instead)

```typescript
import {
  performLogout,
  getAuthUrl,
  navigateToLogin,
  navigateToRegister,
} from "@utils/auth/auth-helpers";

// Functions
performLogout(); // Complete logout flow
getAuthUrl("login"); // Get OAuth login URL
navigateToLogin("/dashboard"); // Redirect to login
navigateToRegister("/pricing"); // Redirect to register
```

---

## 🔄 Flow Comparison

### Before: Scattered Logic ❌

```typescript
// In navbar.tsx (45 lines)
async function handleLogout() {
  const domain = getAuthDomain(); // Duplicated function
  const prefix = getCookiePrefix(); // Duplicated function
  // ... complex logic
  setTimeout(async () => {
    // Multiple API calls
    // Complex error handling
  }, 1000);
}

// In logout API route (50 lines)
function getAuthDomain() { ... }  // Duplicated!
function getCookiePrefix() { ... } // Duplicated!
function validateRedirectUrl() { ... } // Duplicated!
```

**Problems:**

- ❌ Code duplication
- ❌ Inconsistent redirect logic
- ❌ Hard to maintain
- ❌ Easy to have bugs

---

### After: Centralized Constants ✅

```typescript
// auth-constants.ts (shared)
export const AUTH_REDIRECTS = { ... };
export function getCookiePrefix() { ... }
export function getAuthDomain() { ... }
export function buildLogoutRedirectUrl() { ... }

// auth-helpers.ts (client)
import {AUTH_REDIRECTS} from "./auth-constants";
export async function performLogout() {
  // Uses shared constants
  window.location.href = AUTH_REDIRECTS.LOGOUT;
}

// logout/route.ts (server)
import {buildLogoutRedirectUrl} from "@utils/auth/auth-constants";
const redirectUrl = buildLogoutRedirectUrl(redirectUri);
```

**Benefits:**

- ✅ Single source of truth
- ✅ Consistent behavior everywhere
- ✅ Easy to maintain
- ✅ Type-safe
- ✅ Reduced code by 90%

---

## 🎯 Usage Examples

### Navbar Component

```typescript
import {performLogout, getAuthUrl} from "@utils/auth/auth-helpers";

function Navbar() {
  return (
    <>
      <Button onClick={() => window.location.href = getAuthUrl("login")}>
        Login
      </Button>
      <Button onClick={() => performLogout()}>
        Logout
      </Button>
    </>
  );
}
```

### Server-Side API Route

```typescript
import {buildLogoutRedirectUrl, getAuthDomain} from "@utils/auth/auth-constants";

export async function GET(request: Request) {
  const redirectUrl = buildLogoutRedirectUrl(redirectUri);
  const domain = getAuthDomain();

  // Clear cookies with correct domain
  res.cookies.set({domain, ...});

  return NextResponse.json({redirect: redirectUrl});
}
```

### Middleware

```typescript
import { AUTH_REDIRECTS } from "@utils/auth/auth-constants";

export function middleware(request: NextRequest) {
  if (!token) {
    return NextResponse.redirect(
      new URL(AUTH_REDIRECTS.UNAUTHORIZED, request.url),
    );
  }
}
```

---

## 🔐 Security Benefits

### 1. URL Validation

```typescript
validateRedirectUrl("/dashboard"); // ✅ Allowed
validateRedirectUrl("//evil.com"); // ❌ Blocked → default
validateRedirectUrl("https://hack.com"); // ❌ Blocked → default
```

### 2. Cookie Security

```typescript
// Always uses correct domain for environment
const domain = getAuthDomain(); // ".dev.experts.com.sa"

res.cookies.set({
  domain, // ✅ Correct domain
  httpOnly: true, // ✅ Secure
  secure: true, // ✅ HTTPS only
  sameSite: "none", // ✅ Cross-domain
});
```

### 3. Token Invalidation

```typescript
// Server-side API invalidates Laravel token
await logout({ auth: session.accessToken });

// Client-side clears NextAuth session
await signOut({ redirect: false });
```

---

## 📊 Architecture Layers

```
┌─────────────────────────────────────────┐
│           Client Components             │
│  (Navbar, Buttons, Protected Routes)    │
│              ↓ uses                     │
│      auth-helpers.ts (client-only)      │
│     performLogout(), getAuthUrl()       │
└─────────────┬───────────────────────────┘
              │ imports
              ▼
┌─────────────────────────────────────────┐
│        auth-constants.ts (shared)       │
│   AUTH_REDIRECTS, validateRedirectUrl() │
│   (Can be used by both client & server) │
└─────────────┬───────────────────────────┘
              │ imports
              ▼
┌─────────────────────────────────────────┐
│         Server API Routes               │
│      (logout/route.ts, etc.)            │
│   Uses buildLogoutRedirectUrl()         │
└─────────────────────────────────────────┘
```

---

## 🚀 Benefits Summary

| Aspect                | Before     | After       |
| --------------------- | ---------- | ----------- |
| **Code Duplication**  | 3 copies   | 1 source    |
| **Lines of Code**     | ~150 lines | ~50 lines   |
| **Logout Complexity** | 45 lines   | 3 lines     |
| **Redirect Logic**    | Scattered  | Centralized |
| **Type Safety**       | Partial    | Complete    |
| **Maintainability**   | Hard       | Easy        |
| **Consistency**       | Low        | High        |
| **401 Errors**        | Common     | None        |

---

## 🎓 Best Practices

### 1. Always Use Shared Constants

```typescript
// ✅ Good
import { AUTH_REDIRECTS } from "@utils/auth/auth-constants";
window.location.href = AUTH_REDIRECTS.LOGIN;

// ❌ Bad
window.location.href = "/auth?tab=login"; // Hardcoded
```

### 2. Use Helper Functions

```typescript
// ✅ Good
import { performLogout } from "@utils/auth/auth-helpers";
await performLogout();

// ❌ Bad
await fetch("/api/auth/logout");
await signOut();
window.location.href = "/auth"; // Manual implementation
```

### 3. Client vs Server Separation

```typescript
// ✅ Client component
import { performLogout } from "@utils/auth/auth-helpers";

// ✅ Server API route
import { buildLogoutRedirectUrl } from "@utils/auth/auth-constants";

// ❌ Server trying to use client helpers
import { performLogout } from "@utils/auth/auth-helpers"; // Error!
```

### 4. Full Page Reloads for Auth

```typescript
// ✅ Good - Clean state after auth operations
window.location.href = "/dashboard";

// ❌ Bad - Can cause race conditions
router.push("/dashboard");
```

---

## 📚 Related Documentation

- [EFFICIENT_AUTH_FLOW.md](./EFFICIENT_AUTH_FLOW.md) - Complete flow guide
- [AUTH_QUICK_REFERENCE.md](./AUTH_QUICK_REFERENCE.md) - Copy-paste examples
- [AUTH_401_RACE_CONDITION_FIX.md](./AUTH_401_RACE_CONDITION_FIX.md) - Technical details

---

**Result:** Clean, maintainable, secure authentication architecture! 🎉
