---
title: "Experts codebase — Conventions"
date: "2026-03-06"
tags: ["project/experts", "topic/planning", "topic/conventions"]
category: "docs/experts-reference"
repo_root: /Users/ahmedsulaimani/projects/experts/apps/experts-app
monorepo_root: /Users/ahmedsulaimani/projects/experts
updated: "2026-07-15"
---

# Coding Conventions

**Analysis Date:** 2026-03-06

## Naming Patterns

**Files:**

- Handlers: `{domain}-{action}.handler.ts` (e.g., `event-create.handler.ts`, `profile-update.handler.ts`)
- Schemas: `{domain}-{action}.schema.ts` (e.g., `event-create.schema.ts`, `profile-update.schema.ts`)
- Commands: `{domain}-{action}.command.ts` (e.g., `event-create.command.ts`)
- Queries: `{domain}-{action}.query.ts` (e.g., `admin-revenue.query.ts`, `list-plans.query.ts`)
- Mappers: `{domain}.mapper.ts` (e.g., `event.mapper.ts`, `plan.mapper.ts`)
- DTOs: `{domain}.dto.ts` (e.g., `event.dto.ts`, `plan.dto.ts`)
- Hooks: `use-{feature}.ts` (e.g., `use-events.ts`, `use-billing.ts`, `use-is-rtl.ts`)
- React Components: `PascalCase.tsx` (e.g., `CourseCard.tsx`, `EventCard.tsx`)
- API routes: `route.ts` in directory path (e.g., `app/api/auth/register/route.ts`)
- Test files: placed in co-located `__tests__/` subdirectory, named `{subject}.test.ts`

**Functions:**

- Handler functions: `handle{Domain}{Action}` (e.g., `handleEventCreate`, `handleTabbyWebhookEvent`)
- Query functions: verb + noun (e.g., `listPlans`, `getAdminOverview`, `getAdminRevenue`)
- Mapper functions: `map{Source}To{Target}` (e.g., `mapEventToDTO`, `mapPlanToDTO`, `mapActivityCommandToCreateInput`)
- Orchestrators: `orchestrate{Domain}{Action}` (e.g., `orchestrateCourseEnrollmentComplete`)
- Event handlers on components: `handle{Action}` prefix (e.g., `handleClick`, `handleSubmit`)
- Custom hooks: `const useXxx = () => {}` (arrow function, not `function useXxx()`)

**Variables:**

- camelCase for local variables and parameters
- SCREAMING_SNAKE_CASE for module-level constants (e.g., `VAT_RATE`, `VAT_FACTOR`, `DIAGNOSTICS_CHANNEL`)
- Prisma mock objects named `mocks` or `prismaMock` in tests

**Types/Interfaces:**

- PascalCase for interfaces (e.g., `EventCreateCommand`, `SubscriptionCheckoutCommand`)
- PascalCase for type aliases (e.g., `HostRole`, `EventPublishingStatus`)
- Suffix `DTO` for data transfer objects (e.g., `EventScheduleDTO`, `PlanDTO`)
- Suffix `Command` for command objects (e.g., `EventCreateCommand`, `CancelSubscriptionCommand`)
- Suffix `Schema` for Zod schemas (e.g., `ProfileUpdateSchema`, `EventCloneSchema`)
- Suffix `Input` for Zod inferred types (e.g., `ProfileUpdateInput`, `SubscriptionCheckoutInput`)

## Code Style

**Formatting:**

- Tool: Prettier v3 with config at `/home/logix/experts/prettier.config.js`
- Print width: 100 characters for TypeScript
- Tab width: 2 spaces (no tabs)
- Semicolons: required
- Double quotes for strings (not single)
- Trailing commas: `all`
- Arrow parens: `always`
- Tailwind CSS class sorting via `prettier-plugin-tailwindcss`

**Linting:**

- ESLint with `eslint-config-next/core-web-vitals` and `eslint-config-next/typescript`
- Config at `eslint.config.mjs`
- `import/no-anonymous-default-export` is turned off
- `react/jsx-pascal-case` enforced with exceptions for react-pdf components
- `src/lib/**` is excluded from linting (all lib logic bypasses lint)

## Import Organization

**Order (observed pattern):**

1. React and framework imports (`"use client"` directive first if needed)
2. Third-party library imports (next, react, external packages)
3. Internal absolute imports using `@/` alias (e.g., `@/lib/prisma`, `@/components/ui/button`)
4. Relative imports

**Path Aliases:**

- `@/*` maps to `./src/*` — primary alias used throughout
- `@/lib` → `src/lib` (business logic, handlers, queries)
- `@/components` → `src/components` (React components)
- `@/hooks` → `src/hooks` (custom hooks)
- `@/generated` → `src/generated` (Prisma generated client)
- `@/src` → `src/` (direct src access when needed)

