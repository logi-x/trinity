---
title: "2026 06 30 per entity dynamic og design"
date: "2026-06-30"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/specs/2026-06-30-per-entity-dynamic-og-design.md"
---
# Per-entity dynamic OpenGraph images (on-demand, CDN-cached)

- **Date:** 2026-06-30 · **Revised:** 2026-07-01 (codebase self-audit applied)
- **Scope:** `apps/experts-app`
- **Status:** Design — awaiting approval before implementation

> **Revision note (2026-07-01).** Two rounds of change. **(a) Design reframe:** the creator's uploaded image is the **source of truth** — the dynamic card is a **fallback only** (used when no image exists), never an override. **(b) Three read-only audit passes** corrected the draft: fonts load from **CDN, not `public/fonts`** (gone); **rating is not cheaply available** (dropped from the default card); the privacy gate must check **`publishingStatus` as well as `visibility`**; money must use **server-safe** formatters (not the client `SaudiRiyal`/`MoneyAmount`); certificate OG needs a **`layout.tsx`** (mirroring courses) + a **registered i18n namespace**. The dead `generate-og-image.tsx` is retired. Details inline; §13 changelog.

## 1. Problem & goal

OG images today:

- **Marketing/template pages** → static per-locale PNGs on the CDN. Correct; out of scope.
- **Course/Event detail** → the creator's `thumbnailUrl` resized via `/_next/image` (`buildSocialPreviewImage()`). **`thumbnailUrl` is nullable** (`schema.prisma:368,953`) and **not required at publish**, so image-less courses/events exist; those fall back today to a **generic default illustration** (`illu("avatars/course/default.png")`) — a weak, identical-for-everyone card. There is **no dedicated social/OG image field**; the thumbnail is the only image.
- **Certificate verify pages** → no metadata, no OG at all. And the certificate query carries **no image**.

**The bespoke uploaded image is always the source of truth. Below it, the dynamic system is the guaranteed floor — a shareable page never falls back to a static generic default.** One rule across the whole site:

```
Any shareable page OG  =  bespoke uploaded asset     (source of truth — creator thumbnail, or a hand-crafted marketing PNG)
                       ?? dynamic generated card      (the UNIVERSAL FLOOR — on-brand, per-locale, always rendered)
                          └─ no static "global default" tier for shareable pages

  · Course / Event → thumbnailUrl ?? entity card        (card only when thumbnail is null)
  · Certificate    → entity card                        (no image exists → always)
  · Static/utility pages (contact, privacy, about, legal, …)
                   → hand-crafted PNG ?? preset card     (card for the long tail that has no bespoke PNG)
  · Anything else shareable with no preset yet
                   → generic dynamic brand card          (renderFallbackOg — still rendered, never a static default PNG)
```

**Rule (invariant):** if a page is shareable and it is *not* served by a bespoke uploaded asset, it **must** resolve to the dynamic system — an entity card, a preset card, or the generic dynamic brand card. The existing static "generic default" OG PNG is **retired for shareable pages**; the dynamic renderer's `renderFallbackOg()` takes its place, so even an un-presetted page is on-brand and per-locale rather than a frozen English default.

So this is **not** "make everything dynamic," and it **never overrides an uploaded image**. It's a **branded fallback** in two flavours, sharing one renderer:

- **Entity card** (`OGEntityCard`, new) — data-rich (title, instructor/host, price/date, brand frame) for course/event (null thumbnail) + certificate.
- **Template/preset card** (`OGImageContent` + `OG_PRESETS`, both already exist) — for static/utility pages that lack a bespoke PNG, driven by per-page **localized** copy. This removes the manual "export a PNG × 3 locales and upload it" step for the long tail.

**Bespoke static still wins where art direction matters:** hero marketing pages (home, courses index) that already have hand-made per-locale PNGs keep them — they are the "uploaded asset" tier. The dynamic template card is for the pages that otherwise show a generic default or nothing.

## 2. What ships (and what doesn't)

