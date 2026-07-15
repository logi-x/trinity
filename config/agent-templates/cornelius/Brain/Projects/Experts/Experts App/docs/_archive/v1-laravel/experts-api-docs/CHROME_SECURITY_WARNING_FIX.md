---
title: "🔒 Chrome Security Warning Fix"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/experts-api-docs"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🔒 Chrome Security Warning Fix

## Problem

Chrome showed "Dangerous site" warning when accessing:

```
❌ https://app.dev.experts.com.sa/api/auth/callback?token=eyJ0eXAiOiJKV1...
```

**Warning message:**

> Attackers on the site you tried visiting might trick you into installing software or revealing things like your passwords, phone, or credit card numbers.

---

## Why Chrome Blocked It

### Tokens in URLs Are Insecure

**Problems:**

1. ✍️ **Logged everywhere:** Browser history, server logs, proxy logs, analytics
2. 🔗 **Shareable:** Copy URL = copy token
3. 👁️ **Visible:** Over-shoulder viewing, screenshots
4. 📱 **Referrer leaks:** Token sent to external sites via Referer header
5. 🚨 **Chrome detects pattern:** Long random strings in URLs = likely tokens

**Example attack:**

```
User copies URL: https://app.../callback?token=abc123...
Sends to friend: "Check out this cool app!"
Friend gets URL: Now has user's auth token! 💀
```

---

## Solution: Temporary Code Exchange

### Old Flow (Insecure) ❌

```
┌─────────────────────┐
│  Laravel OAuth      │
│  callback           │
└──────────┬──────────┘
           │
           ▼
┌───────────────────────────────────────┐
│  Redirect with token in URL           │
│  ?token=eyJ0eXAi...&refresh_token=... │ ❌ INSECURE!
└──────────┬────────────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Chrome blocks 🚫  │
│  "Dangerous site"   │
└─────────────────────┘
```

### New Flow (Secure) ✅

```
┌──────────────────────┐
│  Laravel OAuth       │
│  callback            │
└──────────┬───────────┘
           │
           ▼
┌────────────────────────────────────┐
│  Generate temporary code           │
│  Cache::put("oauth:{code}", {...}) │
└──────────┬─────────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  Redirect with code only           │
│  ?code=abc123...                   │ ✅ SECURE!
└──────────┬─────────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  Next.js callback                  │
│  POST /v1/auth/exchange-code       │
│  { "code": "abc123..." }           │
└──────────┬─────────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  Laravel validates code            │
│  Returns token data                │
│  Deletes code (one-time use)       │
└──────────┬─────────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  Next.js stores in httpOnly cookie│
│  Redirects to /auth/signin-callback│
└──────────┬─────────────────────────┘
           │
           ▼
┌────────────────────────────────────┐
│  ✅ No Chrome warning!              │
│  ✅ Token never in URL!             │
└────────────────────────────────────┘
```

---

## Implementation

### 1. Laravel OAuth Callback

**File:** `apps/experts-api/routes/web.php`

```php
use Illuminate\Support\Facades\Cache;

Route::get('/oauth/callback', function (Request $request) {
  // Get token from Laravel Passport
  $response = Http::asForm()->post('https://auth.../oauth/token', [...]);
  $responseData = $response->json();

  // ✅ Generate temporary code
  $tempCode = Str::random(64);

  // ✅ Store token data in cache (5-minute expiry)
  Cache::put("oauth_callback:{$tempCode}", [
    'token' => $responseData['access_token'],
    'expires_in' => $responseData['expires_in'],
    'refresh_token' => $responseData['refresh_token'],
    'token_type' => $responseData['token_type'],
    'scope' => $responseData['scope'] ?? '*',
    'callback_url' => $callbackUrl,
  ], now()->addMinutes(5));

  // ✅ Redirect with code only (not token!)
  $query = http_build_query(['code' => $tempCode]);
  $targetUrl = 'https://app.dev.../api/auth/callback?' . $query;

  return Inertia::location($targetUrl);
});
```

### 2. Laravel Code Exchange Endpoint

**File:** `app/Domains/Auth/Controllers/CodeExchangeController.php`

