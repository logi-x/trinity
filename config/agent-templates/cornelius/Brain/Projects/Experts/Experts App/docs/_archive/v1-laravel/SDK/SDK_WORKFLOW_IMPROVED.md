---
title: "SDK Build Workflow - Improved Version"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/sdk"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# SDK Build Workflow - Improved Version

## What Changed?

**Old Approach (Problematic):**

- Generated SDK as tarball (`experts-sdk-1.0.0.tgz`)
- Installed tarball via `./scripts/install-sdk.sh`
- Corrupted `pnpm-lock.yaml` with file paths
- Docker builds failed (tarball not in build context)
- Development workflow broken

**New Approach (Fixed):**

- Generate SDK source directly into `packages/sdk/src/`
- Uses pnpm workspace links (`workspace:*`)
- Clean `pnpm-lock.yaml` (no file paths)
- Works in both local development and Docker builds
- Simpler workflow

## New Workflow

### Complete Deployment Pipeline

```bash
ENV=canary  # or staging, production

# 1. Generate API docs
cd docker/$ENV && docker compose run --rm experts-docs

# 2. Generate SDK source (writes to packages/sdk/src/)
docker compose run --rm experts-sdk

# 3. Build app (no install needed - workspace:* just works!)
cd ../../
./apps/experts-app/docker/build-local.sh $ENV loogix/experts-app:$ENV

# 4. Push image
docker push loogix/experts-app:$ENV
```

## Key Improvements

### 1. No More Tarball Installation

**Before:**

```bash
# Generate tarball
docker compose run --rm experts-sdk
# Output: packages/sdk/dist/experts-sdk-1.0.0.tgz

# Install tarball (corrupts lock file!)
./scripts/install-sdk.sh canary
```

**After:**

```bash
# Generate source files
docker compose run --rm experts-sdk
# Output: packages/sdk/src/*.ts

# Nothing to install - workspace link already exists!
```

### 2. Clean Lock File

**Before (`pnpm-lock.yaml`):**

```yaml
"@experts/sdk":
  specifier: file:/home/logix/experts/packages/sdk/dist/experts-sdk-1.0.0.tgz
  version: file:packages/sdk/dist/experts-sdk-1.0.0.tgz
```

