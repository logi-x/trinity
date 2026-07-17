---
title: "PHP Core Quick Start Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/docker"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# PHP Core Quick Start Guide

## TL;DR - Volume Mount (Default & Recommended)

```bash
# First time setup (one time only)
cd docker/canary
./php-core.sh              # Creates volume - 68.9s once
./verify-php-core.sh       # Verify it works

# Build experts-api (every time)
docker-compose build experts-api  # Takes ~51s (vs 120s before)
```

## Three Build Strategies Available

1. **Volume Mount (DEFAULT)** - Best for dev/staging/prod
   - Image: ~125MB | Build: 51s | Update PHP: restart only
2. **Image-Based** - Best for cloud/standalone
   - Image: ~210MB | Build: 51s | Update PHP: rebuild base
3. **Full Build** - Best for CI/CD
   - Image: ~210MB | Build: 120s | Update PHP: rebuild all

See `HYBRID_APPROACH.md` for detailed comparison.

## What This Does

**Before**: experts-api builds PHP extensions every time (68.9s per build)
**After**: Choose your strategy based on needs
**Result**: Up to 57% faster builds + smaller images

## Commands - Volume Mount Strategy

### Build php-core volume (one time)

```bash
cd docker/canary
./php-core.sh              # Creates ./volumes/php-core
```

### Verify php-core volume

```bash
cd docker/canary
./verify-php-core.sh       # Or: ls -lh volumes/php-core
```

### Build experts-api

```bash
docker-compose -f docker/canary/docker-compose.yml build experts-api
```

### Check volume exists

```bash
ls -lh docker/canary/volumes/php-core
# Should show: usr/ lib/ etc/ directories
```

## Commands - Image-Based Strategy

### Build php-core image (one time)

```bash
cd docker/canary
./build-php-core.sh        # Creates php-core:8.4 image
```

### Check if image exists

```bash
docker images | grep php-core
# Should show: php-core  8.4  185MB
```

## When to Rebuild php-core

✅ **Rebuild when**:

- Upgrading PHP version (8.4 → 8.5)
- Adding/removing PHP extensions
- Updating pnpm, node, npm versions
- Changing system packages

❌ **No rebuild needed**:

- Laravel code changes
- Composer dependency updates
- Environment variables
- Config file changes

## Files & Documentation

- `php-core.sh` - Volume builder (default)
- `build-php-core.sh` - Image builder (alternative)
- `verify-php-core.sh` - Verification script
- `QUICK_START_VOLUME.md` - Detailed volume mount guide
- `HYBRID_APPROACH.md` - Compare all three strategies
- `PHP_CORE_README.md` - Image-based documentation

## Troubleshooting

### Volume Mount: "php: not found"

```bash
# Check volume exists
ls -lh docker/canary/volumes/php-core

# Rebuild if missing
cd docker/canary
./php-core.sh
```

### Image-Based: "php-core:8.4 not found"

```bash
# Build the image
cd docker/canary
./build-php-core.sh
```

### Build still slow (120s instead of 51s)

```bash
# Check docker-compose.yml target
grep "target:" docker/canary/docker-compose.yml
# Should show: target: production-minimal

# Enable BuildKit
export DOCKER_BUILDKIT=1
```

## Recommendations

- **Development**: Use volume mount (fast, flexible)
- **Staging**: Use volume mount (matches production)
- **Production**: Use volume mount (optimal)
- **Cloud**: Use image-based (portable)
- **CI/CD**: Use full build or image-based

## Support

- `QUICK_START_VOLUME.md` - Volume mount detailed guide
- `HYBRID_APPROACH.md` - Compare all strategies
- `PHP_CORE_README.md` - Image-based documentation
