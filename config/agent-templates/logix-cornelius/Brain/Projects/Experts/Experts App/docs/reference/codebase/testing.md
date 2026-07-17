---
title: "Experts codebase — Testing"
date: "2026-03-06"
tags: ["project/experts", "topic/planning", "topic/testing"]
category: "docs/experts-reference"
repo_root: /Users/ahmedsulaimani/projects/experts/apps/experts-app
monorepo_root: /Users/ahmedsulaimani/projects/experts
updated: "2026-07-15"
---

> ↑ [[Projects/Experts/Experts App/docs|Experts App docs]]

# Testing Patterns

**Analysis Date:** 2026-03-06

## Test Framework

**Runner:**

- Vitest v4 (latest)
- Config: `vitest.config.ts` at app root

**Assertion Library:**

- Vitest built-in (`expect`)

**Run Commands:**

```bash
pnpm test                    # Run all tests (with .env.test loaded)
pnpm test:watch              # Watch mode
pnpm test:ui                 # Vitest UI browser interface
pnpm test:coverage           # Coverage report
```

**Vitest Configuration:**

- `globals: true` — no need to import `describe`, `it`, `expect`
- `environment: "node"` — Node.js environment (no jsdom)
- `fileParallelism: false` — test files run serially (prevents database deadlocks)
- `isolate: true` — each test file gets isolated module context (required for `vi.mock` to work correctly when mixing unit and integration tests)
- `maxWorkers: 1` — single worker
- `testTimeout: 20000ms`
- `setupFiles: ["tests/setup/env.guard.ts"]`

## Test File Organization

**Location:**

- Co-located with source: `__tests__/` subdirectory inside the source module directory
- Pattern: `src/lib/{domain}/{layer}/__tests__/{subject}.test.ts`
- No separate top-level test directory (only `tests/` for utility scripts and setup)

**Naming:**

- `{domain}-{action}.handler.test.ts` for handler tests
- `{domain}-{action}.schema.test.ts` for schema/validation tests
- `{domain}-{action}.query.test.ts` for query tests
- `{domain}.policy.test.ts` for policy/rules tests
- `{subject}.test.ts` for utilities

**Examples:**

```
src/lib/events/handlers/__tests__/event-create.handler.test.ts
src/lib/user/profile/commands/__tests__/profile-update.schema.test.ts
src/lib/user/profile/handlers/__tests__/profile-update.handler.test.ts
src/lib/lifecycle/__tests__/lifecycle.policy.test.ts
src/lib/auth/__tests__/auth-credentials.test.ts
src/lib/payments/gateways/tabby/__tests__/tabby.webhook.handler.test.ts
```

## Test Structure

**Suite Organization:**

```typescript
import { beforeEach, describe, expect, it, vi } from "vitest";

// 1. Define all mocks with vi.hoisted() FIRST
const mocks = vi.hoisted(() => ({
  prisma: {
    user: { findUnique: vi.fn() },
  },
  someHelper: vi.fn(),
}));

// 2. Call vi.mock() at module level (hoisted automatically)
vi.mock("@/lib/prisma", () => ({ prisma: mocks.prisma }));
vi.mock("@/lib/some-helper", () => ({
  someHelper: (...args: unknown[]) => mocks.someHelper(...args),
}));

// 3. Import subject AFTER all mocks
import { handleSomething } from "@/lib/domain/handlers/something.handler";

describe("subject-name (unit)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Set default mock return values
    mocks.prisma.user.findUnique.mockResolvedValue({ id: "user-1" });
  });

  it("describes the expected behavior", async () => {
    const result = await handleSomething({ ...args });
    expect(result).toEqual({ expected: "value" });
  });
});
```

**Key patterns:**

- `describe` name uses kebab-case and includes `(unit)` suffix: `"handle-event-create (unit)"`
- `it` descriptions are plain English behavior statements
- `beforeEach` always calls `vi.clearAllMocks()` then re-sets default mock values
- Subject under test is imported AFTER all `vi.mock()` calls to ensure mocks are active

## Mocking

**Framework:** Vitest (`vi.mock`, `vi.fn`, `vi.hoisted`)

**The `vi.hoisted` pattern (required):**
All mock objects must be defined with `vi.hoisted()` so they are available at the top of the module before any `vi.mock()` calls execute:

```typescript
const mocks = vi.hoisted(() => ({
  prisma: {
    category: { findUnique: vi.fn() },
    user: { findMany: vi.fn() },
    $transaction: vi.fn(),
  },
  helperFn: vi.fn(),
}));

vi.mock("@/lib/prisma", () => ({ prisma: mocks.prisma }));
vi.mock("@/lib/some-helper", () => ({
  helperFn: (...args: unknown[]) => mocks.helperFn(...args),
}));
```

