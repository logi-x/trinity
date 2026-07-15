---
title: "EXP-280 — Community post PUT allows owner to reverse admin unpublish — moderation bypass"
date: "2026-06-02"
status: open
resolution: unknown
tags: [bug, security, community, authorization, moderation, project/experts]
linear: "https://linear.app/experts/issue/EXP-280/security-community-post-put-allows-owner-to-reverse-admin-unpublish"
fingerprint: "10787fbfd313"
---

## Summary

`app/api/v1/community/posts/[id]/route.ts` PUT handler spreads `body.isPublished` into the Prisma update when the field is present. An owner whose post was administratively unpublished can call `PUT /api/v1/community/posts/<uuid>` with `{"isPublished": true}` and re-publish the post, bypassing the moderation action.

## Root cause

`apps/experts-app/app/api/v1/community/posts/[id]/route.ts/PUT` — `...(body.isPublished !== undefined && {isPublished: body.isPublished})`. No guard that restricts non-admin callers from setting `isPublished: true`. Admin isPublished control should be gated on DB-fresh `getUserPermissions()`.

Fix: only allow `isPublished: true` for callers with DB-fresh `isAdmin === true`; owner writes to `isPublished` should be ignored or rejected with 403.

## Agent fingerprint

`<!-- agent-fp: 10787fbfd313 -->`

## Status

`open` — Backlog (Medium). Moderation-bypass class; owner can undo admin unpublish decision.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
