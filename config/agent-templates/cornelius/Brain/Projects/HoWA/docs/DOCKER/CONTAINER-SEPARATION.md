---
title: "Container Separation: Vite vs PHP"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Container Separation: Vite vs PHP

## The Golden Rule

> **Vite Container = Node.js ONLY (for HMR)**  
> **PHP Container = PHP + All Laravel Services**

## Understanding the Separation

### Vite Container (Node.js)

- **Purpose:** Hot Module Replacement (HMR) for frontend assets
- **Has:** Node.js, pnpm, Vite
- **Doesn't Have:** PHP, artisan, composer
- **Runs:** `vite` command only

### PHP Container (PHP-FPM + nginx)

- **Purpose:** Laravel application, queue workers, Reverb
- **Has:** PHP, artisan, composer, Node.js (for building)
- **Runs:** PHP-FPM, nginx, queue listeners, Reverb, scheduler

## Common Mistake

### ❌ Running PHP Commands in Vite Container

```yaml
# WRONG! Vite container doesn't have PHP
vite-client:
  command: ["pnpm", "dev"]
  # ^ This runs:
  #   - vite ✅ (works)
  #   - php artisan queue:listen ❌ (fails - no PHP!)
  #   - php artisan reverb:start ❌ (fails - no PHP!)
```

**Error:**

```
sh: php: not found
ELIFECYCLE Command failed
```

### ✅ Correct Separation

```yaml
# Vite container - ONLY Vite
vite-client:
  command: ["pnpm", "dev:app"]
  # ^ Only runs: vite ✅

# PHP container - ALL Laravel services
howa-dev-app:
  # Supervisor manages:
  # - PHP-FPM ✅
  # - nginx ✅
  # - queue:listen ✅
  # - reverb:start ✅
  # - schedule:run ✅
```

## package.json Script Structure

### Current Structure (Correct!)

```json
{
  "scripts": {
    "dev:app": "vite",
    // ↑ For Docker Vite container (Node.js only)

    "listen": "php artisan queue:listen client_notifications",
    "listen:etf": "php artisan queue:listen etf-updates",
    "socket": "php artisan reverb:start",
    // ↑ For PHP container (has artisan)

    "dev": "concurrently \"pnpm dev:app\" \"pnpm listen\" \"pnpm listen:etf\""
    // ↑ For LOCAL development (host machine has both Node + PHP)
  }
}
```

### Usage

| Environment     | Command            | Where          | Why                 |
| --------------- | ------------------ | -------------- | ------------------- |
| **Docker Vite** | `pnpm dev:app`     | Vite container | Only has Node.js    |
| **Docker PHP**  | Supervisor configs | PHP container  | Has PHP + artisan   |
| **Local Dev**   | `pnpm dev`         | Host machine   | Has both Node + PHP |

## Docker Compose Configuration

### Complete Setup (All Services)

```yaml
services:
  # ============================================
  # Vite HMR - Client (Node.js ONLY)
  # ============================================
  vite-client:
    build:
      dockerfile: docker/vite/Dockerfile
      target: development
      args:
        APP_PATH: client
    command: ["pnpm", "dev:app"] # ← ONLY Vite!
    volumes:
      - ./apps/client:/app/apps/client
      - ./apps/shared:/app/apps/shared
      - /app/node_modules
      - /app/apps/client/node_modules
    ports:
      - "5175:5175"

  # ============================================
  # Laravel Client App (PHP + Everything)
  # ============================================
  howa-dev-app:
    build:
      dockerfile: docker/php/Dockerfile
      target: development
      args:
        APP_PATH: client
    volumes:
      - ./apps/client:/app/apps/client
      - ./apps/shared:/app/apps/shared
    # Supervisor handles:
    # - PHP-FPM (web server)
    # - nginx (reverse proxy)
    # - queue:listen client_notifications (queue worker)
    # - queue:listen etf-updates (queue worker)
    # - reverb:start (WebSocket server)
    # - schedule:run (cron jobs)
```

## Where Each Service Runs

