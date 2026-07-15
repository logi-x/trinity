---
title: "EXP-97 — BullMQ removeOnComplete evicts embedding jobs before results are processed"
date: "2026-05-24"
status: resolved
resolution: "PR #453: set removeOnComplete: { age: 3600, count: 100 } and removeOnFail: { age: 86400 } so completed jobs survive long enough for result handlers to read them before eviction."
tags: [bug, ai, embeddings, bullmq, project/experts]
linear: "https://linear.app/logi-x/issue/EXP-97"
fingerprint: "agent-fp:R5-exp80-bullmq-ttl-001"
---

## Summary

BullMQ `removeOnComplete: true` was evicting embedding jobs immediately upon completion, before the result handler could read job output. This caused silent embedding misses — jobs succeeded but their vector outputs were never written to `content_embeddings`.

## Root cause

`EmbedJob` in the AI worker was configured with `removeOnComplete: true`. BullMQ removes completed jobs synchronously after the processor returns, before the `completed` event listener fires in the same event loop tick. Result: the event handler attempted to read a job that no longer existed.

## Agent fingerprint

`<!-- agent-fp:R5-exp80-bullmq-ttl-001 -->`

## Status

Resolved — PR #453 merged 2026-05-24.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