❌ Breaks Docker builds (path doesn't exist in container)

**After (`pnpm-lock.yaml`):**

```yaml
"@experts/sdk":
  specifier: workspace:*
  version: link:../../packages/sdk
```

✅ Works everywhere (local + Docker)

### 3. Simpler Build Process

**Build script changes:**

```bash
# Before
if [ -z "$SDK_TARBALL" ]; then
    echo "Run: ./scripts/install-sdk.sh $ENV"
    exit 1
fi
pnpm install "$TARBALL" --workspace-root

# After
if [ ! -f "$PROJECT_ROOT/packages/sdk/src/index.ts" ]; then
    echo "Run: docker compose run --rm experts-sdk"
    exit 1
fi
# That's it - workspace:* handles the rest!
```

## File Changes

### Modified Files

1. **`packages/sdk/Dockerfile.sdk`**
   - Changed: Generate to `/output/src` instead of packing tarball
   - Volume: Mounts entire `packages/sdk` instead of `packages/sdk/dist`

2. **`docker/{env}/docker-compose.yml`** (all environments)
   - Changed: `volumes: - ../../packages/sdk:/output`
   - Was: `volumes: - ../../packages/sdk/dist:/output`

3. **`apps/experts-app/docker/build-local.sh`**
   - Removed: Tarball checking and installation logic
   - Added: Simple source file existence check

4. **`package.json`** (root)
   - Removed: `"@experts/sdk": "file:/.../experts-sdk-1.0.0.tgz"`
   - Clean: No direct dependencies

5. **`pnpm-lock.yaml`**
   - Fixed: All SDK references use `workspace:*`
   - Clean: No file path references

### Deprecated Files

- **`scripts/install-sdk.sh`** - No longer needed (can be removed)

## Quick Reference

### Generate SDK for Environment

```bash
# Development
cd docker/development
docker compose run --rm experts-sdk
# Output: packages/sdk/src/

# Canary
cd docker/canary
docker compose run --rm experts-docs
docker compose run --rm experts-sdk

# Staging
cd docker/staging
docker compose run --rm experts-docs
docker compose run --rm experts-sdk

# Production
cd docker/production
docker compose run --rm experts-docs
docker compose run --rm experts-sdk
```

### Verify SDK is Ready

```bash
# Check source exists
ls -la packages/sdk/src/

# Verify workspace link
pnpm list @experts/sdk
# Should show: @experts/sdk link:packages/sdk
```

### Build App

```bash
# Local build (fast with Turbo cache)
./apps/experts-app/docker/build-local.sh canary loogix/experts-app:canary

# Docker build
cd docker/canary
docker compose build experts-app
```

## Architecture

### SDK Package Structure

```
packages/sdk/
├── package.json          # Defines @experts/sdk workspace package
├── src/                  # Generated SDK source (from experts-sdk service)
│   ├── index.ts         # Main entry point
│   ├── config.ts        # Runtime configuration
│   ├── setup.ts         # Public API
│   ├── core/            # Auto-generated API client
│   ├── models/          # Auto-generated TypeScript types
│   └── services/        # Auto-generated service classes
├── dist/                # Empty (no longer used for tarballs)
└── Dockerfile.sdk       # Builds SDK source from OpenAPI spec
```

### Workspace Dependency Resolution

```
apps/experts-app/package.json:
  "@experts/sdk": "workspace:*"
        ↓
packages/sdk/src/index.ts
        ↓
Generated from: apps/experts-api/public/docs/{env}/openapi.yaml
```

## Troubleshooting

### Error: Module not found '@experts/sdk'

**Check 1:** SDK source exists

```bash
ls packages/sdk/src/index.ts
```

**Fix:** Generate SDK

```bash
cd docker/{env}
docker compose run --rm experts-docs
docker compose run --rm experts-sdk
```

**Check 2:** Workspace link is correct

```bash
pnpm list @experts/sdk
```

**Fix:** Reinstall dependencies

```bash
pnpm install
```

### Error: ENOENT tarball not found

This means you still have old tarball references in `pnpm-lock.yaml`.

**Fix:**

```bash
# Remove any old tarballs
sudo rm -f packages/sdk/dist/experts-sdk-*.tgz

# Remove tarball reference from root package.json if exists
# (should not have any dependencies section)

# Regenerate lock file
pnpm install --lockfile-only

# Verify clean
grep '@experts/sdk' pnpm-lock.yaml
# Should only show: specifier: workspace:*
```

### Docker Build Fails: SDK Source Missing

**Check:** SDK was generated for correct environment

```bash
# Verify OpenAPI spec exists
ls apps/experts-api/public/docs/canary/openapi.yaml

# Verify SDK source exists
ls packages/sdk/src/index.ts
```

**Fix:** Regenerate for environment

```bash
cd docker/canary
docker compose run --rm experts-docs  # Generate OpenAPI spec
docker compose run --rm experts-sdk   # Generate SDK source
```

## Benefits

✅ **Simpler Workflow**

- No tarball installation step
- Workspace links just work

✅ **Clean Lock File**

- No file path references
- Works in all environments

✅ **Docker-Compatible**

- SDK source in build context
- No external file dependencies

✅ **Development-Friendly**

- Edit SDK config without rebuilding
- Hot reload works

✅ **CI/CD Ready**

- Consistent across all environments
- No permission issues

## Migration from Old Approach

If you're migrating from the old tarball-based approach:

```bash
# 1. Remove old tarballs
sudo rm -rf packages/sdk/dist/experts-sdk-*.tgz

# 2. Clean root package.json (remove dependencies section if exists)

# 3. Regenerate lock file
pnpm install --lockfile-only

# 4. Generate SDK source for your environments
cd docker/canary && docker compose run --rm experts-sdk
cd docker/staging && docker compose run --rm experts-sdk
cd docker/production && docker compose run --rm experts-sdk

# 5. Verify workspace links
pnpm list @experts/sdk
# Should show: @experts/sdk link:packages/sdk

# 6. Test build
./apps/experts-app/docker/build-local.sh canary loogix/experts-app:canary
```

## Related Documentation

- [Environment-Based URLs](../SESSION/ENVIRONMENT_BASED_URLS.md)
- [Version Management](../DOCKER/VERSION_MANAGEMENT.md)
- [SDK Configuration](https://github.com/logi-x/experts/blob/main/packages/sdk/README.md)
