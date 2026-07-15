---
title: "Experts — Schema Naming"
date: 2026-05-18
source: "draft"
tags: [project/experts, guide, schema, naming]
---

# Schema Naming

Yes — you should standardize this now before the schema grows further.
At your current scale in Experts, fixing naming consistency early is much cheaper than carrying mixed conventions forever.

The main issue is that you're currently mixing:

* **domain-prefixed tables**

    * `course_exam_questions`
    * `course_module_assets`

with:

* **context-local tables**

    * `lesson_assets`
    * `lesson_video_watch_states`

That inconsistency becomes painful later when:

* generating Prisma models
* writing joins/raw SQL
* browsing DB schemas
* onboarding contributors/agents
* adding adjacent domains (`event_*`, `community_*`, `academy_*`, etc.)

---

# Recommended Convention

Use:

```sql
course_*
```

for everything that belongs to the Courses bounded context.

Meaning:

```sql
course_lessons
course_lesson_assets
course_lesson_video_watch_states
course_lesson_progress
```

instead of:

```sql
lesson_assets
lesson_video_watch_states
```

---

# Why this scales better

Because `lesson` is not a global entity.

A lesson only exists inside Courses.

Later you may have:

* event_sessions
* academy_lessons
* onboarding_lessons
* certification_lessons

Without prefixes, table names become ambiguous.

---

# Recommended Final Naming

I’d normalize into this structure:

```sql
course_modules
course_lessons

course_assets
course_module_assets
course_lesson_assets

course_exams
course_exam_questions
course_exam_question_assets
course_exam_options
course_exam_attempts
course_exam_answers

course_enrollments
course_lesson_progress
course_lesson_video_watch_states

course_certificates
course_instructors
course_price_versions
```

---

# Specific Notes

## 1. `lesson_assets` vs `lesson_resources`

You already identified the issue correctly.

Pick ONE.

I’d strongly recommend:

```sql
course_lesson_assets
```

Reason:

* "asset" is broader and future-proof
* resources/files/videos/slides/PDFs can all be assets
* consistent with your existing `course_assets`

Delete:

* `lesson_resources`
* `lesson_prerequisites` (if truly unused)

---

## 2. `lesson_video_watch_states`

Rename to:

```sql
course_lesson_video_watch_states
```

because:

* avoids orphan naming
* consistent with `course_lesson_progress`

---

## 3. `course_exam_options`

This one is slightly inconsistent semantically.

Because options belong to questions.

Technically more normalized naming would be:

```sql
course_exam_question_options
```

Same logic as:

```sql
course_exam_question_assets
```

I would actually recommend renaming it now while still early.

So:

```sql
course_exam_questions
course_exam_question_options
course_exam_question_assets
```

becomes beautifully hierarchical.

---

# The Real Rule

The best long-term rule is:

> Table names should remain globally understandable without requiring schema/domain context.

Meaning:

Good:

```sql
course_lesson_assets
```

Bad:

```sql
lesson_assets
```

because when someone sees:

```sql
SELECT * FROM lesson_assets
```

they have no idea:

* which subsystem?
* which lesson type?
* LMS?
* onboarding?
* event workshop?

---

# One More Important Recommendation

You’re approaching a size where a formal naming convention document becomes worth it.

For example:

```md
# Database Naming Conventions

## Tables
- snake_case
- pluralized
- bounded-context prefixed
- hierarchy left-to-right

Examples:
- course_lessons
- course_exam_question_options

## Columns
- snake_case
- foreign keys singular:
  - course_id
  - lesson_id

## Junction tables
- alphabetical or ownership-based

## Enums
- singular uppercase
```

This becomes extremely valuable once:

* migrations increase
* agents contribute
* raw SQL grows
* reporting/views/materialized views appear

And Experts is already at that complexity level.
