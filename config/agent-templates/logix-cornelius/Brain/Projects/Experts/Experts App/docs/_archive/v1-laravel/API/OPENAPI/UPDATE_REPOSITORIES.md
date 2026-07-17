---
title: "Repository Pattern Update Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/api"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Repository Pattern Update Guide

## Overview

With the migration to `@hey-api/openapi-ts`, the SDK no longer exports Service classes. Instead, it exports individual functions.

## Changes Required

### Old Pattern (Service Classes)

```typescript
import { AuthService, UsersService } from "@experts/sdk";

// Old way - Service.method({ requestBody: {...} })
const res = await AuthService.login({
  requestBody: { email, password },
});

const user = await UsersService.getUserProfile({});
```

### New Pattern (Individual Functions)

```typescript
import { login, getUserProfile } from "@experts/sdk";

// New way - functionName({ body: {...} })
const res = await login({
  body: { email, password },
});

const user = await getUserProfile();
```

## Parameter Changes

### Body Parameters

```diff
- AuthService.login({ requestBody: { email, password } })
+ login({ body: { email, password } })

- UsersService.createAUser({ requestBody: data })
+ createAUser({ body: data })
```

### Query Parameters

```diff
- UsersService.getUsers({ page, perPage, sort })
+ getUsers({ query: { page, perPage, sort } })
```

### Path Parameters

```diff
- UsersService.getAUser({ identifierUuid: userId })
+ getAUser({ path: { identifierUuid: userId } })
```

### Mixed Parameters

```diff
- UsersService.updateAUser({ identifierUuid, requestBody: data })
+ updateAUser({ path: { identifierUuid }, body: data })
```

## Files That Need Updates

Based on the codebase scan, these repository files need to be updated:

1. ✅ `packages/utilities/validations/use-form-validation.tsx` - **UPDATED**
2. ⚠️ `packages/models/src/repositories/auth-repository.ts`
3. ⚠️ `packages/models/src/repositories/user-repository.ts`
4. ⚠️ `packages/models/src/repositories/plans-repository.ts`
5. ⚠️ `packages/models/src/repositories/course-repository.ts`
6. ⚠️ `packages/models/src/repositories/checkout-repository.ts`
7. ⚠️ `packages/models/src/repositories/stats-repository.ts`
8. ⚠️ `packages/models/src/repositories/organizations-repository.ts`
9. ⚠️ `packages/models/src/repositories/categories-repository.ts`

## Migration Examples

### auth-repository.ts

**Before:**

```typescript
import {AuthService} from "@experts/sdk";

static async login(email: string, password: string): Promise<IUser> {
  const res = await AuthService.login({requestBody: {email, password}});
  return new IUser(res as UserType);
}

static async validateUsername(username: string) {
  const res = await AuthService.validateUsername({requestBody: {username}});
  return res;
}
```

**After:**

```typescript
import {login, register, validateUsername, validateEmail, validatePhone} from "@experts/sdk";

static async login(email: string, password: string): Promise<IUser> {
  const res = await login({body: {email, password}});
  return new IUser(res.data?.user as UserType);
}

static async validateUsername(username: string) {
  const res = await validateUsername({body: {username}});
  return res.data;
}
```

### user-repository.ts

**Before:**

```typescript
import {UsersService} from "@experts/sdk";

static async getProfile(): Promise<IUser> {
  const res = await UsersService.getUserProfile({});
  return new IUser(res.data as unknown as User);
}

static async getUsers(query: UserFilters): Promise<Collection<IUser>> {
  const res = await UsersService.getUsers({
    include: query.include,
    page: query.page,
    perPage: query.per_page,
  });
  return new Collection(items, res.meta);
}

static async updateUser(identifierUuid: string, requestBody: UpdateUserRequest): Promise<IUser> {
  const res = await UsersService.updateAUser({identifierUuid, requestBody});
  return new IUser(res.data as User);
}
```

**After:**

