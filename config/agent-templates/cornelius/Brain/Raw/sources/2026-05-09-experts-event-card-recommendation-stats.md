---
title: "Experts Event Card Recommendation Stats"
date: "2026-05-09"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts event card recommendation stats placement

Date: 2026-05-09
Project: Experts

## Summary

Adjusted the default `EventCard` layout used by "You might also like" so view, share, and bookmark counts align like the default `CourseCard`.

## Implementation

Moved event interaction counts out of the category chip row and into a bottom-right meta column inside `apps/experts-app/src/components/events/EventCard.tsx`.

## Verification

- `pnpm exec prettier --write src/components/events/EventCard.tsx`
- `pnpm typecheck:touched -- src/components/events/EventCard.tsx`
- `npx gitnexus detect-changes -r experts`

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
