---
title: "🔄 Logout Infinite Loop Fix"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/experts-api-docs"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🔄 Logout Infinite Loop Fix

## Problem

After clicking logout, user gets **auto-logged back in immediately**:

```
1. Click logout
2. NextAuth session cleared ✅
3. Redirect to /oauth/redirect
4. Laravel sees existing session → Auto-login ❌
5. Redirects back to app (logged in again!)
6. Loop repeats in milliseconds
```

---

## Root Cause

### Laravel Session Not Invalidated

The logout API only revoked the **OAuth token** but didn't clear the **Laravel session**:

```php
// ❌ Before - Incomplete logout
public function logout(Request $request) {
    $request->user()->token()->revoke();  // Only revokes token
    return $this->success(...);
    // Session still valid! ❌
}
```

**What happened:**

```
POST /v1/logout
→ Token revoked ✅
→ Session still valid ❌
→ User redirects to /oauth/redirect
→ Laravel checks session: "Oh, user is logged in!"
→ Auto-redirects back to app
→ Infinite loop!
```

---

## Solution: Three-Part Logout

### Part 1: Enhanced Laravel Logout API

**File:** `app/Domains/Auth/Controllers/AuthController.php`

```php
public function logout(Request $request): JsonResponse
{
    // Revoke the OAuth access token
    $token = $request->user()->token();
    if ($token) {
        $token->revoke();
    }

    // ✅ CRITICAL: Also invalidate the Laravel session
    // This prevents auto-login when user redirects to /oauth/redirect
    Auth::guard('web')->logout();
    $request->session()->invalidate();
    $request->session()->regenerateToken();

    return $this->success([], 'User logged out and token revoked successfully.', 202);
}
```

**What it does:**

1. ✅ Revokes OAuth token (can't be reused)
2. ✅ Logs out from web guard
3. ✅ Invalidates session (clears all session data)
4. ✅ Regenerates CSRF token (security)

---

### Part 2: Updated Frontend Logout

**File:** `packages/utilities/auth/auth-helpers.ts`

```typescript
export async function performLogout(redirectTo?: string) {
  // STEP 1: Call Laravel logout API to invalidate Laravel session + OAuth token
  // ✅ CRITICAL: Must happen BEFORE clearing NextAuth (we need the token!)
  await fetch(`${apiUrl}/v1/logout`, {
    method: "POST",
    credentials: "include", // ✅ Sends Laravel session cookies
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "Api-Version": "v1",
      Authorization: `Bearer ${token}`, // ✅ Authenticated request
    },
  });

  // STEP 2: Call NextAuth logout API to clear NextAuth cookies
  await fetch("/api/auth/logout", {
    method: "POST",
    credentials: "include",
  });

  // STEP 3: Clear NextAuth client-side session
  await signOut({ redirect: false });

  // STEP 4: Redirect to Laravel OAuth login
  window.location.href = AUTH_REDIRECTS.LOGOUT;
  // → https://auth.dev.experts.com.sa/oauth/redirect
  // → Laravel checks session: Empty! ✅
  // → Shows login form
}
```

---

## Complete Logout Flow (Fixed)

```
┌───────────────────────────┐
│  User clicks logout       │
└──────────┬────────────────┘
           │
           ▼
┌────────────────────────────────────────┐
│  STEP 1: Call Laravel logout API      │
│  POST /v1/logout (with Bearer token)   │
│  ├─ Revoke OAuth token                │ ✅
│  ├─ Auth::guard('web')->logout()      │ ✅
│  ├─ $session->invalidate()            │ ✅
│  └─ $session->regenerateToken()       │ ✅
└──────────┬─────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────┐
│  STEP 2: Call NextAuth logout API     │
│  POST /api/auth/logout                │
│  └─ Clear NextAuth cookies            │ ✅
└──────────┬─────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────┐
│  STEP 3: Clear NextAuth session       │
│  signOut({redirect: false})            │ ✅
└──────────┬─────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────┐
│  STEP 4: Redirect to Laravel           │
│  https://auth.dev.../oauth/redirect    │
└──────────┬─────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────┐
│  Laravel checks session                │
│  ├─ Session is empty                  │ ✅
│  ├─ User is NOT logged in             │ ✅
│  └─ Shows login form                  │ ✅
└────────────────────────────────────────┘
```

---

## Why It Works Now

### Session Invalidation

```php
// Before logout
Session::get('user_id') // → 123

// After Auth::guard('web')->logout()
Session::get('user_id') // → null

// After $session->invalidate()
Session::all() // → []

// Session is completely cleared! ✅
```

### Token Revocation

```php
// Before logout
Token::where('id', $token->id)->first() // → Active token

// After $token->revoke()
Token::where('id', $token->id)->first()->revoked // → true

// Token is revoked! ✅
```

---

## Testing

### Expected Console Output

**Frontend logout:**

```
🔓 Starting logout...
✅ Laravel session invalidated: {status: "success", message: "..."}
🔓 NextAuth logout response: {status: "success", redirect: "..."}
🔓 Final redirect URL: https://auth.dev.experts.com.sa/oauth/redirect
```

**Laravel logs:**

```
[info] Web logout initiated: {user_id: 123, has_session: true}
[info] Web logout completed: {session_invalidated: true}
```

**After redirect:**

```
✅ Shows login form (not auto-login!)
✅ Session is empty
✅ No infinite loop
```

---

## What You Should NOT See

```
❌ Auto-login after logout
❌ Infinite redirect loop
❌ "Logged in as..." immediately after logout
❌ Session persisting after logout
```

---

## Debugging

### Check Laravel Session

```php
// Add to OAuthController@redirect for debugging
Log::info('OAuth redirect - Session check', [
    'has_session' => $request->hasSession(),
    'session_all' => $request->session()->all(),
    'is_authenticated' => Auth::check(),
]);
```

### Check Token Revocation

```php
// In database
SELECT * FROM oauth_access_tokens WHERE revoked = false;
// Should be empty after logout
```

### Check Session Invalidation

```bash
# Redis (if using Redis sessions)
redis-cli keys "*session*"
# Should not have user's session after logout
```

---

## Environment Configuration

Make sure these are set in `.env`:

```env
# Session driver (must support invalidate())
SESSION_DRIVER=redis

# Session lifetime
SESSION_LIFETIME=120

# Session domain (for cross-subdomain clearing)
SESSION_DOMAIN=.dev.experts.com.sa
```

---

## Security Benefits

### Before

```
❌ OAuth token revoked but session active
❌ User can re-authenticate without credentials
❌ Session hijacking possible
❌ Infinite auto-login loop
```

### After

```
✅ OAuth token revoked
✅ Session completely invalidated
✅ CSRF token regenerated
✅ Forces fresh login with credentials
✅ No auto-login loops
✅ Secure logout
```

---

## Files Changed

1. ✅ `app/Domains/Auth/Controllers/AuthController.php` - Enhanced logout method
2. ✅ `packages/utilities/auth/auth-helpers.ts` - Updated logout flow
3. ✅ `app/Domains/Auth/Controllers/WebLogoutController.php` - Created (optional web route)

---

## Summary

**Problem:** Laravel session persisting after logout → auto-login loop

**Fix:**

1. ✅ Revoke OAuth token
2. ✅ Logout from web guard
3. ✅ Invalidate session
4. ✅ Regenerate CSRF token
5. ✅ Clear NextAuth session
6. ✅ Redirect to login

**Result:** Clean logout, no auto-login, secure! 🎉
