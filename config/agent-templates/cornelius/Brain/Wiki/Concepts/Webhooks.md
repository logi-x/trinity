---
title: "Webhooks"
date: "2026-04-10"
updated: "2026-04-13"
tags: ["entity", "topic", "topic/webhooks", "webhook"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/Webhooks.md"
---

# Webhooks

Webhooks in this vault are mostly external-to-Experts callbacks: payment provider events, async status updates, and system-to-system signals that must be accepted safely, logged clearly, and replayed without damage.

## Core rules

- verify origin before trusting payloads
- make handlers idempotent
- persist enough data to debug or replay events later
- treat webhook receipt as transport, not business completion

## Experts context

The most important webhook-related conversations revolve around:

- payment lifecycle updates
- reconciliation after external provider callbacks
- keeping internal state aligned when a provider succeeds or fails asynchronously
- debugging "captured but not finalized" style incidents

## Recommended flow

1. Receive and verify the webhook.
2. Record raw event metadata for traceability.
3. Translate the payload into an internal domain event.
4. Apply business logic once, guarded against duplicates.
5. Emit follow-up notifications or repair actions if downstream work fails.

## Common failure modes

- duplicate delivery causing double-processing
- provider success not mapped to internal success
- missing audit trail for partial failures
- weak retry behavior when dependent services fail

## Provider-specific gotchas

### Tabby

- `TABBY_WEBHOOK_SECRET` is REQUIRED in production. The webhook verifier fails closed when the
  secret is unset in `NODE_ENV=production`. Without it, `/api/webhooks/tabby` throws on every
  request and no enrollments will complete.
- Decided 2026-05-13 after a forged-payload incident: the previous fail-open path let
  unsigned requests through silently in prod. See `apps/experts-app/src/notifications/channels/webhook/providers/tabby.provider.ts`.
- Operational: before any prod deploy, confirm the secret is present in the environment
  store. Rotate the secret in Tabby dashboard and the env store in lockstep.

## Related

- [[Wiki/Concepts/APIs]]
- [[Wiki/Concepts/Payments]]
- [[Wiki/Concepts/Noon Payments]]
- [[Wiki/Concepts/Access Control]]
