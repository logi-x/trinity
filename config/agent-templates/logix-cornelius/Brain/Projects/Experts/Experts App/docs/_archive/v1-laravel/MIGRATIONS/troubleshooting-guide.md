---
title: "Troubleshooting Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/migrations"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Troubleshooting Guide

## 📋 Overview

This guide provides solutions to common issues encountered after the Next.js consolidation and pnpm migration. Use this as a quick reference when encountering problems during development or deployment.

## 🔍 Quick Diagnosis

### Common Symptoms

| Symptom                                              | Likely Cause                        | Quick Fix                                                         |
| ---------------------------------------------------- | ----------------------------------- | ----------------------------------------------------------------- |
| `pnpm: not found`                                    | pnpm not installed                  | Run `corepack enable && corepack prepare pnpm@10.25.0 --activate` |
| `Module not found: '@experts/...'`                   | Workspace package not installed     | Run `pnpm install`                                                |
| `Cannot find module '@experts/tsconfig/nextjs.json'` | Missing exports in tsconfig package | Check package.json exports field                                  |
| `sh: tsup: not found`                                | tsup in wrong dependency category   | Move tsup to dependencies or skip build                           |
| `ERR_PNPM_NO_GLOBAL_BIN_DIR`                         | Global bin directory not configured | Set `PNPM_HOME` and configure global-bin-dir                      |
| Build timeout in Docker                              | Inefficient Docker layers           | Optimize Dockerfile layer caching                                 |
| Hot reload not working                               | Port conflict or cache issue        | Clear .next cache and restart dev server                          |
| TypeScript errors after install                      | Stale type definitions              | Run `pnpm install` and restart TypeScript server                  |

## 🔧 pnpm Installation Issues

### Issue 1: pnpm Command Not Found

**Symptoms:**

```bash
bash: pnpm: command not found
```

**Diagnosis:**

```bash
# Check if pnpm is installed
which pnpm

# Check Node version
node --version  # Should be >= 20.0.0
```

**Solutions:**

**Option 1: Using corepack (Recommended)**

```bash
# Enable corepack
corepack enable

# Prepare pnpm
corepack prepare pnpm@10.25.0 --activate

# Verify installation
pnpm --version
```

**Option 2: Global installation**

```bash
# Install globally
npm install -g pnpm@10.25.0

# Verify installation
pnpm --version
```

**Option 3: Docker environment**

```dockerfile
# Add to Dockerfile
ENV PNPM_HOME=/root/.local/share/pnpm
ENV PATH=$PNPM_HOME:$PATH
RUN corepack enable && corepack prepare pnpm@10.25.0 --activate
```

### Issue 2: Global Bin Directory Error

**Symptoms:**

```bash
ERR_PNPM_NO_GLOBAL_BIN_DIR Unable to find the global bin directory
```

**Diagnosis:**

```bash
# Check pnpm config
pnpm config list

# Check global bin dir setting
pnpm config get global-bin-dir
```

**Solution:**

```bash
# Set global bin directory
pnpm config set global-bin-dir ~/.local/share/pnpm

# Or in Docker
ENV PNPM_HOME=/root/.local/share/pnpm
ENV PATH=$PNPM_HOME:$PATH
RUN pnpm config set global-bin-dir $PNPM_HOME
```

### Issue 3: Turbo Installation Fails

**Symptoms:**

```bash
pnpm global add turbo
ERR_PNPM_NO_GLOBAL_BIN_DIR
```

**Solution:**

```bash
# Use -g flag instead of global
pnpm add -g turbo

# Or add to package.json
pnpm add turbo --save-dev
```

## 📦 Workspace Package Resolution

### Issue 4: Workspace Package Not Found

**Symptoms:**

```bash
Module not found: Can't resolve '@experts/sdk'
Module not found: Can't resolve '@experts/ui'
```

**Diagnosis:**

```bash
# Check workspace packages
pnpm list --depth=0

# Check specific package
pnpm list @experts/sdk

# Verify workspace config
cat pnpm-workspace.yaml
```

**Solutions:**

