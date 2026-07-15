---
title: "Migration Best Practices and Lessons Learned"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/migrations"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Migration Best Practices and Lessons Learned

## 📋 Overview

This document captures the best practices, lessons learned, and recommendations from the successful Next.js consolidation and Yarn to pnpm migration. Use this guide to inform future architectural decisions and migrations.

## 🎯 Core Principles

### 1. Start with a Clear Plan

- ✅ **DO**: Create detailed migration plan with milestones
- ✅ **DO**: Document current state before starting
- ✅ **DO**: Establish clear success criteria
- ✅ **DO**: Plan for rollback scenarios
- ❌ **DON'T**: Start migration without understanding scope

### 2. Maintain Backwards Compatibility

- ✅ **DO**: Ensure existing functionality works during migration
- ✅ **DO**: Run parallel systems during transition when possible
- ✅ **DO**: Keep rollback option available
- ❌ **DON'T**: Break existing features without plan to fix them
- ❌ **DON'T**: Deploy breaking changes without communication

### 3. Test Thoroughly

- ✅ **DO**: Test each migration step independently
- ✅ **DO**: Run full test suite after each major change
- ✅ **DO**: Validate in staging environment before production
- ✅ **DO**: Test rollback procedures
- ❌ **DON'T**: Skip testing to save time

## 📦 Package Management Best Practices

### pnpm Workspace Configuration

**✅ DO: Use Simple Glob Patterns**

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/**" # Recursive glob for nested packages
```

**❌ DON'T: Overcomplicate Workspace Config**

```yaml
# Avoid overly specific patterns
packages:
  - "packages/core/*"
  - "packages/core/config/*"
  - "packages/core/config/tsconfig/*"
```

### Dependency Management

**✅ DO: Use Workspace Protocol**

```json
{
  "dependencies": {
    "@experts/ui": "workspace:*",
    "@experts/utils": "workspace:*"
  }
}
```

**✅ DO: Be Explicit with Dependencies**

```bash
# Add dependencies explicitly
pnpm add @experts/sdk --filter=@logi-x/experts-app
```

**❌ DON'T: Rely on Phantom Dependencies**

```javascript
// Wrong: Using lodash without declaring it
import _ from "lodash"; // ❌ Not in package.json

// Right: Declare all dependencies
// package.json: "lodash": "^4.17.21"
import _ from "lodash"; // ✅ Explicit dependency
```

### Lock File Management

**✅ DO: Commit Lock Files**

```bash
git add pnpm-lock.yaml
git commit -m "chore: update dependencies"
```

**✅ DO: Use Frozen Lockfile in CI/CD**

```yaml
# .github/workflows/build.yml
- run: pnpm install --frozen-lockfile
```

**❌ DON'T: Manually Edit Lock Files**

```bash
# Never do this
vim pnpm-lock.yaml  # ❌ Don't manually edit
```

## 🏗️ Architecture Best Practices

### Application Structure

**✅ DO: Use Route Groups for Organization**

```typescript
// apps/experts-app/src/app/
├── (admin)/     // Admin routes - invisible to URL
├── (portal)/    // Portal routes - invisible to URL
└── auth/        // Auth routes - visible in URL
```

**✅ DO: Centralize Shared Components**

```typescript
// packages/ui/src/
├── admin/       // Admin-specific
├── portal/      // Portal-specific
├── auth/        // Auth-specific
└── shared/      // Truly shared
```

**❌ DON'T: Duplicate Components Across Apps**

```typescript
// Wrong: Component in multiple places
apps / experts - admin / components / Button.tsx; // ❌
apps / experts - portal / components / Button.tsx; // ❌

// Right: Single source of truth
packages / ui / src / shared / Button.tsx; // ✅
```

### Code Organization

**✅ DO: Follow Consistent Naming**

```typescript
// File naming
Button.tsx; // ✅ Component
use - auth.ts; // ✅ Hook
auth - service.ts; // ✅ Service
auth.types.ts; // ✅ Types
```

**✅ DO: Use Barrel Exports**

```typescript
// packages/ui/src/index.ts
export { Button } from "./shared/Button";
export { Input } from "./shared/Input";
export { Modal } from "./shared/Modal";
```

**❌ DON'T: Mix Naming Conventions**

```typescript
ButtonComponent.tsx; // ❌ Inconsistent
useAuthHook.ts; // ❌ Redundant "Hook"
AuthService.ts; // ❌ PascalCase for service
```

## 🐳 Docker Best Practices

### Dockerfile Optimization

**✅ DO: Use Multi-Stage Builds**

```dockerfile
FROM node:20-alpine AS base
# Setup stage

FROM base AS builder
# Build stage

FROM base AS production
# Production stage
```

**✅ DO: Order Layers by Change Frequency**

```dockerfile
# Rarely changes
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Changes frequently
COPY . .
RUN pnpm build
```

**✅ DO: Setup pnpm Correctly**

```dockerfile
ENV PNPM_HOME=/root/.local/share/pnpm
ENV PATH=$PNPM_HOME:$PATH
RUN corepack enable && corepack prepare pnpm@10.25.0 --activate
RUN pnpm config set global-bin-dir $PNPM_HOME
```

**❌ DON'T: Copy Unnecessary Files**

```dockerfile
# Wrong: Copies everything including node_modules
COPY . .  # ❌ Too broad

# Right: Use .dockerignore
# .dockerignore
node_modules
.next
.git
```

### Docker Performance

**✅ DO: Leverage Build Cache**

```bash
# Use cache from registry
docker build --cache-from myapp:latest -t myapp:new .
```

**✅ DO: Use Smaller Base Images**

```dockerfile
FROM node:20-alpine  # ✅ 120MB
# Not: FROM node:20  # ❌ 900MB
```

**✅ DO: Clean Up in Same Layer**

```dockerfile
RUN apk add --no-cache build-base \
    && pnpm install \
    && apk del build-base  # Clean up in same layer
```

## 🔧 Build System Best Practices

### TypeScript Configuration

**✅ DO: Use Extends for Shared Config**

```json
{
  "extends": "@experts/tsconfig/nextjs.json",
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

**✅ DO: Export TypeScript Configs Properly**

```json
{
  "name": "@experts/tsconfig",
  "exports": {
    "./nextjs.json": "./nextjs.json",
    "./node.json": "./node.json"
  }
}
```

**❌ DON'T: Duplicate TypeScript Config**

```json
// Wrong: Duplicating config across apps
apps/experts-admin/tsconfig.json  // ❌ Full config
apps/experts-portal/tsconfig.json // ❌ Full config

// Right: Extend shared config
apps/*/tsconfig.json  // ✅ Extends shared
```

### Build Optimization

**✅ DO: Skip Unnecessary Builds**

```json
{
  "scripts": {
    "build:fast": "echo 'Using TypeScript sources directly'"
  }
}
```

**✅ DO: Use Turbo for Monorepo Builds**

```json
{
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev"
  }
}
```

**✅ DO: Optimize Bundle Size**

```javascript
// next.config.js
module.exports = {
  compiler: {
    removeConsole: process.env.NODE_ENV === "production",
  },
  experimental: {
    optimizeCss: true,
  },
};
```

## 🚀 CI/CD Best Practices

### Pipeline Configuration

**✅ DO: Use Matrix Jobs for Parallel Builds**

```yaml
jobs:
  test:
    strategy:
      matrix:
        node-version: [18, 20]
    runs-on: ubuntu-latest
    steps:
      - uses: pnpm/action-setup@v2
      - run: pnpm test
