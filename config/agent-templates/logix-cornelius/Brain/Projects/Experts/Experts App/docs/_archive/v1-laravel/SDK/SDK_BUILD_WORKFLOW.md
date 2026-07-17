---
title: "SDK Build Workflow"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/sdk"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# SDK Build Workflow

Complete workflow for generating and using the SDK in the experts ecosystem.

## Overview

The SDK workflow involves a chain of dependencies:

```
experts-api (.env)
    ↓
experts-api (scribe:generate) → OpenAPI spec
    ↓
@experts/sdk (openapi-typescript-codegen) → Generated SDK
    ↓
experts-app (build) → Uses SDK
```

## Complete Workflow

### Step 1: Generate API Documentation

Generate OpenAPI specs for each environment using the `experts-docs` service:

```bash
# Canary
cd docker/canary
docker compose run --rm experts-docs

# Staging
cd docker/staging
docker compose run --rm experts-docs

# Production
cd docker/production
docker compose run --rm experts-docs
```

**Output:** `apps/experts-api/public/docs/{env}/openapi.yaml`

### Step 2: Generate SDK Tarball

Generate SDK from the OpenAPI specs using the `experts-sdk` service:

```bash
# Canary
cd docker/canary
docker compose run --rm experts-sdk

# Staging
cd docker/staging
docker compose run --rm experts-sdk

# Production
cd docker/production
docker compose run --rm experts-sdk
```

**Output:** `packages/sdk/dist/experts-sdk-1.0.0.tgz` (with correct permissions)

### Step 3: Install SDK into Monorepo

Install the generated SDK tarball so experts-app can use it:

```bash
# Install SDK for specific environment
./scripts/install-sdk.sh canary
./scripts/install-sdk.sh staging
./scripts/install-sdk.sh production
```

This installs the tarball into the monorepo's `node_modules`.

### Step 4: Build experts-app

Now you can build experts-app with the generated SDK:

**Option A: Local Build (Fast, uses Turbo cache)**

```bash
# The script will check SDK is installed automatically
./apps/experts-app/docker/build-local.sh canary loogix/experts-app:canary
./apps/experts-app/docker/build-local.sh staging loogix/experts-app:staging
./apps/experts-app/docker/build-local.sh production loogix/experts-app:latest
```

**Option B: Docker Build**

```bash
cd docker/canary
docker compose build experts-app
```

## Quick Reference

### Full Deployment Pipeline

```bash
ENV=canary  # or staging, production

# 1. Generate API docs
cd docker/$ENV && docker compose run --rm experts-docs

# 2. Generate SDK
docker compose run --rm experts-sdk

# 3. Install SDK
cd ../../
./scripts/install-sdk.sh $ENV

# 4. Build app (local - fast!)
./apps/experts-app/docker/build-local.sh $ENV loogix/experts-app:$ENV

# 5. Push image
docker push loogix/experts-app:$ENV
```

### Individual Commands

```bash
# Check SDK installation
pnpm list @experts/sdk

# Verify SDK tarball exists
ls -lh packages/sdk/dist/

# Manually install SDK
pnpm install packages/sdk/dist/experts-sdk-*.tgz --workspace-root

# Generate docs manually (inside running API container)
docker compose exec experts-api php artisan scribe:generate
```

## Architecture

### Files and Services

#### Docker Compose Services

**experts-docs** (docker/{env}/docker-compose.yml)

- Builds: `apps/experts-api/Dockerfile.docs`
- Purpose: Generate OpenAPI specs with correct environment
- Output: `apps/experts-api/public/docs/{env}/openapi.yaml`

**experts-sdk** (docker/{env}/docker-compose.yml)

- Builds: `packages/sdk/Dockerfile.sdk`
- Purpose: Generate SDK tarball from OpenAPI spec
- Output: `packages/sdk/dist/experts-sdk-*.tgz`
- Volume: Mounted to `/output` with correct UID/GID

**experts-app** (docker/{env}/docker-compose.yml)

- Builds: `apps/experts-app/Dockerfile`
- Purpose: Build Next.js application
- Requires: SDK installed in `node_modules`

#### Scripts

**scripts/install-sdk.sh**

- Installs generated SDK tarball into monorepo
- Verifies installation
- Usage: `./scripts/install-sdk.sh {env}`

**apps/experts-app/docker/build-local.sh**

- Fast local build strategy
- Checks SDK is installed
- Auto-installs if needed
- Uses Turbo cache for speed
- Usage: `./build-local.sh {env} {tag}`

### Dockerfiles

**apps/experts-api/Dockerfile.docs**

