---
title: "Unified Dockerfile Usage Guide"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Unified Dockerfile Usage Guide

The project now uses unified Dockerfiles with multiple build targets for both development and production environments.

## Overview

### PHP Applications (admin/client)

**File:** `docker/php/Dockerfile`

- **Target: `production`** - Multi-stage optimized build (598MB)
- **Target: `development`** - Single-stage with dev tools

### Node.js Server

**File:** `docker/node/Dockerfile`

- **Target: `production`** - Multi-stage optimized build (487MB unique)
- **Target: `development`** - Single-stage with dev tools + Chrome

## Usage in docker-compose.yml

### Method 1: Using `build.target`

```yaml
services:
  # Production build
  howa-prod-app:
    build:
      context: ../..
      dockerfile: docker/php/Dockerfile
      target: production # ← Specifies which stage to build
      args:
        APP_PATH: client
    image: loogix/howa-app:prod
    # ... rest of config

  # Development build
  howa-dev-app:
    build:
      context: ../..
      dockerfile: docker/php/Dockerfile
      target: development # ← Specifies dev stage
      args:
        APP_PATH: client
    image: loogix/howa-app:dev
    # ... rest of config
```

### Method 2: Using Environment Variable

**In docker-compose.yml:**

```yaml
services:
  howa-app:
    build:
      context: ../..
      dockerfile: docker/php/Dockerfile
      target: ${BUILD_TARGET:-production} # ← Use env var
      args:
        APP_PATH: client
```

**Usage:**

```bash
# Build production (default)
docker compose build

# Build development
BUILD_TARGET=development docker compose build

# Or export it
export BUILD_TARGET=development
docker compose build
```

### Method 3: Separate Compose Files

**docker-compose.prod.yml:**

```yaml
services:
  howa-app:
    build:
      target: production
      args:
        APP_PATH: client
```

**docker-compose.dev.yml:**

```yaml
services:
  howa-app:
    build:
      target: development
      args:
        APP_PATH: client
```

**Usage:**

```bash
# Production
docker compose -f docker-compose.prod.yml up

# Development
docker compose -f docker-compose.dev.yml up
```

## Complete Example

### Production (docker/production/docker-compose.yml)

```yaml
services:
  # MySQL
  howa-prod-mysql:
    image: mysql:latest
    container_name: howa-prod-mysql
    # ... config

  # Redis
  howa-prod-redis:
    image: redis:latest
    container_name: howa-prod-redis
    # ... config

  # Admin App (Laravel)
  howa-prod-core:
    build:
      context: ../..
      dockerfile: docker/php/Dockerfile
      target: production
      args:
        APP_PATH: admin
    image: loogix/howa-core:prod
    container_name: howa-prod-core
    environment:
      - APP_PATH=admin
      - DB_HOST=howa-prod-mysql
      - REDIS_HOST=howa-prod-redis
    depends_on:
      howa-prod-mysql:
        condition: service_healthy
      howa-prod-redis:
        condition: service_healthy
    networks:
      - howa-shared-network
    volumes:
      - ../../apps/shared/s:/app/apps/shared/s

  # Client App (Laravel)
  howa-prod-app:
    build:
      context: ../..
      dockerfile: docker/php/Dockerfile
      target: production
      args:
        APP_PATH: client
    image: loogix/howa-app:prod
    container_name: howa-prod-app
    environment:
      - APP_PATH=client
      - DB_HOST=howa-prod-mysql
      - REDIS_HOST=howa-prod-redis
    depends_on:
      howa-prod-mysql:
        condition: service_healthy
      howa-prod-redis:
        condition: service_healthy
    networks:
      - howa-shared-network
    volumes:
      - ../../apps/shared/s:/app/apps/shared/s

  # Server (Node.js)
  howa-prod-server:
    build:
      context: ../..
      dockerfile: docker/node/Dockerfile
      target: production
    image: loogix/howa-server:prod
    container_name: howa-prod-server
    environment:
      - NODE_ENV=production
      - PORT=3050
    depends_on:
      howa-prod-mysql:
        condition: service_healthy
      howa-prod-redis:
        condition: service_healthy
    networks:
      - howa-shared-network
    volumes:
      - zatca-sdk:/opt/zatca-sdk

networks:
  howa-shared-network:
    name: howa-shared-network
    driver: bridge

volumes:
  howa-db:
  howa-cache:
  zatca-sdk:
```

### Development (docker/development/docker-compose.yml)

