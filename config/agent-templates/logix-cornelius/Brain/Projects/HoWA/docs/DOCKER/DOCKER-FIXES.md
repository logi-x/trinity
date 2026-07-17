---
title: "Docker Configuration Fixes"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Docker Configuration Fixes

## Issue: "Resource busy" Error

### Problem

When starting containers, you encountered:

```
sed: can't move '/etc/nginx/http.d/default.confIpLbbk' to '/etc/nginx/http.d/default.conf': Resource busy
```

### Root Cause

The entrypoint script was using `sed -i` (in-place edit) on a file mounted as a Docker volume. This doesn't work because:

- Volume-mounted files can't be replaced atomically
- `sed -i` creates a temp file and tries to move it over the original
- Docker prevents this for mounted files

### Solution Implemented

#### 1. **Created Template Files**

Instead of editing mounted configs, we now use templates:

```
docker/nginx/
├── dev.conf                    # Original (deprecated)
├── dev.template.conf          # ✅ NEW: Template with ${APP_PATH}
├── dev-ssl.conf               # Original (deprecated)
├── dev-ssl.template.conf      # ✅ NEW: SSL template
├── prod.conf                  # Used as template
└── prod-ssl.conf              # Used as template
```

#### 2. **Updated Entrypoint Script**

Changed from `sed -i` to `envsubst`:

**Before (broken):**

```bash
sed -i "s|\${APP_PATH}|${APP_PATH}|g" /etc/nginx/http.d/default.conf
```

**After (fixed):**

```bash
if [ -f /etc/nginx/templates/default.conf.template ]; then
    envsubst '${APP_PATH}' < /etc/nginx/templates/default.conf.template > /etc/nginx/http.d/default.conf
fi
```

#### 3. **Updated Dockerfiles**

**Development (`Dockerfile.dev`):**

```dockerfile
# Copy template (processed by entrypoint at runtime)
COPY docker/nginx/dev.template.conf /etc/nginx/templates/default.conf.template
```

**Production (`Dockerfile.prod`):**

```dockerfile
# Process template during build
COPY docker/nginx/prod.conf /tmp/nginx.template
RUN export APP_PATH=${APP_PATH} && \
    envsubst '${APP_PATH}' < /tmp/nginx.template > /etc/nginx/http.d/default.conf && \
    rm /tmp/nginx.template
```

#### 4. **Added gettext Package**

Installed `gettext` for the `envsubst` command:

```dockerfile
RUN apk add --no-cache \
    ...
    gettext  # ✅ Added for envsubst
```

#### 5. **Updated docker-compose.ssl.yml**

Changed to mount templates instead of final configs:

**Before:**

```yaml
volumes:
  - ./docker/nginx/dev-ssl.conf:/etc/nginx/http.d/default.conf # ❌ Mounted file
```

**After:**

```yaml
volumes:
  - ./docker/nginx/dev-ssl.template.conf:/etc/nginx/templates/default.conf.template # ✅ Template
```

#### 6. **Updated Production Compose**

Removed nginx config mounts (processed during build):

```yaml
# Note: nginx config is processed during build, not mounted
```

## How It Works Now

### Development Flow

1. **Build time:**
   - Template copied to `/etc/nginx/templates/`

2. **Container start:**
   - Entrypoint runs
   - `envsubst` replaces `${APP_PATH}` with actual value
   - Generated config written to `/etc/nginx/http.d/default.conf`
   - Nginx starts with processed config

### Production Flow

1. **Build time:**
   - Template copied to `/tmp/nginx.template`
   - `envsubst` processes template with `APP_PATH` from build arg
   - Final config written to `/etc/nginx/http.d/default.conf`
   - Template removed

2. **Container start:**
   - Config already processed
   - Nginx starts immediately

## Files Changed

### New Files

- ✅ `docker/nginx/dev.template.conf`
- ✅ `docker/nginx/dev-ssl.template.conf`

### Modified Files

- ✅ `docker/scripts/entrypoint-php.sh` - Uses envsubst instead of sed -i
- ✅ `docker/php/Dockerfile.dev` - Installs gettext, copies templates
- ✅ `docker/php/Dockerfile.prod` - Installs gettext, processes templates at build
- ✅ `docker-compose.ssl.yml` - Mounts templates instead of configs
- ✅ `docker-compose.prod.yml` - Removed nginx config mounts

## Testing

### Rebuild Images

```bash
# Development
docker-compose build client

# Production
docker-compose -f docker-compose.prod.yml build client
```

### Start Containers

```bash
# Development
docker-compose up -d client

# Development with SSL
docker-compose -f docker-compose.yml -f docker-compose.ssl.yml up -d

# Production
docker-compose -f docker-compose.prod.yml up -d
```

### Verify Nginx Config

```bash
# Check if APP_PATH was replaced correctly
docker-compose exec client cat /etc/nginx/http.d/default.conf | grep "root"

# Should see:
# root /app/apps/client/public;
# NOT:
# root /app/apps/${APP_PATH}/public;
```

## Why This Solution?

### ✅ Benefits

1. **No volume mount conflicts** - Templates can be mounted safely
2. **Runtime flexibility** - Dev configs generated on container start
3. **Build-time optimization** - Prod configs baked into image
4. **Standard tool** - `envsubst` is designed for this purpose
5. **Clean separation** - Templates vs final configs

### 🔄 Alternative Approaches Considered

**1. Don't mount nginx config:**

- ❌ Can't easily change config without rebuilding

**2. Use separate config files per app:**

- ❌ Duplicate config maintenance

**3. Use sed without -i:**

- ✅ Works but less elegant than envsubst

**4. Copy config in entrypoint:**

- ❌ More complex, doesn't solve mount issue

## Rollback Plan

If you need to revert:

1. Use old non-template configs:

```yaml
volumes:
  - ./docker/nginx/dev.conf:/etc/nginx/http.d/default.conf
```

2. Don't mount as volume, copy during build:

```dockerfile
COPY docker/nginx/dev.conf /etc/nginx/http.d/default.conf
```

## Additional Notes

- Templates use `${APP_PATH}` syntax
- `envsubst` only replaces specified variables
- Production processes templates at build time for efficiency
- Development processes templates at runtime for flexibility
- SSL templates work the same way

## Related Documentation

- `DOCKER-SSL.md` - SSL configuration guide
- `SSL-QUICK-REFERENCE.md` - Quick SSL commands
- `DOCKER.md` - Main Docker documentation

---

**Status:** ✅ Fixed and tested
**Impact:** Resolves "Resource busy" error for all services
**Migration:** Rebuild images and restart containers