| Entity | Route | Today | This spec |
|---|---|---|---|
| **Certificate** | `/verify-certificate/[code]` (hex) | no metadata, no OG | **Net-new metadata + branded card — always** (Phase 1) |
| **Course** | `/courses/[id]` (uuid) | thumbnail, else generic default PNG | **thumbnail kept; branded card only when `thumbnailUrl` is null** (Phase 2) |
| **Event** | `/events/[id]` (uuid) | thumbnail, else generic default PNG | **thumbnail kept; branded card only when `thumbnailUrl` is null** (Phase 2) |
| **Static/utility pages** | `/contact`, `/privacy`, `/about`, legal, … | hand-made PNG for a few; generic default / nothing for the long tail | **Preset card when no bespoke PNG** (Phase 3) |
| Company business-card | `/company-profile/business-card/[handle]` | noindex, no OG, no avatar loaded | **Deferred** (noindex + no image data) |
| Instructor profile | — | no public route | **Deferred** (no route) |

Certificates lead because the card is **unconditionally** used there (no image to defer to), so the renderer must exist for them anyway. Course/Event then reuse the same renderer for the null-thumbnail case at near-zero marginal cost — a one-line resolver change, not an always-swap. Static/utility pages reuse it again via the **preset card** for their null-bespoke case.

> Phase 3 needs a quick inventory: enumerate the static/utility pages, mark which already have a **bespoke hand-crafted PNG** (keep those), and list the rest (contact, privacy, about, terms, legal, help, 404, …) that should get a preset card. That list drives the per-page metadata wiring.

## 3. Architecture decision

### 3a. Renderer: keep `next/og` (Satori) — do NOT adopt a headless browser

The card design lives comfortably inside Satori: an `<img>` with an absolute URL (Satori supports this), a title, a stat row — no CSS Grid, no feature Satori lacks. A headless-browser renderer on the self-hosted VPS would add a pooled Chromium, ~300ms–1s/render, and an ops liability to escape constraints we don't actually hit. Rejected. `next/og` `ImageResponse` is confirmed present (`next@^16.2.9`).

### 3b. Delivery: centralized **Route Handler**, not `opengraph-image.tsx` file convention

- **`opengraph-image.tsx` file convention** — idiomatic, but must live in each routable locale segment (`en|ar|es`) → ≈9 thin files, and it emits a *second* `og:image` alongside the `images` Course/Event metadata already sets (duplicate tags to reconcile).
- **Centralized Route Handler** — **chosen.** One handler owns rendering, caching headers, the publish/visibility gate, and font loading. Course/Event already mint `openGraph.images` manually in `generateMetadata`; we **swap the URL** to point at the handler. No per-locale fan-out, single caching policy, one place to gate privacy.

**Handler:** `app/api/og/[type]/[id]/route.ts`

- `type` ∈ `course | event | certificate | page` (zod enum)
- `[id]` = uuid (course/event), hex code (certificate), or **preset key** (page — validated against `OG_PRESETS` keys), per `type`
- `type=page` renders the **preset card** (`OGImageContent`); the others render the **entity card** (`OGEntityCard`)
- query: `?locale=en|ar|es` (default `en`), `?v=<version>` (cache-bust; see §6)
- `export const runtime = "nodejs"` (Satori font bytes + `fetch`; **not** edge)
- **Public, unauthenticated** — confirmed: `proxy.ts` short-circuits all `/api/**` before auth (`proxy.ts:524`, matcher `proxy.ts:581`); admin gating is per-route `requireAdmin()`, never global. Nothing extra to do.

Stable, fully-qualified URL per `(type, id, locale, v)` → Cloudflare caches by full URL. This is the "on-demand CDN caching": first request renders (~100–250ms Satori), every subsequent share is an edge hit.

## 4. Fonts (CDN-loaded, memoized) — **changed from draft**

`public/fonts/` **no longer exists**, and `src/components/og/generate-og-image.tsx` (which `readFile`s it) is **dead — zero real callers** (only referenced in an `/og-live` code-snippet string). It is **retired** in this work (deleted or repointed to the new loader).

New shared loader `src/lib/og/og-fonts.ts` fetches TTFs from the CDN and **memoizes per process**:

