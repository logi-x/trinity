---
title: "SDK BASE URL Fix - Multi-Environment Support"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/sdk"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# SDK BASE URL Fix - Multi-Environment Support

## Problem

Building SDK for one environment (e.g., staging) invalidates all other environments (dev, canary, production) because the BASE URL is hardcoded in the auto-generated `OpenAPI.ts` file.

Error encountered:

```
💥 Login error: TypeError: Failed to parse URL from undefined/v1/login
BASE: undefined
```

## Solution

Implemented a fallback priority system in `getBaseUrl()` that allows runtime environment variable override while maintaining auto-generated defaults.

## How It Works

### 1. Priority Order

The SDK resolves the BASE URL in this order:

1. **NEXT_PUBLIC_API_URL** (runtime environment variable override)
2. **OpenAPI.BASE** (auto-generated from OpenAPI spec during build)
3. **Error** (if both are undefined)

### 2. File Changes

#### `/packages/sdk/src/config.ts` (Lines 38-59)

```typescript
export function getBaseUrl(): string {
  const envUrl =
    typeof process !== "undefined"
      ? process.env?.NEXT_PUBLIC_API_URL
      : undefined;

  if (envUrl) {
    console.log("[SDK] Using NEXT_PUBLIC_API_URL:", envUrl);
    return envUrl;
  }

  if (OpenAPI.BASE && OpenAPI.BASE !== "undefined") {
    console.log("[SDK] Using OpenAPI.BASE:", OpenAPI.BASE);
    return OpenAPI.BASE;
  }

  console.error("[SDK] ⚠️ No BASE URL configured!");
  throw new Error(
    "SDK BASE URL not configured. Please set NEXT_PUBLIC_API_URL or ensure OpenAPI.BASE is generated correctly.",
  );
}
```

#### `/packages/sdk/src/runtime.ts` (User created)

```typescript
export function configureSdk(
  baseUrl: string,
  tokenResolver?: () => Promise<string | undefined>,
) {
  OpenAPI.BASE = baseUrl;
  console.log("[SDK] configureSdk", baseUrl);

  if (tokenResolver) {
    OpenAPI.TOKEN = async () => {
      const token = await tokenResolver();
      return token || "";
    };
  }
}
```

#### `/packages/hooks/src/use-sdk-auth.ts` (Modified)

```typescript
useEffect(() => {
  if (status === "loading") return;

  if (status === "authenticated" && session?.user?.accessToken) {
    configureSdk(getBaseUrl(), async () => session.user.accessToken as string);
    setGlobalInitialized(true);
  } else if (status === "unauthenticated") {
    clearTokenCache();
    configureSdk(getBaseUrl(), async () => "");
    setGlobalInitialized(true);
  }
}, [session, status]);
```

### 3. Usage Scenarios

#### Scenario 1: Production Build (Default behavior)

```bash
# Build SDK with staging API URL
make build-sdk ENV=staging

# OpenAPI.ts gets generated with:
# BASE: 'https://api.stg.experts.com.sa'

# Next.js app uses this URL by default
# No NEXT_PUBLIC_API_URL needed in .env
```

#### Scenario 2: Development Override

```bash
# Build SDK with canary API URL
make build-sdk ENV=canary

# But you want to test with local API during development
# Add to apps/experts-app/.env.local:
NEXT_PUBLIC_API_URL=http://localhost:8000

# SDK will use http://localhost:8000 instead of canary URL
```

#### Scenario 3: Testing Different Environments

```bash
# Build SDK once with canary
make build-sdk ENV=canary

# Test against different environments by changing .env:
# .env.development
NEXT_PUBLIC_API_URL=http://localhost:8000

# .env.staging
NEXT_PUBLIC_API_URL=https://api.stg.experts.com.sa

# .env.production
NEXT_PUBLIC_API_URL=https://api.experts.com.sa
```

## Benefits

1. **No Rebuild Required**: Change API endpoint without rebuilding SDK
2. **Development Flexibility**: Use production SDK with local API
3. **Environment Safety**: Auto-generated URL as safe default
4. **Clear Errors**: Descriptive error if configuration is missing
5. **Debug Logging**: Console logs show which URL is being used

## Environment Variables

### For Next.js App

Add to `apps/experts-app/.env.*`:

```bash
NEXT_PUBLIC_API_URL=https://api.canary.experts.com.sa
```

**Note**: `NEXT_PUBLIC_` prefix is required for Next.js to expose the variable to the browser.

### For Docker Compose

Add to `docker/*/experts-app.env`:

```bash
NEXT_PUBLIC_API_URL=https://api.canary.experts.com.sa
```

## Debugging

Check browser console for SDK initialization logs:

```
[SDK] Using NEXT_PUBLIC_API_URL: https://api.canary.experts.com.sa
[SDK] configureSdk https://api.canary.experts.com.sa
```

Or if using auto-generated URL:

```
[SDK] Using OpenAPI.BASE: https://api.stg.experts.com.sa
[SDK] configureSdk https://api.stg.experts.com.sa
```

## Migration Notes

### Before (Broken)

- Building SDK for staging broke dev/canary/production
- Had to rebuild SDK every time you wanted to change environment
- `getBaseUrl()` returned empty string when env var was undefined

### After (Fixed)

- Build SDK once for any environment
- Override URL via environment variable when needed
- Falls back to auto-generated URL from OpenAPI spec
- Clear error message if both are missing

## Testing

1. Build Next.js app without `NEXT_PUBLIC_API_URL`:
   - Should use auto-generated `OpenAPI.BASE`

2. Add `NEXT_PUBLIC_API_URL` to `.env`:
   - Should override and use environment variable

3. Remove both (set `OpenAPI.BASE = undefined`):
   - Should throw clear error message

## Next Steps (Optional Improvements)

If you want to build SDK for all environments simultaneously, consider:

1. **Per-environment SDK packages**:

   ```
   @experts/sdk-dev
   @experts/sdk-staging
   @experts/sdk-canary
   @experts/sdk-production
   ```

2. **Makefile enhancement**:

   ```makefile
   build-all-sdks:
       make build-sdk ENV=development
       make build-sdk ENV=staging
       make build-sdk ENV=canary
       make build-sdk ENV=production
   ```

3. **Runtime environment detection**:

   ```typescript
   const apiUrls = {
     development: "http://localhost:8000",
     staging: "https://api.stg.experts.com.sa",
     canary: "https://api.canary.experts.com.sa",
     production: "https://api.experts.com.sa",
   };

   const baseUrl = apiUrls[process.env.NEXT_PUBLIC_APP_ENV || "production"];
   ```

But the current fix should handle your immediate needs without requiring these larger changes.
