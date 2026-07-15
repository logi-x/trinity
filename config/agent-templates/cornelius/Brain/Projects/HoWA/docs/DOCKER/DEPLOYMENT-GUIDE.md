---
title: "Production Deployment Guide"
date: "2026-04-25"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

# Production Deployment Guide

Complete guide for deploying HOWA to production with the Docker setup.

## Table of Contents

- [Pre-Deployment](#pre-deployment)
- [Initial Deployment](#initial-deployment)
- [Post-Deployment](#post-deployment)
- [Common Issues](#common-issues)
- [Maintenance](#maintenance)

## Pre-Deployment

### 1. Server Requirements

- **OS**: Ubuntu 20.04 LTS or later (recommended)
- **CPU**: 4+ cores
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 50GB+ SSD
- **Docker**: 20.10+
- **Docker Compose**: 2.0+

### 2. Install Prerequisites

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin

# Add your user to docker group (optional)
sudo usermod -aG docker $USER
```

### 3. Setup Domain & SSL

```bash
# Install Certbot
sudo apt install certbot

# Get SSL certificates
sudo certbot certonly --standalone -d howa.edu.sa \
  -d core.howa.edu.sa \
  -d api.howa.edu.sa \
  -d socket.howa.edu.sa

# Setup auto-renewal
sudo systemctl enable certbot.timer
```

### 4. Configure Firewall

```bash
# Enable UFW
sudo ufw enable

# Allow necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 3306/tcp  # MySQL (if external access needed)

# Check status
sudo ufw status
```

## Initial Deployment

### Step 1: Clone Repository

```bash
cd /home/logix/howal
sudo git clone https://github.com/your-org/howa.git
sudo chown -R $USER:$USER howa
cd howa
```

### Step 2: Configure Environment

```bash
# Copy environment templates
cp docker/production/.env.example docker/production/.env

# Edit with production values
nano docker/production/.env
```

**Required settings:**

```bash
# Database (use strong passwords!)
MYSQL_ROOT_PASSWORD=your_secure_root_password_here
MYSQL_DATABASE=howa
MYSQL_USER=howa
MYSQL_PASSWORD=your_secure_db_password_here

# Redis
REDIS_PASSWORD=your_secure_redis_password_here

# Application
APP_ENV=production
APP_DEBUG=false
```

### Step 3: Create Docker Network

```bash
docker network create howa-shared-network
```

### Step 4: Start Data Services

```bash
cd docker/development/data
docker-compose up -d

# Wait for MySQL to initialize (check logs)
docker-compose logs -f mysql
# Wait until you see "ready for connections"
```

### Step 5: Build Production Images

```bash
cd ../../production
docker-compose build --no-cache
```

This will take 10-20 minutes depending on server specs.

### Step 6: Start Production Services

```bash
docker-compose up -d
```

### Step 7: Run Migrations

```bash
# Admin app
docker-compose exec howa-prod-core php artisan migrate --force --seed

# Client app
docker-compose exec howa-prod-app php artisan migrate --force --seed
```

### Step 8: Fix Shared Storage Permissions

**CRITICAL:** This prevents permission conflicts between containers.

```bash
cd /home/logix/howa
./docker/scripts/fix-shared-storage-permissions.sh
```

Or using Make:

```bash
make fix-shared-storage
```

See [SHARED-STORAGE-FIX.md](SHARED-STORAGE-FIX.md) for details.

### Step 9: Verify Health

```bash
# Check all services are healthy
docker-compose ps

# Run health check
./docker/scripts/monitor-health.sh

# Check logs for errors
docker-compose logs --tail=100
```

## Post-Deployment

### 1. Setup Monitoring

**Health Monitoring (Cron):**

```bash
# Add to crontab
crontab -e

# Add this line (check every 5 minutes)
*/5 * * * * /home/logix/howa/docker/scripts/monitor-health.sh --email admin@howa.edu.sa
```

**Resource Monitoring:**

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor Docker stats
docker stats
```

### 2. Setup Backups

**Database Backup (Daily at 2 AM):**

```bash
crontab -e

# Add this line
0 2 * * * cd /home/logix/howa && make backup-db
```

**Volume Backup (Weekly on Sunday at 3 AM):**

```bash
# Add to crontab
0 3 * * 0 cd /home/logix/howa && make backup-volumes
```

**Test Restore:**

```bash
# Test that backups can be restored
docker-compose exec mysql mysql -u howa -p < backup_20231201_020000.sql
```

### 3. Setup Log Rotation

Logs are already configured with rotation (10MB × 3 files). Monitor disk usage:

```bash
# Check disk usage
df -h

# Check Docker disk usage
docker system df

# Check log sizes
du -sh /var/lib/docker/containers/*/
```

### 4. Security Hardening

**Change Default Passwords:**

```bash
# Database
docker exec -it howa-data-mysql mysql -u root -p
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_strong_password';
mysql> ALTER USER 'howa'@'%' IDENTIFIED BY 'new_strong_password';
mysql> FLUSH PRIVILEGES;
```

**Setup Fail2ban:**

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

**Review Security Checklist:**
See [SECURITY.md](SECURITY.md) for complete checklist.

### 5. Performance Optimization

**Enable Production Caches:**

```bash
# Cache config, routes, views
docker-compose exec howa-prod-core php artisan config:cache
docker-compose exec howa-prod-core php artisan route:cache
docker-compose exec howa-prod-core php artisan view:cache

docker-compose exec howa-prod-app php artisan config:cache
docker-compose exec howa-prod-app php artisan route:cache
docker-compose exec howa-prod-app php artisan view:cache
```

**Adjust Resource Limits (if needed):**

Edit `docker/production/docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: "4" # Increase if more cores available
      memory: 4G # Increase if more RAM available
```

## Common Issues

### Issue: Containers not starting

**Check logs:**

```bash
docker-compose logs [service-name]
```

**Common causes:**

- Port already in use
- Insufficient resources
- Network not created
- Environment variables missing

**Solutions:**

```bash
# Check ports
sudo lsof -i :80
sudo lsof -i :443

# Check resources
free -h
df -h

# Recreate network
docker network rm howa-shared-network
docker network create howa-shared-network

# Verify environment
cat docker/production/.env
```

### Issue: Permission errors in shared storage

**Symptoms:**

```
Error: ENOENT: no such file or directory
Error: EACCES: permission denied
```

**Solution:**

```bash
# Run the fix script
./docker/scripts/fix-shared-storage-permissions.sh

# Restart containers
docker-compose -f docker/production/docker-compose.yml restart
```

See [SHARED-STORAGE-FIX.md](SHARED-STORAGE-FIX.md) for details.

### Issue: Database connection refused

**Check:**

```bash
# Is MySQL running?
docker-compose ps mysql

# Check logs
docker-compose logs mysql

# Test connection
docker exec howa-prod-app sh -c "ping -c 3 howa-data-mysql"
```

**Solution:**

```bash
# Restart MySQL
docker-compose -f docker/development/data/docker-compose.yml restart mysql

# Wait 30 seconds, then test
docker exec howa-prod-app sh -c "php artisan migrate:status"
```

### Issue: SSL certificate errors

**Check certificate:**

```bash
ls -la /etc/letsencrypt/live/howa.edu.sa/
```

**Renew certificate:**

```bash
sudo certbot renew
docker-compose -f docker/production/docker-compose.yml restart
```

### Issue: High resource usage

**Check stats:**

```bash
docker stats

# Check individual containers
docker exec howa-prod-core ps aux
docker exec howa-prod-server ps aux
```

**Solutions:**

- Clear caches
- Restart containers
- Check for memory leaks
- Adjust resource limits

## Maintenance

### Daily Tasks

- Monitor health checks (automated)
- Review error logs
- Check disk space

```bash
# Quick health check
./docker/scripts/monitor-health.sh

# Check disk
df -h

# Check logs for errors
docker-compose logs --tail=100 --since=1h | grep -i error
```

### Weekly Tasks

- Review resource usage
- Check backup success
- Update system packages

```bash
# Resource usage
docker stats --no-stream

# Check backups
ls -lh /home/logix/howa/*backup*.tar.gz

# Update packages
sudo apt update && sudo apt upgrade -y
```

### Monthly Tasks

- Rotate logs manually (if needed)
- Review security logs
- Test backup restore
- Update Docker images

```bash
# Update images
docker-compose pull
docker-compose up -d

# Test backup
docker exec mysql mysql -u howa -p < latest_backup.sql
```

### Updating Application

```bash
# 1. Backup first!
make backup-db
make backup-volumes

# 2. Pull latest code
git pull origin main

# 3. Rebuild images
cd docker/production
docker-compose build

# 4. Stop services
docker-compose down

# 5. Start new version
docker-compose up -d

# 6. Run migrations
docker-compose exec howa-prod-core php artisan migrate --force
docker-compose exec howa-prod-app php artisan migrate --force

# 7. Clear caches
docker-compose exec howa-prod-core php artisan cache:clear
docker-compose exec howa-prod-app php artisan cache:clear

# 8. Verify health
./docker/scripts/monitor-health.sh
```

## Rollback Procedure

If something goes wrong:

```bash
# 1. Stop current version
docker-compose down

# 2. Restore backup
docker exec mysql mysql -u howa -p < backup_before_update.sql

# 3. Checkout previous version
git checkout previous-stable-tag

# 4. Rebuild and start
docker-compose build
docker-compose up -d

# 5. Verify
./docker/scripts/monitor-health.sh
```

## Support

- **Documentation**: See [README.md](README.md)
- **Security**: See [SECURITY.md](SECURITY.md)
- **Shared Storage**: See [SHARED-STORAGE-FIX.md](SHARED-STORAGE-FIX.md)
- **Contact**: <ahmed@logi-x.org>

---

**Status: Production Ready** ✅

Last Updated: 2025-01-04