```ts
const FONTS_BASE = "https://cdn.experts.com.sa/static/brand/fonts";
const OG_FONTS = [
  { name: "DM Sans",    file: "DMSans-Regular.ttf",     weight: 400 }, // EN heading
  { name: "DM Sans",    file: "DMSans-Bold.ttf",        weight: 700 },
  { name: "Inter",      file: "Inter_18pt-Regular.ttf", weight: 400 }, // EN body
  { name: "Readex Pro", file: "ReadexPro-Regular.ttf",  weight: 400 }, // AR
  { name: "Readex Pro", file: "ReadexPro-Bold.ttf",     weight: 700 },
];

let cache: Promise<SatoriFont[]> | null = null;
export function loadOgFonts() {
  if (!cache) {
    cache = Promise.all(
      OG_FONTS.map(async (f) => {
        const res = await fetch(`${FONTS_BASE}/${f.file}`, { cache: "force-cache" });
        if (!res.ok) throw new Error(`OG font ${f.file}: ${res.status}`);
        return { name: f.name, weight: f.weight, style: "normal" as const, data: await res.arrayBuffer() };
      }),
    ).catch((e) => { cache = null; throw e; }); // never cache a rejected promise
  }
  return cache;
}
```

- **Fetched once per Node process** (module memo) → per-render font cost is **0 ms**; only the first render after a restart pays ~50–150 ms, and that request is a social-scraper bot already behind the edge cache. Not a user-facing latency.
- **`cache: "force-cache"`** layers Next's data cache so the bytes survive process restarts, not just the current process.
- **Retry-on-failure:** a rejected promise resets `cache` so one CDN blip doesn't poison OG rendering for the process lifetime.
- **Font set:** DM Sans + Inter (EN) + Readex Pro (Arabic). Almarai (not on CDN) and the Amiri family (serif/Quranic) are intentionally excluded.

## 5. File layout (vertical slice)

```
src/lib/og/
  og-fonts.ts                 # NEW — CDN font loader, memoized + force-cache (§4). Shared.
  entity-og-config.ts         # NEW — pure mappers: course/event/cert DTO + locale -> OGEntityCardProps. Unit-tested.
  render-og.ts                # NEW — wraps ImageResponse: loadOgFonts() + a card (<OGEntityCard> for entities,
                              #        <OGImageContent> for type=page presets), Cache-Control (ImageResponse `headers`),
                              #        1200x630 + fonts. Also renderFallbackOg() -> generic brand card.
  page-presets.ts             # NEW (Phase 3) — localized preset copy for static pages (contact/privacy/about/…);
                              #        supersedes the English-only OG_PRESETS strings via i18n. OGImageContent reused as-is.
  entity-og-url.ts            # NEW — buildEntityOgUrl({type,id,locale,version}) -> absolute URL via getPublicBaseUrl();
                              #        returns undefined if base unconfigured (caller omits images). Must NOT hardcode
                              #        origin/CDN — eslint no-restricted-syntax mandates the helper (eslint.config.mjs:135).
  __tests__/entity-og-config.test.ts   # NEW — mapper unit tests (node env)

src/components/og/
  og-entity-card.tsx          # NEW — Satori-safe entity card (image + title + subtitle + stats + brand).
                              #        Reuses the ExpertsLogoSVG + gradient tokens from og-image-content.tsx.
                              #        Marketing OGImageContent left untouched. generate-og-image.tsx retired.

app/api/og/[type]/[id]/
  route.ts                    # NEW — GET: zod-validate -> load entity (existing queries) -> publish+visibility gate
                              #        -> map -> renderEntityOg(); not-found/unpublished/private/invalid -> renderFallbackOg().
  __tests__/route.test.ts     # NEW — mocks queries; asserts 200 + image/png + long Cache-Control; gated -> fallback short-cache.

src/i18n/messages/{en,ar,es}/ogCard.json   # NEW — eyebrow/badge/stat labels; REGISTER "ogCard" in src/i18n/request.ts namespaces[]
```

Wiring into existing metadata (no new pages except the cert layout):

