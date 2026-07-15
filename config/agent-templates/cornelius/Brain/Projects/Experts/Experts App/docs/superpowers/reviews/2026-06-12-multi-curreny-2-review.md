---
title: "2026 06 12 multi curreny 2 review"
date: "2026-06-12"
updated: "2026-07-15"
tags: ["projects"]
category: "projects"
source: "normalized"
source_id: "Projects/Experts/Experts App/docs/superpowers/reviews/2026-06-12-multi-curreny-2-review.md"
---
Yes, this is aligned with what I would ship, with only a few small refinements.

### What I agree with

✅ Free provider behind an abstraction.

✅ One Redis snapshot containing all rates.

✅ `getDisplayRate()` returning a non-null object.

✅ `stale` as data, not exceptions.

✅ SAR short-circuit.

✅ No WebSockets.

✅ No coupling to payments, settlements, invoices, payouts, ledgers, or PSPs.

✅ Phase 3 ending with a provider that nothing consumes yet.

---

### One thing I'd slightly adjust

Your current wording says:

> stale snapshot, dead Redis, upstream throw → all return { rate: 1, stale: true|false, ... }

I would make the contract more explicit:

#### SAR target

```ts
{
  currency: "SAR",
  rate: 1,
  stale: false,
}
```

always.

#### Non-SAR target + failure

```ts
{
  currency: target,
  rate: 1,
  stale: true,
}
```

always.

That gives a very strong invariant:

```ts
if (fx.stale) {
  // ignore rate entirely
  renderSAROnly();
}
```

No ambiguity.

---

### Another small refinement

I would not hardcode the provider name into the directory structure:

Current:

```txt
providers/
  exchangerate-host.provider.ts
```

I'd also add:

```txt
providers/
  exchangerate-host.provider.ts
  index.ts
```

Then `fx-rates.ts` imports:

```ts
import { fxProvider } from "./providers";
```

instead of:

```ts
import { ExchangeRateHostProvider } from "./providers/exchangerate-host.provider";
```

When you later move to:

* Fixer
* CurrencyAPI
* OpenExchangeRates

the diff is isolated to one file.

---

### Stale-while-revalidate detail

This part is the only area I'd be careful about:

> serves cached + flags background refresh

In Next.js/Laravel-style request lifecycles, "background refresh" can be surprisingly complicated.

I would keep it simple:

```ts
if (age > SOFT_TTL) {
  refresh asynchronously;
}

return cached;
```

and if async refresh fails:

```ts
ignore
```

The request path must never wait for refresh.

---

### One thing I would add to the tests

You currently have:

* cache hit
* cache miss
* stale snapshot
* redis unavailable
* provider failure

I'd add:

```txt
requested currency missing from snapshot
```

Example:

```ts
getDisplayRate("TRY")
```

but snapshot only contains:

```json
{
  "USD": 0.266,
  "EUR": 0.231
}
```

Expected:

```ts
{
  currency: "TRY",
  rate: 1,
  stale: true,
}
```

This protects you when a provider unexpectedly drops a currency.

---

### My only architectural concern

This line:

```ts
stale = (now − providerAsOf) > 48h
```

is correct **if the provider exposes a reliable timestamp**.

Many free providers either:

* don't expose one,
* expose only the fetch date,
* expose inconsistent timestamps.

So I'd specify:

```ts
const effectiveAsOf =
  providerAsOf ?? fetchedAt;
```

and base all calculations on `effectiveAsOf`.

You mention this in prose, but I'd make it part of the implementation contract.

---

Other than those minor refinements, I'd consider the Phase 3 scope locked and implementation-ready. It's appropriately conservative for Experts' "SAR is the only real currency" architecture and leaves plenty of room to evolve later if you ever introduce true multi-currency charging or payouts.

---

**Docs:** [[Projects/Experts/Experts App/docs|Experts App — docs]]
