---
title: "EXP-67 — Creator curriculum upload UX & auth gaps: silent image rejection, quiz 403, lesson-resource position"
date: "2026-05-21"
status: open
resolution: unknown — PR open and In Review
tags: [bug, security, authorization, upload, ux, curriculum, project/experts]
linear: "https://linear.app/experts/issue/EXP-67"
fingerprint: "713f7dfac482"
---

## Summary

Incident#15 surfaced during smoke-testing: (1) image uploads via lesson-resource and module-asset dropzones silently fail with no error/toast; (2) quiz-question file upload returns 403; (3) lesson-resource `position` uniqueness constraint violated on concurrent creates.

## Repro

1. In creator curriculum editor, attempt to upload an image via lesson-resource dropzone
2. Observe: no error shown, no progress, no success — silent failure
3. Attempt quiz-question image upload — observe 403
4. Create multiple lesson resources rapidly — observe position uniqueness violation

## Agent fingerprint

`<!-- agent-fp: 713f7dfac482 -->`

## Status

`open` — PR `fix/lesson-resource-panel-allow-images-20260517` in review. Action-Tracker deadline 2026-05-25.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
