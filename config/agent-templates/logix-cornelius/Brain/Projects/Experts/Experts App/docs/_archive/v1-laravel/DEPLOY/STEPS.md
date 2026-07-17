---
title: "Steps to publish to staging - production"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/deploy"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Steps to publish to staging - production

## Insure API SDK is up to date

### Build the API /docs per `env`

```sh

cd /home/logix/experts/apps/experts-api && docker build --build-arg APP_ENV=local -t loogix/experts-docs:development -f Dockerfile.docs .
cd /home/logix/experts/apps/experts-api && docker build --build-arg APP_ENV=canary -t loogix/experts-docs:canary -f Dockerfile.docs .
cd /home/logix/experts/apps/experts-api && docker build --build-arg APP_ENV=staging -t loogix/experts-docs:staging -f Dockerfile.docs .
cd /home/logix/experts/apps/experts-api && docker build --build-arg APP_ENV=production -t loogix/experts-docs:production -f Dockerfile.docs .

```

```sh
cd /home/logix/experts/docker/development && docker compose run --rm experts-docs
cd /home/logix/experts/docker/canary && docker compose run --rm experts-docs
cd /home/logix/experts/docker/staging && docker compose run --rm experts-docs
cd /home/logix/experts/docker/production && docker compose run --rm experts-docs

```

### Build the SDK

```sh

cd /home/logix/experts && docker build --build-arg APP_ENV=local -t loogix/experts-sdk:development -f packages/sdk/Dockerfile.sdk .
cd /home/logix/experts && docker build --build-arg APP_ENV=canary -t loogix/experts-sdk:canary -f packages/sdk/Dockerfile.sdk .
cd /home/logix/experts && docker build --build-arg APP_ENV=staging -t loogix/experts-sdk:staging -f packages/sdk/Dockerfile.sdk .
cd /home/logix/experts && docker build --build-arg APP_ENV=production -t loogix/experts-sdk:production -f packages/sdk/Dockerfile.sdk .

```

```sh

cd /home/logix/experts/docker/development && docker compose run --rm experts-sdk
cd /home/logix/experts/docker/canary && docker compose run --rm experts-sdk
cd /home/logix/experts/docker/staging && docker compose run --rm experts-sdk
cd /home/logix/experts/docker/production && docker compose run --rm experts-sdk

```

### Build and run SDK to debug

```sh
cd /home/logix/experts/docker/canary && docker compose up -d --build experts-sdk
cd /home/logix/experts/docker/staging && docker compose up -d --build experts-sdk
cd /home/logix/experts/docker/production && docker compose up -d --build experts-sdk

```

### Step by Step dev

```sh

cd /home/logix/experts/apps/experts-api && docker build --build-arg APP_ENV=development -t loogix/experts-docs:development -f Dockerfile.docs . && cd /home/logix/experts/docker/development && docker compose run --rm experts-docs
cd /home/logix/experts && docker build --build-arg APP_ENV=development -t loogix/experts-sdk:development -f packages/sdk/Dockerfile.sdk . && cd /home/logix/experts/docker/development && docker compose run --rm experts-sdk
cd /home/logix/experts/apps/experts-app && ./docker/build-local.sh development loogix/experts-app:development && cd /home/logix/experts/docker/development && docker compose build experts-api experts-server && docker compose up -d --force-recreate experts-api experts-server experts-app

```

### Step by Step canary

```sh

cd /home/logix/experts/apps/experts-api && docker build --build-arg APP_ENV=canary -t loogix/experts-docs:canary -f Dockerfile.docs . && cd /home/logix/experts/docker/canary && docker compose run --rm experts-docs
cd /home/logix/experts && docker build --build-arg APP_ENV=canary -t loogix/experts-sdk:canary -f packages/sdk/Dockerfile.sdk . && cd /home/logix/experts/docker/canary && docker compose run --rm experts-sdk
cd /home/logix/experts/apps/experts-app && ./docker/build-local.sh canary loogix/experts-app:canary && cd /home/logix/experts/docker/canary && docker compose build experts-api experts-server && docker compose up -d --force-recreate experts-api experts-server experts-app

```

### Step by Step staging