```typescript
import {getUserProfile, getUsers, updateAUser} from "@experts/sdk";

static async getProfile(): Promise<IUser> {
  const res = await getUserProfile();
  return new IUser(res.data as unknown as User);
}

static async getUsers(query: UserFilters): Promise<Collection<IUser>> {
  const res = await getUsers({
    query: {
      include: query.include,
      page: query.page,
      perPage: query.per_page,
    }
  });
  return new Collection(items, res.data?.meta);
}

static async updateUser(identifierUuid: string, requestBody: UpdateUserRequest): Promise<IUser> {
  const res = await updateAUser({
    path: { identifierUuid },
    body: requestBody
  });
  return new IUser(res.data as User);
}
```

### plans-repository.ts

**Before:**

```typescript
import {PlansService} from "@experts/sdk";

static async getPlans(): Promise<Collection<IPlan>> {
  const res = await PlansService.getPlans();
  return new Collection(items, res.meta);
}

static async getPlan(slug: string): Promise<IPlan> {
  const res = await PlansService.getPlan({slug});
  return new IPlan(res.data as unknown as Plan);
}
```

**After:**

```typescript
import {getPlans, getPlan} from "@experts/sdk";

static async getPlans(): Promise<Collection<IPlan>> {
  const res = await getPlans();
  return new Collection(items, res.data?.meta);
}

static async getPlan(slug: string): Promise<IPlan> {
  const res = await getPlan({path: {slug}});
  return new IPlan(res.data as unknown as Plan);
}
```

## Response Structure Changes

### Old Response Structure

```typescript
const res = await AuthService.login({...});
// res.data contains the response
// res.meta contains pagination/metadata
// res.success indicates success
```

### New Response Structure

```typescript
const res = await login({...});
// res.data contains the response data
// res.error contains error (if any)
// res.response contains raw Response object
```

## Type Exports

The repository files use `Parameters<typeof Service.method>` for type extraction. This pattern still works:

**Before:**

```typescript
export type CreateUserRequest = Parameters<
  typeof UsersService.createAUser
>[0]["requestBody"];
```

**After:**

```typescript
export type CreateUserRequest = Parameters<typeof createAUser>[0]["body"];
```

## Common Issues and Fixes

### Issue 1: "Export AuthService doesn't exist"

**Error:**

```
Export AuthService doesn't exist in target module
```

**Fix:**

```typescript
// ❌ Wrong
import {AuthService} from "@experts/sdk";
const res = await AuthService.login({...});

// ✅ Correct
import {login} from "@experts/sdk";
const res = await login({...});
```

### Issue 2: "requestBody" parameter not recognized

**Error:**

```
Object literal may only specify known properties, and 'requestBody' does not exist
```

**Fix:**

```typescript
// ❌ Wrong
await login({ requestBody: { email, password } });

// ✅ Correct
await login({ body: { email, password } });
```

### Issue 3: Missing response data

**Error:**

```
Cannot read property 'user' of undefined
```

**Fix:**

```typescript
// ❌ Wrong (old structure)
const res = await login({...});
return res.user; // undefined

// ✅ Correct (new structure)
const res = await login({...});
return res.data?.user;
```

## Finding All Service Usages

Use this command to find all files using Service classes:

```bash
# Find all Service imports
grep -r "Service.*from.*@experts/sdk" --include="*.ts" --include="*.tsx"

# Find specific services
grep -r "AuthService\|UsersService\|PlansService" --include="*.ts" --include="*.tsx"
```

## Automated Migration Steps

1. **Find all Service imports:**

   ```bash
   grep -l "Service.*from.*@experts/sdk" packages/models/src/repositories/*.ts
   ```

2. **For each file:**
   - Replace Service import with individual function imports
   - Change `requestBody` to `body`
   - Change path parameters to `path: {...}`
   - Change query parameters to `query: {...}`
   - Update response access from `res` to `res.data`

3. **Test each repository:**

   ```bash
   pnpm test
   ```

## Verification Checklist

After updating each repository file:

- [ ] All Service imports replaced with function imports
- [ ] All `requestBody` changed to `body`
- [ ] All path parameters use `path: {...}`
- [ ] All query parameters use `query: {...}`
- [ ] Response access updated to `res.data`
- [ ] Type exports updated (if any)
- [ ] File compiles without errors
- [ ] Tests pass (if any)

## Need Help?

See the main documentation:

- [README.md](./README.md) - Full SDK documentation
- [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md) - Complete migration guide
- [QUICK_START.md](./QUICK_START.md) - Quick start guide
