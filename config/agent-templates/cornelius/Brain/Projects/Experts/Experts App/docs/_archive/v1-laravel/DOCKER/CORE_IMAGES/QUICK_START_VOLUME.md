---
title: "Quick Start: Volume Mount Strategy (Default)"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/docker"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Quick Start: Volume Mount Strategy (Default)

## TL;DR

```bash
# 1. Build PHP core volume (one time - 68.9s)
cd docker/canary
./php-core.sh

# 2. Verify it worked
./verify-php-core.sh

# 3. Build experts-api image (every time - 51s)
docker-compose build experts-api

# 4. Run
docker-compose up -d experts-api
```

## Why Volume Mount?

✅ **Fastest**: ~51s builds (0s for PHP runtime)
✅ **Smallest**: ~125MB images (vs 210MB)
✅ **Flexible**: Update PHP without rebuilding images
✅ **Efficient**: Share one PHP core across all containers

## How It Works

```
php-core volume         experts-api image
(built once)           (builds every time)

./volumes/php-core/        alpine:3.22
├── usr/local/  ─────►  + Laravel app only
├── usr/bin/               Size: ~125MB
└── etc/nginx/

Build: 68.9s (once)     Build: ~51s
Size: ~500MB            Runtime: mounts php-core
```

## Step-by-Step Setup

### 1. Build PHP Core Volume (One Time)

```bash
cd /home/logix/experts/docker/canary

# This creates ./volumes/php-core with PHP 8.4 + extensions
./php-core.sh
```

**What this does**:

- Creates `./volumes/php-core/` directory
- Installs PHP 8.4-FPM + Alpine 3.22
- Builds extensions: redis, pcov, gd, pdo, mysql, sqlite, zip
- Installs tools: supervisor, nginx, pnpm, node, npm
- Sets timezone to Asia/Riyadh
- Takes ~68.9 seconds (ONE TIME ONLY)

**Output**:

```
✅ PHP Core volume created at: ./volumes/php-core
📊 Size: 487M
```

### 2. Verify PHP Core Volume

```bash
# Run verification script
./verify-php-core.sh
```

**Expected output**:

```
✅ Volume exists: ./volumes/php-core
📦 PHP Version: 8.4.x
🔧 Extensions: redis, pcov, gd, pdo_mysql, pdo_sqlite, zip
📦 pnpm: 10.22.0
🌍 Timezone: Asia/Riyadh
```

### 3. Build experts-api Image

```bash
# Build the minimal image (Laravel app only)
docker-compose build experts-api
```

**What this does**:

- Uses target: `production-minimal` (default in docker-compose.yml)
- Builds from `alpine:3.22` base (minimal)
- Runs composer install (with PHP from volume during build)
- Copies Laravel application
- Creates ~125MB image
- Takes ~51 seconds

**Build output**:

```
[+] Building 51.2s
 => [dependencies] composer install     30.1s
 => [builder] dump-autoload             14.8s
 => [production-minimal] final          6.3s
```

### 4. Run

```bash
# Start the container
docker-compose up -d experts-api

# Check status
docker-compose ps experts-api

# View logs
docker-compose logs -f experts-api
```

**What happens at runtime**:

1. Container starts from minimal image (~125MB)
2. Volume mounts provide PHP runtime:
   - `/usr/local` → PHP binaries & extensions
   - `/usr/bin` → System tools
   - `/etc/nginx` → Nginx configs
3. Supervisor starts PHP-FPM + Nginx
4. Laravel application runs

## Verify Everything Works

```bash
# Check PHP is available
docker-compose exec experts-api php -v
# PHP 8.4.x (cli) (built: ...)

# Check Laravel
docker-compose exec experts-api php artisan --version
# Laravel Framework X.X.X

# Check extensions
docker-compose exec experts-api php -m | grep redis
# redis

# Check health
curl http://localhost:3026/api/health
```

## File Structure

```
docker/canary/
├── php-core.sh              # Build script (creates volume)
├── verify-php-core.sh       # Verification script
├── docker-compose.yml       # Already configured!
└── volumes/
    └── php-core/            # PHP runtime (created by php-core.sh)
        ├── usr/
        │   ├── local/       # PHP binaries & extensions
        │   ├── bin/         # Tools (supervisor, nginx, pnpm)
        │   ├── sbin/        # System binaries
        │   └── lib/         # Libraries
        ├── lib/             # System libraries
        └── etc/
            ├── nginx/       # Nginx config
            ├── localtime    # Timezone
            └── timezone     # Timezone name
```

## docker-compose.yml Configuration

Already configured in `/home/logix/experts/docker/canary/docker-compose.yml`:

```yaml
services:
  experts-api:
    build:
      target: production-minimal # ← Minimal image (default)
    volumes:
      # PHP core mounts (read-only)
      - ./volumes/php-core/usr/local:/usr/local:ro
      - ./volumes/php-core/usr/bin:/usr/bin:ro
      - ./volumes/php-core/usr/sbin:/usr/sbin:ro
      - ./volumes/php-core/usr/lib:/usr/lib:ro
      - ./volumes/php-core/lib:/lib:ro
      - ./volumes/php-core/etc/nginx:/etc/nginx:ro
      - ./volumes/php-core/etc/localtime:/etc/localtime:ro
      - ./volumes/php-core/etc/timezone:/etc/timezone:ro

      # App storage (read-write)
      - experts_canary_shared_storage:/app/storage/app/s
```

## Update PHP Core

When you need to update PHP or extensions:

```bash
# 1. Rebuild PHP core volume
cd docker/canary
./php-core.sh

# 2. Restart containers (no image rebuild needed!)
docker-compose restart experts-api
```

That's it! The new PHP version is immediately available to all containers.

## Benefits Recap

| Benefit         | Details                                       |
| --------------- | --------------------------------------------- |
| **Build Speed** | 51s (vs 120s with full build) - 57% faster    |
| **Image Size**  | 125MB (vs 210MB) - 40% smaller                |
| **Flexibility** | Update PHP without rebuilding images          |
| **Efficiency**  | Share one PHP core across multiple containers |
| **Development** | Fast iteration, easy debugging                |
| **Production**  | Smaller images, faster deployments            |

## Comparison with Other Methods

| Method           | Build Time | Image Size | Update PHP               |
| ---------------- | ---------- | ---------- | ------------------------ |
| **Volume Mount** | 51s        | 125MB      | Rebuild volume + restart |
| Image-based      | 51s        | 210MB      | Rebuild base + image     |
| Full build       | 120s       | 210MB      | Rebuild everything       |

## Next Steps

- 📖 See `HYBRID_APPROACH.md` for other build strategies
- 🔧 See `php-core.sh` to customize PHP version or extensions
- 📊 See `verify-php-core.sh` to troubleshoot issues

## Common Issues

### "php: not found" when running container

**Fix**: Ensure php-core volume exists and mounts are correct in docker-compose.yml

### Build fails with "composer: not found"

**Fix**: This is expected during dependency/builder stages - they use full PHP build internally

### Slow builds (still 120s)

**Fix**: Check `docker-compose.yml` has `target: production-minimal`

## Support

See `HYBRID_APPROACH.md` for detailed documentation of all build strategies.
