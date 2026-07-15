---
title: "Token Lifetime Configuration Summary"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/auth"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Token Lifetime Configuration Summary

**Date:** 2025-11-07

## Overview

This document outlines the complete token lifetime configuration across the authentication system, including Laravel Passport (backend), NextAuth (session management), and the unified SDK.

## Token Lifetimes by Layer

### 1. Laravel Passport (Backend) - OAuth Tokens

**Configuration Location:** Laravel application (configured via Passport)

| Token Type                 | Lifetime                     | Notes                       |
| -------------------------- | ---------------------------- | --------------------------- |
| **Personal Access Tokens** | **6 months** (180 days)      | Used for API authentication |
| **OAuth Access Tokens**    | **30 days** (4 weeks 2 days) | Standard OAuth tokens       |
| **Refresh Tokens**         | N/A (not configured)         | Not currently used          |

**Source:** Verified via `php artisan tinker`

```php
Passport::personalAccessTokensExpireIn() // 6 months
Passport::tokensExpireIn()              // 4 weeks 2 days
```

**Important Notes:**

- The login endpoint returns **Personal Access Tokens** (6-month lifetime)
- These are the tokens stored in NextAuth JWT and used for API calls
- Token refresh creates a **new** Personal Access Token with full 6-month lifetime
- Old token is **revoked** immediately upon refresh

---

### 2. NextAuth JWT Token (Session Management)

**Configuration Location:** `packages/core/services/auth/shared-config.ts:90-97`

```typescript
session: {
  strategy: "jwt",
  maxAge: 180 * 24 * 60 * 60,    // 6 months (session cookie)
  updateAge: 6 * 60 * 60,          // 6 hours (session update interval)
},
jwt: {
  maxAge: 180 * 24 * 60 * 60,      // 6 months (JWT token)
}
```

| Setting               | Value                   | Purpose                                          |
| --------------------- | ----------------------- | ------------------------------------------------ |
| **JWT maxAge**        | **6 months** (180 days) | Maximum lifetime of the JWT token itself         |
| **Session maxAge**    | **6 months** (180 days) | Maximum lifetime of the session cookie           |
| **Session updateAge** | **6 hours**             | How often to update session expiry with activity |

**Important Notes:**

- The JWT token itself can live for **6 months**
- Session cookie refreshes every **6 hours** of activity
- This is the **NextAuth session layer**, not the Laravel token

---

### 3. Laravel Passport Access Token in JWT

**Configuration Location:** `packages/core/services/auth/shared-config.ts:128-133`

```typescript
const expiresIn = account.expires_in || 3600; // Default 1 hour if not provided

const newToken = {
  accessToken: (user as any).accessToken as string,
  accessTokenExpires: Date.now() + expiresIn * 1000,
  // ... other fields
};
```

| Setting                 | Value                     | Source                                            |
| ----------------------- | ------------------------- | ------------------------------------------------- |
| **accessTokenExpires**  | **3600 seconds (1 hour)** | Default when Laravel doesn't provide `expires_in` |
| **Actual from Laravel** | **Variable**              | Laravel should return token expiry in response    |

**The Problem:**
The code sets `accessTokenExpires` based on `account.expires_in`, which comes from the Laravel login response. However:

1. **Laravel Passport tokens actually live for 6 months** (as configured)
2. **But the code defaults to 1 hour** if `expires_in` is not provided
3. This causes unnecessary token refresh attempts every hour

---

### 4. SDK Token Cache

**Configuration Location:** `packages/sdk/src/config.ts:4-6`

```typescript
let cachedToken: string | null = null;
let tokenExpiry: number = 0;
const CACHE_DURATION = 60000; // 1 minute cache
```

| Setting            | Value        | Purpose                                |
| ------------------ | ------------ | -------------------------------------- |
| **Cache Duration** | **1 minute** | Reduces overhead on frequent API calls |

**Important Notes:**

- This is a **performance optimization** layer
- Caches the resolved token for 1 minute
- Does **not** affect actual token lifetime

---

## Complete Token Lifecycle

### Initial Login

```
User logs in
    ↓
Laravel creates Personal Access Token (6-month lifetime)
    ↓
NextAuth JWT callback receives token
    ↓
Sets accessTokenExpires = now + (expires_in || 3600) seconds
    ↓
Stores in NextAuth JWT (6-month max lifetime)
    ↓
User authenticated
```

