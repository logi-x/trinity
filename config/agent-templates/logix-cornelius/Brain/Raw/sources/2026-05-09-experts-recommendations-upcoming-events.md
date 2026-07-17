---
title: "Experts Recommendations Upcoming Events"
date: "2026-05-09"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts recommendations upcoming events rule

Date: 2026-05-09
Project: Experts

## Summary

Updated the recommendation candidate pipeline so event recommendations do not include past events.

## Product rule

"You might also like" and personalized recommendations should only show events with at least one non-cancelled occurrence whose `endsAt` is greater than or equal to the current time. This allows ongoing events to remain visible while excluding fully ended events.

## Implementation

`apps/experts-app/src/lib/recommendations/queries/recommendation-candidates.ts` now applies the same upcoming-event predicate to:

- fallback event candidates
- hydrated event candidates from vector recommendations

This keeps the API response clean instead of filtering stale events in the UI.

## Verification

- `pnpm exec vitest run src/lib/recommendations/queries/__tests__/recommendation-candidates.test.ts src/lib/recommendations/queries/__tests__/get-personalized-recommendations.query.test.ts app/api/v1/recommendations/__tests__/route.test.ts`
- `pnpm typecheck:touched -- src/lib/recommendations/queries/recommendation-candidates.ts src/lib/recommendations/queries/__tests__/recommendation-candidates.test.ts`
- `npx gitnexus detect-changes -r experts`

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
