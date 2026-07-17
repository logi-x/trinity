---
title: "Tabby payment gateway is KSA-only; all checkout, verify, and webhook paths that invoke Tabby must enforce the KSA geo-re"
date: "2026-05-24"
decision: "Tabby payment gateway is KSA-only; all checkout, verify, and webhook paths that invoke Tabby must enforce the KSA geo-restriction (CF-IPCountry=SA) using a Cloudflare-validated header or origin-IP all"
stakeholders: "Logix, Security"
review_by: "2026-08-24"
source: "[[Raw/sources/2026-05-24-experts-agent-digest.md]]"
tags: [decision, project/experts]
category: "meta"
updated: "2026-07-15"
---

**Decision:** Tabby payment gateway is KSA-only; all checkout, verify, and webhook paths that invoke Tabby must enforce the KSA geo-restriction (CF-IPCountry=SA) using a Cloudflare-validated header or origin-IP allowlist. Staging/dev environments must require `CF_ORIGIN_SECRET` to prevent geo-spoofing in pre-production testing.

**Rationale:** EXP-99/EXP-100/EXP-123/EXP-129. Direct-origin requests bypass Cloudflare and can spoof `CF-IPCountry`. Without a shared secret validating the Cloudflare edge, the restriction is security theatre.

**Stakeholders:** Logix, Security

**Source:** [[Raw/sources/2026-05-24-experts-agent-digest.md]]