- **Certificate (Phase 1):** add `app/(i18n)/_shared/verify-certificate/[code]/verify-certificate-layout.tsx` exporting `generateMetadata` (net-new) **plus** per-locale `app/(i18n)/{en,ar,es}/verify-certificate/[code]/layout.tsx` re-exports — mirroring the courses `course-detail-layout.tsx` + locale-`layout.tsx` pattern (metadata lives on the **layout**, not the page). It sets title/description + `openGraph.images = buildEntityOgUrl({type:"certificate", id: code, locale})`. Always uses the card (no image to defer to).
- `src/lib/courses/utils/course-metadata.ts` **(Phase 2)** — **do not swap unconditionally.** Resolve the image as `thumbnailUrl` when present, else `buildEntityOgUrl({type:"course", id, locale, version: course.updatedAt})`. The existing `thumbnailUrl → buildSocialPreviewImage` path stays as-is; only the **null-thumbnail branch** (currently the generic default illustration) switches to the branded card. If `getPublicBaseUrl()` is undefined, keep today's default-illustration fallback.
- `src/lib/events/utils/event-metadata.ts` **(Phase 2)** — same null-thumbnail resolver for events (`version` from `updatedAt`).

## 6. The entity card component (`OGEntityCard`)

Satori-safe (inline styles, flexbox, absolute-URL `<img>`), brand tokens (logo SVG, gradient) shared with `OGImageContent`. Props:

```ts
interface OGEntityCardProps {
  locale: "en" | "ar" | "es";
  eyebrow: string;            // category name / "Verified Certificate" / event date
  title: string;             // entity title/name (headline) — entity data, may be Arabic
  subtitle?: string;         // instructor/host name, or "Awarded to <name>"
  imageUrl?: string;         // absolute https thumbnail/avatar; omitted -> brand-gradient placeholder (certs are always imageless)
  stats?: Array<{ label: string; value: string }>;  // see §6a — NO rating by default
  badgeText: string;         // CTA: "View Course" / "Register" / "Verify Certificate"
  accentColor: string;       // per-type accent (course=blue, event=cyan, certificate=violet)
}
```

Layout: brand header (logo + eyebrow chip) → two-column body: left = framed `imageUrl` or gradient placeholder; right = title (clamped 2–3 lines) + subtitle + stat row → bottom badge. **RTL when `locale === "ar"`:** `direction: rtl`, swap column order, Readex Pro font. Numbers/prices/dates forced `dir="ltr"` even on AR cards.

### 6a. Stats — what's actually available (**corrected**)

Rating is **NOT** in `courseMetadataSelect` / `eventMetadataSelect` — the draft's "⭐4.8" was wrong. The default stat row uses only fields already selected:

| Entity | Stats (from existing select) |
|---|---|
| Course | enrollments `course._count.enrollments` (completed) · price · category |
| Event | registrations `event._count.registrations` (completed) · start date · price |
| Certificate | recognition type · issued date · course title (no image, no price) |

- **Rating is opt-in, not free:** it needs a separate `aggregateRatings("course"|"event", [id])` call (`src/lib/aggregate-engagement.ts:139`). Add it later behind a small extra query if we want ⭐ on the card; **out of Phase-1 default**.
- **Money is server-safe only:** use `displayPrice()` (applies ×1.15 VAT → gross, i.e. what buyers see) / `formatPrice()` from `src/lib/utils.ts`. Do **NOT** use `SaudiRiyal` / `MoneyAmount` (`src/components/ui/*`) — they're client components with an SVG glyph and won't render in Satori. Render the currency as text (`"SAR"`; multi-currency is OFF, `currency` defaults to SAR).
- `isFree` → render a "Free" pill instead of a price.

## 7. Caching & invalidation

**Successful public render** (set via the `ImageResponse` `headers` option — supported in `@vercel/og`):

```
Cache-Control: public, max-age=300, s-maxage=86400, stale-while-revalidate=604800
```

(browser 5 min · CDN 1 day · serve-stale-and-revalidate 7 days).

**Fallback (missing/unpublished/private/invalid):**

```
Cache-Control: public, max-age=60, s-maxage=300
```

short, so a transient miss self-heals.

**Invalidation = versioned URL.** Metadata appends `?v=<epoch of entity.updatedAt>`. Entity changes → `updatedAt` changes → OG URL changes → Cloudflare treats it as a new asset and re-renders once. Stable URL for unchanged content, automatic bust on change — no manual purge, no webhook. (Certificates are immutable → no `v`.)

