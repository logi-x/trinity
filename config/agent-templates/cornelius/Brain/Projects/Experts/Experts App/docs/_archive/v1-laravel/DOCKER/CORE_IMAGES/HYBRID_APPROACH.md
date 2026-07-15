---
title: "Hybrid PHP Core Build Strategy"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/docker"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Hybrid PHP Core Build Strategy

## Overview

The experts-api Dockerfile now supports **three build strategies** for maximum flexibility. Choose the one that best fits your deployment environment.

## Three Build Strategies

### 1. 🏆 Volume Mount (DEFAULT - Recommended)

**Best for**: Development, Staging, Production with persistent volumes

#### Advantages

- ✅ **Fastest builds**: ~0s for PHP runtime (mounted at runtime)
- ✅ **Smallest images**: ~125MB (no PHP runtime in image)
- ✅ **Easy updates**: Update PHP core once, all containers benefit
- ✅ **Flexible**: Change PHP version without rebuilding images
- ✅ **Resource efficient**: Share one PHP core across multiple containers

#### How it Works

```
┌────────────────────────────────────────┐
│ php-core volume (built once)           │
│ ./volumes/php-core/                    │
│  ├── usr/local/  (PHP + extensions)    │
│  ├── usr/bin/    (tools)               │
│  └── etc/nginx/  (configs)             │
└────────────────────────────────────────┘
                 ↓ (mount at runtime)
┌────────────────────────────────────────┐
│ experts-api image                      │
│ FROM alpine:3.22 (minimal)             │
│ COPY /app (Laravel app only)           │
│ Size: ~125MB                           │
└────────────────────────────────────────┘
```

#### Setup

```bash
# 1. Build PHP core volume (one time)
cd docker/canary
./php-core.sh

# 2. Build experts-api image (minimal)
docker-compose -f docker/canary/docker-compose.yml build experts-api
# Target: production-minimal (default)
# Build time: ~51s

# 3. Run with volume mounts
docker-compose -f docker/canary/docker-compose.yml up experts-api
# Mounts PHP core from ./volumes/php-core at runtime
```

#### Docker Compose Configuration

```yaml
services:
  experts-api:
    build:
      target: production-minimal # Default
    volumes:
      # Mount PHP core (read-only)
      - ./volumes/php-core/usr/local:/usr/local:ro
      - ./volumes/php-core/usr/bin:/usr/bin:ro
      - ./volumes/php-core/usr/sbin:/usr/sbin:ro
      - ./volumes/php-core/usr/lib:/usr/lib:ro
      - ./volumes/php-core/lib:/lib:ro
      - ./volumes/php-core/etc/nginx:/etc/nginx:ro
      - ./volumes/php-core/etc/localtime:/etc/localtime:ro
      - ./volumes/php-core/etc/timezone:/etc/timezone:ro
```

---

### 2. 📦 Image-Based (Standalone)

**Best for**: Standalone deployments, environments without volume support (some cloud platforms)

#### Advantages

- ✅ **Self-contained**: No external dependencies at runtime
- ✅ **Portable**: Works anywhere Docker runs
- ✅ **Fast builds**: ~0s for PHP (uses pre-built image)
- ✅ **No volume management**: Simpler deployment

#### Disadvantages

- ❌ **Larger images**: ~210MB (includes PHP runtime)
- ❌ **Less flexible**: Need to rebuild to change PHP version

#### How it Works

```
┌────────────────────────────────────────┐
│ php-core:8.4 image (built once)        │
│ FROM php:8.4-fpm-alpine3.22            │
│ + All PHP extensions                   │
│ Size: ~185MB                           │
└────────────────────────────────────────┘
                 ↓ (FROM php-core:8.4)
┌────────────────────────────────────────┐
│ experts-api image                      │
│ FROM php-core:8.4                      │
│ + Laravel app                          │
│ Size: ~210MB                           │
└────────────────────────────────────────┘
```

#### Setup

```bash
# 1. Build PHP core image (one time)
cd docker/canary
./build-php-core.sh

# 2. Build experts-api image (standalone)
docker build \
  --build-arg USE_PHP_CORE_IMAGE=true \
  --target production \
  -f apps/experts-api/Dockerfile \
  -t experts-api:production \
  .
# Build time: ~51s

# 3. Run (no volumes needed)
docker run experts-api:production
```

