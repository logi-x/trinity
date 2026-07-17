---
title: "Shared Storage Permission Fix"
date: "2026-04-25"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

# Shared Storage Permission Fix

## Problem Statement

The HOWA platform has three containers that need to read/write shared files:

- **howa-prod-core** (Admin app) - Runs as `www-data` (uid:82, gid:82)
- **howa-prod-app** (Client app) - Runs as `www-data` (uid:82, gid:82)
- **howa-prod-server** (Node.js API) - Runs as `node` (uid:1000, gid:1000)

All three containers mount the same shared storage volume:

```
/home/logix/howa/apps/shared/s → /app/apps/shared/s
```

**The Issue:**
When different containers create files, they use their own user IDs:

- PHP creates files as `82:82` (www-data:www-data)
- Node.js creates files as `1000:1000` (node:node)

This causes permission errors like:

```
Error: ENOENT: no such file or directory
Error: EACCES: permission denied
```

## The Solution

Use a **shared group** (gid:82) that both PHP and Node.js belong to, combined with:

1. **Setgid bit** on directories (2775) - new files inherit the group
2. **Umask 0002** - new files are created with group-write permissions

### Architecture

```
┌─────────────────────────────────────────────────────┐
│          Shared Storage Volume                      │
│     /app/apps/shared/s                     │
│                                                      │
│  Ownership: www-data:shared-storage (82:82)         │
│  Dirs: 2775 (drwxrwsr-x) - setgid bit              │
│  Files: 664 (rw-rw-r--) - group writable           │
└─────────────────────────────────────────────────────┘
           │                    │                    │
           │                    │                    │
    ┌──────▼──────┐      ┌──────▼──────┐     ┌──────▼──────┐
    │ Admin (PHP) │      │Client (PHP) │     │Server (Node)│
    │             │      │             │     │             │
    │ User: 82    │      │ User: 82    │     │ User: 1000  │
    │ Groups: 82  │      │ Groups: 82  │     │ Groups: 1000│
    │             │      │             │     │         82  │
    │ Umask: 0002 │      │ Umask: 0002 │     │ Umask: 0002 │
    └─────────────┘      └─────────────┘     └─────────────┘
```

### How It Works

1. **Shared Group (gid:82)**
   - PHP containers: `www-data` is uid:82, gid:82
   - Node.js container: `node` user is added to group 82

2. **Setgid Bit (2775 on directories)**
   - When a file is created in a setgid directory, it inherits the directory's group
   - Even if Node.js (uid:1000) creates a file, it gets group 82

3. **Umask 0002**
   - New files are created with 664 permissions (rw-rw-r--)
   - Group members can read and write
   - Others can only read

4. **Result**
   - PHP creates: `-rw-rw-r-- 82 82 file.xml` ✅
   - Node creates: `-rw-rw-r-- 1000 82 file.xml` ✅
   - Both can read/write because they share group 82!

## Implementation

### 1. Node.js Dockerfile

```dockerfile
# Create shared group (gid 82) for inter-container file access
RUN groupadd -g 82 shared-storage 2>/dev/null || true \
    && usermod -aG shared-storage node
```

### 2. PHP Entrypoint Script

```bash
# Create shared-storage group if it doesn't exist
if ! getent group shared-storage >/dev/null 2>&1; then
    addgroup -g 82 shared-storage 2>/dev/null || true
fi

# Add www-data to shared-storage group
addgroup www-data shared-storage 2>/dev/null || true

# Set ownership to www-data:shared-storage
chown -R www-data:shared-storage /app/apps/shared/s

# Set permissions with setgid bit
find /app/apps/shared/s -type d -exec chmod 2775 {} \;
find /app/apps/shared/s -type f -exec chmod 664 {} \;

# Set umask for PHP-FPM
echo "umask = 0002" >> /usr/local/etc/php-fpm.d/zz-docker.conf
```

### 3. Supervisor Config (Node.js)

```ini
[program:node-server]
command=node /app/apps/server/index.js
user=node
umask=0002  # Critical: ensures group-writable files
```

## Fixing Existing Files

### Quick Fix (On Host)

```bash
# Run the automated fix script
cd /home/logix/howa
./docker/scripts/fix-shared-storage-permissions.sh

# Or manually:
sudo chown -R 82:82 apps/shared/s
sudo find apps/shared/s -type d -exec chmod 2775 {} \;
sudo find apps/shared/s -type f -exec chmod 664 {} \;
```

### Inside Containers

**PHP Containers:**

```bash
docker exec howa-prod-core sh -c "
  chown -R www-data:shared-storage /app/apps/shared/s
  find /app/apps/shared/s -type d -exec chmod 2775 {} \;
  find /app/apps/shared/s -type f -exec chmod 664 {} \;
"
```

**Or restart to apply entrypoint script:**

```bash
docker-compose -f docker/production/docker-compose.yml restart
```

## Verification

### Check Permissions