**Solution 1: Reinstall dependencies**

```bash
# Clean install
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

**Solution 2: Add missing package**

```bash
# Add to specific workspace
pnpm add @experts/sdk --filter=@logi-x/experts-app

# Or add to all workspaces
pnpm add @experts/sdk --recursive
```

**Solution 3: Fix pnpm-workspace.yaml**

```yaml
# Ensure correct workspace configuration
packages:
  - "apps/*"
  - "packages/**" # Use recursive glob
```

### Issue 5: TypeScript Configuration Not Found

**Symptoms:**

```bash
Cannot find module '@experts/tsconfig/nextjs.json'
File 'node_modules/@experts/tsconfig/nextjs.json' not found
```

**Diagnosis:**

```bash
# Check if package is installed
pnpm list @experts/tsconfig

# Check package exports
cat packages/core/config/tsconfig/package.json
```

**Solution:**

**Step 1: Add exports to package.json**

```json
{
  "name": "@experts/tsconfig",
  "exports": {
    "./base.json": "./base.json",
    "./nextjs.json": "./nextjs.json",
    "./node.json": "./node.json",
    "./react-library.json": "./react-library.json"
  }
}
```

**Step 2: Add as dependency**

```bash
pnpm add @experts/tsconfig --filter=@logi-x/experts-app --save-dev
```

**Step 3: Reinstall**

```bash
pnpm install
```

### Issue 6: Phantom Dependencies

**Symptoms:**

```bash
# Package works locally but fails in CI/CD
TypeError: Cannot read property 'X' of undefined
```

**Diagnosis:**

```bash
# Check for undeclared dependencies
pnpm why <package-name>

# Audit dependencies
pnpm audit
```

**Solution:**

```bash
# Add missing dependency explicitly
pnpm add <missing-package> --filter=<workspace>

# Or configure to allow phantom deps (not recommended)
# .npmrc
shamefully-hoist=true
```

## 🏗️ Build Issues

### Issue 7: Build Tool Not Found

**Symptoms:**

```bash
sh: tsup: not found
sh: tsc: not found
```

**Diagnosis:**

```bash
# Check if tool is installed
pnpm list tsup

# Check package.json scripts
cat package.json | grep -A 5 "scripts"
```

**Solutions:**

**Solution 1: Skip unnecessary builds**

```json
{
  "scripts": {
    "build:fast": "echo 'Skipping build - using TypeScript sources directly'"
  }
}
```

**Solution 2: Move to dependencies**

```bash
# If build tool is needed in production
pnpm remove tsup --filter=@experts/utils
pnpm add tsup --filter=@experts/utils
```

**Solution 3: Use TypeScript sources**

```json
{
  "main": "index.ts",
  "types": "index.ts",
  "exports": {
    ".": "./index.ts"
  }
}
```

### Issue 8: TypeScript Compilation Errors

**Symptoms:**

```bash
TS2307: Cannot find module '@experts/types'
TS2345: Argument of type 'X' is not assignable to parameter of type 'Y'
```

**Diagnosis:**

```bash
# Check TypeScript version
pnpm list typescript

# Check tsconfig.json
cat tsconfig.json

