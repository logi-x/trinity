---
title: "SSL Quick Reference"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# SSL Quick Reference

## ✅ What Was Done

1. ✅ **Created SSL nginx configs** - `docker/nginx/dev-ssl.conf` & `prod-ssl.conf`
2. ✅ **Updated production** - `docker-compose.prod.yml` now uses SSL by default
3. ✅ **Created SSL overlay** - `docker-compose.ssl.yml` for development
4. ✅ **Mounted certificates** - Read-only from `/etc/letsencrypt/`
5. ✅ **Updated Traefik labels** - Routes to HTTPS backends
6. ✅ **Added Makefile commands** - Easy SSL management

## 🚀 Quick Commands

### Development

```bash
# Start with SSL
make up-ssl
# or
docker-compose -f docker-compose.yml -f docker-compose.ssl.yml up -d

# Access
https://local-admin.howa.edu.sa
http://localhost:8000

# Stop
make down-ssl
```

### Production

```bash
# Start (SSL enabled by default)
docker-compose -f docker-compose.prod.yml up -d

# Reload nginx after cert renewal
make reload-nginx
# or
docker-compose -f docker-compose.prod.yml exec admin nginx -s reload
docker-compose -f docker-compose.prod.yml exec client nginx -s reload
```

### Certificate Management

```bash
# Check expiry
make check-ssl

# Renew certificates (on host)
sudo certbot renew

# Reload nginx after renewal
make reload-nginx
```

## 📁 Certificate Locations

**On Host:**

```
/etc/letsencrypt/live/howa.edu.sa/
├── fullchain.pem (certificate + chain)
└── privkey.pem   (private key)
```

**Mounted in Containers:**

```
/etc/letsencrypt/live/howa.edu.sa/     (read-only)
/etc/letsencrypt/archive/howa.edu.sa/  (read-only)
```

## 🔧 Configuration Files

| File                         | Purpose                      |
| ---------------------------- | ---------------------------- |
| `docker/nginx/dev-ssl.conf`  | Dev SSL config               |
| `docker/nginx/prod-ssl.conf` | Prod SSL config (HSTS, OCSP) |
| `docker-compose.ssl.yml`     | Dev SSL overlay              |
| `docker-compose.prod.yml`    | Prod with SSL (updated)      |

## 🔒 Security Features

### Production (prod-ssl.conf)

- ✅ HTTP → HTTPS redirect
- ✅ TLS 1.2 & 1.3 only
- ✅ HSTS (2 years)
- ✅ OCSP stapling
- ✅ Modern ciphers
- ✅ Security headers

### Development (dev-ssl.conf)

- ✅ HTTP → HTTPS redirect
- ✅ TLS 1.2 & 1.3
- ✅ Basic SSL settings

## 🔄 After Certificate Renewal

### Automatic (Recommended)

Create `/etc/letsencrypt/renewal-hooks/post/reload-docker-nginx.sh`:

```bash
#!/bin/bash
cd /home/logix/howa
docker-compose -f docker-compose.prod.yml exec -T admin nginx -s reload
docker-compose -f docker-compose.prod.yml exec -T client nginx -s reload
```

```bash
sudo chmod +x /etc/letsencrypt/renewal-hooks/post/reload-docker-nginx.sh
```

### Manual

```bash
# Test renewal
sudo certbot renew --dry-run

# Actual renewal
sudo certbot renew

# Reload nginx
make reload-nginx
```

## 🐛 Troubleshooting

### Nginx won't start

```bash
# Check config
docker-compose exec admin nginx -t

# Check if certs exist
docker-compose exec admin ls -la /etc/letsencrypt/live/howa.edu.sa/

# View logs
docker-compose logs admin
```

### Certificate not found

```bash
# On host
ls -la /etc/letsencrypt/live/howa.edu.sa/

# Check permissions
sudo ls -la /etc/letsencrypt/archive/howa.edu.sa/
```

### Browser shows "Not Secure"

1. Clear browser cache
2. Check certificate expiry: `make check-ssl`
3. Verify APP_URL in `.env` is `https://...`
4. Check for mixed content warnings in browser console

## 📊 Port Configuration

| Service         | HTTP             | HTTPS                 |
| --------------- | ---------------- | --------------------- |
| **Development** |
| Admin           | 80 (Traefik)     | 443 (Traefik)         |
| Client          | 80 (Traefik)     | 443 (Traefik)         |
| **Production**  |
| Admin           | Redirect → HTTPS | 443 (nginx) → Traefik |
| Client          | Redirect → HTTPS | 443 (nginx) → Traefik |

## 🔗 Traefik → Nginx Flow

**Production:**

```
Browser → Traefik:443 (HTTPS) → Nginx:443 (HTTPS) → PHP-FPM
         └─ TLS termination   └─ SSL backend
```

**Why double HTTPS?**

- End-to-end encryption
- Traefik validates client requests
- Nginx handles application SSL

## ✅ Verification Checklist

- [ ] Certificates exist at `/etc/letsencrypt/live/howa.edu.sa/`
- [ ] Both `fullchain.pem` and `privkey.pem` are present
- [ ] Permissions are correct (readable by Docker)
- [ ] DNS points to your server
- [ ] Firewall allows ports 80 and 443
- [ ] Containers started successfully
- [ ] HTTPS works in browser
- [ ] HTTP redirects to HTTPS
- [ ] No certificate warnings

## 🆘 Need Help?

See full documentation:

- **Detailed guide:** `DOCKER-SSL.md`
- **SSL test:** <https://www.ssllabs.com/ssltest/analyze.html?d=howa.edu.sa>
- **Certificate details:** `make check-ssl`

## 📞 Emergency Commands

```bash
# If something breaks, revert to non-SSL
docker-compose up -d  # Without SSL overlay

# Or stop everything
docker-compose down
docker-compose -f docker-compose.prod.yml down

# Check what's running
docker-compose ps
```

---

**✨ Ready to go!** Your Docker setup now supports SSL with Let's Encrypt certificates mounted as read-only volumes.
