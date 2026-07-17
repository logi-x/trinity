---
title: "Production Build Complete ✅"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Production Build Complete ✅

## All Production Images Built Successfully

```
loogix/howa-core:prod    (admin)  - 2.58GB
loogix/howa-app:prod     (client) - 2.59GB
loogix/howa-server:prod  (server) - 5.48GB
```

---

## 🎯 All Issues Resolved

### 1. ✅ Canvas Build Error Fixed

**Problem**: `Package 'pixman-1' not found` during canvas npm install

**Solution**:

- Added native dependencies to Dockerfile: `pixman-dev`, `cairo-dev`, `pango-dev`, `giflib-dev`, `pkgconfig`, `g++`, `make`, `python3`
- Moved `canvas` & `puppeteer` from root to `apps/server/package.json` only
- Server builds successfully in ~45 seconds

---

### 2. ✅ Laravel Boost Production Error Fixed

**Problem**: `Class "Laravel\Boost\BoostServiceProvider" not found` in production

**Solution**:

**a) Prevent Auto-Discovery** (`composer.json`):

```json
"extra": {
    "laravel": {
        "dont-discover": ["laravel/boost"]
    }
}
```

**b) Conditional Registration** (`AppServiceProvider.php`):

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

**c) Multi-Stage Dockerfile**:

```dockerfile
# Builder stage: Clear cached files
RUN rm -rf bootstrap/cache/*

# Production stage: Regenerate without Boost
RUN composer dump-autoload --optimize --classmap-authoritative \
    && php artisan package:discover --ansi
```

**Verified**: ✅ Boost NOT in `bootstrap/cache/packages.php`

---

### 3. ✅ Puppeteer Permission Error Fixed

**Problem**: `EACCES: permission denied, stat '/root/.config/puppeteer'`

**Solution**:

```dockerfile
# Set cache directory BEFORE install
ENV PUPPETEER_CACHE_DIR=/app/.cache/puppeteer

# After install, set ownership
RUN chown -R node:node /app/.cache \
    && chown -R node:node /app/apps/server
```

**Result**: Puppeteer cache owned by `node` user ✅

---

### 4. ✅ Supervisor Configuration

**Problem**: `could not find config file /etc/supervisor/supervisord.conf`

**Solution**:

```dockerfile
RUN mkdir -p /var/log/supervisor /etc/supervisor/conf.d \
    && chown -R node:node /var/log/supervisor
COPY docker/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY docker/supervisor/server.conf /etc/supervisor/conf.d/server.conf
```

---

### 5. ✅ Package.json Reorganization

Properly separated `dependencies` vs `devDependencies`:

**Root `package.json`**:

- Dependencies: Runtime packages (React, axios, etc.)
- DevDependencies: Build tools (vite, laravel-vite-plugin, tailwindcss, etc.)
- **Removed**: `canvas`, `puppeteer` (server-only)

**`apps/admin/package.json` & `apps/client/package.json`**:

- Dependencies: Runtime UI components
- DevDependencies: `vite`, `laravel-vite-plugin`, `@vitejs/plugin-react`, `tailwindcss`

**`apps/server/package.json`**:

- Dependencies: `canvas`, `puppeteer`, `express`, etc.
- DevDependencies: `jest`, `nodemon`

---

## 📦 Multi-Stage Dockerfile Structure

### PHP Apps (`docker/php/Dockerfile.prod`)

```
┌─────────────────────────────────────────┐
│ Stage 1: base                          │
│ - System dependencies                  │
│ - PHP extensions (gd, redis, etc.)    │
│ - Composer 2.8.12                      │
│ - pnpm 10.20.0                         │
│ - Canvas native deps (for monorepo)   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ Stage 2: dependencies                   │
│ - Copy package manifests                │
│ - composer install --no-dev             │
│ - pnpm install (all deps for build)    │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ Stage 3: builder                        │
│ - Copy source code                      │
│ - php artisan package:discover          │
│ - vite build && vite build --ssr       │
│ - pnpm install --prod (remove devDeps) │
│ - Clear bootstrap/cache/*               │
│ - Remove resources/js & resources/css   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ Stage 4: production (FINAL)            │
│ - Copy built app from builder           │
│ - composer dump-autoload                │
│ - php artisan package:discover (no Boost)│
│ - php artisan config:cache              │
│ - php artisan route:cache               │
│ - Remove build tools (g++, make, etc.) │
│ - Keep only runtime libs                │
└─────────────────────────────────────────┘
```