# Run type check
pnpm run type-check
```

**Solutions:**

**Solution 1: Restart TypeScript server**

```bash
# In VS Code: Cmd/Ctrl + Shift + P
# Type: "TypeScript: Restart TS Server"
```

**Solution 2: Clear TypeScript cache**

```bash
# Remove TypeScript build info
rm -rf **/*.tsbuildinfo

# Clear .next cache
rm -rf .next

# Reinstall
pnpm install
```

**Solution 3: Fix tsconfig paths**

```json
{
  "compilerOptions": {
    "paths": {
      "@experts/*": ["../../packages/*/src", "../../packages/core/*/src"]
    }
  }
}
```

### Issue 9: Next.js Build Errors

**Symptoms:**

```bash
Error: Failed to compile
Module not found: Can't resolve 'X'
```

**Diagnosis:**

```bash
# Check Next.js config
cat next.config.js

# Check for circular dependencies
pnpm run build --verbose
```

**Solutions:**

**Solution 1: Clear Next.js cache**

```bash
rm -rf .next
rm -rf node_modules/.cache
pnpm run build
```

**Solution 2: Fix import paths**

```typescript
// Use correct import syntax
import { Button } from "@experts/ui"; // ✅ Correct
import Button from "@experts/ui/Button"; // ❌ May fail
```

**Solution 3: Add to next.config.js**

```javascript
module.exports = {
  transpilePackages: ["@experts/ui", "@experts/utils"],
};
```

## 🐳 Docker Issues

### Issue 10: Docker Build Fails with pnpm

**Symptoms:**

```bash
pnpm: not found
/bin/sh: pnpm: not found
```

**Solution:**

```dockerfile
FROM node:20-alpine AS base

# Setup pnpm
ENV PNPM_HOME=/root/.local/share/pnpm
ENV PATH=$PNPM_HOME:$PATH
RUN corepack enable && corepack prepare pnpm@10.25.0 --activate
RUN pnpm config set global-bin-dir $PNPM_HOME
```

### Issue 11: Docker Layer Caching Not Working

**Symptoms:**

```bash
# Every build reinstalls all dependencies
Step 5/20 : RUN pnpm install --frozen-lockfile
```

**Solution:**

```dockerfile
# Optimize layer order
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile

# Then copy source files
COPY . .
```

### Issue 12: Docker Build Timeout

**Symptoms:**

```bash
ERROR: process did not complete successfully: signal: killed
```

**Solutions:**

**Solution 1: Increase Docker memory**

```bash
# Docker Desktop: Settings > Resources > Memory
# Increase to at least 4GB
```

**Solution 2: Use multi-stage builds**

```dockerfile
# Separate builder stage
FROM base AS builder
RUN pnpm install --frozen-lockfile
RUN pnpm build

# Smaller production stage
FROM base AS production
COPY --from=builder /app/.next ./next
```

**Solution 3: Optimize build process**

```bash
# Use turbo for faster builds
RUN pnpm turbo build --filter=@logi-x/experts-app
```

## 🚀 Development Server Issues

### Issue 13: Hot Reload Not Working

**Symptoms:**

```bash
# Changes not reflected in browser
# File watching not working
```

**Solutions:**

**Solution 1: Clear cache and restart**

```bash
rm -rf .next
rm -rf node_modules/.cache
pnpm run dev
```

**Solution 2: Increase file watchers**

```bash
# Linux: Increase inotify limit
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

**Solution 3: Check port conflicts**

```bash
# Find process using port 3000
lsof -i :3000

# Kill process if needed
kill -9 <PID>
```

### Issue 14: Port Already in Use

**Symptoms:**

```bash
Error: listen EADDRINUSE: address already in use :::3000
```

**Solutions:**

**Solution 1: Kill existing process**

```bash
# Find and kill process
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 pnpm run dev
```

**Solution 2: Change default port**

```json
{
  "scripts": {
    "dev": "next dev -p 3001"
  }
}
```

### Issue 15: Environment Variables Not Loading

**Symptoms:**

```bash
process.env.NEXT_PUBLIC_API_URL is undefined
```

**Solutions:**

**Solution 1: Check .env file**

```bash
# Ensure .env.local exists
ls -la .env.local

# Verify variables are prefixed correctly
cat .env.local | grep NEXT_PUBLIC_
```

**Solution 2: Restart dev server**

```bash
# Environment variables are loaded on server start
pnpm run dev
```

**Solution 3: Check Next.js config**

```javascript
module.exports = {
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
};
```

## 🔄 CI/CD Issues

### Issue 16: CI/CD Build Failures

**Symptoms:**

```bash
# Build succeeds locally but fails in CI/CD
Error: Cannot find module '@experts/sdk'
```

**Solutions:**

**Solution 1: Use frozen lockfile**

```yaml
# .github/workflows/build.yml
- run: pnpm install --frozen-lockfile
```

**Solution 2: Cache dependencies**

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.pnpm-store
    key: ${{ runner.os }}-pnpm-${{ hashFiles('**/pnpm-lock.yaml') }}
