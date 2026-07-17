---
title: "Authentication Flows: Web App vs Mobile App"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/auth"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Authentication Flows: Web App vs Mobile App

## Two Different Authentication Methods

### 1. Next.js Web App (OAuth2 PKCE Flow)

**Endpoint**: `/oauth/redirect` → `/oauth/callback`

**Flow**:

```
User → Next.js → Laravel OAuth (/oauth/redirect)
     → Passport Authorization
     → OAuth Callback (/oauth/callback)
     → Temporary Code Exchange
     → Next.js creates session
```

**Tokens Created**:

- ✅ **Access Token**: 30 days (OAuth2 token)
- ✅ **Refresh Token**: 90 days (OAuth2 refresh token)
- ✅ **Session**: 180 days (NextAuth JWT)

**Configuration**:

```php
// apps/experts-api/app/Providers/AppServiceProvider.php
Passport::tokensExpireIn(CarbonInterval::days(30));          // ← Used for OAuth2
Passport::refreshTokensExpireIn(CarbonInterval::months(3));  // ← Used for OAuth2
```

**How it works**:

1. Access token expires after 30 days
2. Frontend automatically calls `/oauth/refresh` with refresh token
3. Gets new access token + new refresh token
4. Repeats until refresh token expires (90 days)

---

### 2. Mobile Apps & Direct API (Personal Access Tokens)

**Endpoint**: `POST /v1/auth/login`

**Code**:

```php
// apps/experts-api/app/Domains/Auth/Controllers/AuthController.php (line 267)
$token = $user->createToken(config('session.cookie'), $scopes);

return [
    'token' => $token->accessToken,
    'token_type' => 'Bearer',
    'expires_in' => 15552000, // 6 months = 180 days
];
```

**Token Created**:

- ✅ **Personal Access Token (PAT)**: 180 days
- ❌ **No Refresh Token**: PATs don't support refresh

**Configuration**:

```php
// apps/experts-api/app/Providers/AppServiceProvider.php
Passport::personalAccessTokensExpireIn(CarbonInterval::months(6)); // ← Used for PATs
```

**How it works**:

1. User logs in with email/password
2. Gets a single long-lived token (180 days)
3. **No refresh mechanism** - token valid for full 180 days
4. After 180 days, user must log in again

---

## Why Mobile Apps Use PATs Instead of OAuth2

### Technical Reasons

1. **Simplicity**: Mobile apps store a single token, no need for refresh logic
2. **Offline Support**: PATs work without internet for token refresh
3. **Native Experience**: No web redirects or browser interactions
4. **Consistency**: Same token across app reinstalls (until expiry)

### `createToken()` Method

**What it does**:

```php
$token = $user->createToken('token-name', ['scope1', 'scope2']);
// ↓
// Creates a Personal Access Token in oauth_access_tokens table
// with 'personal_access_client' = true
// Expiry governed by personalAccessTokensExpireIn()
```

**vs OAuth2 tokens**:

```php
// OAuth2 creates tokens via /oauth/token endpoint
// with client_id, code_verifier, etc.
// Expiry governed by tokensExpireIn() + refreshTokensExpireIn()
```

---

## Database Evidence

Run this to see the difference:

```sql
SELECT
    id,
    user_id,
    client_id,
    name,
    scopes,
    expires_at,
    CASE
        WHEN name IS NOT NULL THEN 'Personal Access Token'
        ELSE 'OAuth2 Token'
    END as token_type
FROM oauth_access_tokens
ORDER BY created_at DESC
LIMIT 10;
```

**Personal Access Tokens** have:

- ✅ `name` field populated (e.g., "experts-session")
- ✅ Longer expiry (180 days)
- ❌ No linked refresh token

**OAuth2 Tokens** have:

- ❌ `name` field = NULL
- ✅ Shorter expiry (30 days)
- ✅ Linked refresh token in `oauth_refresh_tokens`

---

## Current Configuration Summary

| Aspect                  | Web App (OAuth2)    | Mobile App (PAT)                 |
| ----------------------- | ------------------- | -------------------------------- |
| **Endpoint**            | `/oauth/redirect`   | `/v1/auth/login`                 |
| **Token Type**          | OAuth2 Access Token | Personal Access Token            |
| **Access Token Expiry** | 30 days             | 180 days                         |
| **Refresh Token**       | Yes (90 days)       | No                               |
| **Session**             | 180 days (NextAuth) | N/A                              |
| **Refresh Mechanism**   | Automatic           | None - re-login required         |
| **Configuration**       | `tokensExpireIn()`  | `personalAccessTokensExpireIn()` |

---

## The Mismatch Problem (Web App Only!)

**Web App Issue**:

```
Day 0:   Login (OAuth2)
Day 30:  Access token expires → refresh ✅
Day 60:  Access token expires → refresh ✅
Day 90:  Refresh token expires → CANNOT refresh ❌
Day 180: Session expires (but broken since day 90)
```

**Mobile App**: NO ISSUE!

```
Day 0:   Login → PAT issued (180 days)
Day 180: PAT expires → Re-login required ✅
```

Mobile apps are unaffected because they use a completely different token system!

---

## Recommendation: Why Mobile Apps DON'T Need Changes

### Current Mobile App Flow is Fine

```php
Passport::personalAccessTokensExpireIn(CarbonInterval::months(6)); // Keep as 180 days
```

**Reasons**:

1. ✅ **No refresh complexity** - single token, simple to manage
2. ✅ **Better UX** - users stay logged in for 6 months
3. ✅ **Industry standard** - mobile apps typically use longer-lived tokens
4. ✅ **No background refresh** - avoids battery/network overhead

### Only Web App Needs Fix

```typescript
// apps/experts-app/src/packages/core/services/auth/shared-config.ts
session: {
    maxAge: 90 * 24 * 60 * 60,  // Change: 180 → 90 days
}
```

**Why**: Align web app session with OAuth2 refresh token lifetime (90 days)

---

## Alternative: Mobile Apps Could Use OAuth2 (Not Recommended)

**If you wanted to**, mobile apps could use OAuth2 PKCE:

```
iOS/Android → Open in-app browser
           → Navigate to /oauth/redirect
           → User authenticates
           → Redirect with code
           → App exchanges code for tokens
           → Store access + refresh token
           → Implement refresh logic
```

**Why we DON'T do this**:

- ❌ More complex implementation
- ❌ Requires in-app browser
- ❌ Worse UX (browser redirects)
- ❌ Refresh logic adds battery drain
- ✅ PATs are simpler and equally secure for mobile

---

## Summary

| Question                                           | Answer                                        |
| -------------------------------------------------- | --------------------------------------------- |
| **Do mobile apps use OAuth2?**                     | No, they use Personal Access Tokens (PATs)    |
| **How do mobile apps get tokens?**                 | `POST /v1/auth/login` → direct token issuance |
| **Do mobile apps have refresh tokens?**            | No, PATs don't support refresh                |
| **How long do mobile tokens last?**                | 180 days (6 months)                           |
| **Are mobile apps affected by the web app issue?** | No, they use different token system           |
| **Should we change mobile app configuration?**     | No, keep PATs at 180 days                     |
| **What needs to change?**                          | Only web app session (180 → 90 days)          |

---

**Conclusion**: Mobile apps use a completely separate authentication system (Personal Access Tokens via `/v1/auth/login`) and are **not affected** by the web app OAuth2 token lifecycle mismatch.
