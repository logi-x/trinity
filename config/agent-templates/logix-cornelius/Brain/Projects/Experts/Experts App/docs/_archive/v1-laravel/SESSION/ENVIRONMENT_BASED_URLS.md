---
title: "Environment-Based URLs Configuration"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/session"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Environment-Based URLs Configuration

## Problem Statement

Previously, both the SDK and API documentation had **hardcoded URLs** pointing to the canary environment:

1. **`packages/sdk/src/core/OpenAPI.ts:23`** - Hardcoded `BASE: 'https://api.canary.experts.com.sa'`
2. **`apps/experts-api/config/scribe.php:28`** - Hardcoded `'base_url' => 'https://api.canary.experts.com.sa'`

This caused issues where:

- Development/staging/production environments would still point to canary API
- API documentation would always show canary URLs regardless of environment
- SDK would make requests to wrong environment

## Solution

### 1. SDK Configuration (`packages/sdk`)

Since `OpenAPI.ts` is **auto-generated** by `openapi-typescript-codegen`, we cannot edit it directly.

#### Runtime Override

The SDK now automatically overrides the hardcoded BASE URL at runtime using environment variables:

**File:** `packages/sdk/src/config.ts`

```typescript
// Override BASE URL from environment variable at runtime
if (typeof process !== "undefined" && process.env?.NEXT_PUBLIC_API_URL) {
  OpenAPI.BASE = process.env.NEXT_PUBLIC_API_URL;
}
```

#### Manual Override (Optional)

You can also manually set the BASE URL:

```typescript
import { setBaseUrl, getBaseUrl } from "@experts/sdk/setup";

// Set custom URL
setBaseUrl("https://api.custom.experts.com.sa");

// Get current URL
console.log(getBaseUrl());
```

#### Environment Variables Used

The SDK reads `NEXT_PUBLIC_API_URL` from environment:

```env
# .env.development
NEXT_PUBLIC_API_URL=https://api.dev.experts.com.sa

# .env.canary
NEXT_PUBLIC_API_URL=https://api.canary.experts.com.sa

# .env.staging
NEXT_PUBLIC_API_URL=https://api.stg.experts.com.sa

# .env.production
NEXT_PUBLIC_API_URL=https://api.prod.experts.com.sa
```

### 2. API Documentation (Scribe)

The API documentation now uses environment variables instead of hardcoded values.

**File:** `apps/experts-api/config/scribe.php`

```php
'base_url' => env('API_EXTERNAL_URL', env('APP_URL', 'http://localhost:3026')),
```

**Fallback chain:**

1. First tries `API_EXTERNAL_URL` (if defined)
2. Falls back to `APP_URL` (current behavior in existing .env files)
3. Falls back to `http://localhost:3026` (development default)

#### Environment Variables Used

The API uses `APP_URL` which is already set in all environment files:

```env
# apps/experts-api/.env.canary
APP_URL=https://api.canary.experts.com.sa

# apps/experts-api/.env.staging
APP_URL=https://api.stg.experts.com.sa

# apps/experts-api/.env.production
APP_URL=https://api.prod.experts.com.sa
```

## Verification

### Test SDK Configuration

```typescript
import { getBaseUrl } from "@experts/sdk/setup";

// Should print environment-specific URL
console.log("SDK Base URL:", getBaseUrl());
```

### Test API Documentation

1. In canary environment, visit: https://api.canary.experts.com.sa/docs
2. Base URL should show: `https://api.canary.experts.com.sa`

3. In staging environment, visit: https://api.stg.experts.com.sa/docs
4. Base URL should show: `https://api.stg.experts.com.sa`

## Important Notes

### For SDK (`OpenAPI.ts`)

1. ❌ **Do NOT edit `OpenAPI.ts` manually** - it's auto-generated
2. ❌ **Do NOT worry about hardcoded URLs in `OpenAPI.ts`** - they're overridden at runtime
3. ✅ **Do ensure `NEXT_PUBLIC_API_URL` is set** in your environment files
4. ✅ **Do regenerate SDK** using `pnpm sdk:generate` commands when API changes

### For API Documentation (`scribe.php`)

1. ✅ **Configuration now uses environment variables**
2. ✅ **No hardcoded URLs** - all environment-based
3. ✅ **Regenerate docs** with `pnpm generate:docs` after changes

## Files Modified

### SDK Package

- ✅ `packages/sdk/src/config.ts` - Added runtime BASE URL override
- ✅ `packages/sdk/src/setup.ts` - Exported `setBaseUrl` and `getBaseUrl`
- ✅ `packages/sdk/README.md` - Added configuration documentation

### API Configuration

- ✅ `apps/experts-api/config/scribe.php` - Changed from hardcoded to `env('APP_URL')`

## Related Documentation

- [SDK README](https://github.com/logi-x/experts/blob/main/packages/sdk/README.md) - SDK configuration details
- [Version Management](../DOCKER/VERSION_MANAGEMENT.md) - Centralized version system
