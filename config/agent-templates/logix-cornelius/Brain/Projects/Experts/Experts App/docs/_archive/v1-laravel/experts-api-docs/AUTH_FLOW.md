---
title: "Enhanced Authentication Flow Documentation"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/experts-api-docs"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Enhanced Authentication Flow Documentation

## Overview

The authentication flow has been simplified and enhanced with robust redirect URL handling, removing the complicated subdomain redirect system in favor of a direct `/auth` path approach.

## Key Changes

### Before (Complex)

- Multiple redirect steps: Login → `/auth/redirect` → `/auth/callback` → Destination
- Complex URL parameter passing: `origin`, `path`, `redirect_uri`
- Subdomain redirects: `app.dev.experts.com.sa` → `auth.dev.experts.com.sa`
- 2-second artificial delays
- Confusing flow with multiple intermediate pages

### After (Simplified)

- Direct flow: Login → `/auth/callback` → Destination
- Single parameter: `redirect_uri` (with backward compatibility)
- Direct `/auth` path on same domain
- Immediate redirects (with minimal UX delay)
- Clear, predictable flow

## Authentication Flow

### 1. Login Flow

```
User visits protected page
  ↓
Redirect to /auth?redirect_uri=/protected-page
  ↓
User submits login form
  ↓
SignIn with NextAuth
  ↓
Redirect to /auth/callback?redirect_uri=/protected-page
  ↓
Session verified
  ↓
Redirect to /protected-page
```

### 2. Logout Flow

```
User clicks logout
  ↓
Call /api/auth/logout?redirect_uri=/some-page
  ↓
Revoke token via Laravel API
  ↓
Clear all auth cookies
  ↓
Redirect to /auth?tab=login&redirect_uri=/some-page
```

## File Structure

```
apps/experts-app/
├── lib/auth/
│   └── redirect-utils.ts          # Centralized redirect URL utilities
├── app/(auth)/auth/
│   └── forms/
│       └── login.tsx               # Enhanced login form
├── app/auth/
│   ├── callback/page.tsx           # Simplified callback handler
│   └── redirect/page.tsx           # Deprecated (kept for compatibility)
├── app/api/auth/
│   └── logout/route.ts             # Enhanced logout with proper token handling
└── packages/ui/src/
    ├── oauth-callback.tsx          # Enhanced callback component
    └── oauth-redirect.tsx          # Deprecated component
```

## Core Components

### 1. Redirect Utilities (`lib/auth/redirect-utils.ts`)

Centralized utilities for secure redirect URL handling:

```typescript
// Validate redirect URLs (prevent open redirects)
isValidRedirectUrl(url: string): boolean

// Sanitize and normalize URLs
sanitizeRedirectUrl(url: string | null | undefined): string

// Build redirect from params (supports legacy format)
buildRedirectUrl(params: RedirectParams): string

// Extract params from search params
extractRedirectParams(searchParams: URLSearchParams): RedirectParams

// Encode/decode for URL safety
encodeRedirectUrl(url: string): string
decodeRedirectUrl(encoded: string | null): string

// Build auth URLs with redirect
buildAuthUrl(tab: "login" | "register", redirectUrl?: string): string

// Get current page URL
getCurrentPageUrl(): string
```

### 2. Enhanced Login Form

**Features:**

- Extracts redirect params from URL
- Builds validated redirect URL
- Loading state during authentication
- Better error handling
- Redirects to `/auth/callback?redirect_uri=...`

**Usage:**

```typescript
// Navigate to login with redirect
router.push("/auth?tab=login&redirect_uri=/dashboard");
```

### 3. Enhanced Callback Page

**Features:**

- Validates redirect URLs (security)
- Supports both new and legacy URL formats
- Shows clear success/error states
- Automatic redirect with minimal delay
- Fallback to login if not authenticated

**Flow:**

1. Check for errors in URL params
2. Verify session is authenticated
3. Extract and validate `redirect_uri`
4. Show success message
5. Redirect to target (1.5s delay for UX)

### 4. Enhanced Logout Route

**Features:**

- Calls Laravel API to revoke token (with proper Bearer token)
- Clears all authentication cookies
- Validates redirect URLs
- Handles errors gracefully
- Logs all operations for debugging

**Usage:**

```typescript
// Logout and return to current page
fetch("/api/auth/logout?redirect_uri=" + window.location.pathname);

// Logout and go to home
fetch("/api/auth/logout?redirect_uri=/");
```

## Security Features

### 1. Open Redirect Prevention

Only allows redirects to:

- Relative URLs starting with `/` (not `//`)
- Absolute URLs on allowed domains:
  - `experts.com.sa`
  - `dev.experts.com.sa`
  - `stg.experts.com.sa`
  - `canary.experts.com.sa`
  - `prod.experts.com.sa`
  - `localhost`

### 2. URL Validation

```typescript
// ✅ Allowed
/dashboard
/courses/123
https://dev.experts.com.sa/profile

// ❌ Blocked
//evil.com
https://evil.com
javascript:alert(1)
```

### 3. Sanitization

- Removes `null` and `undefined` strings
- Trims whitespace
- Validates URL format
- Defaults to safe fallback (`/`)

