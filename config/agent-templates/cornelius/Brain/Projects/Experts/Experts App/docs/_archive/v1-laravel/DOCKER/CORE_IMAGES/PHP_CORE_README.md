---
title: "PHP Core Image Build System"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/docker"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# PHP Core Image Build System

## Overview

This directory contains the build system for creating a reusable PHP core Docker image that eliminates the 68.9-second build time for PHP extensions in the experts-api Dockerfile.

## Architecture

### Before Optimization

```
experts-api Dockerfile:
├── FROM php:8.4-fpm-alpine3.22
├── Install build dependencies (68.9s)
│   ├── apk add build-deps
│   ├── pecl install redis pcov
│   └── docker-php-ext-install gd pdo mysql...
├── Install Composer
├── Copy Laravel app
└── Build Laravel app
```

**Total Build Time**: ~120 seconds (68.9s for PHP + 51s for app)

### After Optimization

```
php-core:8.4 (built once):
├── FROM php:8.4-fpm-alpine3.22
├── Install build dependencies (68.9s ONE TIME)
│   ├── apk add build-deps
│   ├── pecl install redis pcov
│   └── docker-php-ext-install gd pdo mysql...
└── Install pnpm

experts-api Dockerfile:
├── FROM php-core:8.4 (~0s when cached)
├── Install Composer
├── Copy Laravel app
└── Build Laravel app
```

**Total Build Time**: ~51 seconds (0s for PHP + 51s for app)
**Savings**: 68.9 seconds per build = ~57% faster

## Files

### 1. `Dockerfile.php-core`

Creates the reusable PHP core image with all extensions and tools.

**Contents**:

- PHP 8.4-FPM
- Extensions: redis, pcov, gd, pdo, pdo_mysql, pdo_sqlite, pcntl, sockets, zip
- Tools: supervisor, nginx, bash, node, npm, pnpm, curl, nano, jq, wget, zip, su-exec, dumb-init
- Timezone: Asia/Riyadh

### 2. `build-php-core.sh`

Convenience script to build the php-core:8.4 image.

### 3. `php-core.sh` (Legacy)

Volume-based approach (deprecated in favor of image-based approach).

## Usage

### First-Time Setup

1. **Build the PHP core image** (one time only):

   ```bash
   cd docker/canary
   ./build-php-core.sh
   ```

   Or manually:

   ```bash
   docker build -t php-core:8.4 -f docker/canary/Dockerfile.php-core docker/canary
   ```

2. **Build experts-api** (uses php-core:8.4 as base):

   ```bash
   docker-compose -f docker/canary/docker-compose.yml build experts-api
   ```

### Subsequent Builds

Once php-core:8.4 is built, all subsequent experts-api builds will use the cached image:

```bash
docker-compose -f docker/canary/docker-compose.yml build experts-api
# Fast! Only builds Laravel app (~51s)
```

### Fallback Mode

If php-core:8.4 image is not available, the Dockerfile will fail with a clear error. To build without the optimized image:

```bash
docker build \
  --build-arg USE_PHP_CORE=false \
  -f apps/experts-api/Dockerfile \
  .
```

This will use the slow build path (68.9s for PHP extensions).

## When to Rebuild php-core:8.4

Rebuild the PHP core image when:

- ✅ Upgrading PHP version (e.g., 8.4 → 8.5)
- ✅ Adding/removing PHP extensions
- ✅ Updating extension versions
- ✅ Changing system packages
- ✅ Updating pnpm version

You do NOT need to rebuild when:

- ❌ Updating Laravel application code
- ❌ Changing Composer dependencies
- ❌ Updating environment variables
- ❌ Modifying nginx/supervisor configs

## Build Time Comparison

| Build Type        | Before | After | Savings            |
| ----------------- | ------ | ----- | ------------------ |
| First build       | 120s   | 120s  | 0% (one-time cost) |
| Subsequent builds | 120s   | 51s   | 57% faster         |
| CI/CD builds      | 120s   | 51s   | 57% faster         |
| Developer builds  | 120s   | 51s   | 57% faster         |

## Multi-Stage Architecture

The experts-api Dockerfile now uses a multi-stage approach:

```dockerfile
# Stage 1a: Fast path (default)
FROM php-core:8.4 AS base-fast

# Stage 1b: Slow path (fallback)
FROM php:8.4-fpm-alpine3.22 AS base-slow
RUN [68.9s of PHP extension building]

# Stage 1c: Selector
FROM base-fast AS base

# Stage 2: Dependencies
FROM base AS dependencies
RUN composer install

# Stage 3: Builder
FROM base AS builder
COPY app && RUN composer dump-autoload

# Stage 4: Production Minimal
FROM alpine:3.22 AS production-minimal

# Stage 5: Production Standalone
FROM base AS production

# Stage 6: Development
FROM base AS development
```

## Image Sizes

```
php:8.4-fpm-alpine3.22    ~87MB   (base Alpine + PHP)
php-core:8.4              ~185MB  (+ extensions + tools)
experts-api:production    ~210MB  (+ Laravel app)
```

## Troubleshooting

### Error: "failed to solve with frontend dockerfile.v0"

**Cause**: php-core:8.4 image not built yet
**Fix**: Run `./build-php-core.sh` first

### Error: "pull access denied for php-core"

**Cause**: Docker trying to pull from registry instead of using local image
**Fix**: Ensure php-core:8.4 is built locally with `docker images | grep php-core`

### Slow builds despite using php-core

**Cause**: Docker BuildKit cache not being used
**Fix**: Enable BuildKit with `export DOCKER_BUILDKIT=1`

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Build PHP Core Image
  run: |
    cd docker/canary
    docker build -t php-core:8.4 -f Dockerfile.php-core .

- name: Cache PHP Core Image
  uses: actions/cache@v3
  with:
    path: /tmp/php-core.tar
    key: php-core-8.4-${{ hashFiles('docker/canary/Dockerfile.php-core') }}

- name: Build experts-api
  run: docker-compose -f docker/canary/docker-compose.yml build experts-api
```

## Migration Path

If you have existing builds using volume mounts:

1. Remove volume mounts from docker-compose.yml:

   ```yaml
   # Remove these lines:
   # - ./volumes/php-core/usr/local:/usr/local:ro
   # - ./volumes/php-core/usr/bin:/usr/bin:ro
   # etc.
   ```

2. Build php-core image:

   ```bash
   ./build-php-core.sh
   ```

3. Rebuild experts-api:

   ```bash
   docker-compose build experts-api
   ```

## Version History

- **v1.0** (2025-11-15): Initial image-based approach
  - Replaced volume mounts with Docker image
  - Reduced build time from 120s → 51s
  - Improved caching and portability
