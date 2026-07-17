---
title: "Experts Ai Suggest Modal Usability"
date: "2026-05-09"
tags: [session-log, project/experts]
category: "session-log"
---

# Experts AI Suggest modal usability

Date: 2026-05-09

## Context

AI Suggest controls in creator course/event forms used small popovers for generated text and lists. Long suggestions were hard to review because the popover had no bounded scrolling and actions moved with the content.

## Change

Updated shared AI Suggest UI components:

- `apps/experts-app/src/components/ui/ai-suggest-list-button.tsx`
- `apps/experts-app/src/components/ui/ai-suggest-button.tsx`

Both now render a responsive modal surface with a clearer header, bounded scroll area, and pinned footer actions. List suggestions use larger selectable rows with check indicators, wrapped long text, and a selected count in the header.

Also memoized `suggestionList` in `apps/experts-app/src/hooks/use-ai-suggest-list.ts` so selection state is not reset by render-time array recreation.

## Verification

- `pnpm typecheck:touched -- src/components/ui/ai-suggest-list-button.tsx src/components/ui/ai-suggest-button.tsx src/hooks/use-ai-suggest-list.ts`
- `npx gitnexus detect-changes -r experts`

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