### Node.js Server (`docker/node/Dockerfile.prod`)

```
┌─────────────────────────────────────────┐
│ Single Stage (Optimized)               │
│ - OpenJDK 17 + jq (for ZATCA SDK)      │
│ - Canvas native dependencies            │
│ - PUPPETEER_CACHE_DIR=/app/.cache │
│ - pnpm install --prod                   │
│ - chown node:node (cache + app)        │
│ - Supervisor configuration              │
└─────────────────────────────────────────┘
```

---

## 🚀 Build & Deploy

### Build All Images

```bash
cd docker/production
docker compose build --no-cache
```

### Start Production Stack

```bash
docker compose up -d
```

### Verify Services

```bash
# Check all services are running
docker compose ps

# Check logs
docker compose logs -f howa-prod-core
docker compose logs -f howa-prod-app
docker compose logs -f howa-prod-server

# Test endpoints
curl -k https://core.howa.edu.sa/health
curl -k https://app.howa.edu.sa/health
curl http://localhost:3050/health
```

---

## 📊 Image Optimizations

### Size Reduction Techniques

1. **Multi-stage builds** - Build artifacts not in final image
2. **DevDependencies removed** after Vite build
3. **Source files removed** (resources/js, resources/css)
4. **Build tools removed** (g++, make, python3, pkgconfig)
5. **Caches cleared** (composer, npm, pnpm stores)
6. **Test files removed** (tests/, phpunit.xml, boost.json)

### Final Image Contents

- **PHP apps**: Production code + compiled assets + runtime deps only
- **Node.js server**: Production code + canvas + puppeteer runtime
- **NO**: devDependencies, source files, build tools, test files

---

## 🔧 Key Configuration Changes

### 1. Composer.json (both apps)

```json
"extra": {
    "laravel": {
        "dont-discover": ["laravel/boost"]
    }
}
```

### 2. AppServiceProvider.php (both apps)

```php
public function register(): void
{
    if ($this->app->environment('local', 'development', 'testing')) {
        if (class_exists(\Laravel\Boost\BoostServiceProvider::class)) {
            $this->app->register(\Laravel\Boost\BoostServiceProvider::class);
        }
    }
}
```

### 3. Node.js Dockerfile

```dockerfile
ENV PUPPETEER_CACHE_DIR=/app/.cache/puppeteer
RUN chown -R node:node /app/.cache
```

---

## ✅ Verification Tests Passed

- ✅ Canvas builds without errors (45s build time)
- ✅ Vite builds assets successfully (18.6s + 3.7s)
- ✅ Laravel Boost excluded from production
- ✅ `php artisan list` works without errors
- ✅ `bootstrap/cache/packages.php` does NOT contain Boost
- ✅ Puppeteer cache accessible by `node` user
- ✅ Supervisor configs loaded successfully
- ✅ All 3 production images built

---

## 📝 Files Modified

### Package Management

- ✅ `package.json` (root) - Reorganized deps/devDeps
- ✅ `apps/admin/package.json` - Added devDeps (vite, etc.)
- ✅ `apps/client/package.json` - Added devDeps (vite, etc.)
- ✅ `apps/server/package.json` - Added canvas, puppeteer

### Laravel Configuration

- ✅ `apps/admin/composer.json` - Added dont-discover
- ✅ `apps/client/composer.json` - Added dont-discover
- ✅ `apps/admin/app/Providers/AppServiceProvider.php` - Conditional Boost
- ✅ `apps/client/app/Providers/AppServiceProvider.php` - Conditional Boost

### Docker Files

- ✅ `docker/php/Dockerfile.prod` - Multi-stage build
- ✅ `docker/node/Dockerfile.prod` - Puppeteer cache fix
- ✅ `docker/supervisor/server.conf` - Removed duplicate [supervisord]

### Documentation

- ✅ `docs/DOCKER/PACKAGE-JSON-REORGANIZATION.md`
- ✅ `docs/DOCKER/PRODUCTION-BUILD-COMPLETE.md` (this file)

---

## 🎯 Production Ready

All services are ready for deployment with optimized, secure, production-grade Docker images.

**Total Build Time**: ~3-5 minutes per image  
**Canvas Build**: ~45 seconds  
**Vite Build**: ~22 seconds

**Next Steps**: Deploy to production server! 🚀
