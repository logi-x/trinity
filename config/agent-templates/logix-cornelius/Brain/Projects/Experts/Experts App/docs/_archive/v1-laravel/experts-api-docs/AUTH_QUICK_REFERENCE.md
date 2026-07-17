---
title: "🔐 Auth Quick Reference"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/experts-api-docs"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🔐 Auth Quick Reference

## 🎯 TL;DR - Copy & Paste Examples

### Login Button

```typescript
import {getAuthUrl} from "@utils/auth/auth-helpers";

<Button onClick={() => window.location.href = getAuthUrl("login")}>
  Sign In
</Button>
```

### Logout Button

```typescript
import {performLogout} from "@utils/auth/auth-helpers";

<Button onClick={() => performLogout()}>
  Sign Out
</Button>
```

### Register Button

```typescript
import {getAuthUrl} from "@utils/auth/auth-helpers";

<Button onClick={() => window.location.href = getAuthUrl("register")}>
  Sign Up
</Button>
```

### Protected Component

```typescript
import {useSession} from "next-auth/react";
import {navigateToLogin} from "@utils/auth/auth-helpers";

function ProtectedComponent() {
  const {data: session, status} = useSession();

  if (status === "loading") return <Loading />;
  if (status === "unauthenticated") {
    navigateToLogin();
    return null;
  }

  return <Content user={session.user} />;
}
```

---

## 🔑 Helper Functions

### Import

```typescript
import {
  performLogout,
  getAuthUrl,
  navigateToLogin,
  navigateToRegister,
} from "@utils/auth/auth-helpers";
```

### Functions

| Function                        | Purpose           | Usage                            |
| ------------------------------- | ----------------- | -------------------------------- |
| `performLogout(redirectTo?)`    | Logout + redirect | `await performLogout()`          |
| `getAuthUrl(type?)`             | Get auth URL      | `getAuthUrl("login")`            |
| `navigateToLogin(returnTo?)`    | Go to login       | `navigateToLogin("/dashboard")`  |
| `navigateToRegister(returnTo?)` | Go to register    | `navigateToRegister("/pricing")` |

---

## ⚙️ Critical Rules

### After Login (Callback Page)

```typescript
// ✅ ALWAYS do this after signIn()
await signIn("experts-oauth", {...});
await updateSession();                    // Force session refresh
await new Promise(r => setTimeout(r, 200)); // Wait for SDK
window.location.href = callbackUrl;       // Full page reload
```

### For Logout

```typescript
// ✅ ALWAYS use full page reload
window.location.href = "/auth";

// ❌ DON'T use client-side navigation
router.push("/auth"); // This causes state issues
```

### For Protected Routes

```typescript
// ✅ Trust SDKAuthProvider blocking behavior
// It shows loading screen until SDK is ready

// ❌ DON'T manually check isReady in components
const { isReady } = useSDKAuth(); // Not needed anymore
```

---

## 🚨 Common Mistakes

### ❌ Wrong: Client-side navigation after login

```typescript
const result = await signIn(...);
router.push("/dashboard"); // ❌ Race condition!
```

### ✅ Correct: Full page reload

```typescript
const result = await signIn(...);
await updateSession();
await new Promise(r => setTimeout(r, 200));
window.location.href = "/dashboard"; // ✅ Clean state
```

---

### ❌ Wrong: Complex logout

```typescript
setTimeout(async () => {
  await fetch("/api/auth/logout");
  await signOut();
  if (response.ok) {
    router.push("/auth");
  }
}, 1000); // ❌ Why the delay?
```

### ✅ Correct: Simple logout

```typescript
await performLogout(); // ✅ That's it!
```

---

### ❌ Wrong: Manual token management

```typescript
import { setTokenResolver, clearTokenCache } from "@sdk/runtime";

// ❌ Don't do this manually
setTokenResolver(() => token);
clearTokenCache();
```

### ✅ Correct: Let SDKAuthProvider handle it

```typescript
// ✅ Just wrap your app
<SDKAuthProvider>
  <AppDataProvider>
    {children}
  </AppDataProvider>
</SDKAuthProvider>

// Token management happens automatically!
```

---

## 📱 Component Examples

### Navbar with Auth

```typescript
"use client";

import {useSession} from "next-auth/react";
import {performLogout, getAuthUrl} from "@utils/auth/auth-helpers";
import {Button, Avatar} from "@heroui/react";

export function Navbar() {
  const {data: session, status} = useSession();

  return (
    <nav>
      <Logo />

      {status === "loading" && <Skeleton />}

      {status === "unauthenticated" && (
        <>
          <Button onClick={() => window.location.href = getAuthUrl("login")}>
            Login
          </Button>
          <Button onClick={() => window.location.href = getAuthUrl("register")}>
            Sign Up
          </Button>
        </>
      )}

      {status === "authenticated" && (
        <>
          <Avatar src={session.user.image} />
          <Button onClick={() => performLogout()}>
            Logout
          </Button>
        </>
      )}
    </nav>
  );
}
```

---

## 🔍 Debugging

### Check Session State

```typescript
import { useSession } from "next-auth/react";

const { data: session, status } = useSession();
console.log("Session:", { status, session });
```

### Check SDK Token

```typescript
import { getClient } from "@sdk/runtime";

const client = getClient();
const config = client.getConfig();
const token = await config.auth();
console.log("SDK Token:", token ? "present" : "missing");
```

### Monitor Auth Flow

The SDK automatically logs:

```
🔐 Setting up SDK token resolver
✅ SDK token resolver configured and ready
```

Watch console during login/logout for these messages.

---

## 📚 Full Documentation

- [EFFICIENT_AUTH_FLOW.md](./EFFICIENT_AUTH_FLOW.md) - Complete guide
- [AUTH_401_RACE_CONDITION_FIX.md](./AUTH_401_RACE_CONDITION_FIX.md) - Technical details
- [AUTH_401_FIX.md](./AUTH_401_FIX.md) - Original fix documentation

---

**Questions?** Check the full docs or ask in Slack! 🚀
