---
title: "Experts Presentation No Inline Preview"
date: "2026-04-21"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts presentation lessons no longer use inline preview

Date: 2026-04-21
Repo: `/home/logix/experts`
App: `apps/experts-app`

## Decision

Removed inline presentation preview for the `presentation` lesson type in both creator and learner UI.

## Why

- uploaded `.pptx` and similar files can trigger browser download behavior instead of a real preview
- this creates misleading UX because the UI suggests embed support that is not reliable
- the product distinction is already:
  - `PDF` for reliable inline viewing
  - `Presentation` for downloadable files or external deck links

## Result

- creator view now shows an attachment/open action instead of an iframe
- learner view now shows an attachment/open action instead of an iframe
- presentation copy now explicitly frames the asset as an attachment/external link

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