**Module directive:**

- `"use client"` is required at the top of any component using React state, effects, or browser APIs
- No `"use server"` directives detected — API route handlers are plain `async function` exports

## Error Handling

**API Routes:**

- Wrap entire handler body in `try/catch`
- Return `NextResponse.json({error: message}, {status: CODE})` on error
- Use `error instanceof Error ? error.message : "Fallback message"` to extract error text
- Return 400 for validation failures, 401 for unauthorized, 403 for forbidden, 500 for unexpected errors

**Handler Functions (lib layer):**

- Return structured result objects instead of throwing: `{error: "message", status: 403 as const}`
- Use `try/catch` around third-party calls that may throw
- Re-throw domain errors with descriptive messages (e.g., `throw new Error("Username is already taken")`)

**Example pattern:**

```typescript
// API route
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    // ...
    return NextResponse.json({ message: "Success" }, { status: 201 });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : "Operation failed";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}

// Handler (lib layer)
export async function handleEventCreate(command: EventCreateCommand) {
  if (!isInstructor && !isAdmin) {
    return {
      error: "Only instructors can create events",
      status: 403 as const,
    };
  }
  try {
    planInfo = await assertCanCreateEvent(userId);
  } catch (error) {
    const message =
      error instanceof Error ? error.message : "Event limit reached";
    return { error: message, status: 403 as const };
  }
  // ...
}
```

## Logging

**Framework:** Custom `observe` function from `@/lib/observability`

**Patterns:**

- Use `observe("domain.entity.action", payload, {level, dedupeKey})` for business events
- Level options: `"debug"`, `"info"`, `"error"`
- `dedupeKey` format: `"domain.event.name:${entityId}"` to prevent duplicate logging
- `console.warn` for non-critical failures (e.g., email send failure)
- `console.error` for unexpected errors in catch blocks

**Example:**

```typescript
observe(
  "user.registration.completed",
  { id: user.id, requestId },
  { level: "info", dedupeKey: `user.registration.completed:${user.id}` },
);
```

## Comments

**When to Comment:**

- JSDoc for all exported utility functions in `src/lib/utils.ts` (every function has `@param`, `@returns`, `@example`)
- File-level comments for module context (e.g., `// lib/activity/mappers/activity.mapper.ts`)
- Inline comments for non-obvious logic
- Commented-out code is present but should be avoided for new code

**JSDoc pattern (utility functions):**

```typescript
/**
 * Formats a number as a price with thousand separators and decimal places
 * @param price - The price to format (number, string, or Decimal)
 * @param decimals - Number of decimal places (default: 2)
 * @returns Formatted price string (e.g., "1,000.00")
 */
export function formatPrice(
  price: number | string | null | undefined,
  decimals: number = 2,
): string;
```

## Function Design

**Size:** Handlers and routes can be long (100–200 lines) when orchestrating multiple steps; pure logic functions are kept small

**Parameters:** Commands and queries use a single typed object parameter (not positional args):

```typescript
export async function handleEventCreate(command: EventCreateCommand) {}
export async function updateUserProfile({
  userId,
  input,
}: {
  userId: string;
  input: ProfileUpdateInput;
}) {}
```

**Return Values:**

- Handlers return structured objects `{error, status}` or the success payload
- Queries return typed DTOs (e.g., `Promise<AdminOverviewDTO>`)
- API routes always return `NextResponse.json(...)` with explicit status codes

## Module Design

**Exports:**

- Named exports preferred; default exports used only for Next.js page components and API routes
- `export async function` for handlers and queries
- `export const` for hooks and utility constants

**Barrel Files:**

- `index.ts` barrel files used in domain modules under `src/lib/{domain}/`
- Example: `src/lib/user/profile/index.ts` re-exports everything from subdirectories
- Barrel files use `export * from` pattern

## Validation

- **Zod** is the standard schema validation library
- Schemas are named `{Domain}Schema` and live in `commands/{action}.schema.ts`
- Always derive TypeScript type with `z.infer<typeof Schema>` exported as `{Domain}Input`
- Export a `{Domain}Validator` convenience alias: `export const ProfileUpdateValidator = ProfileUpdateSchema.safeParse`

## Component Patterns

**Client Components:**

- Always place `"use client"` as first line (167 client components detected)
- Use `cn()` from `@/lib/utils` for conditional class merging (clsx + tailwind-merge)
- Props interface defined inline above component or as exported type
- Component props always typed with explicit interfaces/types

**UI Libraries:**

- Primary: HeroUI (`@heroui/react` v3.0.0-beta.8) for complex components (Avatar, Chip, Skeleton)
- Secondary: shadcn/ui via Radix UI primitives for layout/form components
- Icons: `lucide-react` exclusively

---

_Convention analysis: 2026-03-06_

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
