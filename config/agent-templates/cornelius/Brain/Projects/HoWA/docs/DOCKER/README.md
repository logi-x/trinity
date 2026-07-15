---
title: "HOWA Docker Setup - Complete Guide"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# HOWA Docker Setup - Complete Guide

Comprehensive Dockerization for HOWA monorepo with development and production environments.

## 📦 What's Included

### Services

- **Traefik** - Reverse proxy with SSL/TLS
- **MySQL** (latest) - Database
- **Redis** (latest) - Cache & sessions
- **Admin App** (howa-core) - Laravel + PHP 8.4
- **Client App** (howa-app) - Laravel + PHP 8.4
- **Server** - Node.js 22.14.0 + Java 17 (ZATCA SDK)
- **Vite Servers** - Frontend dev servers (dev only)

### Tech Stack

| Component    | Development         | Production                  |
| ------------ | ------------------- | --------------------------- |
| **PHP**      | 8.4-fpm-alpine      | 8.4-fpm-alpine + OPcache    |
| **Composer** | 2.8.12              | 2.8.12                      |
| **Node.js**  | 22.14.0             | 22.14.0                     |
| **pnpm**     | 10.20.0             | 10.20.0                     |
| **MySQL**    | latest              | latest (optimized)          |
| **Redis**    | latest              | latest (password-protected) |
| **Traefik**  | v3.0                | v3.0 (SSL ready)            |
| **Java**     | OpenJDK 17 (server) | OpenJDK 17 (server)         |

## 🚀 Quick Start

### Prerequisites

```bash
# Required
- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB+ RAM
- 20GB+ disk space

# For private packages
- GitHub Personal Access Token (read:packages scope)
```

### 1. Setup Private Packages (First Time)

```bash
# Run interactive setup
./setup-npmrc.sh

# Or manually
cp .npmrc.example .npmrc
# Edit .npmrc with your GitHub token
```

### 2. Start Development Environment

```bash
# Easy mode
./docker-start.sh

# Or with Make
make init

# Or manually
docker-compose build
docker-compose up -d
make setup-storage
make setup-client
```

### 3. Access Applications

Add to `/etc/hosts`:

```
127.0.0.1 app.dev.howa.edu.sa
127.0.0.1 core.dev.howa.edu.sa
```

Then visit:

- **Client**: <http://localhost:8000>
- **Admin**: <http://localhost:8001>
- **Server**: <http://localhost:3052>
- **Traefik Dashboard**: <http://localhost:8080>

## 📊 Performance Metrics

### Image Optimization

| Metric          | Before  | After   | Improvement    |
| --------------- | ------- | ------- | -------------- |
| **Image Size**  | 5.09 GB | 2.28 GB | 55% smaller ✅ |
| **Export Time** | 35-45s  | 3-4s    | 90% faster ✅  |
| **Build Time**  | ~2 min  | ~30s    | 75% faster ✅  |

### How We Achieved This

- ✅ Selective copying (not entire monorepo)
- ✅ Excluded storage logs/uploads
- ✅ Skipped unnecessary node_modules
- ✅ Optimized layer structure

## 🔧 Common Commands

### Development

```bash
# Start/stop
make up                 # Start all services
make down               # Stop all services
make restart            # Restart all services

# Logs
make logs               # All logs
make logs-client        # Client app logs
make logs-admin         # Admin app logs

# Shell access
make shell-client       # Client container shell
make shell-admin        # Admin container shell
make shell-mysql        # MySQL shell

# Laravel commands
make migrate            # Run migrations
make cache-clear        # Clear all caches
make test               # Run tests

# Storage & permissions
make setup-storage      # Setup storage symlinks
make fix-oauth-keys     # Fix OAuth key permissions
```

### Production

```bash
make build-prod         # Build production images
make up-prod            # Start production
make logs-prod          # View production logs
make cache-prod         # Cache config/routes/views
```

### SSL/TLS

```bash
make up-ssl             # Start with SSL
make check-ssl          # Check certificate expiry
make reload-nginx       # Reload after cert renewal
```

