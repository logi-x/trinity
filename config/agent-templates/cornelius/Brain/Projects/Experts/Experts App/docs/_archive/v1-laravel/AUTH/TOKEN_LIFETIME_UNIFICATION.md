---
title: "Token and Session Lifetime Unification"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/auth"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Token and Session Lifetime Unification

## Current Configuration Analysis

### Laravel Passport (Backend)

**File**: `apps/experts-api/app/Providers/AppServiceProvider.php`

```php
Passport::tokensExpireIn(CarbonInterval::days(30));              // 30 days
Passport::refreshTokensExpireIn(CarbonInterval::months(3));      // 90 days
Passport::personalAccessTokensExpireIn(CarbonInterval::months(6)); // 180 days
```

### NextAuth (Frontend)

**File**: `apps/experts-app/src/packages/core/services/auth/shared-config.ts`

```typescript
session: {
    strategy: "jwt",
    maxAge: 180 * 24 * 60 * 60,  // 180 days (6 months)
    updateAge: 6 * 60 * 60,       // 6 hours
},
jwt: {
    maxAge: 180 * 24 * 60 * 60,  // 180 days (6 months)
}
```

---

## ⚠️ The Problem

**Timeline visualization**:

```
Day 0: User logs in
│
├─ Day 30: Access token expires ✅ (refreshes automatically)
│
├─ Day 60: Access token expires again ✅ (refreshes automatically)
│
├─ Day 90: Refresh token expires ❌ (CANNOT refresh anymore!)
│
├─ Day 180: Session expires ⏰ (but user already logged out at day 90!)
```

**Issue**: Session lasts 180 days, but refresh token only lasts 90 days.

**Result**:

- User thinks they're logged in (session valid)
- Access token expired at day 30
- Tries to refresh but refresh token expired at day 90
- Gets "RefreshAccessTokenError"
- **User force-logged out despite session showing as valid**

---

## ✅ Proposed Solution

### Strategy: Align Session with Refresh Token Lifetime

**Principle**: Session should never outlive the ability to refresh access tokens.

### Recommended Configuration

```
Access Token:    30 days   (keeps security tight)
Refresh Token:   90 days   (3 months - reasonable balance)
Session:         90 days   (3 months - matches refresh token)
Update Age:      6 hours   (session extends with activity)
```

**Benefits**:

1. ✅ Session lifetime never exceeds refresh token capability
2. ✅ Access tokens refresh automatically every 30 days
3. ✅ Users stay logged in for 90 days with activity
4. ✅ Inactive users (>90 days) must re-authenticate
5. ✅ Clear, predictable behavior

---

## Alternative Strategies

### Option 1: Long-Lived Everything (Less Secure)

```
Access Token:    90 days
Refresh Token:   90 days
Session:         90 days
```

**Pros**: Simpler, less frequent refreshes
**Cons**: Compromised access token valid for 90 days (security risk)

### Option 2: Short-Lived Tokens (Most Secure)

```
Access Token:    1 day
Refresh Token:   90 days
Session:         90 days
```

**Pros**: Maximum security, frequent token rotation
**Cons**: More frequent refresh operations, potential UX impact

### Option 3: Extended Everything (Enterprise)

```
Access Token:    30 days
Refresh Token:   180 days (6 months)
Session:         180 days (6 months)
```

**Pros**: Better UX, fewer re-logins
**Cons**: Refresh tokens valid for 6 months (higher risk if compromised)

---

## Recommended Changes

### 1. Backend (Laravel Passport)

**Keep as is** - current configuration is good:

```php
Passport::tokensExpireIn(CarbonInterval::days(30));          // 30 days
Passport::refreshTokensExpireIn(CarbonInterval::months(3));  // 90 days
Passport::personalAccessTokensExpireIn(CarbonInterval::months(6)); // 180 days (mobile/API)
```

### 2. Frontend (NextAuth)

**Change** session to match refresh token:

```typescript
session: {
    strategy: "jwt",
    maxAge: 90 * 24 * 60 * 60,   // 90 days (3 months) - CHANGED
    updateAge: 6 * 60 * 60,       // 6 hours (keep as is)
},
jwt: {
    maxAge: 90 * 24 * 60 * 60,   // 90 days (3 months) - CHANGED
}
```

---

## Impact Analysis

### User Experience

**Before** (Broken):

- Day 0: Login successful
- Day 30: Token refreshes (transparent)
- Day 60: Token refreshes (transparent)
- Day 90: Refresh fails, user logged out unexpectedly
- Day 91-180: Session shows valid but unusable

**After** (Fixed):

- Day 0: Login successful
- Day 30: Token refreshes (transparent)
- Day 60: Token refreshes (transparent)
- Day 90: Session expires, user logs in again
- Clear communication: "Session expired, please log in"

### Security

| Aspect          | Before   | After   | Impact                                 |
| --------------- | -------- | ------- | -------------------------------------- |
| Access Token    | 30 days  | 30 days | ✅ No change                           |
| Refresh Token   | 90 days  | 90 days | ✅ No change                           |
| Session         | 180 days | 90 days | ✅ **Improved** - aligns with security |
| Inactive Logout | Broken   | 90 days | ✅ **Fixed** - predictable behavior    |

### Mobile Apps (Direct Login)

**No impact** - they use Personal Access Tokens (180 days):

```php
Passport::personalAccessTokensExpireIn(CarbonInterval::months(6)); // Still 6 months
```

---

## Implementation Steps

1. ✅ Update NextAuth session configuration
2. ✅ Update NextAuth JWT configuration
3. ✅ Test token refresh at day 30
4. ✅ Test session expiry at day 90
5. ✅ Update documentation

---

## Testing Scenarios

### Scenario 1: Active User

```
Day 0:  Login
Day 30: Token refresh (automatic) ✅
Day 60: Token refresh (automatic) ✅
Day 89: Still logged in ✅
Day 90: Session expires, prompt re-login ✅
```

### Scenario 2: Inactive User

```
Day 0:  Login
Day 45: Inactive (no visits)
Day 90: Returns, session expired, re-login required ✅
```

### Scenario 3: Very Active User

```
Day 0:  Login
Day 30: Token refresh ✅
Day 60: Token refresh ✅
Day 90: Session would expire, but updateAge (6 hours) extends it
Day 95: Still active, session extended ✅
```

**Note**: With `updateAge: 6 hours`, active users can stay logged in beyond 90 days as long as they use the app at least once every 6 hours.

---

## Rollback Plan

If issues arise:

```typescript
// Revert to original configuration
session: {
    maxAge: 180 * 24 * 60 * 60,  // Back to 6 months
    updateAge: 6 * 60 * 60,
}
```

But fix the root cause: implement proper token refresh error handling.

---

## Recommendation

**Implement the proposed changes** (90-day alignment):

✅ **Pros**:

- Fixes session/token mismatch
- Clear, predictable behavior
- Good security/UX balance
- Aligns with industry standards

⚠️ **Consideration**:

- Users will need to re-login every 90 days of inactivity (down from theoretical 180 days)
- This is actually better UX than silent failures!

---

**Decision Required**: Approve 90-day unified configuration?