```sh

cd /home/logix/experts/apps/experts-api \
&& docker build --build-arg APP_ENV=staging -t loogix/experts-docs:staging -f Dockerfile.docs . \
&& cd /home/logix/experts/docker/staging \
&& docker compose run --rm experts-docs \
&& cd /home/logix/experts \
&& docker build --build-arg APP_ENV=staging -t loogix/experts-sdk:staging -f packages/sdk/Dockerfile.sdk . \
&& cd /home/logix/experts/docker/staging \
&& docker compose run --rm experts-sdk \
&& cd /home/logix/experts/apps/experts-app \
&& ./docker/build-local.sh staging loogix/experts-app:staging \
&& cd /home/logix/experts/docker/staging \
&& docker compose build experts-api experts-server \
&& docker compose up -d --force-recreate experts-api experts-server experts-app \
&& for img in \
  loogix/experts-api:staging \
  loogix/experts-app:staging \
  loogix/experts-server:staging; do
  docker push "$img"
done

cd /home/logix/experts/apps/experts-api && docker build --build-arg APP_ENV=staging -t loogix/experts-docs:staging -f Dockerfile.docs . && cd /home/logix/experts/docker/staging && docker compose run --rm experts-docs && cd /home/logix/experts && docker build --build-arg APP_ENV=staging -t loogix/experts-sdk:staging -f packages/sdk/Dockerfile.sdk . && cd /home/logix/experts/docker/staging && docker compose run --rm experts-sdk && cd /home/logix/experts/apps/experts-app && ./docker/build-local.sh staging loogix/experts-app:staging && cd /home/logix/experts/docker/staging && docker compose build experts-api experts-server && docker compose up -d --force-recreate experts-api experts-server experts-app && for img in loogix/experts-api:staging loogix/experts-app:staging loogix/experts-server:staging; do docker push "$img"; done

```

╔══════════════════════════════════════════════════════════════╗
║ SDK Build Workflow - TESTED & WORKING ✅ ║
╚══════════════════════════════════════════════════════════════╝

🎉 SUCCESS! Your workflow is fully operational.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ VERIFIED WORKING:

1.  Generate SDK Tarball
    ✓ docker compose run --rm experts-sdk
    ✓ Creates: packages/sdk/dist/experts-sdk-1.0.0.tgz
    ✓ Ownership: ubuntu:lxd (UID:GID 1000:1000)
    ✓ Permissions: -rw-r--r-- (readable by all)

2.  Install SDK
    ✓ ./scripts/install-sdk.sh canary
    ✓ Installs @experts/sdk@1.0.0
    ✓ Verified in node_modules

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 THE FIX:

The key issue was that files created at Docker BUILD time
disappear when a volume is mounted at RUN time.

Solution: Use ENTRYPOINT to copy files AFTER volume mount

- Files are in /app (from builder stage)
- Entrypoint copies to /output (mounted volume)
- Sets correct ownership with HOST_UID/HOST_GID
- Result: Tarball on host with correct permissions!

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  📋 COMPLETE WORKFLOW (Tested):

  For canary environment:

# 1. Generate OpenAPI docs

cd docker/canary
docker compose run --rm experts-docs

# 2. Generate SDK tarball

docker compose run --rm experts-sdk

# Output: 📦 Copying SDK tarball to /output

# ✅ SDK tarball ready

# -rw-r--r-- 1 1000 1000 15K experts-sdk-1.0.0.tgz

# 3. Install SDK (or let build script do it automatically)

cd ../../
./scripts/install-sdk.sh canary

# Output: ✅ @experts/sdk@1.0.0 is installed

# 4. Build app (SDK check included!)

./apps/experts-app/docker/build-local.sh canary

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 READY FOR ALL ENVIRONMENTS:

Canary:
docker compose run --rm experts-sdk
./scripts/install-sdk.sh canary

Staging:
cd docker/staging
docker compose run --rm experts-sdk
cd ../../
./scripts/install-sdk.sh staging

Production:
cd docker/production
docker compose run --rm experts-sdk
cd ../../
./scripts/install-sdk.sh production

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 DOCUMENTATION:

Complete guide with troubleshooting:
→ SDK_BUILD_WORKFLOW.md

╔══════════════════════════════════════════════════════════════╗
║ No more root-owned files! Workflow is production-ready! 🚀 ║
╚══════════════════════════════════════════════════════════════╝