| Service                         | Container      | Command        | Purpose              |
| ------------------------------- | -------------- | -------------- | -------------------- |
| **Vite HMR**                    | `vite-client`  | `pnpm dev:app` | Frontend hot reload  |
| **PHP-FPM**                     | `howa-dev-app` | Supervisor     | Process PHP requests |
| **nginx**                       | `howa-dev-app` | Supervisor     | Web server           |
| **Queue: client_notifications** | `howa-dev-app` | Supervisor     | Process jobs         |
| **Queue: etf-updates**          | `howa-dev-app` | Supervisor     | Process jobs         |
| **Reverb (WebSocket)**          | `howa-dev-app` | Supervisor     | Real-time updates    |
| **Scheduler**                   | `howa-dev-app` | Supervisor     | Cron jobs            |

## Supervisor Configuration Example

**docker/supervisor/client.conf:**

```ini
[program:client-php-fpm]
command=/usr/local/sbin/php-fpm --nodaemonize
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/client-fpm.log

[program:client-nginx]
command=/usr/sbin/nginx -g 'daemon off;'
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/client-nginx.log

[program:client-queue-notifications]
command=php artisan queue:listen client_notifications --verbose
directory=/app/apps/client
autostart=true
autorestart=true
user=www-data
stdout_logfile=/var/log/supervisor/client-queue.log

[program:client-queue-etf]
command=php artisan queue:listen etf-updates --verbose
directory=/app/apps/client
autostart=true
autorestart=true
user=www-data
stdout_logfile=/var/log/supervisor/client-queue-etf.log

[program:client-reverb]
command=php artisan reverb:start
directory=/app/apps/client
autostart=true
autorestart=true
user=www-data
stdout_logfile=/var/log/supervisor/client-reverb.log

[program:client-scheduler]
command=php artisan schedule:run
directory=/app/apps/client
autostart=true
autorestart=true
user=www-data
stdout_logfile=/var/log/supervisor/client-scheduler.log
```

## Fixes Applied

### 1. Removed `CI=true` from Vite Dockerfile

**Before:**

```dockerfile
ENV CI=true  # ← Blocks Laravel Vite plugin
```

**After:**

```dockerfile
# Removed CI=true (not needed for Vite HMR)
```

### 2. Changed Command to Vite-Only

**Before:**

```yaml
command: ["pnpm", "dev"]
# Tries to run queue listeners → fails (no PHP)
```

**After:**

```yaml
command: ["pnpm", "dev:app"]
# Only runs vite → works perfectly
```

### 3. Mount Only What's Needed

**Before:**

```yaml
volumes:
  - ../../:/app # ← Everything!
```

**After:**

```yaml
volumes:
  - ../../apps/client:/app/apps/client # ← Just client
  - ../../apps/shared:/app/apps/shared # ← Just shared
  - /app/node_modules # ← Exclude
  - /app/apps/client/node_modules # ← Exclude
```

## Testing

### 1. Rebuild Vite Images

```bash
cd docker/development
docker compose build vite-client vite-admin
```

### 2. Start Services

```bash
docker compose up -d vite-client vite-admin
```

### 3. Check Logs (Should NOT see PHP errors)

```bash
docker compose logs -f vite-client

# ✅ Should see:
#   VITE v7.x.x ready in XXX ms
#   ➜ Local:   http://localhost:5173/
#   ➜ Network: http://0.0.0.0:5173/
#
# ❌ Should NOT see:
#   sh: php: not found
#   Error: You should not run the Vite HMR server in CI environments
```

### 4. Test HMR

```bash
# Edit a file
echo "// test HMR" >> apps/client/resources/js/app.jsx

# Check browser - should update instantly
```

## Production Note

In production, you don't need separate Vite containers! The build happens during the Docker build:

```dockerfile
# PHP Dockerfile - STAGE 3: Builder
RUN pnpm build  # ← Builds assets into public/build/
```

The built assets are served by nginx directly (no Vite dev server needed).

---

**✅ Summary:**

- Vite container = Vite only (no PHP)
- PHP container = PHP + all Laravel services
- Use `pnpm dev:app` in Docker
- Use `pnpm dev` on local machine (host)
