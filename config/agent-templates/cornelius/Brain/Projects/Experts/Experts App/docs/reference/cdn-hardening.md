---
title: CDN & Edge Hardening — `cdn.experts.com.sa`
date: 2026-05-14
status: open
resolution: pending
tags: [security, incident, remediation, workflow]
category: "docs/experts-reference"
updated: "2026-07-15"
---

# CDN & Edge Hardening — `cdn.experts.com.sa`

**Owner:** devops / platform-ops
**Origin incident:** [Security Incident #7](/home/logix/brain-v2/Raw/reviews/incident#7/security-13052026.md), follow-on from incident #2 (PR #308)
**Class:** XSS (CSP + nosniff) and data exposure (bucket listing)
**Status:** open — out-of-repo configuration tracked here

---

## Why this matters

The upload-route hardening from incidents #2 and #6 relies on:

- A constrained MIME allowlist (no `text/javascript`, no `text/html`, no `application/octet-stream`).
- A `Content-Disposition: attachment` header on non-media assets.
- The CDN faithfully serving the bytes and headers we set.

The CDN is the last hop. If it strips headers, sniffs MIMEs, or allows listing, app-layer mitigations collapse silently. This document tracks the four edge-layer items that the app cannot guarantee on its own.

---

## Scope — four items

### 1. `X-Content-Type-Options: nosniff` on every CDN response

**Why:** without this header some browsers will sniff the body and override the declared `Content-Type`. A file uploaded as `text/plain` whose body is HTML could be rendered as HTML by a sniffing browser.

**Where this lives:** Cloudflare Transform Rule or Page Rule on `cdn.experts.com.sa/*`, NOT the R2 bucket directly.

**Verification (curl from anywhere):**

```bash
# Replace <KEY> with any real object key under uploads/ or assets/
curl -sI "https://cdn.experts.com.sa/uploads/courses/3d319abc-17e6-4871-adb3-4986324e3c6c/cf74748d-2abd-434e-920f-8829566b6dd5.png" \
  | grep -i 'x-content-type-options'
# Expected: x-content-type-options: nosniff
```

**If missing — Cloudflare dashboard steps:**

1. Cloudflare dashboard → select zone `experts.com.sa`.
2. Rules → Transform Rules → Modify Response Header.
3. Create rule:
   - Name: `cdn-nosniff`
   - When: `(http.host eq "cdn.experts.com.sa")`
   - Then: Set static header `X-Content-Type-Options` = `nosniff`
4. Deploy. Re-run the curl above to confirm.

---

### 2. App CSP does NOT allowlist `cdn.experts.com.sa` as `script-src`

**Why:** if the app's Content-Security-Policy allows `script-src https://cdn.experts.com.sa`, any attacker-uploaded `.js` file on the CDN becomes executable on the app origin. Incident #2 removed `text/javascript` from the MIME allowlist, but CSP is the platform-layer defense.

**Current state in repo:** the app does **not** ship a CSP from `next.config.ts`. If a CSP is being set, it is being set by **Traefik** (`secure-headers@file` middleware referenced in `docker/production/docker-compose.production.yml`) or by Cloudflare.

**Verification — read CSP from a production app page:**

```bash
curl -sI "https://experts.com.sa/en/dashboard" \
  | grep -i 'content-security-policy'
```

Then audit the policy: `cdn.experts.com.sa` should appear ONLY in:

- `img-src` — images served to `<img>` and `background-image`
- `media-src` — `<video>` / `<audio>` sources
- `connect-src` — XHR / fetch / WebSocket targets (if assets are fetched programmatically)
- `font-src` — only if fonts are served from the CDN

`cdn.experts.com.sa` MUST NOT appear in:

- `script-src` (any variant — `script-src-elem`, `script-src-attr`)
- `default-src` (would inherit to `script-src`)
- `object-src`
- `style-src` with `unsafe-inline` adjacent to it

**If drift is found (Traefik):**

The Traefik middleware lives at the host level, outside this repo. The `secure-headers@file` reference in compose maps to a file like `/etc/traefik/dynamic/secure-headers.yml`. SSH to the production host and:

```yaml
# /etc/traefik/dynamic/secure-headers.yml — exemplar shape
http:
  middlewares:
    secure-headers:
      headers:
        contentSecurityPolicy: >-
          default-src 'self';
          script-src 'self';
          img-src 'self' data: https://cdn.experts.com.sa;
          media-src 'self' https://cdn.experts.com.sa;
          connect-src 'self' https://cdn.experts.com.sa https://api.tabby.ai https://eu-test.oppwa.com;
          font-src 'self' data:;
          frame-ancestors 'none';
          base-uri 'self';
          form-action 'self';
        customResponseHeaders:
          X-Content-Type-Options: "nosniff"
          Referrer-Policy: "strict-origin-when-cross-origin"
          X-Frame-Options: "DENY"
```

Reload Traefik (`docker compose restart traefik` or whatever the deployment uses) and re-run the curl.

**If drift is found (Cloudflare):**

Transform Rules → Modify Response Header → Set static header `Content-Security-Policy` on host `app.experts.com.sa`. Treat the Cloudflare rule as authoritative if Traefik is not in use.

---

### 3. Bucket listing disabled on the R2 public bucket

**Why:** the upload key path is `uploads/<domain>/<entityId>/<filename>`. For `draft-courses`, `entityId === userId`. If the bucket allows anonymous listing, anyone can enumerate a user's draft uploads given their userId.

**Verification (must return 403 or AccessDenied, NOT a directory listing):**

```bash
curl -s "https://cdn.experts.com.sa/" | head
curl -s "https://cdn.experts.com.sa/?list-type=2" | head
curl -s "https://cdn.experts.com.sa/uploads/draft-courses/" | head
```

Expected: every one returns `403`, `AccessDenied`, or an HTML error page — never an XML `ListBucketResult` or directory index.

**If listing is enabled — Cloudflare R2 dashboard steps:**

1. R2 → select bucket `experts-static` (or whatever is bound to `cdn.experts.com.sa`).
2. Settings → Public Access → confirm only **object reads** are permitted; bucket-level `ListBucket` should be denied for anonymous principals.
3. If using a bucket policy: ensure no statement grants `s3:ListBucket` to `Principal: "*"`.
4. If the bucket is fronted by a custom Worker, audit the Worker to ensure it does not implement a directory-listing path itself.

---

### 4. `Content-Disposition: attachment` round-trips through the CDN

**Why:** incident #2's mitigation for non-media MIMEs depends on the app setting `Content-Disposition: attachment` on the upload, and the CDN serving it verbatim. If Cloudflare cache rules, Workers, or Transform Rules ever strip response headers, the mitigation collapses.

**Verification (use a real object known to have been uploaded with `Content-Disposition: attachment`):**

```bash
curl -sI "https://cdn.experts.com.sa/uploads/community/62e627b9-7387-4ef5-a3c4-86cca5a66db3/3c1caf97-8ee8-4b64-882b-1556c24bc9f1.png" \
  | grep -iE '^(content-disposition|content-type|x-content-type-options):'
# Expected:
#   content-disposition: attachment; filename="..."
#   content-type: image/png
#   x-content-type-options: nosniff
```

**If the header is missing — likely causes:**

1. Cloudflare cache served a pre-rule response → purge cache for that object.
2. A Transform Rule is rewriting / dropping the header → audit Transform Rules for any rule that touches `Content-Disposition`.
3. A Worker fronting the bucket is constructing its own `Response` and not copying the header → fix the Worker.

**Monitoring suggestion:** add a synthetic check (Cloudflare Synthetic Monitoring, Datadog, or a cron in the storage-janitor process) that:

- Uploads a small test PDF to `uploads/__healthcheck__/<uuid>.pdf` with `Content-Disposition: attachment`.
- Curls it back through `cdn.experts.com.sa`.
- Alerts if `Content-Disposition` or `X-Content-Type-Options` is missing.
- Deletes the test object.

#### 4a. Inline-renderable MIME allowlist (post incident #12 Step 2)

The `uploadPublicAsset` helper (`apps/experts-app/src/lib/storage/commands/upload-public-asset.command.ts`) uses a strict allowlist — not a prefix match — to decide which MIMEs are served **without** `Content-Disposition: attachment`. Only these eight types render inline:

```
image/jpeg  image/jpg  image/png  image/gif  image/webp
video/mp4   video/webm  video/ogg  video/quicktime
```

Everything else — including `image/svg+xml`, PDFs, archives, source code, audio, Office formats — gets `Content-Disposition: attachment; filename="..."`. Filenames with non-ASCII or special characters additionally get the RFC 5987 `filename*=UTF-8''<encoded>` form, so Arabic / spaces / parentheses round-trip correctly.

**Hard rule:** any new MIME added to the upload validator (`app/api/v1/internal/upload/route.ts`) that is NOT in the inline-renderable allowlist above MUST automatically be served as `attachment` by this helper — verified by the test suite at `src/lib/storage/commands/__tests__/upload-public-asset.command.test.ts`.

**Specifically for incident #12 Step 3** (allowing source-code MIMEs like `application/javascript`, `text/x-python`, `application/x-tar`): no code change to `uploadPublicAsset` is needed — those MIMEs are absent from the inline-renderable set and will receive `Content-Disposition: attachment` automatically.

---

## What this PR did vs. did not

**Did (in repo):**

- Added `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, and `X-Frame-Options: DENY` to `next.config.ts` `headers()`. These cover **app** responses (everything served from `app.experts.com.sa`), providing defense-in-depth regardless of Traefik state. They do NOT cover CDN responses — Cloudflare configures those.
- This runbook for the edge-layer items below.

**Did not (out of repo — owner action required):**

- Cloudflare Transform Rule for `cdn.experts.com.sa/*` nosniff (item 1).
- CSP audit / lock-down (item 2). Full CSP is its own scoped incident; risk of breaking the app is too high to land as a security hotfix without a full third-party origin audit.
- R2 bucket policy verification (item 3).
- `Content-Disposition` round-trip verification + synthetic monitor (item 4).

---

## Hand-off

When the owner of each item completes verification:

1. Note completion in `~/brain/Action-Tracker.md` referencing this file.
2. If a config change was made, link the Cloudflare rule ID / Traefik file path / R2 bucket policy version here.
3. Once all four items are verified and any drift fixed, close incident #7 and update the related action tracker rows.

**Related incidents:** #2 (PR #308), #6 (PR #312).
