---
title: "Centralized Version Management"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/docker"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Centralized Version Management

## Overview

This project uses a centralized version management system where all versions are managed from a single source (`version.json`) and automatically synced to all necessary files.

## Quick Start

### Show Current Versions

```bash
./scripts/version-manager.sh
# or
./scripts/version-manager.sh show
```

### Bump Version

```bash
# Patch: 1.0.25 → 1.0.26
./scripts/version-manager.sh bump patch

# Minor: 1.0.25 → 1.1.0
./scripts/version-manager.sh bump minor

# Major: 1.0.25 → 2.0.0
./scripts/version-manager.sh bump major
```

### Set Specific Version

```bash
# Set all versions to 1.0.30
./scripts/version-manager.sh set 1.0.30

# Set only experts-app version
./scripts/version-manager.sh set-app app 1.0.31

# Set only experts-api version
./scripts/version-manager.sh set-app api 1.0.31

# Set only experts-server version
./scripts/version-manager.sh set-app server 1.0.31
```

### Sync Versions

Manually sync versions from version.json to all files (usually not needed as other commands auto-sync):

```bash
./scripts/version-manager.sh sync
```

## Architecture

### Single Source of Truth

**File:** `/version.json`

```json
{
  "version": "1.0.25",
  "apps": {
    "experts-app": {
      "version": "1.0.25"
    },
    "experts-api": {
      "version": "1.0.25"
    },
    "experts-server": {
      "version": "1.0.25"
    }
  },
  "metadata": {
    "lastUpdated": "2025-11-16T14:54:13.000Z",
    "updatedBy": "version-manager"
  }
}
```

### Managed Files

The version manager automatically updates versions in:

#### Package.json Files

- `apps/experts-app/package.json`
- `apps/experts-api/package.json`
- `apps/experts-server/package.json`

#### App Environment Files

- `apps/experts-app/.env` (APP_VERSION)
- `apps/experts-app/.env.production` (APP_VERSION)
- `apps/experts-app/.env.canary` (APP_VERSION)
- `apps/experts-app/.env.staging` (APP_VERSION)
- `apps/experts-api/.env` (API_VERSION)
- `apps/experts-api/.env.production` (API_VERSION)
- `apps/experts-api/.env.canary` (API_VERSION)
- `apps/experts-api/.env.staging` (API_VERSION)
- `apps/experts-server/.env` (SERVER_VERSION)
- `apps/experts-server/.env.production` (SERVER_VERSION)
- `apps/experts-server/.env.canary` (SERVER_VERSION)
- `apps/experts-server/.env.staging` (SERVER_VERSION)

#### Docker Environment Files

- `docker/canary/.env` (API_VERSION, APP_VERSION, SERVER_VERSION)
- `docker/staging/.env` (API_VERSION, APP_VERSION, SERVER_VERSION)
- `docker/development/.env` (API_VERSION, APP_VERSION, SERVER_VERSION)
- `docker/production/.env` (API_VERSION, APP_VERSION, SERVER_VERSION)

## Common Workflows

### Release Workflow

```bash
# 1. Bump version for release
./scripts/version-manager.sh bump minor

# 2. Verify versions
./scripts/version-manager.sh show

# 3. Commit changes
git add version.json apps/*/package.json apps/*/.env.* docker/*/.env
git commit -m "chore: bump version to $(jq -r '.version' version.json)"

# 4. Tag release
git tag "v$(jq -r '.version' version.json)"
```

### Hotfix Workflow

```bash
# 1. Bump patch version
./scripts/version-manager.sh bump patch

# 2. Commit and tag
git add version.json apps/*/package.json apps/*/.env.* docker/*/.env
git commit -m "chore: hotfix version bump"
git tag "v$(jq -r '.version' version.json)"
```

## Help

For detailed usage information:

```bash
./scripts/version-manager.sh help
```
