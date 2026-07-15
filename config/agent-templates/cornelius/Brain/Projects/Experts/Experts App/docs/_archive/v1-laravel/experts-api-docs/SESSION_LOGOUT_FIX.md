---
title: "🔒 Session Logout Fix - Complete Solution"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/experts-api-docs"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🔒 Session Logout Fix - Complete Solution

## Problem

### Error 500 on Logout

```
POST https://api.dev.experts.com.sa/v1/auth/logout

{
  message: "Session store not set on request.",
  exception: "RuntimeException"
}
```

### Auto-Login Loop

After logout, user immediately logged back in:

```
1. Logout → Clear NextAuth
2. Redirect to /oauth/redirect
3. Laravel sees existing session → Auto-login ❌
4. Back to app (logged in) → Infinite loop!
```

---

## Root Causes

### 1. API Route Had No Session Middleware

```php
// ❌ Before
Route::post('/logout', [AuthController::class, 'logout'])
  ->middleware(['auth:api'])  // No session access!
  ->name('api.logout');

// Inside logout method:
$request->session()->invalidate(); // ❌ RuntimeException!
```

**Problem:** API routes don't include session middleware by default.

### 2. SDK Not Sending Cookies

```typescript
// ❌ Before - SDK config
export const createClientConfig = (config) => ({
  baseUrl: getBaseUrl(),
  headers: {...},
  // No credentials option! Cookies not sent!
});
```

**Problem:** Laravel session cookie wasn't being sent with API requests.

---

## Solution: Two-Part Fix

### Fix 1: Add Session Middleware to Logout Route ✅

**File:** `routes/v1/auth.php`

```php
Route::post('/logout', [AuthController::class, 'logout'])
  ->middleware(['auth:api', \Illuminate\Session\Middleware\StartSession::class])
  ->name('api.logout');
```

**What it does:**

- ✅ Adds session support to API route
- ✅ Allows `$request->session()` access
- ✅ Reads Laravel session cookie from request
- ✅ Enables session invalidation

---

### Fix 2: SDK Sends Credentials ✅

**File:** `packages/sdk/src/runtime.ts`

```typescript
export const createClientConfig: CreateClientConfig = (config) => ({
  ...config,
  baseUrl: getBaseUrl(),
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
    "Api-Version": "v1",
    ...config?.headers,
  },

  // ✅ Include credentials (cookies) for cross-domain requests
  credentials: "include",

  auth: async () => {
    // Bearer token logic
  },
});
```

**What it does:**

- ✅ Sends cookies with every SDK request
- ✅ Includes Laravel session cookie
- ✅ Works cross-domain (`.dev.experts.com.sa`)
- ✅ Required for session invalidation

---

### Fix 3: Enhanced Logout Method ✅

**File:** `app/Domains/Auth/Controllers/AuthController.php`

```php
public function logout(Request $request): JsonResponse
{
    // Revoke the OAuth access token
    $token = $request->user()->token();
    if ($token) {
        $token->revoke();
    }

    // ✅ Check if session exists before invalidating
    if ($request->hasSession()) {
        Auth::guard('web')->logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        Log::info('Logout: Web session invalidated');
    }

    return $this->success([], 'User logged out successfully', 202);
}
```

**What it does:**

- ✅ Checks `hasSession()` before accessing session
- ✅ Prevents runtime errors if session not available
- ✅ Logs session invalidation for debugging
- ✅ Clears both token AND session

---

## Complete Logout Flow (Fixed)

