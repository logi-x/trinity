---
title: "OAuth Keys Permission Fix"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# OAuth Keys Permission Fix

## Issue

Laravel Passport requires OAuth private/public keys to have restrictive permissions (600 or 660) for security reasons. The default 775 permissions are too permissive and will trigger a warning:

```
Key file "file:///app/apps/client/storage/oauth-private.key" permissions are not correct,
recommend changing to 600 or 660 instead of 775
```

## ✅ What Was Fixed

### 1. **Entrypoint Script** (`docker/scripts/entrypoint-php.sh`)

Added automatic OAuth key permission fixing on container startup:

```bash
# Fix OAuth key permissions (must be 600 for security)
if [ -f "/app/apps/${APP_PATH}/storage/oauth-private.key" ]; then
    chmod 600 /app/apps/${APP_PATH}/storage/oauth-*.key || true
    echo "OAuth keys permissions set to 600"
fi
```

### 2. **Development Dockerfile** (`docker/php/Dockerfile.dev`)

Added OAuth key permission fix during build:

```dockerfile
RUN chown -R www-data:www-data /app/apps/${APP_PATH}/storage \
    ...
    # Fix OAuth key permissions if they exist (security requirement)
    && if [ -f "/app/apps/${APP_PATH}/storage/oauth-private.key" ]; then \
        chmod 600 /app/apps/${APP_PATH}/storage/oauth-*.key; \
    fi
```

### 3. **Production Dockerfile** (`docker/php/Dockerfile.prod`)

Same fix applied for production builds.

### 4. **Host Files**

Fixed permissions on host for admin app:

```bash
chmod 600 /home/logix/howa/apps/admin/storage/oauth-*.key
chmod 600 /home/logix/howa/apps/client/storage/oauth-*.key
```

## 🔒 Security Explanation

### Why 600 Permissions?

- **600 = -rw-------** (read/write for owner only)
- Private keys should NEVER be readable by others
- Prevents unauthorized access to encryption keys
- Laravel Passport enforces this for security compliance

### Permission Breakdown

| Permission | Octal     | Meaning                                   |
| ---------- | --------- | ----------------------------------------- |
| **600** ✅ | rw------- | Owner can read/write (secure)             |
| **660** ✅ | rw-rw---- | Owner + group can read/write (acceptable) |
| **775** ❌ | rwxrwxr-x | Everyone can read (INSECURE)              |

## 📁 Affected Files

- `apps/admin/storage/oauth-private.key` - RSA private key
- `apps/admin/storage/oauth-public.key` - RSA public key
- `apps/client/storage/oauth-private.key` - RSA private key
- `apps/client/storage/oauth-public.key` - RSA public key

## 🔧 Manual Fix (If Needed)

### Inside Container

```bash
# Fix for specific app
docker-compose exec howa-app sh -c "chmod 600 /app/apps/client/storage/oauth-*.key"

# Verify
docker-compose exec howa-app ls -la /app/apps/client/storage/ | grep oauth
```

### On Host (if owned by your user)

```bash
chmod 600 apps/admin/storage/oauth-*.key
chmod 600 apps/client/storage/oauth-*.key
```

## 🔄 Regenerating OAuth Keys

If you need to regenerate OAuth keys:

### For Passport (OAuth 2.0)

```bash
# Generate new keys
docker-compose exec howa-app php artisan passport:keys --force

# Keys will automatically get correct permissions via entrypoint script on next restart
docker-compose restart howa-app
```

### For Sanctum (if used instead)

Sanctum doesn't use RSA keys - it uses database tokens, so this doesn't apply.

## ✅ Verification

Check if permissions are correct:

```bash
# Inside container
docker-compose exec howa-app ls -la /app/apps/client/storage/ | grep oauth

# Should show:
# -rw-------  1 www-data www-data  3322 oauth-private.key
# -rw-------  1 www-data www-data   812 oauth-public.key
```

## 🚀 Testing

After the fix, verify Laravel Passport works:

```bash
# Check if the warning is gone
docker-compose logs howa-app | grep oauth

# Test OAuth endpoints (if you have them)
curl -I http://localhost:8000/oauth/authorize
```

## 📊 Implementation Status

| File                | Status     | Description           |
| ------------------- | ---------- | --------------------- |
| `entrypoint-php.sh` | ✅ Updated | Auto-fixes on startup |
| `Dockerfile.dev`    | ✅ Updated | Fixes during build    |
| `Dockerfile.prod`   | ✅ Updated | Fixes during build    |
| Admin keys          | ✅ Fixed   | 600 permissions set   |
| Client keys         | ✅ Fixed   | 600 permissions set   |

## 🐛 Troubleshooting

### Still Getting Warning?

1. **Restart container:**

   ```bash
   docker-compose restart howa-app
   ```

2. **Check actual permissions:**

   ```bash
   docker-compose exec howa-app stat /app/apps/client/storage/oauth-private.key
   ```

3. **Manually fix:**

   ```bash
   docker-compose exec howa-app sh -c "chmod 600 /app/apps/client/storage/oauth-*.key"
   ```

### Keys Don't Exist?

Generate them first:

```bash
docker-compose exec howa-app php artisan passport:install
```

### Permission Denied When Changing?

This is normal if files are owned by www-data and you're trying to change from host. The entrypoint script handles it automatically.

## 🔐 Security Best Practices

1. ✅ **Never commit OAuth keys to git** - Add to `.gitignore`
2. ✅ **Use different keys per environment** - Dev vs Production
3. ✅ **Rotate keys periodically** - Security best practice
4. ✅ **Backup keys securely** - Store encrypted backups
5. ✅ **Monitor key access** - Log OAuth key usage

## 📝 Related Laravel Commands

```bash
# List Passport clients
docker-compose exec howa-app php artisan passport:client

# Create new client
docker-compose exec howa-app php artisan passport:client --password

# Clear cached config after key changes
docker-compose exec howa-app php artisan config:clear
```

## 🎯 Summary

The OAuth key permissions issue is now **automatically handled** in three places:

1. **Container startup** - Entrypoint script checks and fixes
2. **Development build** - Dockerfile sets correct permissions
3. **Production build** - Dockerfile sets correct permissions

**No manual intervention needed** - keys will always have secure 600 permissions! 🔒

---

**Last Updated:** November 1, 2025  
**Applies To:** Laravel Passport OAuth 2.0 keys