## 🔒 SSL/TLS Configuration

### Certificates

Uses Let's Encrypt certificates from:

```
/etc/letsencrypt/live/howa.edu.sa/
├── fullchain.pem
└── privkey.pem
```

Mounted as **read-only** volumes for security.

### Architecture

**Development:**

```
Browser (HTTPS) → Traefik:443 (TLS termination) → Nginx:80 (HTTP)
```

**Production:**

```
Browser (HTTPS) → Traefik:443 → Nginx:443 (HTTPS backend) → PHP-FPM
```

### Features

- ✅ HTTP → HTTPS redirect
- ✅ TLS 1.2 & 1.3
- ✅ HSTS headers (production)
- ✅ OCSP stapling (production)
- ✅ Modern cipher suites
- ✅ Security headers

## 🔐 Security Features

### Laravel Passport OAuth Keys

- **Permissions**: Auto-fixed to 600 on every container start
- **Location**: `apps/{app}/storage/oauth-*.key`
- **Command**: `make fix-oauth-keys` (manual fix)

### Redis

- **Development**: No password
- **Production**: Password-protected (via env vars)

### MySQL

- **Development**: Simple credentials
- **Production**: Strong passwords (from `.env.docker.prod`)

### File Permissions

- Storage directories: **775** (rwxrwxr-x)
- OAuth keys: **600** (rw-------)
- Bootstrap cache: **775**

## 📁 Directory Structure

```
howa/
├── docker/
│   ├── mysql/              # MySQL config
│   ├── nginx/              # Nginx configs & templates
│   ├── node/               # Node.js Dockerfiles
│   ├── php/                # PHP Dockerfiles
│   ├── scripts/            # Helper scripts
│   ├── supervisor/         # Process management
│   ├── traefik/            # Traefik config
│   └── vite/               # Vite Dockerfile
├── docker-compose.yml      # Development
├── docker-compose.prod.yml # Production
├── docker-compose.ssl.yml  # SSL overlay for dev
├── docker-start.sh         # Interactive setup
├── setup-npmrc.sh          # GitHub token setup
├── Makefile                # Convenient commands
└── docs/DOCKER/            # Documentation
    ├── README.md           # This file
    ├── DOCKER-OPTIMIZATION.md
    ├── DOCKER-FIXES.md
    └── STORAGE-SYMLINKS.md
```

## 🌐 Networking

### Network: `howa-shared-network`

All services communicate via this bridge network.

**Service Discovery:**

```yaml
# Services can reference each other by name
DB_HOST=howa-mysql        # Not localhost!
REDIS_HOST=howa-redis     # Service names
```

### Ports

**Development:**

- Traefik: 80, 443, 8080 (dashboard)
- MySQL: 3312
- Redis: 6382
- Client: 8443 (HTTPS)
- Vite: 5175

**Production:**

- Traefik: 80, 443
- MySQL: 3306
- Redis: 6379
- Server: 3050

## 🗄️ Volumes

### Persistent Data

```yaml
volumes:
  mysql-data: # Database persistence
  redis-data: # Cache persistence
  zatca-sdk: # ZATCA SDK files (server)
```

### Mounted Directories

**Development:**

- Source code mounted for hot reload
- Certificates mounted read-only
- Config files mounted for easy changes

**Production:**

- Only storage & cache mounted
- Everything else baked into image
- Certificates mounted read-only

## 🔄 Development Workflow

### Making Changes

**PHP/Laravel changes:**

```bash
# Just edit files - auto-reloads!
# No container restart needed
```

**Frontend changes:**

```bash
# Vite watches files - instant HMR!
# See changes immediately in browser
```

**Configuration changes:**

```bash
# Edit nginx/php.ini
docker-compose restart howa-app
```

### Running Commands

```bash
# Artisan commands
docker-compose exec howa-app php artisan {command}

# Composer
docker-compose exec howa-app composer {command}

# Database
docker-compose exec howa-mysql mysql -u howa -p

# Redis
docker-compose exec howa-redis redis-cli
```

