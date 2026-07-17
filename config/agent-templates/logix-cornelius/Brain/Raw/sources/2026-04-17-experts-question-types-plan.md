---
title: "Experts — next quiz and exam question types plan"
date: "2026-04-17"
updated: "2026-04-17"
tags: ["project/experts", "topic/lms", "topic/product", "topic/assessments", "source/plan"]
category: "Raw/sources"
source: "generated"
source_id: "Raw/sources/2026-04-17-experts-question-types-plan.md"
---

# Experts — next quiz and exam question types plan

Implementation plan for the next assessment question types after the current **`multiple_choice`** and **`true_false`** support in `apps/experts-app`.

## Implementation status — 2026-04-17

### Done in `question-types-plan`

`multi_select` has been implemented as the next shipped assessment type for both quizzes and course exams.

Completed work:

- creator schemas and DTOs now allow `multi_select`
- creator validation requires at least 2 correct options for `multi_select`
- quiz and exam start/status payloads now expose question `type`
- learner UI now renders `multi_select` as checkbox-based selection
- quiz and exam submit flows now accept normalized `optionIds[]`
- submit APIs remain backward-compatible with legacy single-select `optionId`
- quiz and exam attempt answers now persist one row per selected option
- scoring now uses strict exact-set matching for `multi_select`
- targeted tests were added for creator validation and exact-set scoring

Related note:

- [[Wiki/Concepts/Assessments]]

### Still pending

Not yet done from this plan:

- constrained `short_answer`
- strict `fill_in_blank`
- text-answer persistence for quiz/exam attempts
- accepted-answer authoring and storage
- normalized text matching rules
- learner resume flow for text answers
- tests for text-answer grading and resume behavior

### Current recommendation

Next slice should be:

1. ship constrained `short_answer`
2. optionally model `fill_in_blank` as the same storage/grading path with different authoring copy

## Recommendation

Implement in this order:

1. **`multi_select`**
2. **Constrained `short_answer`** or **strict `fill_in_blank`**

Do **not** implement yet:

- `matching`
- `ordering`
- `long_answer`

These are higher complexity and do not fit the current instant auto-graded runtime as cleanly.

## Why this order

### `multi_select`

Best next step because it fits the current option-based model and makes sense for both quizzes and course exams.

Expected value:

- higher-quality knowledge checks
- better differentiation between shallow guessing and actual understanding
- useful for compliance, definition groups, “select all that apply”, and edge-case checks

Why it is still manageable:

- question authoring already has options and `isCorrect`
- current question schema already carries a string `type`
- learner rendering can evolve from radio-style choice to checkbox-style choice

Main implementation cost:

- allow multiple selected answers per question
- update submit payload shape
- update persistence so one question can store multiple chosen options
- update scoring to require full correct-set match

### `short_answer` / strict `fill_in_blank`

Good second step if kept intentionally narrow and auto-graded.

Expected value:

- terminology recall
- exact concept names
- acronyms, vocabulary, simple factual recall

Constraints:

- must stay auto-graded
- accepted answers should be explicit
- normalization should stay simple: trim, lowercase, collapse spaces

Main implementation cost:

- add text-answer storage
- add accepted-answer authoring
- add deterministic text comparison rules
- update learner UI and submit flow for text input

## Current code constraints

Current implementation shape suggests these decisions:

- **Schema supports option correctness well**, but answer persistence is currently single-option-per-question.
- **Scoring assumes one selected option per question**.
- **Creator DTOs are still limited to `multiple_choice | true_false`** even though broader question types are named elsewhere.

Implication:

- `multi_select` is a real feature, not a pure config toggle.
- `short_answer` needs a new answer shape, not just a new label.

## Plan — `multi_select`

### Phase 1: Data model

- Update quiz and exam answer persistence to support multiple selected options per question.
- Remove the assumption that one question maps to one `optionId`.
- Keep exact-match scoring for v1:
  learner passes a question only if the selected set equals the correct set.

### Phase 2: API and handler updates

- Update quiz and exam submit payloads to accept `optionIds[]` for `multi_select`.
- Keep existing payload shape for current question types to avoid unnecessary regressions.
- Update start/status responses so learner clients know whether a question is single-select or multi-select.

### Phase 3: Creator authoring

- Add `multi_select` as an allowed question type in creator schemas and DTOs.
- Reuse the current options editor.
- Add validation:
  - minimum 2 options
  - at least 2 correct options for `multi_select`
  - prevent publishing invalid questions

### Phase 4: Learner UI

- Render `multiple_choice` and `true_false` with radio controls.
- Render `multi_select` with checkbox controls.
- Make answer state explicit before submit.
- Show instruction copy such as “Select all correct answers.”

### Phase 5: Tests

- creator validation accepts valid `multi_select`
- creator validation rejects one-correct-option `multi_select`
- learner submit stores multiple selections
- scoring gives credit only on full exact-set match
- existing `multiple_choice` and `true_false` behavior remains unchanged

## Plan — `short_answer` / strict `fill_in_blank`

### Phase 1: Product rule

Keep v1 strict:

- one text input
- auto-graded only
- no AI grading
- no partial credit

### Phase 2: Data model

- Add a text-answer storage path for quiz and exam attempts.
- Add accepted-answer storage on the question definition.
- Support multiple accepted answers for aliases or spelling variants.

### Phase 3: Authoring

- Add `short_answer` as an allowed question type.
- Let creators define one or more accepted answers.
- Add validation so publishing is blocked if no accepted answers are defined.

### Phase 4: Runtime scoring

- Normalize learner input with:
  - trim
  - lowercase
  - collapse internal spaces
- Compare against normalized accepted answers.
- Do not add fuzzy matching in v1.

### Phase 5: Learner UI

- Render a single text input.
- Show short helper copy that the answer must match the expected term.
- Preserve entered value on resume.

### Phase 6: Tests

- accepted-answer matching works for normalized equivalents
- incorrect free text fails deterministically
- resume flow restores typed answer
- current option-based question types still work unchanged

## Explicit non-goals for now

Do not implement in the next slice:

- `matching`
- `ordering`
- `long_answer`
- manual grading
- partial credit
- fuzzy text grading
- AI scoring

These belong in a later assessment-system expansion, not the next incremental release.

## Suggested execution order

1. Ship `multi_select`
2. Observe creator usage and learner results
3. Then ship constrained `short_answer`

This keeps the next step useful, low-risk, and aligned with the current Experts assessment architecture.

## Links

- [[Entities/Projects/Experts App]]
- [[Raw/sources/2026-04-17-experts-exams-vs-quizzes-curriculum]]

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
