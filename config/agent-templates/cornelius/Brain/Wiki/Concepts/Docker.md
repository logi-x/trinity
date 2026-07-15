---
title: "Docker"
date: "2026-04-10"
updated: "2026-05-24"
tags: ["entity", "topic", "tech/docker"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Docker.md"
---

# Docker

Docker in this vault is mostly about environment reproducibility for Experts services: local containers, deployment images, network behavior, and making app/runtime expectations explicit.

## Frequent concerns

- local dev container setup
- multi-stage image optimization
- port and hostname mismatches
- networking between app, workers, Redis, and proxies
- keeping Docker-oriented flows separate from normal local web dev when needed
- scheduled jobs in VPS deployments should live in Docker Compose as sidecar services when they need to travel with the deployment

## Why it shows up

Many runtime or deployment problems are really environment problems. Docker conversations often surface hidden assumptions about paths, hostnames, ports, or startup order.

## Experts Deployment Notes

- 2026-04-27: Experts app is deployed on a VPS inside Docker Compose, not Vercel. Vercel-only cron config was removed from `apps/experts-app/vercel.json`.
- 2026-05-05: Experts app CI gained a Docker artifact and VPS deployment layer in `.github/workflows/experts-app.yml`. Pushes to the deploy branch, default `staging`, now run CI checks first, then a self-hosted runner builds `apps/experts-app/Dockerfile`, pushes `loogix/core:experts-staging` plus a SHA tag, pulls the stable tag on the VPS, and recreates only the `experts-app` Compose service.
- Scheduled jobs now use a Docker cron sidecar in `docker/staging/docker-compose.yml`.
- The cron sidecar calls internal Next.js routes over the Compose network using `APP_BASE_URL=http://experts-app:3025`.
- `CRON_SECRET` must be present in `docker/staging/.env` and shared by both `experts-app` and the `cron` sidecar.
- Current schedules:
  - every 2 minutes: `POST /api/v1/internal/embeddings/sync`
  - daily at 03:00: `POST /api/v1/admin/payments/reconcile/batch`
- Avoid `instrumentation.ts` `setInterval` for cron-like jobs unless the app runs as exactly one server instance; multiple replicas would duplicate scheduled execution.
- 2026-05-06: For Docker images that use Corepack-managed pnpm, keep `COREPACK_HOME` stable between build and runtime and do not point Compose at an empty temporary cache. In `apps/experts-prisma/Dockerfile`, pnpm is prepared into `/usr/local/share/corepack`; `docker/staging/docker-compose.yml` should not override `COREPACK_HOME` to `/tmp/corepack` for `experts-stg-prisma`, or each `docker compose run --rm` may prompt to download pnpm again.

## Hardening rules — production compose (incident 2026-05-24)

Two HIGH-severity findings shipped together in PR [#436](https://github.com/logi-x/experts/pull/436) (Cleanup/docker remote branch) and were fixed manually via [#459](https://github.com/logi-x/experts/pull/459) (ports) and [#462](https://github.com/logi-x/experts/pull/462) (image pin). Both rules are now invariants — any future change that violates either is a regression.

### Rule 1: NEVER bind database / cache ports to `0.0.0.0` in production or staging compose (EXP-101)

- A bare `5432:5432` (or `6379:6379`, `5433:5432`, `6378:6379`) in a Compose `ports:` stanza binds to `0.0.0.0` on the host. The port is publicly reachable on the VPS IP.
- **Docker bypasses UFW.** Docker injects its own iptables rules ABOVE the FORWARD chain UFW uses. A host-level `ufw deny 5432` has zero effect on published Docker ports. The only line of defense becomes the database password itself.
- **Correct form** (loopback only — remote access requires SSH tunnel):
  ```yaml
  experts-prd-postgres:
    ports:
      - "127.0.0.1:5432:5432"
  experts-prd-redis:
    ports:
      - "127.0.0.1:6379:6379"
  ```
- **Better form** (preferred — drop the stanza entirely): app/workers/cron reach postgres+redis by service name on `experts-shared-network`. The `ports:` stanza serves only ops tooling; remove it unless someone is actively running DBA queries from outside the host.
- `experts-shared-network` `external: true` does NOT protect this. That setting controls intra-container routing only; `ports:` operates at the host kernel level via iptables independently of any Docker network configuration.
- Same rule for staging: ports rebound to `127.0.0.1:5433:5432` (postgres) and `127.0.0.1:6378:6379` (redis).

### Rule 2: NEVER use the `:latest` tag for any image in production or staging compose (EXP-102)

- `redis:latest` (or any unpinned tag) means `docker compose pull` / `docker compose up --pull always` silently fetches whatever Docker Hub currently resolves the tag to. Three concrete failure modes:
  1. **Silent major-version upgrades** — `latest` moves from Redis 7.x → 8.x without warning. Breaking changes in AUTH, config keys, or RESP protocol surface in production.
  2. **CVE response blindspot** — you can't answer "which Redis version is in prod?" so CVE triage goes from hours to days.
  3. **Supply-chain compromise** — a hijacked Docker Hub tag (credential theft, maintainer takeover) is pulled silently on next deploy. The compromised container shares `experts-shared-network` with the app, workers, and database = full lateral movement.
- **Correct form** (tag + digest = reproducible + supply-chain protected):
  ```yaml
  experts-prd-redis:
    image: redis:8.6.3-alpine@sha256:d146f83b1e0f02fc27c26a50cee39338c736674c5959db84363e6ae3cd9e02d2
  ```
- Tag (`8.6.3-alpine`) tells humans what version is running. Digest (`@sha256:...`) tells Docker EXACTLY which image bytes to pull — immutable, can't be force-overwritten by a hijack.
- Alpine variant = smaller attack surface than the Debian-based default tag.
- Same rule for staging: identical pin (`redis:8.6.3-alpine@sha256:...`).
- Periodic upgrade is intentional: bump the tag + digest in a PR, review, deploy. Don't drift silently.

### Audit check before any docker compose change

When editing `docker/production/docker-compose.yml` or `docker/staging/docker-compose.yml`:

```bash
# Rule 1 violation check (must return ZERO lines):
grep -nE '^\s*-\s*"?[0-9]+:[0-9]+"?\s*(#|$)' docker/production/docker-compose.yml docker/staging/docker-compose.yml

# Rule 2 violation check (must return ZERO lines):
grep -nE 'image:\s*\S+:latest' docker/production/docker-compose.yml docker/staging/docker-compose.yml
```

If either grep returns anything, the change regresses EXP-101 or EXP-102. Fix before commit. Worth adding both checks as a CI lint step.

## Related

- [[Wiki/Concepts/Nginx]]
- [[Wiki/Concepts/Node.js]]
- [[Wiki/Concepts/Laravel Reverb]]
- [[Projects/Experts/DEVELOPER_GUIDE]]