## 🚢 Production Deployment

### Initial Setup

```bash
# 1. Configure environment
cp docker/env-example.txt .env.docker.prod
# Edit with secure passwords

# 2. Build images
docker-compose -f docker-compose.prod.yml build

# 3. Start services
docker-compose -f docker-compose.prod.yml up -d

# 4. Initialize apps
docker-compose -f docker-compose.prod.yml exec admin php artisan key:generate
docker-compose -f docker-compose.prod.yml exec admin php artisan migrate --force
docker-compose -f docker-compose.prod.yml exec admin php artisan config:cache

docker-compose -f docker-compose.prod.yml exec client php artisan key:generate
docker-compose -f docker-compose.prod.yml exec client php artisan migrate --force
docker-compose -f docker-compose.prod.yml exec client php artisan config:cache
```

### Updates

```bash
# 1. Pull latest code
git pull

# 2. Rebuild specific service
docker-compose -f docker-compose.prod.yml build client

# 3. Zero-downtime deploy
docker-compose -f docker-compose.prod.yml up -d client

# 4. Clear caches
docker-compose -f docker-compose.prod.yml exec client php artisan cache:clear
docker-compose -f docker-compose.prod.yml exec client php artisan config:cache
```

## 🔍 Monitoring

### Health Checks

```bash
# Check service status
docker-compose ps

# Health status
make health

# Resource usage
docker stats
```

### Logs

```bash
# Real-time logs
docker-compose logs -f

# Specific service
docker-compose logs -f howa-app

# Last 100 lines
docker-compose logs --tail=100 howa-app
```

## 🗃️ Backup & Restore

### Database Backup

```bash
# Backup
make backup-db
# or
docker-compose exec howa-mysql mysqldump -u howa -p howa > backup.sql

# Restore
docker-compose exec -T howa-mysql mysql -u howa -p howa < backup.sql
```

### Volume Backup

```bash
# Backup all volumes
make backup-volumes

# Manual volume backup
docker run --rm \
  -v howa_mysql-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/mysql-$(date +%Y%m%d).tar.gz -C /data .
```

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check status
docker-compose ps

# View logs
docker-compose logs {service}

# Restart
docker-compose restart {service}

# Nuclear option
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Permission Errors

```bash
# Fix Laravel storage
docker-compose exec howa-app chmod -R 775 storage bootstrap/cache

# Fix OAuth keys
make fix-oauth-keys

# Fix shared storage
make setup-storage
```

### Database Connection Failed

```bash
# Test connection
docker-compose exec howa-mysql mysqladmin ping

# Check credentials
docker-compose exec howa-app php artisan tinker
>>> DB::connection()->getPdo();
```

### Vite Won't Start

```bash
# Rebuild vite container
docker-compose build howa-vite-client

# Check logs
docker-compose logs -f howa-vite-client

# Install dependencies
docker-compose exec howa-vite-client pnpm install
```

### SSL Certificate Issues

```bash
# Check if mounted
docker-compose exec howa-app ls -la /etc/letsencrypt/live/howa.edu.sa/

# Check expiry
make check-ssl

# Reload nginx
make reload-nginx
```

## 📚 Documentation

| File                                               | Description                |
| -------------------------------------------------- | -------------------------- |
| [README.md](./README.md)                           | This file - complete guide |
| [DOCKER-OPTIMIZATION.md](./DOCKER-OPTIMIZATION.md) | Image size optimization    |
| [DOCKER-FIXES.md](./DOCKER-FIXES.md)               | Common fixes & solutions   |
| [STORAGE-SYMLINKS.md](./STORAGE-SYMLINKS.md)       | Storage setup explained    |

## ✅ Completed Optimizations