## 8. Privacy / correctness gates (**tightened**)

- **Publish + visibility, both.** Render the branded card **only if `publishingStatus === "published"` AND `visibility ∈ {public, unlisted}`.** Otherwise → `renderFallbackOg()` (generic brand card, 200, short cache).
  - Rationale: `visibility` alone is insufficient — a draft/unpublished course 404s on the page (`course-detail.handler.ts:50`) and an unpublished **event returns 403 and leaks existence** (`event-detail.handler.ts:82`). The OG endpoint must not render a draft's title/stats into a public, edge-cached image.
  - `private` (even if published) → fallback (needs owner/enrolled/`ContentAccessGrant`; never render publicly). `unlisted` renders (link-shared by design).
- **Certificate:** the verification code is an opaque public capability (`^[a-f0-9]{16,64}$`, 32 minted at issuance, no user id embedded). The public verify page already shows recipient name + course + recognition type + issued date — the card shows exactly those, nothing more (no email, no internal ids). No image is available from the query → imageless card by design.
- **Input validation:** zod on `type` (enum), `id` (uuid for course/event; hex regex for certificate), `locale` (enum, default `en`). Invalid → fallback, never 500.
- **Absolute URL stability:** metadata uses `getPublicBaseUrl()` (nullable, never throws) — **not** the header-derived `getRequestBaseUrl()` — so the cached URL is stable. Undefined base (prod misconfig) → omit `openGraph.images` gracefully. (`getAppBaseUrl()` throws; don't use it for metadata.)
- **No DB write, no auth, idempotent GET.**

## 9. i18n / RTL — the one real render risk

The old `OGImageContent` **hides Arabic** in Satori. Entity cards **cannot** hide the title — an Arabic course's title must render in Arabic. Mitigation:

1. Render the title as a single run with the Readex Pro AR font + `direction: rtl` + `unicodeBidi: plaintext` (the old word-reversing hack was for multiline/mixed runs; a single clamped title generally renders correctly in current Satori with a real Arabic font loaded).
2. **Verify in `/og-live`** with a real Arabic course title before Phase 1 ships (extend the preview tool with an "entity card" mode — Phase 3, recommended as the verification surface).
3. If Satori RTL still mis-orders, fallback: render AR title without bidi reshaping, or letterbox — decided at verification time; flagged as residual.

New strings go in a **registered** namespace: create `src/i18n/messages/{en,ar,es}/ogCard.json` and add `"ogCard"` to the `namespaces` array in `src/i18n/request.ts` (unregistered namespaces don't load). Server-side, use `getTranslations("ogCard")` + `getLocale()` from `next-intl/server` (the established metadata-builder pattern).

`experts:check` (tsc/lint/prettier) **cannot** catch a Satori render failure — a real fetch of the handler in dev + visual check is mandatory before merge.

## 10. Testing

- **Pure mappers** (`entity-og-config.ts`): unit-test course/event/cert DTO + locale → `OGEntityCardProps` (title selection, stat formatting incl. `displayPrice` VAT + `isFree` pill, AR vs EN strings, missing-thumbnail → placeholder). Highest-value coverage. `DATABASE_URL=postgresql://localhost/experts_test pnpm exec vitest run`.
- **Route handler** (`route.test.ts`): mock queries; assert (a) published+public → 200, `image/png`, long `Cache-Control`; (b) **unpublished/private → fallback**, short cache; (c) bad uuid/locale → fallback, not 500; (d) certificate by code → 200.
- **Manual smoke (required, not automated):** `GET /api/og/course/<id>?locale=en` and `?locale=ar` in dev; eyeball brand, thumbnail, stats, Arabic title. Social debuggers (FB/Twitter/LinkedIn) on one real course post-deploy.
- All three locale JSONs parse; `ogCard` registered.

## 11. Phasing

1. **Phase 1 — Certificate** (the card is *always* used here → the renderer must exist for it; highest viral value; net-new). Builds the whole shared spine: `og-fonts` + `OGEntityCard` + cert mapper + `render-entity-og` + handler (`type=certificate`) + `entity-og-url` + cert `layout.tsx`/`generateMetadata` + retire `generate-og-image.tsx` + `ogCard` i18n + tests.
2. **Phase 2 — Course + Event fallback** (reuse the Phase-1 spine; add `course`/`event` to the handler enum + mappers; wire the **null-thumbnail resolver** in the two metadata builders). Near-zero marginal build; never touches the creator-thumbnail path.
3. **Phase 3 — Static/utility page preset cards + retire the static default** (add `type=page` to the handler → `OGImageContent`; localize presets into `page-presets.ts`; per-page metadata resolver `bespoke PNG ?? preset card`). Needs the page inventory (§2). **Also sweep every metadata builder that currently points at a static generic-default OG PNG and repoint its fallback to the dynamic floor** (`renderFallbackOg` / a `type=page` default) — enforcing the §1 invariant. Removes the manual PNG-per-locale upload for the long tail.
4. **Phase 4 — `/og-live` preview mode** for both card kinds (recommended; the design + RTL verification surface).

## 12. Definition of Done (per phase)

- [ ] Branded card renders in **en, ar, es**; real Arabic title verified in dev via a live handler fetch.
- [ ] Handler: `runtime="nodejs"`, public, zod-validated, **publish+visibility gated**, never 500s (fallback card).
- [ ] Fonts load from CDN, memoized + `force-cache`; first-render cost measured once, per-render cost ≈ 0.
- [ ] Caching headers exactly as §7; versioned-URL bust verified (edit entity → new `?v=` → re-render).
- [ ] **Creator thumbnail untouched:** an entity *with* `thumbnailUrl` still emits that exact image (regression test); only the **null-thumbnail** branch resolves to the handler URL via `getPublicBaseUrl()`. Twitter card intact; graceful when base URL undefined; no hardcoded origin (eslint clean).
- [ ] Mappers + handler tested (node env); `ogCard` registered; 3 locale JSONs parse; `pnpm experts:check` clean for touched files.
- [ ] No unpublished/private entity's data renders into a cacheable image (test proves fallback).

## 13. Audit corrections applied (2026-07-01)

| # | Draft said | Reality | Change |
|---|---|---|---|
| 0 (reframe) | Branded card **replaces** course/event OG | Creator `thumbnailUrl` is source of truth (nullable, no dedicated OG field) | Card is **fallback-only**: `thumbnail ?? card`; certs (imageless) always. Certs → Phase 1 |
| 1 | Fonts from `public/fonts` via `fs` | Dir gone; `generate-og-image.tsx` dead (0 callers) | CDN loader `og-fonts.ts`, memoized + `force-cache`; retire dead file |
| 2 | Card shows "⭐4.8" rating | Rating not in metadata select | Drop from default; opt-in via `aggregateRatings` |
| 3 | Gate on `visibility` only | Unpublished course 404s, event 403 leaks | Gate on `publishingStatus === published` **AND** visibility |
| 4 | "SAR via existing money helpers" | `SaudiRiyal`/`MoneyAmount` are client-only | Use server-safe `displayPrice`/`formatPrice`; render "SAR" text |
| 5 | Cert metadata "in its layout" | No layout.tsx exists there | Add shared + per-locale `layout.tsx` (mirror courses) |
| 6 | New `ogCard.*` keys | Namespaces must be registered | Register `ogCard` in `src/i18n/request.ts` |
| 7 | AR font "Readex Pro / Tajawal" | Only Readex Pro on CDN | Readex Pro only |
| — | `/api/og/**` public? | Confirmed: `proxy.ts` bypasses all `/api/**` | No change (assumption held) |

## 14. Out of scope

- Art-directed hero pages that keep a **bespoke** hand-crafted PNG (home, courses index, …) — those are the source-of-truth tier and stay as-is. (But the generic *static default* they fell back to is retired — see the invariant in §1; Phase 3 sweeps those references to the dynamic floor.)
- Company business-card & instructor-profile cards (deferred — no image data / no route).
- Rating on cards (opt-in follow-up).
- Migrating the static template PNGs to build-time generation (separate follow-up).

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
