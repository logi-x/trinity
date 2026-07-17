---
title: "HOWA Docker Setup"
date: "2026-04-25"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

> ↑ [[Entities/Projects/HoWA|HoWA]]

# HOWA Docker Setup

Complete Docker containerization for the HOWA education platform with development and production environments.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Development Setup](#development-setup)
- [Production Deployment](#production-deployment)
- [Services](#services)
- [Health Checks](#health-checks)
- [Resource Management](#resource-management)
- [Logging](#logging)
- [Backup & Restore](#backup--restore)
- [Troubleshooting](#troubleshooting)

## Overview

This Docker setup provides:

- **Multi-stage builds** for optimized image sizes
- **Separate development and production** environments
- **Health checks** for all services
- **Resource limits** for production stability
- **Log rotation** to prevent disk space issues
- **Traefik integration** for reverse proxy and SSL

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Traefik (Reverse Proxy)               │
│                         SSL Termination                      │
└─────────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼─────┐  ┌─────▼──────┐  ┌────▼──────┐
    │   Admin    │  │   Client   │  │  Server   │
    │   (PHP)    │  │   (PHP)    │  │  (Node)   │
    │  + Nginx   │  │  + Nginx   │  │  + ZATCA  │
    └──────┬─────┘  └─────┬──────┘  └────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼─────┐  ┌─────▼──────┐  ┌────▼──────┐
    │   MySQL    │  │   Redis    │  │  Shared   │
    │            │  │            │  │  Storage  │
    └────────────┘  └────────────┘  └───────────┘
```

### Components

- **Admin App** (howa-core): Administration panel (Laravel + Inertia + React)
- **Client App** (howa-app): Student/public interface (Laravel + Inertia + React)
- **Server** (howa-server): Node.js API server with ZATCA e-invoicing integration
- **MySQL**: Database (shared between all apps)
- **Redis**: Cache and queue backend
- **Vite** (dev only): Hot module replacement for frontend development

## Quick Start

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Traefik reverse proxy (or modify configs to use without)
- At least 4GB RAM available for containers

### Initial Setup

1. **Create the shared network:**

```bash
docker network create howa-shared-network
```

1. **Start data services (MySQL, Redis):**

```bash
cd docker/development/data
docker-compose up -d
```

1. **Start development environment:**

```bash
cd docker/development
docker-compose up -d
```

1. **Run initial setup:**

```bash
# From project root
make init
```

## Development Setup

### Environment Configuration

1. Copy environment example:

```bash
cp docker/development/.env.example docker/development/.env
```

1. Update `/etc/hosts`:

```
127.0.0.1 app.dev.howa.edu.sa
127.0.0.1 core.dev.howa.edu.sa
127.0.0.1 api.dev.howa.edu.sa
127.0.0.1 socket.dev.howa.edu.sa
```

### Starting Development

```bash
# Start all services
make up

# View logs
make logs

# Stop services
make down
```

### Development URLs

- **Client App**: <http://localhost:8000>
- **Admin Panel**: <http://localhost:8001>
- **API Server**: <http://localhost:3052>
- **WebSocket**: wss://socket.dev.howa.edu.sa
- **Traefik Dashboard**: <http://localhost:8080>

### Hot Module Replacement (HMR)

Vite dev servers run in separate containers providing HMR:

- Admin Vite: `howa-dev-core-vite` (port 5176)
- Client Vite: `howa-dev-app-vite` (port 5175)

Code changes are instantly reflected without rebuilding containers.

## Production Deployment

### Pre-deployment Checklist

- [ ] SSL certificates installed at `/etc/letsencrypt/live/howa.edu.sa/`
- [ ] Strong passwords configured in `.env`
- [ ] Database backup strategy in place
- [ ] Resource limits reviewed and adjusted
- [ ] Domain DNS configured

### Production Setup

1. **Copy and configure environment:**

```bash
cp docker/production/.env.example docker/production/.env
# Edit .env with strong passwords and production settings
```

1. **Build production images:**

```bash
make build-prod
```

1. **Start production services:**

```bash
make up-prod
```

1. **Verify health status:**

```bash
make health
```

### Production URLs

- **Client App**: <https://howa.edu.sa>
- **Admin Panel**: <https://core.howa.edu.sa>
- **API Server**: <https://api.howa.edu.sa>
- **WebSocket**: wss://socket.howa.edu.sa

## Services

### PHP Applications (Admin & Client)

**Image**: `loogix/howa-core:prod` / `loogix/howa-app:prod`

**Features**:

- PHP 8.4 FPM with Alpine Linux
- Nginx web server
- Supervisor for process management
- Queue workers with Laravel Horizon
- WebSocket server (Reverb) for real-time features

**Resource Limits** (Production):

- CPU: 2 cores (limit), 0.5 cores (reservation)
- Memory: 2GB (limit), 512MB (reservation)

### Node.js Server

**Image**: `loogix/howa-server:prod`

**Features**:

- Node.js 22 LTS
- Google Chrome for PDF generation (Puppeteer)
- ZATCA SDK for Saudi e-invoicing
- Arabic/UTF-8 locale support

**Resource Limits** (Production):

- CPU: 1.5 cores (limit), 0.25 cores (reservation)
- Memory: 1.5GB (limit), 256MB (reservation)

### MySQL Database

**Image**: `mysql:latest`

**Volumes**:

- Development: `howa-dev-db`
- Production: Bind mount recommended for backups

**Ports**:

- Development: 3312 (external)
- Production: 3306 (internal only)

### Redis Cache

**Image**: `redis:latest`

**Volumes**:

- Development: `howa-dev-cache`
- Production: Named volume or bind mount

**Ports**:

- Development: 6382 (external)
- Production: 6379 (internal only)

## Health Checks

All services include health checks to ensure reliability:

### PHP Applications

```bash
# Check PHP-FPM, Nginx, and HTTP response
pgrep -x php-fpm && pgrep -x nginx && wget --spider http://localhost/health
```

**Parameters**:

- Interval: 30s
- Timeout: 10s
- Retries: 3
- Start period: 40s

### Node.js Server

```bash
# Check HTTP endpoint
wget --spider http://localhost:3050/health
```

**Parameters**:

- Interval: 30s
- Timeout: 10s
- Retries: 3
- Start period: 30s

### Database Services

```bash
# MySQL
mysqladmin ping -h localhost

# Redis
redis-cli ping
```

### Check Health Status

```bash
# View health status of all services
docker-compose ps

# Or use make command
make health
```

## Resource Management

### Production Resource Limits

Resource limits prevent any single container from consuming all system resources:

| Service | CPU Limit | Memory Limit | CPU Reserve | Memory Reserve |
| ------- | --------- | ------------ | ----------- | -------------- |
| Admin   | 2 cores   | 2GB          | 0.5 cores   | 512MB          |
| Client  | 2 cores   | 2GB          | 0.5 cores   | 512MB          |
| Server  | 1.5 cores | 1.5GB        | 0.25 cores  | 256MB          |

### Adjusting Limits

Edit `docker-compose.yml` deploy section:

```yaml
deploy:
  resources:
    limits:
      cpus: "2"
      memory: 2G
    reservations:
      cpus: "0.5"
      memory: 512M
```

### Monitoring Resources

```bash
# Real-time resource usage
docker stats

# Or use make command
make stats
```

## Logging

### Log Configuration

All production services use JSON file driver with rotation:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m" # Maximum log file size
    max-file: "3" # Keep 3 rotated files
```

This limits logs to 30MB per container (10MB × 3 files).

### Viewing Logs

```bash
# All services
make logs

# Specific service
make logs-admin
make logs-client
make logs-server

# Follow logs in production
make logs-prod

# Supervisor logs (inside container)
docker exec howa-prod-core tail -f /var/log/supervisor/supervisord.log
```

### Log Locations

**Host** (JSON files):

```
/var/lib/docker/containers/[container-id]/[container-id]-json.log
```

**Inside containers**:

```
/var/log/supervisor/          # Supervisor logs
/var/log/nginx/               # Nginx logs (if enabled)
/app/apps/*/storage/logs/  # Laravel logs
```

## Backup & Restore

### Database Backup

```bash
# Manual backup
make backup-db

# Automated backup (schedule with cron)
0 2 * * * cd /path/to/howa && make backup-db
```

### Volume Backup

```bash
# Backup all volumes (MySQL, Redis, ZATCA SDK)
make backup-volumes
```

### Restore from Backup

```bash
# Stop services
make down-prod

# Restore database
docker-compose exec mysql mysql -u root -p howa < backup_20231201_020000.sql

# Restore volumes
docker run --rm -v howa_mysql-data:/data -v $(pwd):/backup alpine \
  tar xzf /backup/mysql-backup_20231201_020000.tar.gz -C /data

# Start services
make up-prod
```

## Troubleshooting

### Container Won't Start

1. **Check logs:**

```bash
docker-compose logs [service-name]
```

1. **Verify network:**

```bash
docker network ls | grep howa-shared-network
# If missing:
docker network create howa-shared-network
```

1. **Check resource availability:**

```bash
docker system df
```

### Permission Issues

```bash
# Fix storage permissions
make setup-storage

# Fix OAuth keys (Laravel Passport)
make fix-oauth-keys
```

### Database Connection Errors

1. **Verify MySQL is running:**

```bash
docker-compose ps mysql
```

1. **Check connectivity:**

```bash
docker exec howa-dev-app sh -c "ping -c 3 howa-data-mysql"
```

1. **Verify credentials:**

```bash
docker exec -it howa-data-mysql mysql -u howa -p
```

### SSL Certificate Issues

1. **Check certificate paths:**

```bash
ls -la /etc/letsencrypt/live/howa.edu.sa/
```

1. **Verify expiry:**

```bash
make check-ssl
```

1. **Reload after renewal:**

```bash
make reload-nginx
```

### Performance Issues

1. **Check resource usage:**

```bash
make stats
```

1. **Review container health:**

```bash
make health
```

1. **Increase resources** if needed in `docker-compose.yml`

### Clear Caches

```bash
# Laravel caches
make cache-clear

# Rebuild production caches
make cache-prod

# Full container rebuild
make down
make build
make up
```

## Maintenance

### Update Images

```bash
# Development
docker-compose pull
docker-compose up -d

# Production (requires rebuild)
make build-prod
make down-prod
make up-prod
```

### Prune Unused Resources

```bash
# Remove unused images, containers, networks
docker system prune -a

# Remove unused volumes (careful!)
docker volume prune
```

### Monitor Disk Usage

```bash
# Check Docker disk usage
docker system df

# Check log sizes
docker ps -q | xargs -I {} sh -c 'echo {} $(docker inspect --format="{{.LogPath}}" {} | xargs ls -lh)'
```

## Security Best Practices

1. **Use strong passwords** in production `.env`
2. **Keep images updated** regularly
3. **Limit exposed ports** - only expose what's necessary
4. **Enable SSL/TLS** for all external connections
5. **Use read-only volumes** where possible (`:ro`)
6. **Run containers as non-root** (already configured for Node.js server)
7. **Regular backups** - automate database and volume backups
8. **Monitor logs** for suspicious activity

## Support

For issues or questions:

- Check logs: `make logs`
- Review health status: `make health`
- Inspect containers: `docker-compose ps`
- Contact: <ahmed@logi-x.org>

## License

Proprietary - HOWA Education Platform
