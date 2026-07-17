---
title: "TESTING"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/testing"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

## Testing Guide (PHPUnit + Vitest)

### Overview

- JS/TS apps use Vitest with a shared preset in `packages/test`.
- Laravel API uses PHPUnit (via `php artisan test`).
- Tests live under each app’s `src/__tests__/` or `src/**/__tests__/`.

### Quick Commands

- JS (all apps, headless):

  ```bash
  cd packages/test
  yarn test:global
  ```

- JS (watch in browser mode – opens a Chrome instance):

  ```bash
  cd packages/test
  yarn test:global:watch
  ```

- JS (limit to one app from the shared runner):

  ```bash
  cd packages/test
  vitest run --include "../../apps/experts-app/src/**/__tests__/**/*.{test,spec}.{ts,tsx,js,jsx}" "../../apps/experts-app/src/__tests__/**/*.{test,spec}.{ts,tsx,js,jsx}"
  ```

- PHP (Laravel API):

  ```bash
  docker exec experts-development-api bash -lc "php artisan test --colors=always | cat"
  ```

  - Filter by class or method:

  ```bash
  docker exec experts-development-api bash -lc "php artisan test --filter=CreateCourseActionTest --colors=always | cat"
  ```

### JS/TS (Vitest)

- Central config: `packages/test/src/vitest/preset.ts`
  - Environment: `happy-dom` <!-- and 'node' for experts-server -->
  - Globals enabled; CSS enabled <!-- except for experts-server -->
  - Includes tests from all apps under `apps/**/src/**/__tests__/`
  - Setup: `@experts/test/vitest/setup`

- Per-app config (optional): each app has `vitest.config.ts`.
  - commands:
    "test": "vitest run",
    "test:watch": "vitest watch",
    "test:watch:browser": "vitest watch --browser.enabled true",
    "test:run": "vitest run",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage",

- Global configs for all apps testing: `packages/test`
  - commands:
    "test:global": "vitest run",
    "test:coverage:global": "vitest run --coverage", --> not supported <--
    "test:global:watch": "vitest watch",
    "test:global:watch:browser": "vitest watch --browser.enabled true",
    "test:global:run": "vitest run",
    "test:global:ui": "vitest --ui",

- Shared render helper (NextAuth + SWR wired):

  ```ts
  // @experts/test
  import { render, screen } from "@experts/test";
  import Component from "@/path/to/Component"; // using specific component path, e.g. import {Button} from "@experts/ui/button"; instead of import {Button} from "@ui/buttons";

  it("renders", () => {
    render(<Component />);
    expect(screen.getByText(/something/i)).toBeInTheDocument();
  });
  ```

  - `render` wraps `SessionProvider` with a static session and `SWRConfig` (no dedupe, no revalidate-on-focus).
  - Add additional providers locally if needed by composing a wrapper.

- Globals & polyfills (from `@experts/test/vitest/setup`):
  - `fetch` via `whatwg-fetch`
  - `process.env` shim for browser mode

- Browser mode
  - Default is disabled. Use `yarn test:global:watch` to enable Chrome and watch.
  - For CI or headless-only, keep browser mode disabled.

- Troubleshooting
  - Node modules tests bleeding in (e.g., `next-auth` internal `__tests__`):
    - Run from `packages/test` (uses strict include globs).
    - If needed, add an exclude in a local config:

    ```ts
    test: {
      exclude: ["**/node_modules/next-auth/**/src/**/__tests__/**"];
    }
    ```

    - If a package tries to import optional deps like `msw` from its own tests, exclude/alias in your config if encountered.

  - “fetch is not defined” in Node context: ensured by shared setup; verify `@experts/test/vitest/setup` is in `setupFiles`.

### PHP (Laravel / PHPUnit)

- Host testing

```bash
cd /home/logix/experts/apps/experts-api && yarn test --colors=always | cat
```

- Filtered runs:

  ```bash
  cd /home/logix/experts/apps/experts-api && yarn test --filter=ProviderResolverTest --colors=always | cat
  cd /home/logix/experts/apps/experts-api && yarn test --filter=CreateCourseActionTest --colors=always | cat
  ```

- Container: `experts-development-api`
- Run full suite:

  ```bash
  docker exec experts-development-api bash -lc "php artisan test --colors=always | cat"
  ```

- Filtered runs:

  ```bash
  docker exec experts-development-api bash -lc "php artisan test --filter=ProviderResolverTest --colors=always | cat"
  docker exec experts-development-api bash -lc "php artisan test --filter=CreateCourseActionTest --colors=always | cat"
  ```

- Tips
  - Use factories for test data
  - Prefer policies/gates assertions where relevant
  - Keep UUIDs in public API assertions; hide integer IDs

### Conventions

- Place component/hook tests under `src/__tests__/` near implementation.
- Favor RTL patterns: query by role/text/label, assert on user-visible output.
- Use SWR-friendly tests (no background revalidation surprises due to shared config).
- Frontend calls must hit Next.js API routes (never Laravel directly) in integration-style tests.

### Where Things Live

- Shared preset (vitest): `packages/test/src/vitest/preset.ts`
- Shared setup (vitest): `packages/test/src/vitest/setup.ts`
- Shared render (vitest): `packages/test/src/test/render/render.tsx`
- Shared mocks (vitest): `packages/test/src/test/mocks/mocks.tsx`
- Shared utils (vitest): `packages/test/src/test/utils/index.tsx`
- Shared providers (vitest): `packages/test/src/test/providers/providers.tsx`
- Shared fixtures (vitest): `packages/test/src/test/fixtures/fixtures.tsx`
- Shared assertions (vitest): `packages/test/src/test/assertions/assertions.tsx`
- App configs (vitest): `apps/*/vitest.config.ts`
- Laravel tests (PHPUnit): `apps/experts-api/tests/**`

### CI Notes (optional)

- Run JS tests from `packages/test` to cover all apps.
- Run Laravel tests via the API container.
