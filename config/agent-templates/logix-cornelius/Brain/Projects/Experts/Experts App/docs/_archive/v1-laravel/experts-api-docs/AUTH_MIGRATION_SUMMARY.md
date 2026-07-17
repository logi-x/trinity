---
title: "Authentication Flow Enhancement - Summary"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/experts-api-docs"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Authentication Flow Enhancement - Summary

## What Changed?

✅ **Simplified** the login → callback → redirect flow
✅ **Enhanced** redirect URL handling with robust validation
✅ **Improved** security with open redirect prevention
✅ **Better** error handling and logging
✅ **Fixed** logout token passing issue

## Files Modified

### 1. **NEW:** `lib/auth/redirect-utils.ts`

Centralized utilities for secure redirect URL handling.

```typescript
import { buildAuthUrl, sanitizeRedirectUrl } from "@/lib/auth/redirect-utils";

// Build login URL with redirect
const loginUrl = buildAuthUrl("login", "/dashboard");
// Result: /auth?tab=login&redirect_uri=%2Fdashboard

// Validate and sanitize URLs
const safeUrl = sanitizeRedirectUrl(userInput);
```

### 2. **ENHANCED:** `app/(auth)/auth/forms/login.tsx`

- Added loading state
- Simplified redirect handling
- Better error messages
- Removed complex URL building

**Before:**

```typescript
const fullReturnUrl = `origin=${origin}&path=${path}&redirect_uri=${redirectUri}`;
router.replace("/auth/redirect?" + fullReturnUrl);
```

**After:**

```typescript
const redirectUrl = buildRedirectUrl(redirectParams);
router.replace(`/auth/callback?redirect_uri=${encodeRedirectUrl(redirectUrl)}`);
```

### 3. **SIMPLIFIED:** `app/auth/callback/page.tsx`

- Removed complex URL parameter handling
- Direct redirect_uri support
- Cleaner code

**Before:**

```typescript
const constructUrlParams = {
  origin: origin,
  path: path,
  redirect_uri: redirectUri,
};
```

**After:**

```typescript
// Just pass through to OAuthCallbackPage
<OAuthCallbackPage />
```

### 4. **ENHANCED:** `packages/ui/src/oauth-callback.tsx`

- Better session handling
- Improved redirect validation
- More informative UI states
- Automatic fallback to login

**New Features:**

- Shows destination URL before redirect
- 1.5s delay for better UX
- Fallback timeout for expired sessions
- Clear error messages

### 5. **FIXED:** `app/api/auth/logout/route.ts`

- **CRITICAL FIX:** Now properly passes Bearer token to Laravel API
- Simplified redirect handling
- Better error handling
- Comprehensive logging

**Before:**

```typescript
const response = await logout(); // ❌ No token!
```

**After:**

```typescript
const response = await logout({
  auth: session.accessToken as string, // ✅ Properly authenticated
});
```

### 6. **DEPRECATED:** `app/auth/redirect/page.tsx`

- Marked as deprecated
- Forwards to `/auth/callback` for backward compatibility
- Will be removed in future version

## New Authentication Flow

### Login Flow (Simplified)

```
┌─────────────────┐
│   User visits   │
│ protected page  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ /auth?tab=login&redirect_uri=/dashboard │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  User submits   │
│  credentials    │
└────────┬────────┘
         │
         ▼
┌────────────────────────────────┐
│ /auth/callback?redirect_uri=   │
│         /dashboard             │
└────────┬───────────────────────┘
         │
         ▼
┌─────────────────┐
│   /dashboard    │
│  (destination)  │
└─────────────────┘
```

### Logout Flow (Enhanced)

```
┌─────────────────┐
│  User clicks    │
│     logout      │
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────┐
│  /api/auth/logout?redirect_uri=  │
│         /current-page            │
└────────┬─────────────────────────┘
         │
         ├─► Call Laravel API (with Bearer token) ✅
         ├─► Clear all cookies
         │
         ▼
┌────────────────────────────────────┐
│ /auth?tab=login&redirect_uri=      │
│         /current-page              │
└────────────────────────────────────┘
```