```

**✅ DO: Cache Dependencies**

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.pnpm-store
    key: ${{ runner.os }}-pnpm-${{ hashFiles('**/pnpm-lock.yaml') }}
```

**✅ DO: Fail Fast on Critical Errors**

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: pnpm lint
      - run: pnpm type-check

  test:
    needs: lint # Only run if lint passes
    runs-on: ubuntu-latest
```

**❌ DON'T: Skip Important Checks**

```yaml
# Wrong: Skipping type checking
- run: pnpm build --no-type-check # ❌

# Right: Always type check
- run: pnpm run type-check # ✅
- run: pnpm build # ✅
```

### Deployment Strategy

**✅ DO: Use Staging Environment**

```yaml
# Deploy to staging first
- name: Deploy to Staging
  if: github.ref == 'refs/heads/develop'

# Then to production
- name: Deploy to Production
  if: github.ref == 'refs/heads/main'
```

**✅ DO: Include Health Checks**

```yaml
- name: Health Check
  run: |
    curl -f https://api.example.com/health
```

**✅ DO: Enable Rollback**

```yaml
- name: Rollback on Failure
  if: failure()
  run: |
    kubectl rollout undo deployment/experts-app
```

## 💡 Development Workflow Best Practices

### Local Development

**✅ DO: Use Consistent Node Version**

```json
{
  "engines": {
    "node": ">=20.0.0",
    "pnpm": ">=10.0.0"
  }
}
```

**✅ DO: Document Environment Variables**

```bash
# .env.example
NEXT_PUBLIC_API_URL=https://api.example.com
DATABASE_URL=postgresql://user:pass@localhost:5432/db
```

**✅ DO: Use Pre-commit Hooks**

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "pnpm lint-staged",
      "pre-push": "pnpm test"
    }
  }
}
```

**❌ DON'T: Commit Secrets**

```bash
# .gitignore
.env.local
.env.production
*.pem
*.key
```

### Code Quality

**✅ DO: Run Linters Before Commit**

```bash
# Run before committing
pnpm run lint
pnpm run type-check
pnpm run test
```

**✅ DO: Use Consistent Formatting**

```json
{
  "scripts": {
    "format": "prettier --write \"**/*.{ts,tsx,js,jsx,json,md}\"",
    "format:check": "prettier --check \"**/*.{ts,tsx,js,jsx,json,md}\""
  }
}
```