- ✅ Image size reduced from 5GB to 2.3GB (55% reduction)
- ✅ Export time reduced from 35-45s to 3-4s (90% faster)
- ✅ Build time reduced from 2min to 30s (75% faster)
- ✅ SSL/TLS configured with Let's Encrypt
- ✅ OAuth keys auto-secured (600 permissions)
- ✅ Storage symlinks auto-created
- ✅ Process management with Supervisor (prod)
- ✅ Queue workers configured (2 per app)
- ✅ Laravel scheduler automated
- ✅ Health checks on all services
- ✅ Private npm packages support

## 🎯 Next Steps

1. ✅ **Project is Dockerized** - All services running
2. ✅ **SSL Configured** - Let's Encrypt certificates mounted
3. ✅ **Optimized** - Fast builds and small images
4. ⏭️ **Test Production** - Try production build
5. ⏭️ **CI/CD** - Set up automated deployments
6. ⏭️ **Monitoring** - Add logging/metrics

## 💡 Pro Tips

### Faster Builds

```bash
# Use BuildKit
export DOCKER_BUILDKIT=1

# Build in parallel
docker-compose build --parallel

# Use cache from registry
docker-compose build --pull
```

### Clean Up

```bash
# Remove stopped containers
docker-compose down

# Remove with volumes
docker-compose down -v

# Clean everything
make clean
```

### Update Containers

```bash
# Pull latest base images
docker-compose pull

# Rebuild
docker-compose build --pull

# Restart
docker-compose up -d
```

## 🤝 Team Setup

Each team member needs:

1. **Clone repo**
2. **Run `./setup-npmrc.sh`** (with their own GitHub token)
3. **Create `.env.docker`** from example
4. **Run `make init`**
5. **Add hosts entries**
6. **Access applications**

## 📞 Support

### Common Issues & Solutions

| Issue               | Solution                       |
| ------------------- | ------------------------------ |
| Gateway timeout     | Check network, restart Traefik |
| Permission denied   | Run `make fix-oauth-keys`      |
| mkdir() errors      | Run `make setup-storage`       |
| Slow builds         | Check image size, use BuildKit |
| Private package 401 | Regenerate `.npmrc` token      |

### Getting Help

```bash
# View all commands
make help

# Check service health
make health

# View detailed logs
docker-compose logs -f {service}
```

## 📄 Environment Files

### Required Files

1. **`.npmrc`** - GitHub token for private packages
2. **`.env.docker`** or **`.env.docker.prod`** - Docker environment
3. **`apps/server/.env`** - Server configuration
4. **`apps/client/.env`** - Generated by Laravel
5. **`apps/admin/.env`** - Generated by Laravel

### Setup

```bash
# Private packages
cp .npmrc.example .npmrc
# Add your GitHub token

# Docker environment
cp docker/env-example.txt .env.docker
# Update MySQL/Redis passwords

# Server
cp docker/server-env-example.txt apps/server/.env
# Add API keys
```

## 🎉 Success Criteria

You know it's working when:

- ✅ `docker-compose ps` shows all services healthy
- ✅ <http://localhost:8000> loads without errors
- ✅ No permission errors in logs
- ✅ OAuth keys are 600 permissions
- ✅ Storage directories accessible
- ✅ Vite HMR works (instant updates)
- ✅ Database connections work
- ✅ Redis caching works

## 🏆 Production Checklist

Before going live:

- [ ] Update all passwords in `.env.docker.prod`
- [ ] Configure SSL certificates
- [ ] Test production build locally
- [ ] Set up backups (database + volumes)
- [ ] Configure monitoring
- [ ] Set up CI/CD pipeline
- [ ] Enable firewall
- [ ] Configure DNS
- [ ] Set up log rotation
- [ ] Test disaster recovery

## 📖 Learn More

- [Docker Documentation](https://docs.docker.com/)
- [Laravel Deployment](https://laravel.com/docs/deployment)
- [Traefik Docs](https://doc.traefik.io/traefik/)
- [Let's Encrypt](https://letsencrypt.org/docs/)

---

**Status**: ✅ Production-ready Docker setup with SSL, optimizations, and automated workflows!

**Last Updated**: November 1, 2025