```
┌─────────────────────────────────┐
│  User clicks logout button      │
└──────────┬──────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  performLogout() - Frontend              │
│  STEP 1: Call Laravel /v1/logout         │
│  ├─ SDK adds Authorization header        │ ✅
│  ├─ SDK includes credentials             │ ✅
│  ├─ Sends Laravel session cookie         │ ✅
│  └─ POST /v1/logout                      │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  Laravel Logout Handler                  │
│  ├─ StartSession middleware active       │ ✅
│  ├─ $request->hasSession() = true        │ ✅
│  ├─ Revoke OAuth token                   │ ✅
│  ├─ Auth::guard('web')->logout()         │ ✅
│  ├─ $session->invalidate()               │ ✅
│  ├─ $session->regenerateToken()          │ ✅
│  └─ Return 202                           │ ✅
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  performLogout() - Continued             │
│  STEP 2: Call NextAuth /api/auth/logout  │
│  └─ Clear NextAuth cookies               │ ✅
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  STEP 3: signOut({redirect: false})      │
│  └─ Clear NextAuth client session        │ ✅
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  STEP 4: Redirect                        │
│  window.location.href =                  │
│  https://auth.dev.../oauth/redirect      │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  Laravel /oauth/redirect                 │
│  ├─ Checks web session                  │
│  ├─ Session is empty                    │ ✅
│  ├─ User not authenticated              │ ✅
│  └─ Redirects to /oauth/authorize       │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  Shows login form                        │
│  ✅ No auto-login!                        │
│  ✅ No infinite loop!                     │
└──────────────────────────────────────────┘
```

---

## Files Changed

1. ✅ `routes/v1/auth.php` - Added `StartSession` middleware to logout route
2. ✅ `app/Domains/Auth/Controllers/AuthController.php` - Enhanced logout with session check
3. ✅ `packages/sdk/src/runtime.ts` - Added `credentials: 'include'`
4. ✅ `packages/utilities/auth/auth-helpers.ts` - Uses SDK logout (sends cookies)

---

## Testing

### Expected Console Output

**Frontend:**

```
🔓 Starting logout...
✅ Laravel session invalidated: {status: "success", message: "User logged out successfully"}
🔓 NextAuth logout response: {status: "success", ...}
🔓 Final redirect URL: https://auth.dev.experts.com.sa/oauth/redirect
```

**Laravel logs:**

```
[info] Logout: Web session invalidated
```

**Browser:**

```
✅ Redirect to https://auth.dev.experts.com.sa/oauth/redirect
✅ Shows login form
✅ No auto-login
✅ No 500 errors
```

---

## Debugging

### Check if Session Cookie is Sent

```
1. Open DevTools → Network
2. Click logout
3. Find POST /v1/logout request
4. Check Request Headers:
   ✅ Should see: Cookie: laravel_session=...
```

### Check Session Invalidation

```php
// Add to logout method for debugging
Log::info('Before logout', [
    'session_data' => $request->session()->all(),
    'is_authenticated' => Auth::check(),
]);

// After invalidate
Log::info('After logout', [
    'has_session' => $request->hasSession(),
    'is_authenticated' => Auth::check(),
]);
```

### Verify No Auto-Login

```
1. Logout
2. Check Network tab for /oauth/redirect
3. Should see response: 302 redirect to /oauth/authorize
4. Should NOT see immediate redirect back to app
```

---

## Security Considerations

### Same-Domain Session Sharing

**Your setup:**

```
SESSION_DOMAIN=.dev.experts.com.sa

Subdomains:
- auth.dev.experts.com.sa  (Laravel auth server)
- app.dev.experts.com.sa   (Next.js app)
- api.dev.experts.com.sa   (Laravel API)
```

**Implications:**

- ✅ Shared session across subdomains
- ✅ Logout from one = logout from all
- ✅ Consistent user experience
- ⚠️ All apps share same session (intended behavior)

### Cookie Security

```php
// Session cookie settings
'secure' => true,           // HTTPS only
'http_only' => true,        // No JavaScript access
'same_site' => 'lax',       // CSRF protection
'domain' => '.dev.experts.com.sa',  // Shared
```

---

## Summary

**Problems Fixed:**

1. ✅ 500 error on logout (no session middleware)
2. ✅ Auto-login infinite loop (session not invalidated)
3. ✅ Cookies not sent (SDK missing credentials)

**Solution:**

1. ✅ Added `StartSession` middleware to logout route
2. ✅ Enhanced logout to invalidate web session
3. ✅ SDK configured to send credentials
4. ✅ Frontend uses SDK logout (includes cookies)

**Result:** Clean logout, no loops, no errors! 🎉
