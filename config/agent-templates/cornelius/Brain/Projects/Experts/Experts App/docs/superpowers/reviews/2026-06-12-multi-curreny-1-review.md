---
title: "2026 06 12 multi curreny 1 review"
date: "2026-06-12"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/reviews/2026-06-12-multi-curreny-1-review.md"
---
For Experts, I would **not use WebSockets for FX rates**.

Your proposed Phase 3 is actually very close to what I'd recommend for a marketplace / learning platform where:

* SAR is the settlement currency.
* FX is display-only.
* Estimates can be several hours old without business impact.
* The platform must continue working if the FX provider disappears.

### Why WebSockets are the wrong tool here

WebSockets make sense when:

* Trading platforms
* Forex platforms
* Crypto exchanges
* Real-time dashboards
* Sub-second price sensitivity

Your use case is:

```
SAR 150
≈ €34.72
```

If tomorrow it becomes:

```
SAR 150
≈ €34.69
```

Nobody cares.

Even airlines, hotels, SaaS products, event platforms, and marketplaces usually don't stream FX rates to browsers.

The cost/complexity ratio is terrible:

```
WebSocket Provider
    ↓
Experts Server
    ↓
Redis
    ↓
Browser clients
```

vs.

```
Every 6h:
Provider
    ↓
Experts Server
    ↓
Redis

Read from Redis forever
```

The second architecture wins.

---

## What I'd change

### 1. Make stale-while-revalidate explicit

Instead of:

```ts
getDisplayRate("EUR")
```

I'd expose:

```ts
type FxRate = {
  currency: string;
  rate: number;
  asOf: string;
  stale: boolean;
};

export async function getDisplayRate(
  target: string,
): Promise<FxRate>;
```

Exactly as your spec says.

Then:

```ts
const fx = await getDisplayRate("EUR");

if (fx.stale) {
  // render SAR only
}
```

No exceptions.

No retries.

No UI errors.

Just SAR.

---

### 2. Use one snapshot, not per-currency caching

Store:

```json
{
  "base": "SAR",
  "asOf": "2026-06-12T00:00:00Z",
  "rates": {
    "USD": 0.266,
    "EUR": 0.231,
    "GBP": 0.197,
    "AED": 0.978
  }
}
```

under one Redis key.

Not:

```
fx:USD
fx:EUR
fx:GBP
```

Reason:

* one upstream request
* one cache refresh
* all currencies consistent

Much simpler.

---

### 3. Hard fallback should still return rate=1

I would return:

```ts
{
  currency: target,
  rate: 1,
  stale: true,
  asOf: lastKnownTimestamp
}
```

instead of:

```ts
null
```

because Phase 5 only needs:

```ts
if (stale) {
  render SAR;
}
```

No null checks.

No optional handling.

---

## Which feed?

For Experts today:

### Option 1 — Free feed

I'd choose this.

Examples:

* exchangerate.host
* open.er-api.com

Why?

The platform:

* settles in SAR
* invoices in SAR
* ledger in SAR
* charges in SAR

FX is merely:

```
≈ €34.72
```

You don't need:

* historical data
* enterprise SLA
* minute-level updates
* paid support

The fallback already protects you.

---

## Future-proofing

I would still abstract the provider:

```ts
interface FxProvider {
  getRates(base: string): Promise<FxSnapshot>;
}
```

Then:

```ts
class ExchangeRateHostProvider {}
```

Later:

```ts
class OpenExchangeRatesProvider {}
class CurrencyApiProvider {}
```

The rest of the system never changes.

That gives you the benefit of option 3 without delaying implementation.

---

## One thing I'd add to the spec

Store the **source timestamp** from the provider, not just the fetch timestamp.

Example:

```ts
{
  fetchedAt: "...",
  providerAsOf: "...",
  rates: {}
}
```

Some providers publish when the market data was generated.

Then your staleness logic becomes:

```ts
providerAsOf > 48h
```

instead of:

```ts
lastFetch > 48h
```

which is more accurate.

---

For the Experts roadmap, my recommendation would be:

1. Keep the Redis-based Phase 3 design.
2. Use a free REST feed.
3. Refresh every 12 hours.
4. Hard fallback after 48 hours.
5. No WebSockets.
6. Abstract the provider interface so a commercial feed can be swapped in later without touching the rest of the codebase.

That architecture will still be perfectly adequate even if Experts grows to hundreds of thousands of users, because FX conversion is display-only and all financial truth remains in SAR.

So the roadmap becomes:

✅ Ship now using a free feed.
✅ Build behind an interface.
✅ Swap providers later without touching business logic.
❌ Don't leave it as a fake/TODO provider.

Use a free FX provider behind a provider interface.

The initial implementation uses a free SAR-based exchange-rate feed. The provider is abstracted behind FxProvider so a commercial provider can be substituted later without changing cache, UI, or conversion logic.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
