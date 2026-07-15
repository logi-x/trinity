---
title: "Token Refresh Testing Instructions"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/auth"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Token Refresh Testing Instructions

## Quick Test

Run the automated test script:

```bash
cd /home/logix/experts

# Test with default credentials (test@example.com / password)
./test-refresh-token.sh

# Or with custom credentials
./test-refresh-token.sh your-email@example.com your-password
```

This script will:

1. ✅ Login and get an access token
2. ✅ Refresh the token
3. ✅ Verify old token is revoked
4. ✅ Verify new token works

---

## Manual Testing

### Step 1: Login

```bash
curl -X POST https://api.dev.experts.com.sa/v1/auth/login \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"email":"test@example.com","password":"password"}' | jq '.'
```

**Copy the token from the response** (under `.data.token`)

### Step 2: Refresh Token

Replace `YOUR_TOKEN_HERE` with the token from Step 1:

```bash
curl -X POST https://api.dev.experts.com.sa/v1/auth/refresh-token \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" | jq '.'
```

**Expected Success Response:**

```json
{
  "status": "success",
  "success": true,
  "message": "Token refreshed successfully.",
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...",
    "token_type": "Bearer",
    "expires_in": 3600
  },
  "code": 200,
  "timestamp": "2025-10-31T..."
}
```

### Step 3: Verify Old Token is Revoked

Try using the OLD token again (should fail):

```bash
curl -X POST https://api.dev.experts.com.sa/v1/auth/refresh-token \
  -H "Authorization: Bearer OLD_TOKEN_HERE" | jq '.'
```

**Expected Error Response:**

```json
{
  "status": "error",
  "success": false,
  "message": "Unauthorized",
  "code": 401
}
```

---

## Test via Next.js Proxy

### Through the Next.js Application

```bash
# 1. Login
curl -X POST http://localhost:3000/api/internal/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}' | jq '.'

# 2. Refresh (replace YOUR_TOKEN_HERE)
curl -X POST http://localhost:3000/api/internal/refresh-token \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" | jq '.'
```

---

## Check Logs

### Laravel Logs

```bash
# Watch logs in real-time
tail -f /home/logix/experts/apps/experts-api/storage/logs/laravel.log | grep -i refresh

# Or view recent refresh attempts
grep "Token refreshed" /home/logix/experts/apps/experts-api/storage/logs/laravel.log | tail -10
```

**Look for:**

- `✅ Token refreshed successfully` - Success
- `💥 Token Refresh Exception` - Errors

---

## Test with Postman/Insomnia

### Request 1: Login

- **Method**: POST
- **URL**: `https://api.dev.experts.com.sa/v1/auth/login`
- **Headers**:
  - `Content-Type: application/json`
  - `Accept: application/json`
- **Body** (JSON):

  ```json
  {
    "email": "test@example.com",
    "password": "password"
  }
  ```

### Request 2: Refresh Token

- **Method**: POST
- **URL**: `https://api.dev.experts.com.sa/v1/auth/refresh-token`
- **Headers**:
  - `Content-Type: application/json`
  - `Accept: application/json`
  - `Authorization: Bearer YOUR_TOKEN_FROM_LOGIN`

---

## Database Verification

Check if tokens are being revoked properly:

```bash
# Connect to database and run:
SELECT id, user_id, revoked, created_at, updated_at
FROM oauth_access_tokens
WHERE user_id = (SELECT id FROM users WHERE email = 'test@example.com')
ORDER BY created_at DESC
LIMIT 10;
```

You should see:

- Old tokens with `revoked = 1`
- Latest token with `revoked = 0`

---

## Troubleshooting

### Issue: "Route not found"

**Check route is registered:**

```bash
cd /home/logix/experts/apps/experts-api
php artisan route:list --path=refresh-token
```

Should show:

```
POST  v1/refresh-token  api.refresh-token
```

### Issue: "Unauthorized" (401)

**Possible causes:**

1. Token is expired or invalid
2. Token was already revoked
3. Wrong Authorization header format

**Solution:** Get a fresh token via login

### Issue: "No active token found"

**Cause:** Token not found in database

**Solution:** Check database connection and ensure token exists

### Issue: Connection refused

**Check if Laravel is running:**

```bash
ps aux | grep php
```

**Check Next.js is running:**

```bash
ps aux | grep next
```

---

## Performance Test

Test refresh speed:

```bash
time curl -X POST https://api.dev.experts.com.sa/v1/auth/refresh-token \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o /dev/null -s
```

Expected time: < 100ms

---

## Frontend Integration Test

Once logged into the Next.js app:

1. Open browser DevTools (F12)
2. Go to Network tab
3. Wait for token to expire (or manually trigger refresh)
4. Watch for automatic `/api/internal/refresh-token` call
5. Verify API calls continue working seamlessly

**Look for:**

- Status 200 on refresh call
- New token in response
- Subsequent API calls use new token

---

## Success Criteria

- ✅ Login returns valid token
- ✅ Refresh endpoint returns new token
- ✅ New token is different from old token
- ✅ Old token is revoked (cannot be reused)
- ✅ New token can be used for API calls
- ✅ Logs show successful refresh
- ✅ No errors in console
- ✅ Response time < 100ms

---

Generated: 2025-10-31
