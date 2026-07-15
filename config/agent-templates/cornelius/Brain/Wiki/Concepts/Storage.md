---
title: "Storage"
date: "2026-04-10"
updated: "2026-06-22"
tags: ["entity", "topic", "topic/storage", "ssd", "nvme"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Storage.md"
---

# Storage

Storage refers to how the projects handle persistent files, generated artifacts, and long-term document retention across the web app, deployment environments, and supporting workflows.

## Context in Experts

Storage is especially relevant for billing documents, signed ZATCA artifacts, certificates, uploads, and environment-dependent file handling in Experts App.

## What tends to live here

- Uploaded media and attachments
- Generated PDFs and certificates
- Signed invoice artifacts and compliance documents
- Operational files needed by workers or deploy environments

## Why it matters

Ahmed's project notes explicitly call out long-term storage strategy for signed documents as part of the Saudi compliance workflow. That makes storage a business and compliance concern, not just an infrastructure detail.

## Operational stance

- Storage decisions should match deployment reality, not just local dev convenience
- Compliance-related documents need durable retention
- Generated files should fit the async worker model used elsewhere in Experts
- Ready-file deletion must be owned by the domain that created the file. Never
  infer that an `Attachment` is orphaned from the absence of a partial set of
  relations. The former orphan-attachment janitor only checked five course asset
  relations, so it deleted legitimate course/event/community thumbnails and
  certification documents after 24 hours. The sweep was decommissioned on
  2026-06-22; stale cron and BullMQ invocations must remain fail-closed no-ops.

## Related

- [[Wiki/Concepts/PDF]]
- [[Wiki/Concepts/ZATCA]]

