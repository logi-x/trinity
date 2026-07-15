---
title: "Vite Dockerfile Usage"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Vite Dockerfile Usage

The unified Vite Dockerfile provides proper isolation per app with **build-time** dependency installation.

## Key Improvements

### ❌ Before (Runtime Installation - Slow!)

```yaml
vite-client:
  image: node:22.14.0-alpine
  command: sh -c "pnpm --filter @howa/client... install && pnpm dev:client"
  # ^ Installs dependencies EVERY TIME container starts (slow!)
```

### ✅ After (Build-time Installation - Fast!)

```yaml
vite-client:
  build:
    context: ../..
    dockerfile: docker/vite/Dockerfile
    target: development # ← Use development target
    args:
      APP_PATH: client # ← Isolated per app
  image: loogix/howa-vite-client:dev
  # Dependencies already installed in image!
  # Container starts in ~1 second
```

## Dockerfile Structure

```
Stage 1: base         - System dependencies (alpine + build tools)
Stage 2: dependencies - Install packages for APP_PATH (BUILD TIME!)
Stage 3: development  - Vite HMR server (fast startup)
Stage 4: production   - Build static assets
```

## Usage in docker-compose.yml

### Development Environment

```yaml
services:
  # Client Vite HMR
  vite-client:
    build:
      context: ../..
      dockerfile: docker/vite/Dockerfile
      target: development
      args:
        APP_PATH: client
    image: loogix/howa-vite-client:dev
    container_name: howa-vite-client
    working_dir: /app/apps/client
    ports:
      - "5173:5173"
    networks:
      - howa-shared-network
    volumes:
      # Volume mount for HMR (hot reload)
      - ../../apps/client:/app/apps/client
      - ../../apps/shared:/app/apps/shared
      # Exclude node_modules (use image's version)
      - /app/node_modules
      - /app/apps/client/node_modules
    environment:
      - NODE_ENV=development
    command: ["pnpm", "dev"]

  # Admin Vite HMR
  vite-admin:
    build:
      context: ../..
      dockerfile: docker/vite/Dockerfile
      target: development
      args:
        APP_PATH: admin
    image: loogix/howa-vite-admin:dev
    container_name: howa-vite-admin
    working_dir: /app/apps/admin
    ports:
      - "5174:5173"
    networks:
      - howa-shared-network
    volumes:
      # Volume mount for HMR (hot reload)
      - ../../apps/admin:/app/apps/admin
      - ../../apps/shared:/app/apps/shared
      # Exclude node_modules (use image's version)
      - /app/node_modules
      - /app/apps/admin/node_modules
    environment:
      - NODE_ENV=development
    command: ["pnpm", "dev"]
```

### Production Build (Optional - for pre-building assets)

```yaml
services:
  # Build client assets
  vite-build-client:
    build:
      context: ../..
      dockerfile: docker/vite/Dockerfile
      target: production
      args:
        APP_PATH: client
    image: loogix/howa-vite-client:prod
    # Use this to extract built assets:
    # docker cp howa-vite-build-client:/app/apps/client/public/build ./build-output
```

## Benefits

### 🚀 Fast Startup

- **Before:** 30-60 seconds (pnpm install at runtime)
- **After:** 1-2 seconds (dependencies pre-installed)

### 📦 Better Layer Caching

```dockerfile
COPY package.json ...     # ← Only changes when dependencies change
RUN pnpm install ...      # ← Cached layer! Fast rebuilds

COPY apps/${APP_PATH} ... # ← Changes frequently (code changes)
```

**Result:** When you change code, Docker only rebuilds the last layer. Dependencies are cached!

### 🎯 Proper Isolation

- Each app (`client`, `admin`) gets its own image
- Dependencies scoped to `--filter @howa/${APP_PATH}...`
- No accidental dependency conflicts

### 🔄 Hot Module Replacement Works Perfectly

- Volume mount for code changes
- Node modules from image (stable, fast)
- HMR updates in milliseconds

## Queue Listeners & Reverb (Important!)

### ⚠️ Vite Container = Vite Only

The Vite container **only has Node.js**, not PHP. It should **only run Vite dev server**.

**❌ Wrong (tries to run PHP in Node.js container):**

