---
title: "Docker Storage Symlinks & Directory Setup"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Docker Storage Symlinks & Directory Setup

## 🐛 Problem Solved

### Error Encountered

```
ErrorException: mkdir(): No such file or directory
at app/Http/Controllers/ImageController.php:63
```

### Root Cause

1. **Laravel storage:link creates symlinks** with absolute host paths
2. **Inside container**, these paths don't match
3. **Shared storage** (`public/s`) points to `/home/logix/howa/apps/shared/s`
4. **Container mount** is at `/app/apps/shared` (missing `/howa`)
5. **Result:** Broken symlinks, mkdir() fails

## ✅ Solutions Implemented

### 1. **Dual Volume Mount** (docker-compose.yml)

```yaml
howa-app:
  volumes:
    - ./apps/client:/app/apps/client
    - ./apps/shared:/app/apps/shared
    # Also mount at symlink target path
    - ./apps/shared:/home/logix/howa/apps/shared # ← Fixes broken symlinks
```

**Why:** Laravel's `storage:link` creates symlinks using the full host path. By mounting shared at both paths, symlinks work correctly.

### 2. **Auto-Create Directories** (entrypoint-php.sh)

```bash
# Create storage symlink
php artisan storage:link

# Ensure shared directories exist
mkdir -p /home/logix/howa/apps/shared/s/cache
mkdir -p /home/logix/howa/apps/shared/s/invoice
mkdir -p /home/logix/howa/apps/shared/s/qr
chmod -R 775 /home/logix/howa/apps/shared/s
```

**When:** Runs automatically on every container start.

### 3. **Makefile Commands**

Added `make setup-storage` to manually setup storage for all apps:

```bash
make setup-storage  # Setup storage symlinks and directories
make setup-client   # Full client setup (includes storage)
make setup-admin    # Full admin setup (includes storage)
```

## 📁 Storage Structure

### Symlinks Created by Laravel

| App    | Symlink           | Target                           |
| ------ | ----------------- | -------------------------------- |
| Client | `/public/storage` | `storage/app/public`             |
| Client | `/public/s`       | `/home/logix/howa/apps/shared/s` |
| Admin  | `/public/storage` | `storage/app/public`             |
| Admin  | `/public/s`       | `/home/logix/howa/apps/shared/s` |

### Shared Directory Structure

```
apps/shared/s/
├── cache/          # Image/file cache
│   ├── invoice/
│   ├── course/
│   └── user/
├── invoice/        # Invoice files
├── qr/             # QR codes
├── credit-note/    # Credit notes
├── course/         # Course materials
└── ...
```

## 🔧 How It Works

### Development Flow

```
1. Container starts
   ↓
2. Entrypoint runs
   ↓
3. php artisan storage:link
   - Creates /public/storage → storage/app/public
   - Creates /public/s → /home/logix/howa/apps/shared/s
   ↓
4. mkdir creates shared directories
   ↓
5. Application can write to public/s/cache/{folder}/
```

### Why Dual Mount?

**Host filesystem:**

```
/home/logix/howa/apps/shared/s
```

**Container expects (from symlink):**

```
/home/logix/howa/apps/shared/s  ← Same path!
```

**Without dual mount:**

```
Container path: /app/apps/shared/s
Symlink points: /home/logix/howa/apps/shared/s  ← Broken!
```

**With dual mount:**

```
Both paths exist → Symlinks work! ✅
```

## 🚀 Quick Commands

### Setup Storage (First Time)

```bash
# After starting containers
make setup-storage

# Or manually for specific app
docker-compose exec howa-app php artisan storage:link
docker-compose exec howa-app mkdir -p public/s/cache
```

### Verify Storage Links

```bash
# Check symlinks
docker-compose exec howa-app ls -la /app/apps/client/public/ | grep "^l"

# Should show:
# storage -> /app/apps/client/storage/app/public
# s -> /home/logix/howa/apps/shared/s

# Test accessibility
docker-compose exec howa-app test -d /app/apps/client/public/s/cache && echo "✓ OK"
```

### Fix Broken Links

```bash
# If storage links are broken
docker-compose exec howa-app rm /app/apps/client/public/storage
docker-compose exec howa-app rm /app/apps/client/public/s
docker-compose restart howa-app
```

## 🐛 Troubleshooting

### mkdir() Still Fails?

```bash
# Check if directories exist
docker-compose exec howa-app ls -la /app/apps/client/public/s/

# Check if writable
docker-compose exec howa-app touch /app/apps/client/public/s/cache/test.txt

# Fix permissions
docker-compose exec howa-app chmod -R 775 /home/logix/howa/apps/shared/s
```

### Symlink Points to Wrong Path?

```bash
# Remove and recreate
docker-compose exec howa-app rm /app/apps/client/public/s
docker-compose exec howa-app php artisan storage:link
docker-compose restart howa-app
```

### Directory Not Found in Production?

Production should create directories during build:

```dockerfile
# In Dockerfile.prod
RUN mkdir -p /app/apps/${APP_PATH}/public/s/cache \
    && mkdir -p /app/apps/${APP_PATH}/public/s/invoice \
    && chmod -R 775 /app/apps/${APP_PATH}/public/s
```

## 📊 Files Modified

| File                               | Change                  | Purpose                      |
| ---------------------------------- | ----------------------- | ---------------------------- |
| `docker-compose.yml`               | Added dual mount        | Fix symlink paths            |
| `docker/scripts/entrypoint-php.sh` | Auto-create directories | Ensure dirs exist on startup |
| `Makefile`                         | Added setup-storage     | Easy setup command           |

## ✅ Verification Checklist

- [x] `public/storage` symlink exists
- [x] `public/s` symlink exists
- [x] `public/s/cache` directory accessible
- [x] `public/s/invoice` directory accessible
- [x] `public/s/qr` directory accessible
- [x] Directories writable (775 permissions)
- [x] Symlinks work across container restarts
- [x] No mkdir() errors in logs

## 🔒 Security Note

- Symlinks use **775** permissions (rwxrwxr-x)
- Allows web server (nginx/www-data) to write files
- Cache directories need write access for image processing
- OAuth keys remain **600** (separate security requirement)

## 🎯 Summary

**Problem:** Broken symlinks + missing directories = mkdir() errors

**Solution:**

1. ✅ Dual mount shared directory
2. ✅ Auto-create structure on startup
3. ✅ Added setup commands

**Status:** ✅ Fixed - `storage:link` + directory creation now automatic!

---

**No manual intervention needed** - everything handles automatically on container startup! 🚀
