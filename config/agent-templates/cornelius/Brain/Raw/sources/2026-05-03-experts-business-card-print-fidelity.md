---
title: "Experts Business Card Print Fidelity"
date: "2026-05-03"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts business card print fidelity

Date: 2026-05-03
Project: Experts company profile collateral

## Summary

Adjusted the Next.js TSX business-card generator to more closely match the InDesign print-ready export for 3.5 in × 2 in cards.

## Notes

- Browser-exported print cards should use physical CSS dimensions with `@page { size: 3.5in 2in; margin: 0; }`, not scaled large pixel artboards.
- The InDesign export page order is dark logo back first, white contact front second.
- Chrome PDF output rendered QR SVG stroke paths differently from InDesign QR modules; generating a PNG data URL for the QR is more print-stable.
- SVG logo components were unreliable in Chrome PDF output for these card exports; stable PNG logo assets produced closer print results.
- The final comparison was rendered at 300 DPI using Poppler, and measured content bounds landed within a few pixels of the InDesign export.

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
