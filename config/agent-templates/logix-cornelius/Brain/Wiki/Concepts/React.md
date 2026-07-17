---
title: "React"
date: "2026-04-10"
updated: "2026-05-09"
tags: ["entity", "topic", "tech/react"]
category: "entity/topic"
source: "generated"
source_id: "Wiki/Concepts/React.md"
---

# React

React in this vault usually means component architecture and state flow inside the Experts App, not generic framework tutorials. It sits under most UI, form, and interaction-heavy conversations.

## Typical discussion areas

- component decomposition
- state ownership and prop boundaries
- interactive UI behavior
- performance and rerender churn
- making complex product flows still feel maintainable

## Practical lens

If a conversation references React here, the real issue is often architecture: responsibilities are too mixed, state is in the wrong place, or component behavior no longer matches the product flow.

## Experts App notes

- React 19 lint rejects the old hydration gate pattern `useEffect(() => setMounted(true), [])` because it synchronously sets state in an effect. For SSR-safe client-only snapshots, use `useSyncExternalStore(noopSubscribe, () => true, () => false)` so the server snapshot is false and the hydrated client snapshot becomes true without effect-driven state.
- React 19+ also rejects syncing render-derived values with `useEffect(() => setState(...), [propsOrState])`. Prefer deriving values during render, using `useMemo` only for expensive derivations, resetting state at explicit user/action boundaries, or using a keyed remount when identity changes. Effects are for external subscriptions and imperative integrations, not props-to-state synchronization.

## Related

- [[Wiki/Concepts/Next.js]]
- [[Wiki/Concepts/TypeScript]]
- [[Wiki/Concepts/CSS]]
- [[Wiki/Concepts/Testing]]
