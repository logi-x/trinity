---
title: "SSL/TLS Configuration for Docker"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# SSL/TLS Configuration for Docker

This guide explains how to use Let's Encrypt SSL certificates with your Dockerized HOWA application.

## 📋 Prerequisites

1. **Let's Encrypt certificates** already obtained on your host machine
2. Certificates located at: `/etc/letsencrypt/live/howa.edu.sa/`
3. Valid DNS records pointing to your server

## 🔒 Certificate Files

Your Let's Encrypt certificates should be at:

```
/etc/letsencrypt/live/howa.edu.sa/
├── fullchain.pem    # Full certificate chain
├── privkey.pem      # Private key
├── cert.pem         # Certificate only
└── chain.pem        # CA chain
```

And the actual files (symlinks) point to:

```
/etc/letsencrypt/archive/howa.edu.sa/
├── fullchain1.pem
├── privkey1.pem
├── cert1.pem
└── chain1.pem
```

## 🚀 Quick Start

### Development with SSL

Use the SSL overlay file:

```bash
# Start with SSL enabled
docker-compose -f docker-compose.yml -f docker-compose.ssl.yml up -d

# View logs
docker-compose -f docker-compose.yml -f docker-compose.ssl.yml logs -f

# Stop
docker-compose -f docker-compose.yml -f docker-compose.ssl.yml down
```

### Production with SSL

Production compose file already includes SSL by default:

```bash
# Start production (SSL auto-enabled)
docker-compose -f docker-compose.prod.yml up -d

# Restart to apply certificate changes
docker-compose -f docker-compose.prod.yml restart admin client
```

## 📁 Files Created

### Nginx Configurations

1. **`docker/nginx/dev-ssl.conf`** - Development SSL config
   - HTTP to HTTPS redirect
   - Basic SSL settings
   - For testing with real certificates

2. **`docker/nginx/prod-ssl.conf`** - Production SSL config
   - HTTP to HTTPS redirect
   - Modern SSL/TLS protocols (TLS 1.2 & 1.3)
   - HSTS headers
   - OCSP stapling
   - Security headers
   - Optimized caching

### Docker Compose Files

1. **`docker-compose.ssl.yml`** - Development SSL overlay
   - Mounts certificates (read-only)
   - Uses SSL nginx config
   - Exposes HTTPS ports

2. **`docker-compose.prod.yml`** - Production (updated)
   - SSL enabled by default
   - Mounts certificates
   - Traefik configured for HTTPS backend

## 🔧 Configuration Details

### Volume Mounts (Read-Only)

Both configurations mount certificates as **read-only** for security:

```yaml
volumes:
  # Live certificates (symlinks)
  - /etc/letsencrypt/live/howa.edu.sa:/etc/letsencrypt/live/howa.edu.sa:ro
  # Archive (actual files)
  - /etc/letsencrypt/archive/howa.edu.sa:/etc/letsencrypt/archive/howa.edu.sa:ro
```

### Why Mount Both Directories?

- `/etc/letsencrypt/live/` contains **symlinks** to current certificates
- `/etc/letsencrypt/archive/` contains the **actual certificate files**
- Mounting both ensures symlinks work correctly inside containers

### Nginx SSL Configuration

```nginx
server {
    listen 443 ssl http2;

    ssl_certificate /etc/letsencrypt/live/howa.edu.sa/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/howa.edu.sa/privkey.pem;

    # Modern SSL protocols
    ssl_protocols TLSv1.2 TLSv1.3;

    # Security headers
    add_header Strict-Transport-Security "max-age=63072000" always;
}
```

## 🌐 Traefik Integration

### Development

When using `docker-compose.ssl.yml`, Traefik routes to nginx HTTPS:

```yaml
labels:
  # HTTP route
  - "traefik.http.routers.client-dev.entrypoints=web"
  - "traefik.http.services.client-dev.loadbalancer.server.port=80"

  # HTTPS route
  - "traefik.http.routers.client-dev-secure.entrypoints=websecure"
  - "traefik.http.services.client-dev-secure.loadbalancer.server.port=443"
  - "traefik.http.services.client-dev-secure.loadbalancer.server.scheme=https"
```

### Production

Traefik terminates TLS, then forwards to nginx HTTPS backend:

```yaml
labels:
  - "traefik.http.services.client-prod.loadbalancer.server.port=443"
  - "traefik.http.services.client-prod.loadbalancer.server.scheme=https"
```

## 🔄 Certificate Renewal

### Automatic Renewal with Certbot

1. **Set up certbot renewal** on host:

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot auto-renews via cron/systemd timer
sudo systemctl status certbot.timer
```

2. **Reload nginx after renewal:**

```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.ssl.yml restart admin client

# Production
docker-compose -f docker-compose.prod.yml exec admin nginx -s reload
docker-compose -f docker-compose.prod.yml exec client nginx -s reload
```

3. **Automate with post-renewal hook:**

Create `/etc/letsencrypt/renewal-hooks/post/reload-docker-nginx.sh`:

```bash
#!/bin/bash
# Reload nginx in Docker containers after certificate renewal

cd /home/logix/howa

# Reload production containers
docker-compose -f docker-compose.prod.yml exec -T admin nginx -s reload
docker-compose -f docker-compose.prod.yml exec -T client nginx -s reload

