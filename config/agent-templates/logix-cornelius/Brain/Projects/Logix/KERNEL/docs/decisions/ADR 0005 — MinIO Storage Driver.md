---
title: "ADR 0005 — MinIO Storage Driver"
date: "2026-07-05"
updated: "2026-07-05"
tags: ["project/logix", "project/logix-kernel", "topic/adr"]
category: "docs/logix-kernel"
up: "[[Projects/Logix/KERNEL/docs]]"
repo_root: "/home/logix/logix-kernel"
source: "curated"
source_id: "docs/adr/0005-minio-storage-driver.md"
---

↑ [[Projects/Logix/KERNEL/docs|Docs index]]

# ADR 0005: MinIO Storage Driver

## Status

Accepted.

## Context

Phase 1 needs real file metadata, versioning, share links, and local development without a cloud account.

## Decision

Use MinIO locally with the AWS S3 client API. The API owns upload/download/share behavior and records file events/access logs.

## Consequences

The storage boundary can later point at S3-compatible production storage. Seeded file metadata is present for product demos; fresh uploads exercise the full storage driver.
