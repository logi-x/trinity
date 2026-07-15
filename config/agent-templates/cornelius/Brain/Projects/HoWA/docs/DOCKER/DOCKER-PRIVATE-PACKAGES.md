---
title: "Setting Up Private NPM Packages for Docker"
date: "2026-04-11"
tags: ["project/howa", "docs/howa", "tech/docker"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Setting Up Private NPM Packages for Docker

Your project uses private GitHub packages (`@logi-x/*`) that require authentication. Follow these steps to set up Docker builds with private packages.

## Quick Setup

### 1. Create GitHub Personal Access Token

1. Go to: <https://github.com/settings/tokens>
2. Click "Generate new token" → "Generate new token (classic)"
3. Name it: `HOWA Docker Build`
4. Select scopes:
   - ✅ `read:packages` (required)
   - ✅ `repo` (if packages are in private repos)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)

### 2. Create .npmrc File

```bash
# Copy the example file
cp .npmrc.example .npmrc

# Edit .npmrc and replace YOUR_GITHUB_TOKEN_HERE with your actual token
nano .npmrc
```

Your `.npmrc` should look like:

```
@logi-x:registry=https://npm.pkg.github.com
@jsr:registry=https://npm.jsr.io
//npm.pkg.github.com/:_authToken=ghp_YourActualTokenHere123456789
```

### 3. Secure Your Token

**Important:** The `.npmrc` file contains your secret token!

```bash
# Make sure .npmrc is in .gitignore (already done)
grep -q ".npmrc" .gitignore && echo "✓ .npmrc is ignored" || echo ".npmrc" >> .gitignore

# Set proper permissions
chmod 600 .npmrc
```

### 4. Build Docker Images

Now you can build normally:

```bash
# Development
docker-compose build

# Production
docker-compose -f docker-compose.prod.yml build
```

## Alternative: Using Build Arguments

For CI/CD or when you don't want to use `.npmrc` file:

### 1. Create .npmrc with Build Arg

Create `docker/node/Dockerfile.dev` modification:

```dockerfile
# Add this near the top
ARG GITHUB_TOKEN

# Before pnpm install
RUN if [ -n "$GITHUB_TOKEN" ]; then \
        echo "@logi-x:registry=https://npm.pkg.github.com" > .npmrc && \
        echo "//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}" >> .npmrc; \
    fi
```

### 2. Build with Argument

```bash
# Pass token during build
docker-compose build --build-arg GITHUB_TOKEN=your_token_here

# Or export as environment variable
export GITHUB_TOKEN=your_token_here
docker-compose build
```

### 3. Update docker-compose.yml

Add build args:

```yaml
services:
  server:
    build:
      context: .
      dockerfile: ./docker/node/Dockerfile.dev
      args:
        GITHUB_TOKEN: ${GITHUB_TOKEN}
```

## For CI/CD (GitHub Actions)

### 1. Add GitHub Secret

1. Go to your repo → Settings → Secrets and variables → Actions
2. New repository secret:
   - Name: `GITHUB_TOKEN` (or use built-in `GITHUB_TOKEN`)
   - Value: Your personal access token

### 2. Use in Workflow

```yaml
- name: Build Docker images
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    echo "@logi-x:registry=https://npm.pkg.github.com" > .npmrc
    echo "//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}" >> .npmrc
    docker-compose build
```

## Troubleshooting

### Error: 401 Unauthorized

**Cause:** Token is missing or invalid

**Solution:**

1. Check your `.npmrc` file exists
2. Verify token is correct (no extra spaces/newlines)
3. Check token hasn't expired
4. Ensure token has `read:packages` scope

### Error: Token still not working

**Try:**

```bash
# Test token locally first
pnpm install

# If that works, rebuild Docker
docker-compose build --no-cache
```

### Error: Permission denied

```bash
# Fix .npmrc permissions
chmod 600 .npmrc
```

### Check if .npmrc is being copied

```bash
# Build with verbose output
docker-compose build --progress=plain

# Look for: "COPY .npmrc* ./"
```

## Security Best Practices

### DO ✅

- Use personal access tokens with minimal scopes
- Add `.npmrc` to `.gitignore`
- Use Docker secrets in production
- Rotate tokens regularly
- Use different tokens for different environments

### DON'T ❌

- Commit `.npmrc` to git
- Share tokens between team members
- Use tokens with write permissions for builds
- Hardcode tokens in Dockerfiles
- Push images with tokens still in them

## Production Deployment

For production servers, consider:

1. **Use Docker Secrets:**

```bash
echo "your_token" | docker secret create github_token -
```

2. **Mount as volume:**

```yaml
volumes:
  - ~/.npmrc:/root/.npmrc:ro
```

3. **Environment variable:**

```yaml
environment:
  - GITHUB_TOKEN=${GITHUB_TOKEN}
```

## Team Setup

For team members:

1. Each member creates their own token
2. Each member creates their own `.npmrc`
3. Never share tokens
4. Document the process (this file!)

## Quick Checklist

Before building:

- [ ] GitHub token created with `read:packages` scope
- [ ] `.npmrc` file created from example
- [ ] Token added to `.npmrc`
- [ ] `.npmrc` is in `.gitignore`
- [ ] `.npmrc` permissions set to 600
- [ ] Test with `pnpm install` locally first
- [ ] Build Docker images

## Need Help?

Common issues:

- Token expired → Generate new one
- Wrong scope → Regenerate with correct scopes
- File not copied → Check `.dockerignore`
- Still failing → Try `--no-cache` build

---

**Note:** This setup is already configured in the Dockerfiles. You just need to create your `.npmrc` file!
