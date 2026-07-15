---
title: "Quick Start Guide: @hey-api/openapi-ts SDK"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/api"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Quick Start Guide: @hey-api/openapi-ts SDK

This guide will help you get started with the new SDK structure in **5 minutes**.

## 1. Basic Setup

### Install (already done)

```bash
pnpm add @experts/sdk
```

### Configure SDK

Add this to your app initialization (e.g., `App.tsx` or `layout.tsx`):

```typescript
import { configureSdk } from "@experts/sdk/config";

// Automatically uses NEXT_PUBLIC_API_URL from .env
configureSdk();
```

### With Authentication

If you're using NextAuth:

```typescript
import { useSDKAuth } from '@experts/hooks';

function App() {
  const { isReady, isAuthenticated } = useSDKAuth();

  if (!isReady) return <Loading />;

  return <YourApp />;
}
```

That's it! The SDK is now configured and ready to use.

## 2. Making API Calls

### Login

```typescript
import { login } from "@experts/sdk";

const response = await login({
  body: {
    email: "user@example.com",
    password: "password",
  },
});

if (response.data) {
  console.log("Logged in:", response.data.user);
}
```

### Get User Profile

```typescript
import { getProfile } from "@experts/sdk";

const profile = await getProfile();
console.log("User:", profile.data);
```

### List Courses

```typescript
import { coursesIndex } from "@experts/sdk";

const courses = await coursesIndex({
  query: { page: 1, limit: 10 },
});

courses.data.forEach((course) => {
  console.log(course.title);
});
```

## 3. Environment Configuration

Create `.env.local` (or use existing environment files):

```env
NEXT_PUBLIC_API_URL=https://api.dev.experts.com.sa
```

The SDK will automatically use this URL.

## 4. Regenerate SDK (when API changes)

```bash
cd packages/sdk
pnpm sdk:generate
```

## Common Patterns

### Error Handling

```typescript
try {
  const response = await login({ body: { email, password } });

  if (response.error) {
    console.error("API error:", response.error);
  } else {
    console.log("Success:", response.data);
  }
} catch (error) {
  console.error("Network error:", error);
}
```

### Custom Headers

```typescript
import { addHeaders } from "@experts/sdk/runtime";

addHeaders({
  "X-App-Version": "1.0.0",
});
```

### Request Logging

```typescript
import { addRequestInterceptor } from "@experts/sdk/runtime";

addRequestInterceptor(async (request) => {
  console.log("Request:", request.url);
  return request;
});
```

## That's It!

You're now ready to use the SDK. For more advanced usage, see:

- [README.md](./README.md) - Full documentation
- [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) - Migration from old SDK

## Key Takeaways

✅ Import from `@experts/sdk` for API methods
✅ Import from `@experts/sdk/config` for configuration
✅ Use `configureSdk()` once at app startup
✅ Use `useSDKAuth()` hook for React integration
✅ All methods are type-safe from OpenAPI spec