```bash
# On host
ls -la /home/logix/howa/apps/shared/s/credit-note/

# Inside container
docker exec howa-prod-server ls -la /app/apps/shared/s/credit-note/
```

**Expected output:**

```
drwxrwsr-x 2 82   shared-storage 4096 Nov 4 12:30 320/
drwxrwsr-x 2 82   shared-storage 4096 Nov 4 12:16 995/
-rw-rw-r-- 1 82   shared-storage 1234 Nov 4 12:30 file.xml
-rw-rw-r-- 1 1000 shared-storage 5678 Nov 4 12:31 file.signed.xml
```

### Check Group Membership

**PHP Container:**

```bash
docker exec howa-prod-core sh -c "id www-data"
# Expected: uid=82(www-data) gid=82(www-data) groups=82(www-data),82(shared-storage)
```

**Node.js Container:**

```bash
docker exec howa-prod-server sh -c "id node"
# Expected: uid=1000(node) gid=1000(node) groups=1000(node),82(shared-storage)
```

### Test File Creation

**From PHP:**

```bash
docker exec howa-prod-core sh -c "
  touch /app/apps/shared/s/test-php.txt
  ls -la /app/apps/shared/s/test-php.txt
"
# Expected: -rw-rw-r-- 1 82 82 0 ... test-php.txt
```

**From Node.js:**

```bash
docker exec howa-prod-server sh -c "
  touch /app/apps/shared/s/test-node.txt
  ls -la /app/apps/shared/s/test-node.txt
"
# Expected: -rw-rw-r-- 1 1000 82 0 ... test-node.txt
```

**Cross-Container Access:**

```bash
# Node.js can read/write PHP's file
docker exec howa-prod-server sh -c "cat /app/apps/shared/s/test-php.txt"

# PHP can read/write Node.js's file
docker exec howa-prod-core sh -c "cat /app/apps/shared/s/test-node.txt"
```

## Troubleshooting

### Issue: Files still have wrong permissions after restart

**Cause:** Existing files created before the fix

**Solution:**

```bash
./docker/scripts/fix-shared-storage-permissions.sh
```

### Issue: New files don't inherit group

**Cause:** Directory missing setgid bit (2775)

**Check:**

```bash
ls -ld /home/logix/howa/apps/shared/s/credit-note/
# Should show 's' in group execute: drwxrwsr-x
```

**Fix:**

```bash
find /home/logix/howa/apps/shared/s -type d -exec chmod 2775 {} \;
```

### Issue: New files are not group-writable

**Cause:** Wrong umask

**Check PHP-FPM:**

```bash
docker exec howa-prod-core sh -c "cat /usr/local/etc/php-fpm.d/zz-docker.conf | grep umask"
# Should show: umask = 0002
```

**Check Supervisor:**

```bash
docker exec howa-prod-server sh -c "cat /etc/supervisor/conf.d/server.conf | grep umask"
# Should show: umask=0002
```

**Fix:** Rebuild images or restart containers

### Issue: Node.js not in group 82

**Check:**

```bash
docker exec howa-prod-server sh -c "groups node"
# Should include: shared-storage or 82
```

**Fix:** Rebuild Node.js image

```bash
cd docker/production
docker-compose build howa-prod-server
docker-compose up -d howa-prod-server
```

## Monitoring

### Watch for Permission Issues

```bash
# Check for files not in group 82
watch -n 5 'find /home/logix/howa/apps/shared/s -not -group 82 2>/dev/null | head -20'

# Check for directories without setgid
find /home/logix/howa/apps/shared/s -type d ! -perm -2000 -ls

# Check for non-writable files
find /home/logix/howa/apps/shared/s -type f ! -perm -0660 -ls
```

### Automated Daily Check

Add to crontab:

```bash
0 2 * * * /home/logix/howa/docker/scripts/fix-shared-storage-permissions.sh >> /var/log/shared-storage-fix.log 2>&1
```

## Best Practices

1. **Always use the shared storage path** for files that need cross-container access
2. **Don't change ownership manually** - let the setgid bit handle it
3. **Keep umask = 0002** in all supervisord configs
4. **Run the fix script** after major updates or migrations
5. **Monitor logs** for ENOENT and EACCES errors
6. **Test cross-container access** when deploying new features

## Summary

| Aspect         | Value               | Purpose                         |
| -------------- | ------------------- | ------------------------------- |
| **Group**      | 82 (shared-storage) | Common group for all containers |
| **Dir Perms**  | 2775 (drwxrwsr-x)   | Setgid bit ensures inheritance  |
| **File Perms** | 664 (rw-rw-r--)     | Group members can read/write    |
| **Umask**      | 0002                | Creates group-writable files    |
| **PHP User**   | www-data (82:82)    | Primary owner                   |
| **Node User**  | node (1000:1000,82) | Member of group 82              |

---

**Status:** ✅ Fixed and Tested

For questions or issues, contact: <ahmed@logi-x.org>
