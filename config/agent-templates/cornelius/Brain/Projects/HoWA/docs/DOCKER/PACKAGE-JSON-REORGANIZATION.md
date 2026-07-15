---
title: "Package.json Reorganization & Production Build Fix"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Package.json Reorganization & Production Build Fix

## Problem

Production builds were failing with:

```
Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'laravel-vite-plugin'
```

**Root Cause**: The production Dockerfile was installing dependencies with `--prod` flag (which skips devDependencies), but then trying to build assets which requires build tools like `vite`, `laravel-vite-plugin`, `@vitejs/plugin-react`, etc.

## Solution

### 1. Package.json Reorganization

Reorganized all package.json files to follow standard conventions:

#### Root `package.json`

- **Dependencies**: Runtime packages shared by multiple apps (React, axios, lodash, etc.)
  - **Removed**: `canvas` (only needed by server), `buffer` (only needed by admin)
- **DevDependencies**: Build tools, test tools, type definitions, linters
  - Moved: `vite`, `laravel-vite-plugin`, `@vitejs/plugin-react`, `tailwindcss`, `puppeteer`, `@uiw/react-md-editor`, `concurrently`, etc.

#### `apps/admin/package.json`

- **Dependencies**: Runtime packages used by admin app
- **DevDependencies**: Build tools specific to admin
  - Added: `laravel-vite-plugin`, `vite`, `@vitejs/plugin-react`, `tailwindcss`

#### `apps/client/package.json`

- **Dependencies**: Runtime packages used by client app
- **DevDependencies**: Build tools specific to client
  - Added: `laravel-vite-plugin`, `vite`, `@vitejs/plugin-react`, `tailwindcss`

#### `apps/server/package.json`

- **Dependencies**: Runtime packages for Node.js server
- **DevDependencies**: Development and testing tools
  - Moved: `jest`, `nodemon`

### 2. Production Dockerfile Fix

Updated `docker/php/Dockerfile.prod` build process:

```dockerfile
# OLD (broken):
RUN pnpm install --filter @howa/${APP_PATH}... --prod  # Skips devDependencies
RUN pnpm build:admin  # FAILS - no vite, no laravel-vite-plugin!

# NEW (fixed):
# 1. Install ALL dependencies (including devDependencies for build)
RUN pnpm install --filter @howa/${APP_PATH}... --frozen-lockfile

# 2. Build frontend assets (requires devDependencies)
RUN if [ "$APP_PATH" = "admin" ]; then \
        pnpm build:admin; \
    elif [ "$APP_PATH" = "client" ]; then \
        pnpm build:client; \
    fi

# 3. Remove devDependencies after build to save space
RUN pnpm install --filter @howa/${APP_PATH}... --prod --frozen-lockfile
```

### 3. Enhanced Cleanup

Added more aggressive cleanup to reduce image size:

```dockerfile
RUN rm -rf /app/node_modules \
    # Remove test files
    && rm -rf /app/apps/${APP_PATH}/tests \
    && rm -rf /app/apps/${APP_PATH}/phpunit.xml* \
    # Remove development files
    && rm -rf /app/apps/${APP_PATH}/_ide_helper*.php \
    && rm -rf /app/apps/${APP_PATH}/.phpunit* \
    && rm -rf /app/apps/${APP_PATH}/boost.json \
    # Remove build source files (keep only /public/build)
    && rm -rf /app/apps/${APP_PATH}/resources/js \
    && rm -rf /app/apps/${APP_PATH}/resources/css \
    # Remove npm/composer caches
    && rm -rf /root/.composer/cache \
    && rm -rf /root/.npm \
    && rm -rf /root/.cache \
    && rm -rf /tmp/* \
    && rm -rf /root/.local \
    # Remove .npmrc (contains GitHub token!)
    && rm -f /app/.npmrc \
    # Remove package manager files
    && rm -rf /app/package.json \
    && rm -rf /app/pnpm-lock.yaml \
    && rm -rf /app/pnpm-workspace.yaml \
    # Remove pnpm store
    && rm -rf /root/.local/share/pnpm \
    # Remove unneeded binaries after build
    && rm -rf /usr/local/bin/pnpm \
    && npm uninstall -g pnpm || true
```

## Benefits

1. **Fixes Production Build**: Assets build successfully with all required dependencies
2. **Smaller Image Size**: DevDependencies and build artifacts removed after build
3. **Standard Structure**: Follows npm/pnpm conventions for dependencies vs devDependencies
4. **Security**: Removes .npmrc containing GitHub token
5. **Clarity**: Clear separation between runtime and build-time dependencies

## Testing

```bash
# Rebuild production images
cd docker/production
docker-compose build --no-cache howa-core
docker-compose build --no-cache howa-app

# Verify build completes without errors
# Verify image size is reasonable
docker images | grep howa-
```

## Canvas Package Issue

**Problem**: `canvas` package requires native dependencies (`pixman-1`, `cairo`, `pango`) that aren't available in the PHP Alpine image.

**Solution**: Moved `canvas` from root `package.json` to `apps/server/package.json` only, since:

- Only the Node.js server uses `canvas` (for QR code generation)
- The PHP images (admin/client) don't need it
- This avoids installing unnecessary native build dependencies in PHP containers

Similarly, `buffer` was moved to `apps/admin/package.json` only.

## Laravel Boost in Production Fix

**Problem**: `Class "Laravel\Boost\BoostServiceProvider" not found` error in production.

**Root Cause**:

- `laravel/boost` is in `require-dev` (not installed with `--no-dev`)
- Laravel was auto-discovering and trying to load it from cached `bootstrap/cache/packages.php`

**Solution**:

1. **Prevent auto-discovery** in `composer.json`:

```json
"extra": {
    "laravel": {
        "dont-discover": ["laravel/boost"]
    }
}
```

2. **Manual registration** in `app/Providers/AppServiceProvider.php`:

```php
public function register(): void
{
    // Register Laravel Boost only in development
    if ($this->app->environment('local', 'development', 'testing')) {
        if (class_exists(\Laravel\Boost\BoostServiceProvider::class)) {
            $this->app->register(\Laravel\Boost\BoostServiceProvider::class);
        }
    }
}
```

3. **Multi-stage Dockerfile** clears cached files and regenerates them in production:

```dockerfile
# Builder stage: Clear bootstrap/cache/*
RUN rm -rf /app/apps/${APP_PATH}/bootstrap/cache/*

# Production stage: Regenerate without Boost
RUN composer dump-autoload --optimize --classmap-authoritative \
    && php artisan package:discover --ansi \
    && php artisan config:cache \
    && php artisan route:cache
```

## Multi-Stage Dockerfile Structure

```
Stage 1: base         → System deps, PHP extensions, Composer, pnpm
Stage 2: dependencies → Install packages (Composer --no-dev, pnpm all)
Stage 3: builder      → Build assets, clear caches
Stage 4: production   → Copy built app, regenerate caches (without Boost)
```

## Notes

- Multi-stage build separates build-time from runtime dependencies
- Canvas builds successfully with native dependencies installed
- Build tools (g++, make, python3) removed in final image
- Final image contains only production dependencies + compiled assets
- Workspace-specific packages (`canvas`, `puppeteer`) moved to their respective workspaces
- Laravel Boost works in development, excluded from production
