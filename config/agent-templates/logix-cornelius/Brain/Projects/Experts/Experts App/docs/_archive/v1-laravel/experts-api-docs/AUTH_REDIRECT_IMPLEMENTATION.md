---
title: "Authenticated User Auth Page Redirect Implementation"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/experts-api-docs"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Authenticated User Auth Page Redirect Implementation

## Problem

Authenticated users could still access auth pages, creating bad UX:

- `https://auth.experts.com.sa/*` (auth subdomain)
- `https://app.experts.com.sa/auth/*` (auth path)

## Solution

### 1. Created Middleware (`middleware.ts`)

Next.js middleware that executes on every request to:

- Check user authentication status via session token
- Redirect authenticated users away from auth pages
- Allow NextAuth callback routes to pass through

**File**: `/middleware.ts`

```typescript
export async function middleware(request) {
  return proxy(request);
}
```

### 2. Updated Proxy Logic (`proxy.ts`)

Added authentication redirect logic:

```typescript
// Redirect authenticated users away from auth pages
const isAuthPage = host.startsWith("auth.") || pathname.startsWith("/auth");
const isAuthCallback =
  pathname.startsWith("/auth/callback") || pathname.startsWith("/api/auth");

if (accessToken && isAuthPage && !isAuthCallback) {
  console.log(
    "🔐 Authenticated user accessing auth page - redirecting to home",
  );
  const homeUrl = new URL(
    process.env.NEXT_PUBLIC_APP_URL || "https://app.experts.com.sa",
  );
  return NextResponse.redirect(homeUrl);
}
```

**Protected Routes**:

- ❌ `https://auth.experts.com.sa/*` → Redirects to app home
- ❌ `https://app.experts.com.sa/auth/*` → Redirects to app home
- ✅ `https://app.experts.com.sa/auth/callback` → Allowed (NextAuth)
- ✅ `https://app.experts.com.sa/api/auth/*` → Allowed (NextAuth API)

### 3. Updated Middleware Matcher

Removed `auth` from exclusions to allow middleware to run on auth paths:

```typescript
// Before
matcher: ["/((?!_next|static|favicon.ico|api|auth|oauth|...).*)"];

// After
matcher: ["/((?!_next|static|favicon.ico|api|oauth|...).*)"];
//                                               ^^^^ removed
```

## How It Works

### Flow for Authenticated Users

```
1. User logs in → Session created with accessToken
2. User tries to visit auth.experts.com.sa
3. Middleware checks session → accessToken exists
4. Checks if visiting auth page → YES
5. Checks if auth callback → NO
6. Redirects to home → https://app.experts.com.sa
```

### Flow for Unauthenticated Users

```
1. User (not logged in) → No session/accessToken
2. User visits auth.experts.com.sa
3. Middleware checks session → No accessToken
4. Allows request → Shows login page
```

### Flow for Auth Callbacks

```
1. User completes OAuth/login
2. Redirected to /auth/callback
3. Middleware checks session → Might have accessToken
4. Checks if auth callback → YES
5. Allows request → NextAuth processes callback
6. After callback, session established
7. NextAuth redirects to app
```

## Testing

### Test 1: Authenticated User on Auth Subdomain

1. **Login** to the app
2. Navigate to `https://auth.experts.com.sa`
3. **Expected**: Immediately redirected to `https://app.experts.com.sa`
4. **Console**: Should see `🔐 Authenticated user accessing auth page - redirecting to home`

### Test 2: Authenticated User on Auth Path

1. **Login** to the app
2. Navigate to `https://app.experts.com.sa/auth`
3. **Expected**: Immediately redirected to `https://app.experts.com.sa`
4. **Console**: Should see `🔐 Authenticated user accessing auth page - redirecting to home`

### Test 3: Unauthenticated User

1. **Logout** or use incognito
2. Navigate to `https://auth.experts.com.sa`
3. **Expected**: See login page (no redirect)

### Test 4: Login Flow Still Works

1. **Logout**
2. Navigate to `https://auth.experts.com.sa`
3. **Login** with credentials
4. **Expected**: After successful login, redirected to app home
5. **Verify**: Login successful, session active

### Test 5: OAuth Callbacks Work

1. **Logout**
2. Try **GitHub/Google OAuth** login
3. **Expected**: OAuth flow completes, redirected to app
4. **Verify**: Callback route wasn't blocked

## Environment Variables Used

- `NEXT_PUBLIC_APP_URL` - Home URL to redirect to (default: `https://app.experts.com.sa`)
- `NEXTAUTH_SECRET` - Required for session validation

## Files Modified

1. **Created**: `/middleware.ts` - Next.js middleware entry point
2. **Modified**: `/proxy.ts` - Added auth redirect logic and updated matcher
3. **Created**: This documentation file

## Troubleshooting

### Issue: Still Can Access Auth Pages When Logged In

**Check**:

1. Restart your dev server (middleware changes require restart)
2. Clear cookies and re-login
3. Check console for `🔐 Authenticated user accessing auth page` message
4. Verify `NEXT_PUBLIC_APP_URL` is set correctly

### Issue: Can't Login (Redirect Loop)

**Check**:

1. Make sure auth callbacks are excluded (line 57 in proxy.ts)
2. Check `/api/auth/*` routes are working
3. Verify `NEXTAUTH_SECRET` is set

### Issue: 401 Error During Login

This is a separate issue related to token refresh - see the earlier fix with:

- Auto-logout on `RefreshAccessTokenError`
- Simplified auth config without refresh tokens

## Related Changes

This complements the earlier auth fixes:

1. ✅ Auto-logout when token refresh fails
2. ✅ Redirect authenticated users from auth pages (this change)
3. ⏳ Simplified auth config without refresh complexity (optional)
