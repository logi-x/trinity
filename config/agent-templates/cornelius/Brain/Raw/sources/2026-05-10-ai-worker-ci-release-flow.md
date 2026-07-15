---
title: "Ai Worker Ci Release Flow"
date: "2026-05-10"
tags: [session-log, project/experts]
category: "session-log"
---

# AI Worker CI Release Flow

Date: 2026-05-10
Repo: `/home/logix/experts`
Branch: `feat/add-ai-worker`

## Summary

Implemented the deferred GitHub Actions release path for the shared pure worker image used by PDF, ZATCA, and AI workers.

## Changes

- Added `.github/ci/docker-worker-release.sh`.
- Added `force_build_worker` to `.github/workflows/experts-app.yml`.
- Added worker change detection output.
- Added Docker build/push step for `experts-{stg,prd}-worker`.
- Added deploy restart step for worker services:
  - `experts-stg-pdf-worker`
  - `experts-stg-zatca-worker`
  - `experts-stg-ai-worker`
  - `experts-prd-pdf-worker`
  - `experts-prd-zatca-worker`
  - `experts-prd-ai-worker`
- Added `EXPERTS_WORKER_IMAGE` override support to staging and production compose worker services, preserving existing image tags as defaults.

## Commits

- `10a1d973 Add worker image release flow`
- `360bfb78 Make worker release script executable`

## Verification

- `bash -n .github/ci/docker-worker-release.sh .github/ci/docker-app-release.sh .github/ci/docker-prisma-release.sh .github/ci/docker-realtime-release.sh` passed.
- `pnpm exec prettier --check .github/workflows/experts-app.yml` passed.
- All four compose files passed `docker compose config --quiet`.
- `EXPERTS_WORKER_IMAGE` override resolved correctly for staging and production deployed compose files.
- `npx gitnexus detect-changes --scope all --repo experts` reported no indexed symbol changes.

## Remaining Operational Check

Run the GitHub workflow manually on staging with `force_build_worker=true` and confirm Docker Hub push plus server restart for the three staging worker services.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