## URL Parameters

### Redirect URI (New Standard)

**Parameter:** `redirect_uri`

**Description:** Direct URL to redirect after auth

**Examples:**

```
/auth?redirect_uri=/dashboard
/auth?redirect_uri=/courses/123
/auth/callback?redirect_uri=/profile
```

### Legacy Format (Backward Compatible)

**Parameters:** `origin`, `path`, `redirect_uri`

**Description:** Old format for compatibility

**Example:**

```
/auth?origin=https://app.dev.experts.com.sa&path=/auth/callback&redirect_uri=/dashboard
```

**Handled by:** `buildRedirectUrl()` in redirect-utils

## Usage Examples

### 1. Protected Route

```typescript
// middleware.ts or page component
import { buildAuthUrl, getCurrentPageUrl } from "@/lib/auth/redirect-utils";

if (!session) {
  const currentUrl = getCurrentPageUrl();
  const authUrl = buildAuthUrl("login", currentUrl);
  return NextResponse.redirect(authUrl);
}
```

### 2. Login Button

```typescript
import {buildAuthUrl} from '@/lib/auth/redirect-utils';

function LoginButton() {
  const handleLogin = () => {
    const authUrl = buildAuthUrl('login', window.location.pathname);
    router.push(authUrl);
  };

  return <button onClick={handleLogin}>Login</button>;
}
```

### 3. Logout Button

```typescript
function LogoutButton() {
  const handleLogout = async () => {
    const currentPath = window.location.pathname;
    const response = await fetch(
      `/api/auth/logout?redirect_uri=${encodeURIComponent(currentPath)}`
    );

    const data = await response.json();
    if (data.redirect) {
      router.push(data.redirect);
    }
  };

  return <button onClick={handleLogout}>Logout</button>;
}
```

### 4. After Registration

```typescript
// After successful registration
const redirectUrl = buildRedirectUrl({
  redirect_uri: "/onboarding",
});

router.push(`/auth/callback?redirect_uri=${encodeRedirectUrl(redirectUrl)}`);
```

## Debugging

### Console Logs

The enhanced flow includes comprehensive logging:

**Login:**

```
🔐 Login attempt: {email, redirectUrl}
✅ Login successful, redirecting to: /auth/callback?redirect_uri=...
```

**Callback:**

```
✅ Authentication successful: {user, accessToken, redirecting_to}
⚠️ Not authenticated in callback
❌ Still not authenticated, redirecting to login
```

**Logout:**

```
🔓 Calling Laravel logout API...
✅ Logout API response: {data}
⚠️ Error calling Laravel logout API (non-fatal)
🔓 Logout successful, redirecting to: /auth?tab=login
```

### Error States

All error states include user-friendly messages and proper logging:

- Invalid credentials
- Session expired
- Network errors
- Invalid redirect URLs
- Missing configuration

## Migration Guide

### For Existing Code

**Old way:**

```typescript
const params = `origin=${origin}&path=${path}&redirect_uri=${redirectUri}`;
router.push(`/auth/redirect?${params}`);
```

**New way:**

```typescript
import { buildAuthUrl } from "@/lib/auth/redirect-utils";

const authUrl = buildAuthUrl("login", redirectUri);
router.push(authUrl);
```

### Backward Compatibility

The system still supports the old format:

- `origin + path + redirect_uri` → automatically converted
- Old URLs still work but log warnings
- Gradual migration recommended

## Testing

### Test Cases

1. **Basic Login**
   - Navigate to `/auth?redirect_uri=/dashboard`
   - Submit credentials
   - Verify redirect to `/dashboard`

2. **Login Without Redirect**
   - Navigate to `/auth`
   - Submit credentials
   - Verify redirect to `/` (default)

3. **Logout**
   - Click logout from `/profile`
   - Verify redirect to `/auth?tab=login&redirect_uri=/profile`
   - Login again
   - Verify redirect to `/profile`

4. **Invalid Redirect**
   - Try `/auth?redirect_uri=https://evil.com`
   - Verify blocked and redirected to `/`

5. **Session Expiry**
   - Wait for session to expire
   - Try accessing protected route
   - Verify redirect to login with current URL

## Troubleshooting

### Issue: Redirect not working

**Check:**

1. Is `redirect_uri` properly URL encoded?
2. Is the URL on an allowed domain?
3. Check browser console for validation warnings

### Issue: Logout fails silently

**Check:**

1. Is `NEXTAUTH_SECRET` configured?
2. Are cookies being cleared? (Check DevTools → Application)
3. Check server logs for Laravel API errors

### Issue: Loop redirects

**Check:**

1. Is there a redirect loop in middleware?
2. Are both old and new redirect params present?
3. Check session state in callback

## Future Enhancements

- [ ] Add refresh token flow
- [ ] Support OAuth providers (Google, GitHub)
- [ ] Add remember me functionality
- [ ] Implement rate limiting
- [ ] Add audit logging
- [ ] Support MFA/2FA
- [ ] Add session management UI

## References

- [NextAuth.js Documentation](https://next-auth.js.org/)
- [OWASP Open Redirect Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html)
- [Laravel Passport Documentation](https://laravel.com/docs/passport)