**Wrapping function mocks:**
Named function exports are wrapped with a spread pattern to preserve call forwarding:

```typescript
vi.mock("@/lib/events/mappers/event.mapper", () => ({
  mapEventToDTO: (...args: unknown[]) => mocks.mapEventToDTO(...args),
}));
```

**Mocking Prisma transactions:**

```typescript
mocks.tx = {
  event: { create: vi.fn() },
};
mocks.prisma.$transaction.mockImplementation(
  async (fn: (tx: unknown) => unknown) => fn(mocks.tx),
);
```

**What to Mock:**

- `@/lib/prisma` — always mocked in unit tests (database not accessed)
- External SDKs (`argon2`, `next-auth`, `@aws-sdk/*`)
- `next/headers` (cookies, headers)
- Cross-domain handler/service dependencies
- Infrastructure services (`@/lib/observability`, `@/lib/storage/*`)

**What NOT to Mock:**

- The subject under test itself
- Pure utility functions and schemas (test them directly)
- Type-only imports

## Test Safety

**Database guard:**
`tests/setup/env.guard.ts` is run as a `setupFiles` entry and throws an error if `DATABASE_URL` does not include `experts_test`:

```typescript
if (!process.env.DATABASE_URL?.includes("experts_test")) {
  throw new Error("TESTS ARE NOT USING experts_test DATABASE!");
}
```

**Environment:**

- Tests load `.env.test` via `dotenv` before running
- `process.env` is overridden in individual tests for env-dependent behavior, then restored in `afterEach`

## Fixtures and Factories

**Test Data:**

- UUIDs generated inline with `uuidv4()` from the `uuid` package
- Hardcoded UUID-format strings used as stable IDs within a single test file:

```typescript
const baseEventId = "11111111-1111-4111-8111-111111111111";
const baseUserId = "22222222-2222-4222-8222-222222222222";
```

- Minimal fixture objects built inline per test (no shared factory utilities detected)
- Default mock return values set in `beforeEach` to keep each test focused on overrides

**Location:**

- No dedicated fixtures directory; test data is defined inline in each test file
- `tests/` directory contains manual integration scripts (`tests/billing/`, `tests/zatca/`)

## Coverage

**Requirements:** No enforced coverage thresholds configured
**View Coverage:**

```bash
pnpm test:coverage
```

## Test Types

**Unit Tests (74 `.test.ts` files, 2 `.test.tsx` files):**

- Scope: single handler, query, schema, or policy function
- All dependencies mocked
- Focus on business rules: authorization checks, data transformations, edge cases
- File suffix pattern: `*.handler.test.ts`, `*.schema.test.ts`, `*.query.test.ts`, `*.policy.test.ts`

**Integration Tests:**

- Manual scripts in `tests/billing/` and `tests/zatca/` (not run by Vitest automatically)
- Require running services (database, queues)
- Run via `pnpm test:pdf`, `pnpm test:pdf:queue`

**E2E Tests:**

- Not detected

## Common Patterns

**Async Testing:**

```typescript
it("returns error on failure", async () => {
  mocks.someService.mockRejectedValue(new Error("Service failed"));
  const result = await handleSomething(args);
  expect(result).toEqual({ error: "Service failed", status: 403 });
});
```

**Error Testing (thrown errors):**

```typescript
it("rejects taken username", async () => {
  mocks.prisma.user.findUnique.mockResolvedValue({ id: "user-2" });
  await expect(
    updateUserProfile({ userId: "user-1", input: { username: "taken_name" } }),
  ).rejects.toThrow("Username is already taken");
});
```

**Schema Validation Testing:**

```typescript
it("rejects invalid input", () => {
  const result = ProfileUpdateSchema.safeParse({ username: "bad-name" });
  expect(result.success).toBe(false);
});
```

**Verifying a function was NOT called:**

```typescript
expect(mocks.prisma.course.create).not.toHaveBeenCalled();
```

**Partial object matching:**

```typescript
expect(mocks.tx.event.create).toHaveBeenCalledWith(
  expect.objectContaining({
    data: expect.objectContaining({ price: 0, isFree: true }),
  }),
);
```

**Environment variable testing:**

```typescript
const originalEnv = process.env;
beforeEach(() => {
  process.env = { ...originalEnv };
  process.env.R2_BUCKET = "bucket";
});
afterEach(() => {
  process.env = originalEnv;
  vi.clearAllMocks();
});
```

---

_Testing analysis: 2026-03-06_
