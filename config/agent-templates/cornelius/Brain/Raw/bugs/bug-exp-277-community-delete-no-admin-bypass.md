---
title: "EXP-277 — Community posts DELETE has no admin bypass — admin moderation and data-erasure blocked"
date: "2026-06-02"
status: open
resolution: unknown
tags: [bug, community, authorization, moderation, project/experts]
linear: "https://linear.app/experts/issue/EXP-277/bug-community-posts-delete-has-no-admin-bypass-admin-moderation-and"
fingerprint: "300e6e064c43"
---

## Summary

`app/api/v1/community/posts/[id]/route.ts` DELETE handler checks `if (post.userId !== session.user.id)` and returns 403. No admin bypass is attempted. An admin cannot delete harmful posts for moderation, cannot perform GDPR erasure on behalf of a user, and cannot remove spam. This is a content-safety and legal compliance gap.

## Root cause

`apps/experts-app/app/api/v1/community/posts/[id]/route.ts/DELETE` — ownership check `post.userId !== session.user.id` with no `|| isAdmin` branch. The EXP-241 sweep (PR #756) added DB-fresh `getUserPermissions()` for the PUT handler but the DELETE handler was filed as a separate follow-up.

Fix: add DB-fresh `getUserPermissions()` check and allow delete when `isAdmin === true`.

## Agent fingerprint

`<!-- agent-fp: 300e6e064c43 -->`

## Status

`open` — Backlog (High). Content moderation and GDPR erasure blocked for admins.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