## Security Enhancements

### 1. Open Redirect Prevention

```typescript
// ✅ Allowed
/dashboard
/courses/123
https://dev.experts.com.sa/profile

// ❌ Blocked (logs warning)
//evil.com
https://evil.com
javascript:alert(1)
```

### 2. URL Validation

All redirect URLs are validated against:

- Allowed domains (dev/stg/canary/prod experts.com.sa)
- Relative URL format (must start with `/`, not `//`)
- No protocol-relative URLs
- No JavaScript URLs

### 3. Fallback Behavior

Invalid URLs default to `/` instead of potentially dangerous redirects.

## Usage Examples

### 1. Login with Redirect

```typescript
// From a protected route
import { buildAuthUrl, getCurrentPageUrl } from "@/lib/auth/redirect-utils";

if (!session) {
  const currentUrl = getCurrentPageUrl();
  router.push(buildAuthUrl("login", currentUrl));
}
```

### 2. Logout with Return

```typescript
// Logout and return to current page
function LogoutButton() {
  const handleLogout = async () => {
    const current = window.location.pathname;
    const res = await fetch(
      `/api/auth/logout?redirect_uri=${encodeURIComponent(current)}`
    );

    const data = await res.json();
    router.push(data.redirect);
  };

  return <button onClick={handleLogout}>Logout</button>;
}
```

### 3. Protected Link

```typescript
// In a component
import {buildAuthUrl} from '@/lib/auth/redirect-utils';

function ProtectedLink({href, children}) {
  const {data: session} = useSession();

  const handleClick = (e) => {
    if (!session) {
      e.preventDefault();
      router.push(buildAuthUrl('login', href));
    }
  };

  return <a href={href} onClick={handleClick}>{children}</a>;
}
```

## Testing Checklist

- [ ] Login without redirect → goes to `/`
- [ ] Login with redirect → goes to specified page
- [ ] Logout from page → returns to same page after login
- [ ] Invalid redirect → blocked and goes to `/`
- [ ] Session expiry → redirects to login with current URL
- [ ] Bearer token sent correctly on logout
- [ ] All cookies cleared on logout
- [ ] Error states show proper messages

## Debugging

### Console Logs

Look for these helpful logs:

**Login:**

```
🔐 Login attempt: {email, redirectUrl}
✅ Login successful, redirecting to: /auth/callback?redirect_uri=...
```

**Callback:**

```
✅ Authentication successful: {user, accessToken, redirecting_to}
```

**Logout:**

```
🔓 Calling Laravel logout API...
✅ Logout API response: {data}
🔓 Logout successful, redirecting to: /auth?tab=login
```

**Security:**

```
🚨 Blocked invalid redirect URL: https://evil.com
```

## Breaking Changes

### None!

The system maintains backward compatibility:

- Old `origin + path + redirect_uri` format still works
- `/auth/redirect` page still exists (forwards to `/auth/callback`)
- All existing code continues to work

### Recommended Updates

While backward compatible, update to the new format:

**Old:**

```typescript
router.push(`/auth/redirect?origin=${origin}&path=${path}&redirect_uri=${uri}`);
```

**New:**

```typescript
import { buildAuthUrl } from "@/lib/auth/redirect-utils";
router.push(buildAuthUrl("login", uri));
```

## Benefits

1. **Simpler Flow**: One less redirect step
2. **Better Security**: Open redirect prevention
3. **More Robust**: Proper URL validation
4. **Better UX**: Clear error states, informative messages
5. **Easier Debugging**: Comprehensive logging
6. **Maintainable**: Centralized utilities
7. **Fixed Bugs**: Logout now properly sends Bearer token

## Next Steps

1. Test the new flow in development
2. Update any custom auth logic to use new utilities
3. Monitor logs for deprecated `/auth/redirect` usage
4. Plan to remove deprecated components in next major version

## Questions?

See the full documentation: `docs/AUTH_FLOW.md`
