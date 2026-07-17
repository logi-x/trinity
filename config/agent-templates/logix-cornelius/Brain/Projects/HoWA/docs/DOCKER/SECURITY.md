---
title: "Docker Security Best Practices"
date: "2026-04-25"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

# Docker Security Best Practices

Security considerations and hardening guidelines for HOWA Docker deployment.

## Table of Contents

- [Image Security](#image-security)
- [Container Security](#container-security)
- [Network Security](#network-security)
- [Data Security](#data-security)
- [Access Control](#access-control)
- [Monitoring & Auditing](#monitoring--auditing)
- [Security Checklist](#security-checklist)

## Image Security

### Base Images

We use official base images from trusted sources:

- **PHP**: `php:8.4-fpm-alpine` (Alpine Linux - minimal attack surface)
- **Node.js**: `node:22.14.0-bullseye-slim` (Debian slim variant)
- **MySQL**: `mysql:latest` (Official MySQL image)
- **Redis**: `redis:latest` (Official Redis image)

### Multi-Stage Builds

Our Dockerfiles use multi-stage builds to:

- Minimize final image size
- Remove build tools and dev dependencies
- Reduce attack surface

### Vulnerability Scanning

Regularly scan images for vulnerabilities:

```bash
# Install Trivy (vulnerability scanner)
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image loogix/howa-core:prod

# Or use Docker Scout
docker scout cves loogix/howa-core:prod
```

## Container Security

### Non-Root User

The Node.js server runs as non-root user:

```dockerfile
USER node  # uid:1000
```

PHP containers run as `www-data` (uid:82) for web server compatibility.

### Read-Only Volumes

Use read-only mounts where possible:

```yaml
volumes:
  - /etc/letsencrypt/live/howa.edu.sa:/etc/letsencrypt/live/howa.edu.sa:ro
  - ./zatca-sdk/certs:/opt/zatca-sdk/Data/Certificates:ro
```

### Resource Limits

Production containers have resource limits to prevent DoS:

```yaml
deploy:
  resources:
    limits:
      cpus: "2"
      memory: 2G
```

### Disabled Functions

PHP has dangerous functions disabled in `php.ini`:

```ini
disable_functions = exec,passthru,shell_exec,system,proc_open,popen
```

### Session Security

Secure session configuration:

```ini
session.cookie_httponly = 1    # Prevent XSS access
session.cookie_secure = 1      # HTTPS only
session.use_strict_mode = 1    # Prevent session fixation
session.cookie_samesite = "Lax" # CSRF protection
```

## Network Security

### Network Isolation

Services communicate via isolated Docker network:

```yaml
networks:
  howa-shared-network:
    driver: bridge
    external: true
```

### Port Exposure

**Development**: Exposes ports for local testing
**Production**: Only essential ports exposed, behind Traefik

| Service | Dev Port | Prod Port         | Notes                |
| ------- | -------- | ----------------- | -------------------- |
| MySQL   | 3312     | Internal only     | Not exposed          |
| Redis   | 6382     | Internal only     | Not exposed          |
| Admin   | 9443     | 443 (via Traefik) | SSL required         |
| Client  | 8443     | 443 (via Traefik) | SSL required         |
| Server  | 3052     | 3050              | Can be internal only |

### SSL/TLS Configuration

All external traffic should use HTTPS:

- Traefik handles SSL termination
- Let's Encrypt certificates auto-renewal
- HTTP to HTTPS redirection

### Nginx Security Headers

Our nginx configs include security headers:

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

Consider adding additional headers for production:

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Content-Security-Policy "default-src 'self'" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

## Data Security

### Environment Variables

**NEVER commit sensitive data to git:**

1. Use `.env` files (gitignored)
2. Use Docker secrets in production
3. Rotate credentials regularly

**Critical secrets:**

- `MYSQL_ROOT_PASSWORD`
- `MYSQL_PASSWORD`
- `REDIS_PASSWORD`
- `APP_KEY` (Laravel)
- API keys and tokens

### Password Requirements

Production passwords should meet these criteria:

- Minimum 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- No dictionary words
- Use password manager

Generate strong passwords:

```bash
# OpenSSL
openssl rand -base64 32

# /dev/urandom
tr -dc A-Za-z0-9 </dev/urandom | head -c 32
```

### OAuth Keys

Laravel Passport private keys must have restricted permissions:

```bash
chmod 600 storage/oauth-*.key
```

This is handled automatically by entrypoint script, but verify:

```bash
make fix-oauth-keys
```

### Database Backups

1. **Encrypt backups** before storing:

```bash
# Backup and encrypt
mysqldump -u root -p howa | gpg -e -r your@email.com > backup.sql.gpg

# Decrypt and restore
gpg -d backup.sql.gpg | mysql -u root -p howa
```

2. **Store offsite** - Don't keep backups only on same server
3. **Test restores** regularly
4. **Automate** with cron jobs

### Shared Storage

The shared storage volume (`apps/shared/s/`) contains user uploads:

**Security measures:**

1. Validate file types before upload (Laravel does this)
2. Scan for malware if possible
3. Set proper permissions (775, owned by www-data)
4. Store outside web root where possible
5. Use CDN with virus scanning for production

## Access Control

### SSH Access

Production server should have:

- SSH key authentication only (disable passwords)
- Fail2ban installed
- Non-standard SSH port (optional)
- Regular security updates

### Docker Socket

**Never expose Docker socket to containers** unless absolutely necessary:

```yaml
# DON'T DO THIS unless required:
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

If needed, use Docker socket proxy with limited permissions.

### Supervisor Access

Supervisor runs as root inside containers to manage processes. Access is restricted to:

- Local Unix socket: `/var/run/supervisor.sock`
- Permissions: 0700 (root only)

### Database Access

1. **Remove test databases:**

```bash
docker exec -it howa-data-mysql mysql -u root -p
mysql> DROP DATABASE test;
mysql> DELETE FROM mysql.user WHERE User='';
mysql> FLUSH PRIVILEGES;
```

2. **Limit MySQL root access to localhost:**

```sql
RENAME USER 'root'@'%' TO 'root'@'localhost';
```

3. **Use principle of least privilege** - app user should only access its database

## Monitoring & Auditing

### Log Collection

Centralize logs for security monitoring:

```bash
# Export to external log aggregator
docker logs -f howa-prod-core 2>&1 | nc logserver.example.com 514
```

Consider using:

- ELK Stack (Elasticsearch, Logstash, Kibana)
- Graylog
- Splunk
- CloudWatch / Azure Monitor

### Security Events to Monitor

1. **Failed login attempts**
2. **Privilege escalations**
3. **File modifications** in sensitive directories
4. **Unusual network traffic**
5. **Container restarts**
6. **Resource usage spikes**

### Health Check Monitoring

Set up external monitoring for health endpoints:

```bash
# Automated health check (cron every 5 min)
*/5 * * * * curl -f https://howa.edu.sa/health || alert-team.sh
```

Use services like:

- UptimeRobot
- Pingdom
- StatusCake
- Datadog

### Audit Logs

Enable audit logging for compliance:

**Laravel Audit Log** (install package):

```bash
composer require owen-it/laravel-auditing
```

**MySQL Audit Log**:

```sql
SET GLOBAL general_log = 'ON';
SET GLOBAL general_log_file = '/var/log/mysql/general.log';
```

## Security Checklist

### Pre-Production

- [ ] Strong passwords in all `.env` files
- [ ] SSL certificates installed and valid
- [ ] Database root password changed from default
- [ ] Redis password set
- [ ] OAuth keys have correct permissions (600)
- [ ] Unnecessary ports not exposed
- [ ] Security headers enabled in nginx
- [ ] PHP dangerous functions disabled
- [ ] File upload validation working
- [ ] CSRF protection enabled (Laravel default)
- [ ] SQL injection protection verified (use Eloquent ORM)
- [ ] XSS protection enabled (Laravel escaping)

### Post-Production

- [ ] Change all default passwords
- [ ] Enable firewall (ufw/iptables)
- [ ] Configure fail2ban
- [ ] Set up automated backups
- [ ] Test backup restoration
- [ ] Configure log rotation
- [ ] Set up monitoring/alerting
- [ ] Security scan completed (Trivy/Scout)
- [ ] Vulnerability patching plan in place
- [ ] Incident response plan documented
- [ ] Regular security audit scheduled

### Ongoing Maintenance

- [ ] Weekly: Review security logs
- [ ] Monthly: Update base images
- [ ] Monthly: Scan for vulnerabilities
- [ ] Quarterly: Rotate passwords/keys
- [ ] Quarterly: Security audit
- [ ] Annually: Penetration testing
- [ ] Annually: Disaster recovery drill

## Incident Response

If security breach suspected:

1. **Isolate** affected containers:

```bash
docker-compose stop [service-name]
```

2. **Preserve evidence**:

```bash
# Export container
docker export howa-prod-core > evidence.tar

# Copy logs
docker logs howa-prod-core > incident-logs.txt
```

3. **Analyze** logs and container state
4. **Patch** vulnerability
5. **Rebuild** affected images
6. **Redeploy** with new credentials
7. **Document** incident and lessons learned

## Security Resources

- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Laravel Security](https://laravel.com/docs/security)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)

## Reporting Security Issues

If you discover a security vulnerability:

- **DO NOT** create a public GitHub issue
- Email security concerns to: <ahmed@logi-x.org>
- Include detailed description and steps to reproduce
- Allow time for patching before disclosure

## Compliance

For Saudi Arabian regulations:

- **ZATCA e-invoicing**: Already integrated
- **PDPL** (Personal Data Protection Law): Ensure user data handling compliance
- **NCA** (National Cybersecurity Authority): Follow ECC controls

---

**Remember: Security is not a one-time task, it's an ongoing process.**

Last Updated: 2025-01-04