```dockerfile
FROM experts-api AS docs-generator
RUN php artisan scribe:generate
# Outputs to public/docs/{APP_ENV}/
```

**packages/sdk/Dockerfile.sdk**

```dockerfile
# Stage 1: Generate SDK
FROM node:lts AS builder
COPY apps/experts-api/public/docs/${APP_ENV}/openapi.yaml ./
RUN openapi-typescript-codegen ...
RUN npm pack

# Stage 2: Output with permissions
FROM alpine AS runner
COPY --from=builder *.tgz /output/
RUN chown ${HOST_UID}:${HOST_GID} /output
```

## Environment Configuration

### Required Environment Variables

Each environment needs proper configuration:

**API (.env.{env})**

```env
APP_ENV=canary
API_EXTERNAL_URL=https://api.canary.experts.com.sa
```

**App (.env.{env})**

```env
NEXT_PUBLIC_APP_ENV=canary
NEXT_PUBLIC_API_URL=https://api.canary.experts.com.sa
```

### SDK Configuration Override

The SDK auto-configures from environment variables:

**packages/sdk/src/config.ts**

```typescript
// Automatically reads NEXT_PUBLIC_API_URL
if (typeof process !== "undefined" && process.env?.NEXT_PUBLIC_API_URL) {
  OpenAPI.BASE = process.env.NEXT_PUBLIC_API_URL;
}
```

## Troubleshooting

### SDK tarball owned by root

**Issue:** After running `docker compose run --rm experts-sdk`, tarball is owned by root

**Solution:** Already fixed! The Dockerfile now:

1. Accepts `HOST_UID` and `HOST_GID` build args
2. Sets ownership in the runner stage
3. Outputs to volume with correct permissions

### SDK not found during build

**Issue:** `Module not found: @experts/sdk`

**Solutions:**

1. Check tarball exists: `ls packages/sdk/dist/`
2. Run: `./scripts/install-sdk.sh {env}`
3. Verify: `pnpm list @experts/sdk`

### Wrong API URL in SDK

**Issue:** SDK points to wrong environment

**Cause:** Generated from wrong OpenAPI spec or wrong env vars

**Solutions:**

1. Ensure `experts-docs` ran with correct `APP_ENV`
2. Check `apps/experts-api/public/docs/{env}/openapi.yaml` exists
3. Verify `base_url` in `apps/experts-api/config/scribe.php`
4. Regenerate SDK for correct environment

### Build fails with old SDK

**Issue:** App builds with outdated SDK

**Solution:**

```bash
# 1. Regenerate docs
cd docker/{env} && docker compose run --rm experts-docs

# 2. Regenerate SDK
docker compose run --rm experts-sdk

# 3. Reinstall SDK (forces update)
rm -rf node_modules/@experts/sdk
pnpm install packages/sdk/dist/experts-sdk-*.tgz --workspace-root

# 4. Rebuild app
./apps/experts-app/docker/build-local.sh {env}
```

## Best Practices

### 1. Always Regenerate SDK for Environment Changes

When API changes or environment configuration changes:

```bash
docker compose run --rm experts-docs
docker compose run --rm experts-sdk
./scripts/install-sdk.sh {env}
```

### 2. Version SDK Tarballs (Optional)

You can keep SDK tarballs per environment:

```bash
# Rename to include environment
mv packages/sdk/dist/experts-sdk-1.0.0.tgz \
   packages/sdk/dist/experts-sdk-1.0.0-canary.tgz
```

### 3. CI/CD Integration

```yaml
# .github/workflows/build-app.yml
- name: Generate Docs
  run: docker compose -f docker/$ENV/docker-compose.yml run --rm experts-docs

- name: Generate SDK
  run: docker compose -f docker/$ENV/docker-compose.yml run --rm experts-sdk

- name: Install SDK
  run: ./scripts/install-sdk.sh $ENV

- name: Build App
  run: ./apps/experts-app/docker/build-local.sh $ENV loogix/experts-app:$ENV
```

### 4. Keep SDK in Sync

Add to your development workflow:

```bash
# After pulling latest code
./scripts/install-sdk.sh canary

# After API changes
cd docker/canary
docker compose run --rm experts-docs
docker compose run --rm experts-sdk
cd ../../
./scripts/install-sdk.sh canary
```

## Related Documentation

- [Version Management](../DOCKER/VERSION_MANAGEMENT.md)
- [Environment-Based URLs](../SESSION/ENVIRONMENT_BASED_URLS.md)
- [SDK README](https://github.com/logi-x/experts/blob/main/packages/sdk/README.md)
