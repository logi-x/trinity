---
title: "HOWA Docker Quick Start Guide"
date: "2026-04-25"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

# HOWA Docker Quick Start Guide

Get up and running in 5 minutes.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB+ RAM available

## Development Setup (5 Steps)

### 1. Create Network

```bash
docker network create howa-shared-network
```

### 2. Start Database Services

```bash
cd docker/development/data
docker-compose up -d
```

Wait 30 seconds for MySQL to initialize.

### 3. Start Application Services

```bash
cd ../  # Back to docker/development/
docker-compose up -d
```

### 4. Install Dependencies & Setup

```bash
cd ../../  # Back to project root

# Install dependencies
docker-compose -f docker/development/docker-compose.yml exec howa-dev-core composer install
docker-compose -f docker/development/docker-compose.yml exec howa-dev-app composer install

# Generate app keys
docker-compose -f docker/development/docker-compose.yml exec howa-dev-core php artisan key:generate
docker-compose -f docker/development/docker-compose.yml exec howa-dev-app php artisan key:generate

# Run migrations
docker-compose -f docker/development/docker-compose.yml exec howa-dev-core php artisan migrate --seed
docker-compose -f docker/development/docker-compose.yml exec howa-dev-app php artisan migrate --seed

# Setup storage
docker-compose -f docker/development/docker-compose.yml exec howa-dev-core php artisan storage:link
docker-compose -f docker/development/docker-compose.yml exec howa-dev-app php artisan storage:link
```

### 5. Update /etc/hosts

```bash
sudo nano /etc/hosts
```

Add these lines:

```
127.0.0.1 app.dev.howa.edu.sa
127.0.0.1 core.dev.howa.edu.sa
127.0.0.1 api.dev.howa.edu.sa
127.0.0.1 socket.dev.howa.edu.sa
```

## Access Your Application

Open in browser:

- **Client App**: <http://localhost:8000>
- **Admin Panel**: <http://localhost:8001>
- **API Server**: <http://localhost:3052>
- **Traefik Dashboard**: <http://localhost:8080>

## Using Make Commands (Easier)

If you prefer using Makefile commands:

```bash
# From project root
make build          # Build images
make up            # Start services
make install       # Install dependencies
make setup-admin   # Setup admin app
make setup-client  # Setup client app
```

Or all at once:

```bash
make init
```

## Common Commands

```bash
# View logs
docker-compose -f docker/development/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/development/docker-compose.yml down

# Restart a service
docker-compose -f docker/development/docker-compose.yml restart howa-dev-app

# Access container shell
docker-compose -f docker/development/docker-compose.yml exec howa-dev-app sh

# Run artisan commands
docker-compose -f docker/development/docker-compose.yml exec howa-dev-app php artisan migrate

# Clear caches
docker-compose -f docker/development/docker-compose.yml exec howa-dev-app php artisan cache:clear
```

## Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
sudo lsof -i :3312
sudo lsof -i :6382

# Kill the process or change ports in docker-compose.yml
```

### Permission Errors

```bash
# Fix storage permissions
docker-compose -f docker/development/docker-compose.yml exec howa-dev-app sh -c "chmod -R 775 storage bootstrap/cache"
```

### Database Connection Refused

```bash
# Make sure MySQL container is running and healthy
docker-compose -f docker/development/data/docker-compose.yml ps
docker-compose -f docker/development/data/docker-compose.yml logs mysql

# Wait for MySQL to fully start (can take 30-60 seconds on first run)
```

### Can't Access URLs

1. Check `/etc/hosts` entries
2. Verify Traefik is running: `docker ps | grep traefik`
3. Check service status: `docker-compose -f docker/development/docker-compose.yml ps`

## Production Deployment

For production, see full [README.md](./README.md) for detailed instructions.

Quick production start:

```bash
# 1. Configure environment
cp docker/production/.env.example docker/production/.env
# Edit .env with production settings

# 2. Build and start
cd docker/production
docker-compose build
docker-compose up -d

# 3. Run migrations
docker-compose exec howa-prod-core php artisan migrate --force
docker-compose exec howa-prod-app php artisan migrate --force
```

## Next Steps

- Read full [Docker README](./README.md) for detailed documentation
- Review [Security Best Practices](./SECURITY.md)
- Customize your setup with `docker-compose.override.yml`
- Set up automated backups
- Configure monitoring

## Getting Help

- Check logs: `docker-compose logs [service]`
- Check container status: `docker-compose ps`
- View resource usage: `docker stats`
- Read documentation: See README.md files in each directory

---

Welcome to HOWA! Happy coding! 🚀
