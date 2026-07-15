---
title: "EXP-52 — JSON-LD JSON.stringify does not escape </script>; stored XSS on public course pages"
date: "2026-05-20"
status: open
resolution: unknown
tags: [bug, security, xss, stored-xss, json-ld, critical, project/experts]
linear: "https://linear.app/experts/issue/EXP-52"
fingerprint: "43a087f194c2"
---

## Summary

`json-ld.tsx` embeds structured data as:

```html
<script type="application/ld+json">{JSON.stringify(data)}</script>
```

`JSON.stringify` does not escape `</script>` sequences. A course title or description containing `</script><script>alert(1)</script>` closes the script tag and injects arbitrary JavaScript into the page. Since course pages are public (no auth required for published courses), this is a stored XSS affecting all visitors.

**Severity: CRITICAL** — stored XSS on public pages, exploitable by any course creator.

## Repro

1. Create a course with title `Test</script><script>alert(document.cookie)</script>`.
2. Publish the course.
3. Visit the public course page as any user (including anonymous).
4. Observe: alert fires with cookie contents.

## Agent fingerprint

`<!-- agent-fp: 43a087f194c2 -->`

## Fix (not yet implemented)

Replace `JSON.stringify(data)` with output that escapes `</` sequences:

```ts
JSON.stringify(data).replace(/<\//g, '\\u003c/')
```

Or use a dedicated HTML-safe JSON serialiser. Verify the CSP nonce (added in commit `c00a8bfc`) is also applied to this script tag.

## Status

`open` — no PR yet. CRITICAL severity; needs immediate triage.

---

**Project:** [[Projects/Experts/Experts App/Bugs & Ops|Experts App — Bugs & Ops]]
