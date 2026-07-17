---
title: "EXP-75 — Certificate POST: caller-supplied courseTitle written to DB — credential title forgery"
date: "2026-05-22"
status: open
resolution: unknown
tags: [bug, security, authorization, business-logic, certificates, project/experts]
linear: "https://linear.app/experts/issue/EXP-75/bug-certificate-post-caller-supplied-coursetitle-written-to-db"
fingerprint: "b9f675e5f4db"
---

## Summary

`POST /api/v1/user/certificates` writes the caller-supplied `courseTitle` field directly to the certificate record without reading the actual course title from the database. Any user who has legitimately completed any course can forge credential titles — issuing a certificate that reads, for example, "Advanced Machine Learning" for a "Basic JavaScript" course.

## Repro

1. Complete any course (enrollment status `completed`).
2. Call `POST /api/v1/user/certificates` with:
   ```json
   { "courseId": "<legitimate-courseId>", "userName": "Dr. John Smith", "courseTitle": "Advanced Machine Learning PhD Program" }
   ```
3. A certificate is created with the forged title. The certificate PDF/verification page reflects the attacker-controlled string.

## Impact

Credential fraud. A user can mint certificates claiming completion of high-value courses they never took, using their own completed enrollment in any free/cheap course as the gate.

## Agent fingerprint

`<!-- agent-fp: b9f675e5f4db -->`

## Status

`open` — In Progress as of 2026-05-22T06:34:38Z. R3 has started working on this; no PR yet.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
