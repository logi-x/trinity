---
title: "Cursor Rules Updated for Universal Client Pattern"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/course"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Cursor Rules Updated for Universal Client Pattern

## Overview

The cursor rules have been comprehensively updated to enforce the Universal Client Pattern across all API integrations, using the task management implementation as the gold standard.

## 📋 Rules Updated

### 1. New Rule: universal-client-pattern.mdc

**Purpose**: Comprehensive guide for implementing the Universal Client Pattern
**Scope**: All API integrations across frontend and backend

**Key Enforcements:**

- ✅ Types → Repository → Hooks → Components flow
- ✅ `useApiQuery` for data fetching with authentication
- ✅ `useApiMutation` for mutations with cache invalidation
- ✅ Generated SDK usage only (no direct fetch/proxy routes)
- ✅ Proper authentication state handling
- ✅ Smart cache invalidation patterns

### 2. Updated: api-architecture (Experts) · api-architecture.mdc (repo)

**Changes:**

- Updated architecture flow to include hooks layer
- Replaced direct SDK examples with Universal Client Pattern
- Added authentication handling requirements
- Deprecated `createAuthenticatedServerApiClient` usage
- Enhanced with repository and hook patterns

### 3. Updated: shared-packages.mdc

**Changes:**

- Added Universal Client Pattern guidelines for package development
- Updated hooks package section with `useApiQuery`/`useApiMutation` patterns
- Converted services package to models/repositories pattern
- Added API integration guidelines with step-by-step implementation
- Enhanced with authentication handling requirements

### 4. Updated: laravel-api-backend.mdc

**Changes:**

- Added frontend integration section
- Connected Laravel controllers to generated SDK
- Showed complete flow from Laravel → OpenAPI → TypeScript
- Added benefits of the integrated approach
- Cross-referenced Universal Client Pattern rule

## 🎯 Enforcement Patterns

### Required Implementation Flow

**For any new API feature:**

1. **Laravel Backend**:

   ```php
   // Domain-driven controller with Scribe docs
   /**
    * @group {Domain}
    * @subgroup {Entity}
    */
   class {Entity}Controller extends Controller
   ```

2. **Generated SDK**:

   ```bash
   # Automatic generation
   php artisan scribe:generate
   yarn experts:sdk:generate
   ```

3. **Frontend Types**:

   ```typescript
   // packages/core/types/src/{domain}.ts
   export interface {Entity} { ... }
   ```

4. **Repository Layer**:

   ```typescript
   // packages/models/src/repositories/{domain}-repository.ts
   export class {Entity}Repository {
     static async get{Entities}() {
       return {Entity}Service.list{Entities}();
     }
   }
   ```

5. **Hook Layer**:

   ```typescript
   // packages/hooks/src/{domain}/use-{entity}.ts
   export function use{Entities}() {
     return useApiQuery('{entities}', () => {Entity}Repository.get{Entities}(), {}, { requireAuth: true });
   }
   ```

6. **Component Usage**:

   ```tsx
   function {Entity}List() {
     const { {entities}, tokenReady, isLoading } = use{Entities}();
     if (!tokenReady) return <AuthPrompt />;
     return <List items={{entities}} />;
   }
   ```

### Anti-Patterns Now Prevented

**❌ Blocked by rules:**

- Direct fetch calls in components
- Next.js API proxy routes
- Direct SWR usage without authentication
- `createAuthenticatedServerApiClient` usage
- Missing cache invalidation
- Missing authentication state handling
- Inconsistent error handling patterns

**✅ Enforced patterns:**

- Universal Client Pattern flow
- `useApiQuery` for data fetching
- `useApiMutation` for mutations
- Generated SDK usage only
- Proper authentication handling
- Smart cache management
- Type-safe implementations

## 🔧 Developer Experience

### Auto-Completion and Type Safety

- IntelliSense support for all operations
- Compile-time validation of API calls
- Generated types from OpenAPI spec
- Consistent interfaces across domains

### Error Prevention

- Prevents direct API calls bypassing authentication
- Enforces cache invalidation after mutations
- Requires authentication state handling
- Validates proper hook usage patterns

### Consistency

- Same patterns across all domains
- Standardized error handling
- Consistent loading states
- Unified authentication flow

## 📊 Implementation Status

### Task Management (Reference Implementation)

- ✅ Complete Universal Client Pattern implementation
- ✅ All hooks use `useApiQuery`/`useApiMutation`
- ✅ Repository layer with generated SDK
- ✅ Comprehensive TypeScript types
- ✅ Smart cache invalidation
- ✅ Authentication handling

### Other Domains

- 🔄 **Ready for migration** to Universal Client Pattern
- 🔄 **Existing patterns** should be updated to follow new rules
- 🔄 **New implementations** must follow Universal Client Pattern

## 🚀 Next Steps

### For New Features

1. Follow the enforced Universal Client Pattern
2. Use task management as reference implementation
3. Implement all required layers (types → repository → hooks → components)
4. Test authentication and cache invalidation

### For Existing Code

1. Migrate from direct fetch to Universal Client Pattern
2. Replace `createAuthenticatedServerApiClient` with repositories
3. Update direct SWR usage to `useApiQuery`
4. Add proper authentication handling

### Quality Assurance

1. Cursor rules now prevent anti-patterns
2. TypeScript compilation enforces type safety
3. Tests validate authentication flow
4. Documentation stays in sync with implementation

The cursor rules now provide comprehensive guidance and enforcement for maintaining consistency, type safety, and proper authentication across all API integrations in the Experts Project.
