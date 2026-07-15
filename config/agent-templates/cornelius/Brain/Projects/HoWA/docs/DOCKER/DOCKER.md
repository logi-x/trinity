---
title: "Docker Setup for HOWA"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Docker Setup for HOWA

This document provides instructions for running the HOWA project using Docker for both development and production environments.

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 4GB of available RAM
- At least 20GB of available disk space

## 🏗️ Architecture

The project consists of multiple services:

- **Traefik** - Reverse proxy and load balancer
- **MySQL** - Database server (latest)
- **Redis** - Cache and session storage (latest)
- **Admin** - Laravel + Inertia admin application (PHP 8.4)
- **Client** - Laravel + Inertia client application (PHP 8.4)
- **Server** - Node.js Express API server (Node 22.14.0)
- **Vite** - Frontend development servers (dev only)

## 🚀 Quick Start

### Development Environment

1. **Copy environment files:**

```bash
# Copy Docker environment
cp docker/env-example.txt .env.docker

# Copy server environment
cp docker/server-env-example.txt apps/server/.env

# Update values in both files as needed
```

2. **Update `/etc/hosts` (local development):**

```
127.0.0.1 local-admin.howa.edu.sa
127.0.0.1 local-client.howa.edu.sa
127.0.0.1 local-server.howa.edu.sa
```

3. **Start the services:**

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f admin
docker-compose logs -f server
```

4. **Initialize the Laravel applications:**

```bash
# Admin application
docker-compose exec admin php artisan key:generate
docker-compose exec admin php artisan migrate --seed
docker-compose exec admin php artisan storage:link

# Client application
docker-compose exec client php artisan key:generate
docker-compose exec client php artisan migrate --seed
docker-compose exec client php artisan storage:link
```

5. **Access the applications:**

- Admin: <http://local-admin.howa.edu.sa>
- Client: <http://local-client.howa.edu.sa>
- Server API: <http://local-server.howa.edu.sa:3052>
- Traefik Dashboard: <http://localhost:8080>

### Production Environment

1. **Copy and configure environment:**

```bash
cp docker/env-example.txt .env.docker.prod
# Edit .env.docker.prod with secure production values
```

2. **Start production services:**

```bash
docker-compose -f docker-compose.prod.yml --env-file .env.docker.prod up -d --build
```

3. **Initialize Laravel applications:**

```bash
# Admin
docker-compose -f docker-compose.prod.yml exec admin php artisan key:generate
docker-compose -f docker-compose.prod.yml exec admin php artisan migrate --force
docker-compose -f docker-compose.prod.yml exec admin php artisan config:cache
docker-compose -f docker-compose.prod.yml exec admin php artisan route:cache
docker-compose -f docker-compose.prod.yml exec admin php artisan view:cache

# Client
docker-compose -f docker-compose.prod.yml exec client php artisan key:generate
docker-compose -f docker-compose.prod.yml exec client php artisan migrate --force
docker-compose -f docker-compose.prod.yml exec client php artisan config:cache
docker-compose -f docker-compose.prod.yml exec client php artisan route:cache
docker-compose -f docker-compose.prod.yml exec client php artisan view:cache
```

## 📦 Service Details

### Ports

**Development:**

- Traefik: 80, 443, 8080 (dashboard)
- MySQL: 3306
- Redis: 6379
- Server: 3052
- Vite Admin: 5173
- Vite Client: 5174

**Production:**

- Traefik: 80, 443
- MySQL: 3306
- Redis: 6379
- Server: 3050

### Networks

All services communicate via the `howa-shared-network` bridge network.

### Volumes

- `mysql-data` - MySQL database persistence
- `redis-data` - Redis data persistence
- `zatca-sdk` - ZATCA SDK files for the server

## 🛠️ Common Commands

### Development

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Rebuild a specific service
docker-compose up -d --build admin

# View logs
docker-compose logs -f

# Access container shell
docker-compose exec admin sh
docker-compose exec server sh

# Run Laravel commands
docker-compose exec admin php artisan migrate
docker-compose exec client php artisan queue:work

# Install PHP dependencies
docker-compose exec admin composer install

# Install Node dependencies
docker-compose exec server pnpm install
```

### Production

```bash
# Start services
docker-compose -f docker-compose.prod.yml up -d

# Stop services
docker-compose -f docker-compose.prod.yml down

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart a service
docker-compose -f docker-compose.prod.yml restart admin

# Clear Laravel caches
docker-compose -f docker-compose.prod.yml exec admin php artisan cache:clear
docker-compose -f docker-compose.prod.yml exec admin php artisan config:clear
docker-compose -f docker-compose.prod.yml exec admin php artisan route:clear
docker-compose -f docker-compose.prod.yml exec admin php artisan view:clear
```

## 🔧 Troubleshooting

### Container won't start

```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs <service-name>

# Remove and rebuild
docker-compose down -v
docker-compose up -d --build
```

### Permission issues (Laravel)

```bash
# Fix storage permissions
docker-compose exec admin chown -R www-data:www-data storage bootstrap/cache
docker-compose exec admin chmod -R 775 storage bootstrap/cache
```

### Database connection issues

```bash
# Verify MySQL is running
docker-compose exec mysql mysqladmin ping -h localhost

# Check MySQL logs
docker-compose logs mysql

# Restart MySQL
docker-compose restart mysql
```

### Redis connection issues

```bash
# Test Redis connection
docker-compose exec redis redis-cli ping

# Check Redis logs
docker-compose logs redis
```

### ZATCA SDK issues

```bash
# Check if ZATCA SDK volume is mounted
docker-compose exec server ls -la /opt/zatca-sdk

# Verify Java installation
docker-compose exec server java -version

# Copy ZATCA SDK files to volume
docker cp ./path/to/zatca-sdk/. $(docker-compose ps -q server):/opt/zatca-sdk/
```

## 🔐 Security Considerations

### Production Checklist

- [ ] Change all default passwords in `.env.docker.prod`
- [ ] Use strong, unique passwords for MySQL and Redis
- [ ] Configure SSL/TLS certificates for Traefik
- [ ] Enable firewall rules to restrict access to database ports
- [ ] Regularly update Docker images
- [ ] Monitor container logs for suspicious activity
- [ ] Backup database and volumes regularly
- [ ] Use Docker secrets for sensitive data
- [ ] Limit container resources (CPU/memory)
- [ ] Scan images for vulnerabilities

### SSL/TLS Setup

For production with SSL, update Traefik configuration to use Let's Encrypt or custom certificates.

## 📊 Monitoring

### Health Checks

All services include health checks:

```bash
# View service health
docker-compose ps

# Detailed health status
docker inspect --format='{{json .State.Health}}' <container-name>
```

### Resource Usage

```bash
# View resource usage
docker stats

# View disk usage
docker system df
```

## 🗄️ Backup & Restore

### Database Backup

```bash
# Backup MySQL
docker-compose exec mysql mysqldump -u howa -p howa > backup.sql

# Restore MySQL
docker-compose exec -T mysql mysql -u howa -p howa < backup.sql
```

### Volume Backup

```bash
# Backup volumes
docker run --rm -v howa_mysql-data:/data -v $(pwd):/backup alpine tar czf /backup/mysql-backup.tar.gz -C /data .
docker run --rm -v howa_redis-data:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup.tar.gz -C /data .
docker run --rm -v howa_zatca-sdk:/data -v $(pwd):/backup alpine tar czf /backup/zatca-backup.tar.gz -C /data .
```

## 📝 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Laravel Documentation](https://laravel.com/docs)

## 🤝 Support

For issues related to Docker setup, please create an issue in the project repository.
