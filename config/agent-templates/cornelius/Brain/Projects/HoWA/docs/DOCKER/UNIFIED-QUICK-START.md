---
title: "Unified Dockerfile Quick Start"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Unified Dockerfile Quick Start

## 🎯 TL;DR

Both PHP and Node.js apps now use **unified Dockerfiles** with build targets:

```yaml
# Production
build:
  dockerfile: docker/php/Dockerfile
  target: production

# Development
build:
  dockerfile: docker/php/Dockerfile
  target: development
```

## 📁 File Structure

```
docker/
├── php/
│   └── Dockerfile              # Unified (5 stages)
├── node/
│   └── Dockerfile              # Unified (5 stages)
├── nginx/
│   ├── dev.conf
│   └── prod.conf
├── scripts/
│   └── entrypoint-php.sh       # Handles dev/prod differences
├── production/
│   └── docker-compose.yml      # Uses target: production
└── development/
    └── docker-compose.yml      # Uses target: development
```

## 🚀 Quick Commands

### Production

```bash
# Build
cd docker/production
docker compose build

# Run
docker compose up -d

# Check
docker compose ps
docker images | grep loogix
```

### Development

```bash
# Build
cd docker/development
docker compose build

# Run
docker compose up -d

# Check
docker compose ps
docker logs howa-dev-app
```

## 🎨 Build Targets

### PHP Dockerfile (`docker/php/Dockerfile`)

| Stage             | Purpose             | Size          | Use Case                  |
| ----------------- | ------------------- | ------------- | ------------------------- |
| `base`            | Common runtime      | ~200MB        | Foundation for both       |
| `dependencies`    | Install packages    | -             | Production multi-stage    |
| `builder`         | Build assets        | -             | Production multi-stage    |
| **`production`**  | **Final optimized** | **591-598MB** | **Production deployment** |
| **`development`** | **Dev-friendly**    | **~900MB**    | **Local development**     |

### Node Dockerfile (`docker/node/Dockerfile`)

| Stage             | Purpose                  | Size       | Use Case                  |
| ----------------- | ------------------------ | ---------- | ------------------------- |
| `base`            | Common runtime + Chrome  | ~500MB     | Foundation for both       |
| `dependencies`    | Install + build tools    | -          | Production multi-stage    |
| `builder`         | Copy code                | -          | Production multi-stage    |
| **`production`**  | **Final optimized**      | **1.93GB** | **Production deployment** |
| **`development`** | **Dev-friendly + tools** | **~2.2GB** | **Local development**     |

## 📝 Example docker-compose.yml

### Production Build

```yaml
services:
  howa-prod-app:
    build:
      context: ../..
      dockerfile: docker/php/Dockerfile
      target: production # ← Production target
      args:
        APP_PATH: client
    image: loogix/howa-app:prod
    container_name: howa-prod-app
    environment:
      - APP_PATH=client
      - DB_HOST=howa-prod-mysql
    networks:
      - howa-shared-network
    volumes:
      - ../../apps/shared/s:/app/apps/shared/s
```

### Development Build

```yaml
services:
  howa-dev-app:
    build:
      context: ../..
      dockerfile: docker/php/Dockerfile
      target: development # ← Development target
      args:
        APP_PATH: client
    image: loogix/howa-app:dev
    container_name: howa-dev-app
    environment:
      - APP_PATH=client
      - DB_HOST=howa-dev-mysql
    networks:
      - howa-shared-network
    volumes:
      # Bind mount for hot reload
      - ../../apps/client:/app/apps/client
      - ../../apps/shared:/app/apps/shared
```

## 🔑 Key Differences

### Production Target

✅ Multi-stage build (smaller images)  
✅ Only runtime dependencies  
✅ Optimized caching (config, routes, views)  
✅ No dev tools (pnpm removed)  
✅ Build tools removed (python, g++, etc.)  
✅ Supervisor for process management

### Development Target

✅ Single-stage build (simpler, faster rebuilds)  
✅ Includes dev dependencies  
✅ Build tools included (for canvas, puppeteer)  
✅ Chrome included (for PDF generation)  
✅ OPcache with timestamp validation  
✅ No supervisor (PHP-FPM + nginx directly)  
✅ Volume mounts for hot reload

## 🔄 Switching Between Environments

### Method 1: Navigate to directory

```bash
# Production
cd docker/production
docker compose up -d

# Development
cd docker/development
docker compose up -d
```

### Method 2: Use environment variable

```bash
# Production (default)
docker compose build

# Development
BUILD_TARGET=development docker compose build
```

### Method 3: Override compose file

```bash
# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up

# Development
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## ⚙️ Entrypoint Behavior

The `entrypoint-php.sh` script automatically detects the environment:

### Production (has supervisord)

```bash
✅ Update .env with runtime env vars
✅ Generate ALL caches (config + routes + views)
✅ Create storage symlinks
✅ Fix permissions
✅ Start supervisor
```

### Development (no supervisord)

```bash
✅ Update .env with runtime env vars
✅ Generate config cache ONLY (routes/views change frequently)
✅ Create storage symlinks
✅ Fix permissions
✅ Start PHP-FPM + nginx directly
```

## 🎯 Image Size Comparison

### Production (Optimized)

```
REPOSITORY          TAG    SIZE      UNIQUE
loogix/howa-core    prod   598MB     124MB
loogix/howa-app     prod   591MB     120MB
loogix/howa-server  prod   1.93GB    487MB
───────────────────────────────────────────
Total Unique Size:                  731MB
```

### Development (Full-featured)

```
REPOSITORY          TAG    SIZE      INCLUDES
loogix/howa-core    dev    ~900MB    + dev deps
loogix/howa-app     dev    ~900MB    + dev deps
loogix/howa-server  dev    ~2.2GB    + build tools + Chrome
```

## 📦 What's Included

### Both Environments

- ✅ PHP 8.4-FPM with all extensions
- ✅ Node.js 22.14.0
- ✅ pnpm 10.20.0
- ✅ Composer 2.8.12
- ✅ MySQL client
- ✅ Redis extension
- ✅ Nginx
- ✅ Chrome (Node.js only - for Puppeteer)
- ✅ OpenJDK 17 + jq (Node.js only - for ZATCA SDK)

### Development Only

- ✅ Build tools (python3, build-essential, pkg-config)
- ✅ Canvas development libraries
- ✅ OPcache with timestamp validation
- ✅ gettext for envsubst
- ✅ All devDependencies

### Production Only

- ✅ Multi-stage optimization
- ✅ Supervisor for process management
- ✅ Aggressive cleanup (removed tests, docs, etc.)
- ✅ Optimized autoloader
- ✅ Full caching (config + routes + views)

## 🧪 Testing

```bash
# Build production image
cd docker/production
docker compose build howa-prod-app

# Build development image
cd docker/development
docker compose build howa-dev-app

# Check image sizes
docker images | grep loogix/howa-app

# Run and test
docker compose up -d
docker compose logs -f howa-prod-app
docker compose exec howa-prod-app php artisan --version
```

## 📚 Full Documentation

See [UNIFIED-DOCKERFILE-USAGE.md](./UNIFIED-DOCKERFILE-USAGE.md) for complete documentation.

---

**✨ Production deployments remain unchanged - existing configs work as-is!**