```yaml
services:
  # MySQL
  howa-dev-mysql:
    image: mysql:latest
    container_name: howa-dev-mysql
    # ... config

  # Redis
  howa-dev-redis:
    image: redis:latest
    container_name: howa-dev-redis
    # ... config

  # Admin App (Laravel)
  howa-dev-core:
    build:
      context: ../..
      dockerfile: docker/php/Dockerfile
      target: development # ← Dev target
      args:
        APP_PATH: admin
    image: loogix/howa-core:dev
    container_name: howa-dev-core
    environment:
      - APP_PATH=admin
      - DB_HOST=howa-dev-mysql
      - REDIS_HOST=howa-dev-redis
    depends_on:
      howa-dev-mysql:
        condition: service_healthy
      howa-dev-redis:
        condition: service_healthy
    networks:
      - howa-shared-network
    volumes:
      # Bind mount for hot reload
      - ../../apps/admin:/app/apps/admin
      - ../../apps/shared:/app/apps/shared

  # Client App (Laravel)
  howa-dev-app:
    build:
      context: ../..
      dockerfile: docker/php/Dockerfile
      target: development # ← Dev target
      args:
        APP_PATH: client
    image: loogix/howa-app:dev
    container_name: howa-dev-app
    environment:
      - APP_PATH=client
      - DB_HOST=howa-dev-mysql
      - REDIS_HOST=howa-dev-redis
    depends_on:
      howa-dev-mysql:
        condition: service_healthy
      howa-dev-redis:
        condition: service_healthy
    networks:
      - howa-shared-network
    volumes:
      # Bind mount for hot reload
      - ../../apps/client:/app/apps/client
      - ../../apps/shared:/app/apps/shared

  # Server (Node.js)
  howa-dev-server:
    build:
      context: ../..
      dockerfile: docker/node/Dockerfile
      target: development # ← Dev target
    image: loogix/howa-server:dev
    container_name: howa-dev-server
    environment:
      - NODE_ENV=development
      - PORT=3052
    depends_on:
      howa-dev-mysql:
        condition: service_healthy
      howa-dev-redis:
        condition: service_healthy
    networks:
      - howa-shared-network
    volumes:
      # Bind mount for hot reload with nodemon
      - ../../apps/server:/app/apps/server
      - ../../apps/shared:/app/apps/shared
      - zatca-sdk:/opt/zatca-sdk

networks:
  howa-shared-network:
    name: howa-shared-network
    driver: bridge

volumes:
  howa-db:
  howa-cache:
  zatca-sdk:
```

## Benefits of Unified Dockerfiles

### ✅ Single Source of Truth

- One Dockerfile per application type
- Easier to maintain and update
- Consistent base configuration

### ✅ Production Intact

- Production stages unchanged
- Same optimizations (multi-stage, layer caching)
- Same image sizes (598MB PHP, 487MB Node)

### ✅ Development Optimized

- Chrome included for Puppeteer (dev + prod)
- Build tools available for native modules
- Faster iteration with volume mounts

### ✅ Flexible Deployment

- Choose target via `build.target`
- Or use environment variables
- Or separate compose files

### ✅ Clear Stage Structure

**PHP Dockerfile:**

1. `base` - Common runtime (PHP 8.4 + extensions)
2. `dependencies` - Install packages (prod multi-stage)
3. `builder` - Build assets (prod multi-stage)
4. `production` - Final optimized image
5. `development` - Dev-friendly single-stage

**Node Dockerfile:**

1. `base` - Common runtime (Node 22 + Chrome + Java)
2. `dependencies` - Install with build tools (prod)
3. `builder` - Copy code (prod)
4. `production` - Final optimized image
5. `development` - Dev-friendly with build tools

## Migration from Separate Dockerfiles

### Before

```
docker/php/Dockerfile.dev
docker/php/Dockerfile.prod
docker/node/Dockerfile.dev
docker/node/Dockerfile.prod
```

### After

```
docker/php/Dockerfile  (with targets: production, development)
docker/node/Dockerfile (with targets: production, development)
```

### Update docker-compose.yml

**Before:**

```yaml
build:
  dockerfile: docker/php/Dockerfile.prod
```

**After:**

```yaml
build:
  dockerfile: docker/php/Dockerfile
  target: production
```

## Testing the Setup

```bash
# Build production images
cd docker/production
docker compose build

# Build development images
cd docker/development
docker compose build

# Or build specific target
docker compose build --build-arg BUILD_TARGET=development

# Run production
cd docker/production
docker compose up -d

# Run development
cd docker/development
docker compose up -d
```

## Image Sizes

### Production (Multi-stage)

```
loogix/howa-core:prod    598MB (124MB unique)
loogix/howa-app:prod     591MB (120MB unique)
loogix/howa-server:prod  1.93GB (487MB unique)
```

### Development (Single-stage)

```
loogix/howa-core:dev     ~900MB  (includes dev tools)
loogix/howa-app:dev      ~900MB  (includes dev tools)
loogix/howa-server:dev   ~2.2GB  (includes build tools + Chrome)
```

Development images are larger but include all necessary tools for hot reload and rebuilding.

---

**Note:** The unified Dockerfiles maintain backward compatibility. Existing production deployments continue to work without changes.
