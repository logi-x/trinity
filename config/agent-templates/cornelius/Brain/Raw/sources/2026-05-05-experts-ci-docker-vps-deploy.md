---
date: "2026-05-05"
source: "codex-session"
project: "Experts"
topic: "CI Docker VPS deploy"
tags: [project/experts]
---

# Experts CI Docker VPS Deploy

Implemented the pending deployment artifact layer in `/home/logix/experts/.github/workflows/experts-app.yml`.

Summary:

- Existing `verify` job remains the gate for typecheck, lint, unit tests, and build.
- New `docker-release` job runs on a self-hosted runner after `verify`.
- The Docker release builds `apps/experts-app/Dockerfile` target `runner` for `linux/amd64`.
- The release pushes both `loogix/core:experts-staging` and `loogix/core:experts-staging-${GITHUB_SHA}` by default.
- New `deploy` job runs on a self-hosted runner after the image push.
- Deployment pulls the stable tag and runs `docker compose up -d --force-recreate --no-deps experts-app` in `/home/logix/experts/docker/staging`.
- The deploy job polls the `experts-staging` container health status and prints recent logs on failure.

Config knobs are GitHub repository variables:

- `EXPERTS_APP_DEPLOY_BRANCH` default `staging`
- `EXPERTS_APP_DOCKER_IMAGE` default `loogix/core`
- `EXPERTS_APP_DOCKER_TAG` default `experts-staging`
- `EXPERTS_APP_DEPLOY_COMPOSE_DIR` default `/home/logix/experts/docker/staging`
- `EXPERTS_APP_DEPLOY_SERVICE` default `experts-app`
- `EXPERTS_APP_DEPLOY_CONTAINER` default `experts-staging`
- `EXPERTS_APP_PUBLIC_URL` default `https://app.stg.experts.com.sa`
- `EXPERTS_APP_REALTIME_WS_URL` default `https://socket.stg.experts.com.sa`

Required GitHub secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
