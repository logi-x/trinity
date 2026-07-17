---
title: "Truth-tested locally: `curl -sI http://localhost:3025/en \\ grep -oE 'script-src [^;]+'` confirmed `'unsafe-eval'` presen"
date: "2026-05-17"
owner: "Logix (Ahmed)"
due: "2026-05-19"
priority: "medium"
status: "open"
source: "Actions from Experts Platform Review Call — 22 May 2026"
tags: [action, project/experts]
category: "meta"
up: "[[Action-Tracker]]"
updated: "2026-07-15"
---

> ↑ [[Action-Tracker]]

Truth-tested locally: `curl -sI http://localhost:3025/en \ grep -oE 'script-src [^;]+'` confirmed `'unsafe-eval'` present in dev. **Production truth-test outstanding** — after `fix/lesson-resource-panel-allow-images-20260517` PR merges + deploys, curl `https://app.experts.com.sa/en` and confirm `'unsafe-eval'` absent.

**Source:** Actions from Experts Platform Review Call — 22 May 2026