```php
/**
 * Exchange temporary code for OAuth token data
 *
 * @unauthenticated
 * @bodyParam code string required Temporary code
 */
public function exchange(Request $request): JsonResponse
{
    $code = $request->validate(['code' => 'required|string|size:64'])['code'];

    // ✅ Retrieve from cache
    $tokenData = Cache::get("oauth_callback:{$code}");

    if (!$tokenData) {
        return $this->error('Invalid or expired code', 400);
    }

    // ✅ Delete immediately (one-time use)
    Cache::forget("oauth_callback:{$code}");

    return $this->success($tokenData);
}
```

**Route:** `POST /v1/auth/exchange-code`

### 3. Next.js Callback Route

**File:** `app/api/auth/callback/route.ts`

```typescript
export async function GET(request: NextRequest) {
  // ✅ Extract code (not token!)
  const code = url.searchParams.get("code");

  if (!code) {
    return NextResponse.redirect("/auth/error?msg=missing_code");
  }

  // ✅ Exchange code for token data
  const tokenResponse = await fetch(`${apiUrl}/v1/auth/exchange-code`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Api-Version': 'v1',
    },
    body: JSON.stringify({code}),
  });

  const tokenData = await tokenResponse.json();
  const {token, expires_in, refresh_token, ...} = tokenData.data;

  // ✅ Store in httpOnly cookies
  response.cookies.set({
    name: '__Secure-experts.access-token',
    value: token,
    httpOnly: true,
    secure: true,
    // ...
  });

  // ✅ Redirect to signin-callback (no token in URL!)
  return NextResponse.redirect('/auth/signin-callback');
}
```

---

## Security Benefits

### Before (Insecure)

```
URL: /callback?token=eyJ0eXAiOiJKV1QiLCJhbGciOi...
❌ Token in browser history
❌ Token in server logs
❌ Token shareable via URL
❌ Chrome security warning
❌ Token visible in network tab
```

### After (Secure)

```
URL: /callback?code=abc123def456
✅ Code is temporary (5-minute expiry)
✅ Code is one-time use (deleted after exchange)
✅ Code is random (64 characters)
✅ Token transferred via POST body (not URL)
✅ Token stored in httpOnly cookies
✅ No Chrome warning!
```

---

## Additional Security Features

### 1. One-Time Use Codes

```php
// Code can only be used once
Cache::forget("oauth_callback:{$code}");
```

### 2. Short Expiry

```php
// Code expires in 5 minutes
Cache::put($key, $data, now()->addMinutes(5));
```

### 3. Code Validation

```php
// Code must be exactly 64 characters
$request->validate(['code' => 'required|string|size:64']);
```

### 4. HTTPS Only

```typescript
// Cookies are secure
httpOnly: true,
secure: true,
sameSite: "lax",
```

---

## Testing

### Expected Flow

1. Complete OAuth login
2. Redirect to: `https://app.dev.../api/auth/callback?code=abc123...`
3. ✅ **No Chrome warning!** (code, not token)
4. Code exchanged for token via POST
5. Token stored in httpOnly cookie
6. Redirect to signin-callback
7. Login completes

### Console Logs

```
📥 OAuth Callback - Code received
✅ Code exchanged successfully
✅ Token received: eyJ0eXAiOiJKV1...
✅ Stored in httpOnly cookie
✅ Redirecting to signin-callback
```

---

## Comparison

| Aspect              | Before  | After  |
| ------------------- | ------- | ------ |
| **Chrome Warning**  | Yes     | None   |
| **Token in URL**    | Yes     | No     |
| **Token in Logs**   | Yes     | No     |
| **Shareable Token** | Yes     | No     |
| **Security Level**  | Low     | High   |
| **User Experience** | Blocked | Smooth |

---

## Related Standards

- [OAuth 2.0 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

**Key principle:** Never put sensitive data (tokens, passwords, keys) in URLs!

---

## Summary

**Problem:** Chrome blocking callback URL with token in query params

**Fix:** Use temporary code exchange pattern

**Result:** ✅ No security warnings, improved security, smooth UX! 🎉