#### Docker Compose Configuration

```yaml
services:
  experts-api:
    build:
      target: production
      args:
        USE_PHP_CORE_IMAGE: true
    # No volume mounts needed
```

---

### 3. 🔨 Full Build (Fallback)

**Best for**: CI/CD without caching, first-time setup, testing

#### Advantages

- ✅ **No dependencies**: Builds everything from scratch
- ✅ **Self-contained**: No pre-built images or volumes needed
- ✅ **Reproducible**: Same build every time

#### Disadvantages

- ❌ **Slowest builds**: 68.9s for PHP extensions every time
- ❌ **Larger images**: ~210MB

#### How it Works

```
┌────────────────────────────────────────┐
│ experts-api image                      │
│ FROM php:8.4-fpm-alpine3.22            │
│ + Build PHP extensions (68.9s)         │
│ + Laravel app                          │
│ Size: ~210MB                           │
└────────────────────────────────────────┘
```

#### Setup

```bash
# Build everything from scratch
docker build \
  --build-arg BUILD_PHP_FULL=true \
  --target production \
  -f apps/experts-api/Dockerfile \
  -t experts-api:production \
  .
# Build time: ~120s (68.9s PHP + 51s app)
```

---

## Comparison Table

| Feature         | Volume Mount     | Image-Based    | Full Build     |
| --------------- | ---------------- | -------------- | -------------- |
| **Build time**  | ~51s             | ~51s           | ~120s          |
| **Image size**  | ~125MB           | ~210MB         | ~210MB         |
| **PHP update**  | Update volume    | Rebuild base   | Rebuild all    |
| **Portability** | Requires volumes | Fully portable | Fully portable |
| **Flexibility** | High             | Medium         | Low            |
| **Complexity**  | Medium           | Low            | Low            |
| **Best for**    | Dev/Staging/Prod | Cloud deploys  | CI/CD          |

## When to Use Each Approach

### Use Volume Mount When

- ✅ Running on servers with volume support (Docker Compose, Kubernetes with volumes)
- ✅ You want to share PHP core across multiple containers
- ✅ You need to update PHP without rebuilding images
- ✅ You want the smallest possible images
- ✅ You're in development or staging environments

### Use Image-Based When

- ✅ Deploying to cloud platforms without volume support
- ✅ You need fully self-contained images
- ✅ You're distributing images to third parties
- ✅ You want simpler deployment (no volume management)
- ✅ You're deploying to container registries (Docker Hub, ECR, GCR)

### Use Full Build When

- ✅ First-time setup (no php-core image/volume yet)
- ✅ Testing in CI/CD without caching
- ✅ You need reproducible builds from scratch
- ✅ You don't have php-core image/volume available
- ✅ Build time is not a concern

## Switching Between Strategies

### From Full Build → Volume Mount

```bash
# 1. Build PHP core volume
cd docker/canary
./php-core.sh

# 2. Update docker-compose.yml target
target: production-minimal

# 3. Add volume mounts to docker-compose.yml
volumes:
  - ./volumes/php-core/usr/local:/usr/local:ro
  # ... (see Volume Mount section)

# 4. Rebuild
docker-compose build experts-api
```

### From Volume Mount → Image-Based

```bash
# 1. Build PHP core image
cd docker/canary
./build-php-core.sh

# 2. Update docker-compose.yml
target: production
args:
  USE_PHP_CORE_IMAGE: true

# 3. Remove volume mounts from docker-compose.yml

# 4. Rebuild
docker-compose build experts-api
```

### From Image-Based → Full Build

```bash
# 1. Update docker-compose.yml
target: production
args:
  BUILD_PHP_FULL: true
  USE_PHP_CORE_IMAGE: false

# 2. Rebuild
docker-compose build experts-api
```

## Build Time Breakdown

### Volume Mount

```
┌─────────────────────────┐
│ Phase 1: Build PHP Core │  68.9s (ONE TIME)
│ ./php-core.sh           │
└─────────────────────────┘
         ↓
┌─────────────────────────┐
│ Phase 2: Build Image    │  ~51s (EVERY TIME)
│ - Dependencies: 30s     │
│ - Builder: 15s          │
│ - Production: 6s        │
└─────────────────────────┘
         ↓
┌─────────────────────────┐
│ Phase 3: Start          │  ~2s
│ Mount volumes & run     │
└─────────────────────────┘

Total first build: 121.9s
Total subsequent: 51s
```