```

**Solution 3: Check Node version**

```yaml
- uses: actions/setup-node@v3
  with:
    node-version: "20"
```

### Issue 17: Docker Build in CI/CD Fails

**Symptoms:**

```bash
ERROR: failed to solve: process did not complete successfully
```

**Solutions:**

**Solution 1: Use buildx with cache**

```yaml
- uses: docker/build-push-action@v4
  with:
    cache-from: type=registry,ref=${{ env.IMAGE }}:latest
    cache-to: type=inline
```

**Solution 2: Increase timeout**

```yaml
timeout-minutes: 30
```

**Solution 3: Use smaller base image**

```dockerfile
FROM node:20-alpine  # Instead of node:20
```

## 📊 Performance Issues

### Issue 18: Slow Package Installation

**Symptoms:**

```bash
# pnpm install takes > 3 minutes
```

**Solutions:**

**Solution 1: Use pnpm store**

```bash
# Set store directory
pnpm config set store-dir ~/.pnpm-store

# Clean old packages
pnpm store prune
```

**Solution 2: Enable network concurrency**

```ini
# .npmrc
network-concurrency=16
fetch-retries=3
fetch-retry-mintimeout=10000
```

**Solution 3: Use local registry mirror**

```ini
# .npmrc
registry=https://registry.npmjs.org/
```

### Issue 19: Large node_modules Size

**Symptoms:**

```bash
# node_modules > 1GB
```

**Solutions:**

**Solution 1: Remove duplicate packages**

```bash
# Check for duplicates
pnpm list --depth=Infinity | grep -A 2 "^[├└]"

# Deduplicate
pnpm dedupe
```

**Solution 2: Use pnpm's content-addressable storage**

```bash
# Already enabled by default with pnpm
# Verify with
pnpm config get store-dir
```

**Solution 3: Remove unused dependencies**

```bash
# Check for unused deps
pnpm outdated

# Remove unused
pnpm prune
```

## 🛠️ Common Quick Fixes

### Universal Reset Procedure

When in doubt, try this reset procedure:

```bash
# 1. Clean everything
rm -rf node_modules pnpm-lock.yaml
rm -rf .next .turbo
rm -rf packages/*/node_modules
rm -rf apps/*/node_modules

# 2. Clear pnpm cache
pnpm store prune

# 3. Fresh install
pnpm install

# 4. Rebuild
pnpm run build

# 5. Restart dev server
pnpm run dev
```

### Quick Diagnostic Commands

```bash
# Check pnpm version
pnpm --version

# List workspace packages
pnpm list --depth=0

# Check specific package
pnpm why <package-name>

# Verify workspace config
cat pnpm-workspace.yaml

# Check for TypeScript errors
pnpm run type-check

# Check for linting errors
pnpm run lint

# Verify build works
pnpm run build --dry-run
```

## 📞 Getting Help

### Information to Provide

When asking for help, provide:

1. **Error message** (full stack trace)
2. **pnpm version**: `pnpm --version`
3. **Node version**: `node --version`
4. **OS**: `uname -a` (Linux/Mac) or `ver` (Windows)
5. **Steps to reproduce**
6. **Recent changes** made before error occurred

### Useful Debug Commands

```bash
# Verbose pnpm output
pnpm install --verbose

# Debug mode
pnpm install --loglevel=debug

# Check pnpm config
pnpm config list

# Validate workspace
pnpm list --depth=0 --json
```

## 🔗 Related Documentation

- [Next.js Consolidation](./nextjs-consolidation.md)
- [Yarn to pnpm Migration](./yarn-to-pnpm-migration.md)
- [Docker Optimization](./docker-optimization.md)
- [Performance Comparison](./performance-comparison.md)
- [Best Practices](./best-practices.md)
- [Developer Onboarding](./developer-onboarding.md)

---

**Last Updated**: October 29, 2025  
**Status**: ✅ Active Reference Guide  
**Next Steps**: Report issues not covered here for documentation updates
