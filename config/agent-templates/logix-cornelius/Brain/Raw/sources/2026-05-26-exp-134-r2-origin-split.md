---
title: "EXP-134 R2 origin split cleanup"
date: "2026-05-26"
source: "codex-session"
tags: ["project/experts", "r2", "storage", "cloudflare", "linear"]
---

## Summary

Worked EXP-134, EXP-104, EXP-105, and EXP-135 on branch `codex/exp-134-r2-upload-split`.

Key implementation decision: user-upload writes now use `R2_BUCKET_USER_UPLOADS`, matching URLs returned from `R2_USER_UPLOADS_PUBLIC_URL`. Profile cover deletion routes files-origin URLs through the same public-asset delete path, while legacy trusted-CDN cover URLs still delete through the historical static-bucket path.

## Cloudflare Check

Cloudflare API token verification succeeded and DNS records for `cdn.experts.com.sa` and `files.experts.com.sa` were visible in the `experts.com.sa` zone. Both CNAME to `public.r2.dev`. The available token could not read R2 bucket custom-domain bindings; R2 bucket/domain endpoints returned authentication errors. DNS alone does not prove the R2 custom-domain bucket binding.

## Follow-Up

Confirm the actual Cloudflare R2 custom-domain binding for `files.experts.com.sa` in the dashboard, or with a token that has R2 read permissions, and verify it points at the `files` bucket.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
