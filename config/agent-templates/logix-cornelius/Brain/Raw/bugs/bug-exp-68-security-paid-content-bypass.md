---
title: "EXP-68 — Paid-content bypass: forge course completion without payment + quiz access without enrollment + Noon credentials logged"
date: "2026-05-21"
status: open
resolution: unknown — no PR yet
tags: [bug, security, authorization, business-logic, paid-content, credentials, urgent, project/experts]
linear: "https://linear.app/experts/issue/EXP-68"
fingerprint: "95b437cb68ba"
---

## Summary

Three findings from incident#16:
1. Progress/watch/certificate endpoints accept requests without verifying `enrollment.status === completed`; unenrolled users can forge completion
2. Quiz start/resume/submit accessible without active enrollment in paid course
3. `noon.client.ts` contains `console.log(makeNoonAuthHeader())` which writes Noon merchant credentials (API key + secret) to runtime logs in production

## Repro

1. Do not enroll in a paid course; POST to `/api/v1/courses/<id>/progress` — observe success
2. POST to `/api/v1/courses/<id>/modules/<m>/lessons/<l>/watch-progress` — observe success
3. Check production logs for `makeNoonAuthHeader` output — observe credentials in plaintext

## Agent fingerprint

`<!-- agent-fp: 95b437cb68ba -->`

## Status

`open` — CRITICAL. No PR yet. Noon credential rotation required immediately. Action-Tracker deadline 2026-05-23 for credentials, 2026-05-30 for access gates.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