**Current Issue:** If Laravel doesn't provide `expires_in`, it defaults to **1 hour**, even though the actual token lives for **6 months**.

### Token Refresh Flow

```
JWT callback checks if accessTokenExpires < now
    ↓
Calls refreshAccessToken()
    ↓
SDK calls POST /v1/refresh-token with current token
    ↓
Laravel revokes old token, creates new token (6-month lifetime)
    ↓
Returns new token with expires_in
    ↓
Updates JWT with new token and expiry
```

---

## Token Expiry Timeline

Based on current configuration:

| Time          | Event                                                           |
| ------------- | --------------------------------------------------------------- |
| **T+0**       | User logs in, receives Passport token (6-month actual lifetime) |
| **T+1 hour**  | NextAuth thinks token expired (due to 1-hour default)           |
| **T+1 hour**  | Attempts token refresh                                          |
| **T+1 hour**  | Gets new Passport token (new 6-month lifetime)                  |
| **T+2 hours** | Another refresh attempt                                         |
| **Repeat**    | Refreshes every hour unnecessarily                              |

**Actual Passport Token:** Would be valid for 6 months without refresh

---

## Recommendations

### 1. Fix Token Expiry Mismatch

**Problem:** NextAuth defaults to 1-hour expiry when Laravel Passport tokens actually live 6 months.

**Solution:** Ensure Laravel returns `expires_in` in login response, or update default:

```typescript
// Option A: Fix Laravel to return expires_in
// In AuthController.php login response:
return $this->success([
    'token' => $token->accessToken,
    'token_type' => 'Bearer',
    'expires_in' => 15552000, // 6 months in seconds
    'user' => $user
]);

// Option B: Update NextAuth default to match Passport
const expiresIn = account.expires_in || 15552000; // 6 months default
```

### 2. Align Token Lifetimes

Consider standardizing token lifetimes across the stack:

| Recommendation          | Setting   | Reasoning                                |
| ----------------------- | --------- | ---------------------------------------- |
| **Short-lived tokens**  | 1-2 hours | More secure, uses refresh mechanism      |
| **Medium-lived tokens** | 24 hours  | Balance of security and UX               |
| **Long-lived tokens**   | 6 months  | Current setup, less secure but better UX |

### 3. Implement Refresh Tokens

Instead of creating new Personal Access Tokens on refresh:

- Use OAuth refresh tokens
- Keep access tokens short-lived (1 hour)
- Use refresh tokens (30-90 days) to get new access tokens
- More secure than reissuing long-lived tokens

### 4. Monitor Token Refresh Frequency

Add analytics to track:

- How often tokens are refreshed
- How many refreshes fail
- Average token lifetime before refresh

---

## Current Configuration Issues

### Issue #1: Token Expiry Mismatch

- **What:** NextAuth thinks tokens expire in 1 hour, but they actually live 6 months
- **Impact:** Unnecessary token refresh every hour
- **Severity:** Medium (wastes API calls, but doesn't break functionality)

### Issue #2: No Refresh Token Implementation

- **What:** Using Personal Access Tokens for everything
- **Impact:** Less secure than proper OAuth flow with refresh tokens
- **Severity:** Low (acceptable for current use case)

### Issue #3: 401 Errors on Refresh

- **What:** Token refresh getting 401 Unauthorized from Laravel
- **Impact:** Token refresh failing, forcing re-authentication
- **Severity:** **HIGH** (breaks the refresh mechanism)
- **Root Cause:** Being investigated (token not being sent or recognized)

---

## Summary

**Current Token Lifetimes:**

| Layer                          | Configured     | Actual Behavior       |
| ------------------------------ | -------------- | --------------------- |
| Laravel Passport               | 6 months       | ✅ 6 months           |
| NextAuth JWT                   | 6 months       | ✅ 6 months           |
| Passport Token (stored in JWT) | 1 hour default | ⚠️ Should be 6 months |
| SDK Cache                      | 1 minute       | ✅ 1 minute           |

**Key Takeaway:**
The Passport tokens themselves are valid for **6 months**, but NextAuth is configured to think they expire in **1 hour** (default), causing unnecessary refresh attempts.

**Priority Fix:**

1. Ensure Laravel returns `expires_in: 15552000` (6 months) in login response
2. Fix the 401 error on token refresh (current blocker)
3. Consider implementing proper OAuth refresh tokens for better security
