---
title: "EXP-100 — harden `resolveTabbyEligibility` in `payment-eligibility.ts` to validate origin IP (Cloudflare IP range check "
date: "2026-05-24"
owner: "Logix (Ahmed)"
due: "2026-05-31"
priority: "high"
status: "open"
source: "[[Raw/sources/2026-05-24-experts-agent-digest.md]]"
tags: [action, project/experts]
category: "meta"
up: "[[Action-Tracker]]"
updated: "2026-07-15"
---

> ↑ [[Action-Tracker]]

EXP-100 — harden `resolveTabbyEligibility` in `payment-eligibility.ts` to validate origin IP (Cloudflare IP range check or shared secret header) in addition to `CF-IPCountry`; prevents header spoof bypass when origin is directly reachable

**Source:** [[Raw/sources/2026-05-24-experts-agent-digest.md]]
