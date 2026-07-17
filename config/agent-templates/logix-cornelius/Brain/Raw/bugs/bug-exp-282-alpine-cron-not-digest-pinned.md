---
title: "EXP-282 — Production cron image alpine:3.23 not digest-pinned — supply-chain risk"
date: "2026-06-02"
status: open
resolution: unknown
tags: [bug, security, infrastructure, docker, supply-chain, cron, project/experts]
linear: "https://linear.app/experts/issue/EXP-282/security-production-cron-image-alpine323-not-digest-pinned-supply"
fingerprint: "bcd1d1b0ba51"
---

## Summary

`docker/production/docker-compose.yml` — `experts-prd-cron` service uses `alpine:3.23` as its base image without a digest pin (`@sha256:...`). A supply-chain attacker who compromises the `alpine:3.23` tag on Docker Hub could push a malicious image that executes arbitrary code in the cron sidecar on the next `docker compose pull`. Other services in production are digest-pinned (e.g. Redis was pinned by PR #714).

## Root cause

`docker/production/docker-compose.yml` — `experts-prd-cron` `image: alpine:3.23`. Fix: append `@sha256:<digest>` (pinned to a known-good current Alpine 3.23 digest, e.g. `alpine:3.23.4@sha256:...`) and update on intentional Alpine upgrades.

## Agent fingerprint

`<!-- agent-fp: bcd1d1b0ba51 -->`

## Status

`open` — Backlog (Medium). Supply-chain risk. Low likelihood but easy to fix.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
