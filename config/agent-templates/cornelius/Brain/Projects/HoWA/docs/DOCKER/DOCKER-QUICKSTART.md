---
title: "Docker Quick Start Guide"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Docker Quick Start Guide

Get the HOWA project running in Docker in under 5 minutes.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

## Quick Start

### 1. Run the Setup Script

```bash
./docker-start.sh
```

This interactive script will guide you through the setup process.

### 2. Or Use Makefile (Development)

```bash
# Initialize everything (first time only)
make init

# Or manually:
make build      # Build images
make up         # Start services
make install    # Install dependencies
make setup-admin   # Setup admin app
make setup-client  # Setup client app
```

### 3. Access Applications

Add to `/etc/hosts`:

```
127.0.0.1 local-admin.howa.edu.sa
127.0.0.1 local-client.howa.edu.sa
127.0.0.1 local-server.howa.edu.sa
```

Then access:

- **Admin**: <http://local-admin.howa.edu.sa>
- **Client**: <http://local-client.howa.edu.sa>
- **Server**: <http://local-server.howa.edu.sa:3052>
- **Traefik Dashboard**: <http://localhost:8080>

## Common Commands

```bash
# View logs
make logs

# Stop services
make down

# Restart services
make restart

# Access shell
make shell-admin
make shell-client
make shell-server

# Run migrations
make migrate

# Clear caches
make cache-clear

# Run tests
make test
```

## Environment Setup

### Development

1. Copy environment files:

```bash
cp docker/env-example.txt .env.docker
cp docker/server-env-example.txt apps/server/.env
```

2. Update values as needed

### Production

1. Copy environment file:

```bash
cp docker/env-example.txt .env.docker.prod
```

2. **Important**: Update all passwords with secure values

3. Run:

```bash
make build-prod
make up-prod
```

## Services

| Service     | Port (Dev)       | Port (Prod)      | Description   |
| ----------- | ---------------- | ---------------- | ------------- |
| Traefik     | 80, 443, 8080    | 80, 443          | Reverse proxy |
| MySQL       | 3306             | 3306             | Database      |
| Redis       | 6379             | 6379             | Cache         |
| Admin       | 80 (via Traefik) | 80 (via Traefik) | Admin app     |
| Client      | 80 (via Traefik) | 80 (via Traefik) | Client app    |
| Server      | 3052             | 3050             | API server    |
| Vite Admin  | 5173             | -                | Dev server    |
| Vite Client | 5174             | -                | Dev server    |

## Troubleshooting

### Services won't start

```bash
docker-compose ps              # Check status
docker-compose logs <service>  # Check logs
docker-compose down -v         # Clean up
docker-compose up -d --build   # Rebuild
```

### Permission errors

```bash
docker-compose exec admin chown -R www-data:www-data storage bootstrap/cache
docker-compose exec admin chmod -R 775 storage bootstrap/cache
```

### Database connection failed

```bash
docker-compose exec mysql mysqladmin ping -h localhost
docker-compose restart mysql
```

### ZATCA SDK not found

```bash
# Copy SDK files to volume
docker cp /path/to/zatca-sdk/. $(docker-compose ps -q server):/opt/zatca-sdk/
```

## Need Help?

- Full documentation: [DOCKER.md](./DOCKER.md)
- Makefile commands: `make help`
- Docker commands: `docker-compose --help`

## Production Deployment

```bash
# 1. Set up environment
cp docker/env-example.txt .env.docker.prod
# Edit with secure passwords

# 2. Build and start
make build-prod
make up-prod

# 3. Initialize apps
docker-compose -f docker-compose.prod.yml exec admin php artisan key:generate
docker-compose -f docker-compose.prod.yml exec admin php artisan migrate --force
docker-compose -f docker-compose.prod.yml exec admin php artisan config:cache

docker-compose -f docker-compose.prod.yml exec client php artisan key:generate
docker-compose -f docker-compose.prod.yml exec client php artisan migrate --force
docker-compose -f docker-compose.prod.yml exec client php artisan config:cache
```

## File Structure

```
howa/
├── docker/                    # Docker configuration
│   ├── nginx/                # Nginx configs
│   ├── php/                  # PHP Dockerfiles
│   ├── node/                 # Node.js Dockerfiles
│   ├── mysql/                # MySQL config
│   ├── traefik/              # Traefik config
│   ├── supervisor/           # Supervisor configs
│   └── scripts/              # Helper scripts
├── docker-compose.yml        # Development compose file
├── docker-compose.prod.yml   # Production compose file
├── docker-start.sh           # Interactive setup script
├── Makefile                  # Convenient commands
└── DOCKER.md                 # Full documentation
```
