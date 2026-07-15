---
title: "`proxy.ts` is the sole authoritative CSP source; Traefik `headers.contentSecurityPolicy` must be removed. The app now ow"
date: "2026-05-22"
decision: "`proxy.ts` is the sole authoritative CSP source; Traefik `headers.contentSecurityPolicy` must be removed. The app now owns the entire CSP header; any Traefik override silently doubles or duplicates CS"
stakeholders: "Logix, Security"
review_by: "2026-06-01"
source: "[[Raw/sources/2026-05-22-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** `proxy.ts` is the sole authoritative CSP source; Traefik `headers.contentSecurityPolicy` must be removed. The app now owns the entire CSP header; any Traefik override silently doubles or duplicates CSP directives, breaking the security model. Traefik config should be updated immediately after confirming the app CSP is correct in production.

**Rationale:** EXP-71 shipped. App-owned CSP is correct. Traefik static header is now a liability, not a safeguard.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-22-experts-agent-digest.md]]