### Image-Based

```
┌─────────────────────────┐
│ Phase 1: Build Core Img │  68.9s (ONE TIME)
│ ./build-php-core.sh     │
└─────────────────────────┘
         ↓
┌─────────────────────────┐
│ Phase 2: Build Image    │  ~51s (EVERY TIME)
│ - Dependencies: 30s     │
│ - Builder: 15s          │
│ - Production: 6s        │
└─────────────────────────┘
         ↓
┌─────────────────────────┐
│ Phase 3: Start          │  ~2s
│ Run container           │
└─────────────────────────┘

Total first build: 119.9s
Total subsequent: 51s
```

### Full Build

```
┌─────────────────────────┐
│ Phase 1: Build Image    │  ~120s (EVERY TIME)
│ - PHP Build: 68.9s      │
│ - Dependencies: 30s     │
│ - Builder: 15s          │
│ - Production: 6s        │
└─────────────────────────┘
         ↓
┌─────────────────────────┐
│ Phase 2: Start          │  ~2s
│ Run container           │
└─────────────────────────┘

Total every build: 120s
```

## Dockerfile Stages Explained

```dockerfile
# Stage 1a: Base from php-core image (for image-based)
FROM php-core:8.4 AS base-from-image

# Stage 1b: Base with full PHP build (for volume mount build)
FROM php:8.4-fpm-alpine3.22 AS base-full-build
RUN [build PHP extensions - 68.9s]

# Stage 1c: Base minimal (for volume mount runtime)
FROM alpine:3.22 AS base-minimal
RUN [minimal dependencies only]

# Stage 1d: Base selector (default: minimal)
FROM base-minimal AS base

# Stage 2: Builder base (uses full-build for dependencies/builder)
FROM base-full-build AS builder-base

# Stage 3: Dependencies (installs composer packages)
FROM builder-base AS dependencies

# Stage 4: Builder (builds Laravel app)
FROM builder-base AS builder

# Stage 5: Production Minimal (DEFAULT - volume mount)
FROM alpine:3.22 AS production-minimal
COPY --from=builder /app /app

# Stage 6: Production Standalone (image-based)
FROM base-full-build AS production
COPY --from=builder /app /app

# Stage 7: Development
FROM base-full-build AS development
```

## Recommended Strategy by Environment

- **Development**: Volume Mount (fast iterations, easy PHP updates)
- **Staging**: Volume Mount (matches production, cost-effective)
- **Production**: Volume Mount (optimal performance, easy updates)
- **CI/CD**: Image-Based or Full Build (portable, no volumes)
- **Cloud Deployments**: Image-Based (simpler, no volume management)

## Maintenance

### Update PHP Version (Volume Mount)

```bash
# Update php-core.sh PHP_VERSION
vim docker/canary/php-core.sh
# Change PHP_VERSION="8.4" to "8.5"

# Rebuild volume
cd docker/canary
./php-core.sh

# Restart containers (no image rebuild needed!)
docker-compose restart experts-api
```

### Update PHP Extensions (All Strategies)

1. Update Dockerfile.php-core or php-core.sh
2. Rebuild php-core (image or volume)
3. For volume mount: restart containers
4. For image-based: rebuild experts-api image

## Troubleshooting

### Volume Mount: PHP not found

**Problem**: Container can't find PHP binaries
**Solution**: Verify volume mounts in docker-compose.yml and ensure php-core volume exists

### Image-Based: php-core:8.4 not found

**Problem**: Base image not available
**Solution**: Run `./build-php-core.sh` first

### Slow builds despite optimization

**Problem**: Still taking 120s to build
**Solution**: Check docker-compose.yml target is correct and BuildKit is enabled

## Summary

The **hybrid approach** gives you the flexibility to choose the right strategy for each environment:

- 🏆 **Volume Mount (Default)**: Best overall - fast, flexible, efficient
- 📦 **Image-Based**: Best for cloud - portable, self-contained
- 🔨 **Full Build**: Best for CI/CD - reproducible, no dependencies

Choose based on your needs, and switch strategies easily by changing docker-compose.yml configuration!