```yaml
vite-client:
  command: ["pnpm", "dev"] # ← Runs concurrently with queue:listen (PHP!)
```

**✅ Correct (only runs Vite):**

```yaml
vite-client:
  command: ["pnpm", "dev:app"] # ← Only runs vite
```

### Where Queue Listeners Should Run

Queue listeners need PHP, so they run in the **PHP container**:

```yaml
# PHP container (has PHP + artisan)
howa-dev-app:
  image: loogix/howa-app:dev
  command: >
    sh -c "
      php artisan queue:listen client_notifications &
      php artisan queue:listen etf-updates &
      php artisan reverb:start &
      php-fpm -D && nginx -g 'daemon off;'
    "
```

Or better yet, use **Supervisor** in production to manage these processes.

### Script Separation

Your `package.json` should have separate scripts:

```json
{
  "scripts": {
    "dev:app": "vite", // ← For Vite container
    "listen": "php artisan queue:listen", // ← For PHP container
    "dev": "concurrently ..." // ← For local development only
  }
}
```

## Commands

### Build Images

```bash
# Build client Vite image
docker build -t howa-vite-client:dev \
  --target development \
  --build-arg APP_PATH=client \
  -f docker/vite/Dockerfile .

# Build admin Vite image
docker build -t howa-vite-admin:dev \
  --target development \
  --build-arg APP_PATH=admin \
  -f docker/vite/Dockerfile .

# Or use docker-compose
docker compose build vite-client vite-admin
```

### Run Containers

```bash
# Start Vite HMR servers
docker compose up -d vite-client vite-admin

# Check logs
docker compose logs -f vite-client

# Restart after package.json changes (rebuild needed)
docker compose up -d --build vite-client
```

### Access Vite Dev Server

- Client: `http://localhost:5173`
- Admin: `http://localhost:5174`

## When to Rebuild

### ✅ Rebuild Required (dependencies changed)

- Modified `package.json`
- Modified `pnpm-lock.yaml`
- Added/removed dependencies

```bash
docker compose build vite-client
docker compose up -d vite-client
```

### ❌ No Rebuild Needed (code changed)

- Modified `.tsx/.jsx/.ts/.js` files
- Modified `.css` files
- Modified components

HMR handles this automatically! Just save the file.

## Troubleshooting

### Dependencies not found

**Problem:** Added new package but getting `Cannot find module`

**Solution:** Rebuild the image

```bash
docker compose build vite-client
docker compose up -d vite-client
```

### Port already in use

**Problem:** `Error: listen EADDRINUSE: address already in use :::5173`

**Solution:**

1. Stop the conflicting container: `docker compose stop vite-client`
2. Or change the port in `docker-compose.yml`: `"5175:5173"`

### Slow HMR

**Problem:** Hot reload takes 5+ seconds

**Solution:** Check volume mounts - make sure `node_modules` is excluded:

```yaml
volumes:
  - ../../apps/client:/app/apps/client
  - /app/node_modules # ← Exclude this!
```

## Comparison: Old vs New

| Aspect           | Old (Runtime Install) | New (Build-time Install) |
| ---------------- | --------------------- | ------------------------ |
| **Startup Time** | 30-60 seconds         | 1-2 seconds              |
| **Dependencies** | Installed at runtime  | Pre-installed in image   |
| **Caching**      | No caching            | Layer caching            |
| **Rebuilds**     | Always slow           | Fast (cached layers)     |
| **Isolation**    | Shared deps           | Per-app isolation        |
| **HMR**          | Works                 | Works (faster)           |

## Example: Complete Flow

### 1. First Time Setup

```bash
# Build images (one time)
cd docker/development
docker compose build vite-client vite-admin

# Start services
docker compose up -d

# Check logs
docker compose logs -f vite-client
```

### 2. Daily Development

```bash
# Just start containers (fast!)
docker compose up -d

# Code in your editor
# HMR updates automatically
# No need to restart containers
```

### 3. After Adding Dependencies

```bash
# Added new package to package.json
pnpm install  # (on host, or skip if you prefer Docker-only)

# Rebuild image
docker compose build vite-client

# Restart container
docker compose up -d vite-client
```

---

**🎉 Your Vite containers now start in 1-2 seconds instead of 30-60 seconds!**