echo "Docker nginx reloaded with new certificates"
```

Make it executable:

```bash
sudo chmod +x /etc/letsencrypt/renewal-hooks/post/reload-docker-nginx.sh
```

## 🔍 Verification

### Check Certificate Inside Container

```bash
# View certificate details
docker-compose exec admin openssl x509 -in /etc/letsencrypt/live/howa.edu.sa/fullchain.pem -text -noout

# Check certificate expiry
docker-compose exec admin openssl x509 -in /etc/letsencrypt/live/howa.edu.sa/fullchain.pem -enddate -noout

# Verify private key matches certificate
docker-compose exec admin openssl x509 -noout -modulus -in /etc/letsencrypt/live/howa.edu.sa/fullchain.pem | openssl md5
docker-compose exec admin openssl rsa -noout -modulus -in /etc/letsencrypt/live/howa.edu.sa/privkey.pem | openssl md5
```

### Test SSL Configuration

```bash
# Test with curl
curl -I https://howa.edu.sa

# Test SSL with openssl
openssl s_client -connect howa.edu.sa:443 -servername howa.edu.sa

# Check SSL rating (external tool)
# https://www.ssllabs.com/ssltest/analyze.html?d=howa.edu.sa
```

## 🛡️ Security Best Practices

### ✅ Implemented

- ✅ **Read-only mounts** - Certificates mounted as `:ro`
- ✅ **Modern protocols** - TLS 1.2 and 1.3 only
- ✅ **HSTS headers** - Force HTTPS for 2 years
- ✅ **OCSP stapling** - Faster certificate validation
- ✅ **HTTP to HTTPS redirect** - Automatic upgrade
- ✅ **Strong ciphers** - Modern encryption algorithms
- ✅ **Security headers** - X-Frame-Options, X-Content-Type-Options, etc.

### 🔒 Additional Recommendations

1. **Set proper file permissions on host:**

```bash
sudo chmod 600 /etc/letsencrypt/live/howa.edu.sa/privkey.pem
sudo chown root:root /etc/letsencrypt/live/howa.edu.sa/privkey.pem
```

2. **Monitor certificate expiration:**

```bash
# Add to cron
0 0 * * * certbot renew --quiet --post-hook "cd /home/logix/howa && docker-compose -f docker-compose.prod.yml restart admin client"
```

3. **Enable firewall:**

```bash
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

## 🐛 Troubleshooting

### Certificate not found

```bash
# Check if certificates exist on host
ls -la /etc/letsencrypt/live/howa.edu.sa/

# Check inside container
docker-compose exec admin ls -la /etc/letsencrypt/live/howa.edu.sa/
```

### Nginx fails to start

```bash
# Check nginx config
docker-compose exec admin nginx -t

# View nginx logs
docker-compose logs admin
```

### Certificate expired

```bash
# Renew immediately
sudo certbot renew --force-renewal

# Restart containers
docker-compose -f docker-compose.prod.yml restart admin client
```

### Permission denied

```bash
# Verify container can read certificates
docker-compose exec admin cat /etc/letsencrypt/live/howa.edu.sa/fullchain.pem

# If fails, check host permissions
sudo ls -la /etc/letsencrypt/live/howa.edu.sa/
sudo ls -la /etc/letsencrypt/archive/howa.edu.sa/
```

### Mixed content warnings

Ensure all assets are loaded over HTTPS:

- Update `APP_URL` in `.env` to `https://...`
- Check for hardcoded `http://` URLs in code
- Enable `APP_FORCE_HTTPS=true` if available

## 📊 SSL Configuration Comparison

| Feature               | dev-ssl.conf | prod-ssl.conf     |
| --------------------- | ------------ | ----------------- |
| HTTP → HTTPS redirect | ✅           | ✅                |
| TLS 1.2/1.3           | ✅           | ✅                |
| HSTS                  | ❌           | ✅ (2 years)      |
| OCSP Stapling         | ❌           | ✅                |
| Security Headers      | Basic        | Full              |
| Session Cache         | 10m          | 1d                |
| Session Tickets       | On           | Off (more secure) |

## 🔄 Switching Configurations

### Switch to Non-SSL (Development)

```bash
# Use base docker-compose.yml only
docker-compose up -d

# Certificates won't be mounted
```

### Switch to SSL (Development)

```bash
# Use SSL overlay
docker-compose -f docker-compose.yml -f docker-compose.ssl.yml up -d
```

### Production (Always SSL)

```bash
# SSL is default in production
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 Additional Resources

- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)
- [Certbot Documentation](https://certbot.eff.org/docs/)

## 🎯 Quick Commands Reference

```bash
# Development with SSL
docker-compose -f docker-compose.yml -f docker-compose.ssl.yml up -d

# Production (SSL by default)
docker-compose -f docker-compose.prod.yml up -d

# Reload nginx after cert renewal
docker-compose -f docker-compose.prod.yml exec admin nginx -s reload
docker-compose -f docker-compose.prod.yml exec client nginx -s reload

# Check certificate expiry
docker-compose exec admin openssl x509 -enddate -noout \
  -in /etc/letsencrypt/live/howa.edu.sa/fullchain.pem

# Test SSL
curl -I https://howa.edu.sa
```

---

**Note:** The production compose file (`docker-compose.prod.yml`) now has SSL enabled by default. You don't need any additional overlay files for production!