**✅ DO: Write Meaningful Commit Messages**

```bash
# Good commit messages
git commit -m "feat(auth): add OAuth2 login support"
git commit -m "fix(ui): resolve button alignment issue"
git commit -m "chore(deps): update dependencies"

# Bad commit messages
git commit -m "update"  # ❌ Too vague
git commit -m "fix"     # ❌ No context
```

## 📊 Performance Best Practices

### Optimization Strategies

**✅ DO: Measure Before Optimizing**

```typescript
// Use performance monitoring
import { performance } from "perf_hooks";

const start = performance.now();
// ... code to measure
const end = performance.now();
console.log(`Execution time: ${end - start}ms`);
```

**✅ DO: Optimize Bundle Size**

```javascript
// Use dynamic imports for large components
const HeavyComponent = dynamic(() => import("./HeavyComponent"), {
  ssr: false,
  loading: () => <div>Loading...</div>,
});
```

**✅ DO: Implement Caching**

```typescript
// Use SWR or React Query for data caching
import useSWR from "swr";

function useData() {
  const { data, error } = useSWR("/api/data", fetcher, {
    revalidateOnFocus: false,
    dedupingInterval: 10000,
  });
  return { data, error };
}
```

**❌ DON'T: Premature Optimization**

```typescript
// Wrong: Optimizing before identifying bottleneck
const memoizedComponent = useMemo(() => <Component />, [])  // ❌

// Right: Optimize based on profiling
// Use React DevTools Profiler to identify slow components first
```

### Resource Management

**✅ DO: Clean Up Resources**

```typescript
useEffect(() => {
  const subscription = api.subscribe();

  // Cleanup function
  return () => {
    subscription.unsubscribe();
  };
}, []);
```

**✅ DO: Implement Error Boundaries**

```typescript
class ErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    // Log error to monitoring service
    logErrorToService(error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />
    }
    return this.props.children
  }
}
```

## 🎯 Lessons Learned

### What Worked Well

1. **Incremental Migration**: Breaking down migration into phases
2. **Comprehensive Testing**: Testing at each step prevented major issues
3. **Clear Documentation**: Documenting changes as we went
4. **Team Communication**: Regular updates kept everyone informed
5. **Rollback Plan**: Having fallback options provided confidence

### What Could Be Improved

1. **Earlier Testing**: Should have tested Docker builds earlier
2. **Dependency Audit**: Could have audited dependencies before migration
3. **Performance Benchmarks**: Should have established baselines earlier
4. **Training**: Could have provided team training before migration
5. **Monitoring**: Should have set up monitoring from day one

### Key Takeaways

1. **Plan Thoroughly**: Time spent planning saves time during execution
2. **Test Continuously**: Catching issues early prevents major problems
3. **Document Everything**: Good documentation helps everyone
4. **Communicate Often**: Keep stakeholders informed
5. **Stay Flexible**: Be ready to adjust plan based on learnings

## 🔄 Future Recommendations

### Short-term (1-3 months)

1. **Monitoring**: Implement comprehensive performance monitoring
2. **Optimization**: Continue optimizing build and bundle sizes
3. **Documentation**: Keep migration docs updated
4. **Training**: Conduct team training on new architecture
5. **Feedback**: Gather and address team feedback

### Medium-term (3-6 months)

1. **Performance**: Analyze and optimize based on real-world data
2. **Scaling**: Plan for scaling unified application
3. **Features**: Add features that leverage unified architecture
4. **Testing**: Enhance test coverage
5. **Security**: Conduct security audit

### Long-term (6-12 months)

1. **Architecture**: Evaluate and refine architecture based on growth
2. **Infrastructure**: Optimize infrastructure costs
3. **Developer Experience**: Continue improving developer workflow
4. **Best Practices**: Refine and document new best practices
5. **Knowledge Sharing**: Share learnings with wider community

## 📚 Recommended Reading

### Official Documentation

- [pnpm Documentation](https://pnpm.io/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Turborepo Documentation](https://turbo.build/repo/docs)

### Community Resources

- [Monorepo Best Practices](https://monorepo.tools/)
- [Package Management Comparison](https://npmtrends.com/)
- [Next.js Performance Optimization](https://nextjs.org/docs/advanced-features/measuring-performance)

## 🔗 Related Documentation

- [Next.js Consolidation](./nextjs-consolidation.md)
- [Yarn to pnpm Migration](./yarn-to-pnpm-migration.md)
- [Docker Optimization](./docker-optimization.md)
- [Performance Comparison](./performance-comparison.md)
- [Troubleshooting Guide](./troubleshooting-guide.md)
- [Developer Onboarding](./developer-onboarding.md)

---

**Last Updated**: October 29, 2025  
**Status**: ✅ Living Document - Continuously Updated  
**Next Review**: January 2026  
**Contributions**: Welcome - Submit PRs with new learnings
