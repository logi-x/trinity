---
title: "Experts — exams vs quizzes framing and implementation status"
date: "2026-04-17"
updated: "2026-04-17"
tags: ["project/experts", "topic/lms", "topic/product", "source/session"]
category: "Raw/sources"
source: "generated"
source_id: "Raw/sources/2026-04-17-experts-exams-vs-quizzes-curriculum.md"
---

# Experts — exams vs quizzes framing and implementation status

Vault capture of product criteria vs what shipped in **experts** (`apps/experts-app`) around **course exams** and **curriculum** (April 2026).

## Product framing — how an exam should differ from a quiz

| Dimension     | Quiz                    | Exam                                                                                                               |
| ------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Placement** | Inside modules          | End of course or unit                                                                                              |
| **Stakes**    | Checks understanding    | Certifies readiness / completion                                                                                   |
| **Policy**    | Often multiple retries  | Tighter attempt limits; manual reset / admin override more common                                                  |
| **UX**        | Lightweight             | Serious framing, countdown emphasis, warning copy, stronger result state, explicit tie to certificate / completion |
| **Reporting** | Another curriculum item | Milestone visibility                                                                                               |

## Two implementation strategies (both valid)

1. **Low complexity — extend existing quiz model**  
   Add an assessment discriminator on the same underlying type, e.g. `practice | graded | final_exam`, and branch behavior + UI. Delivers most differentiation (placement can still be “only at end” by convention or validation) without a second entity graph.

2. **Separate `Exam` entity**  
   Worth it when the product needs capabilities that do not fit the current quiz model well, for example: manual grading or mixed question types; question banks / randomized pools; exam-specific release windows; invigilation / identity checks; certificate rules keyed specifically to final exam outcome; separate analytics, permissions, or instructor workflows.

## Where the codebase is today (repo, not vault)

**What exists**

- **`CourseExam`** Prisma model (`course_exams`): course-scoped title + description; relation from `Course`.
- **Creator API:** `POST/PATCH` under `/api/v1/creator/courses/[id]/exams` (camelCase JSON).
- **Catalog path:** course DTOs include `exams[]` from `courseExams`.
- **Creator curriculum UI:** inline **Exam** editor in the same shell as module / lesson / quiz (sidebar list of course exams + add flow); i18n under `creator.courses.curriculum` including `examDialog` and `builder.courseExams*`.

**What was not done at the time of the first capture**

- No **`assessmentKind`** (or similar) on the existing **quiz** model — quizzes and exams were still **two shapes** (module quiz items vs `CourseExam`), not a unified discriminator.
- **Learner** experience for `CourseExam` (attempts, delivery, grading) was **not** wired yet.
- **Certificate / completion** logic did not yet treat course exams as a distinct milestone.

## Product decision

Current implementation direction:

- **Keep `CourseExam`** as a separate course-level assessment entity.

Implication:

- Module **`Quiz`** remains the formative assessment shape.
- **`CourseExam`** is now the dedicated summative / milestone assessment path.
- A future convergence into one assessment model is still possible, but it is no longer the active implementation direction.

## Links

- [[Entities/Projects/Experts App]] — web app entity hub
- [[Entities/Projects/Experts]] — product umbrella

## Implementation update — shipped runtime slice

- Extended `CourseExam` into a deliverable assessment with runtime policy fields: `durationSec`, `passingScore`, `maxAttempts`, `cooldownMin`, `isPublished`.
- Added separate exam runtime graph in Prisma: `CourseExamQuestion`, `CourseExamOption`, `CourseExamAttempt`, `CourseExamAnswer`.
- Added creator authoring support for exam policy + questions in the curriculum exam editor and creator exam API.
- Added learner runtime routes for course exams: start/resume, submit, progress, and creator-side attempt reset.
- Added learner learn-page exam section with final-exam framing, curriculum-core gating, pass/pending status, and certificate/completion linkage.
- Updated course completion progress to include published course exams; certificate issuance now requires `enrollment.completedAt`.
- Focused verification passed: `app/api/v1/course-exams/[id]/start/__tests__/route.test.ts` and `app/api/v1/user/certificates/__tests__/route.test.ts`.
- Repo still has broad pre-existing TypeScript errors outside this slice; filtered checks showed no remaining errors in the touched exam/curriculum/certificate files.

## Current status

### Done

- Separate **`CourseExam`** path is established and active.
- Creator authoring supports exam policy and question authoring.
- Learner runtime supports exam start/resume/submit and pass/fail flow.
- Course completion progress includes published course exams.
- Certificate issuance is blocked until course completion is actually achieved.
- Learner-facing exam UX now exists with stronger final-assessment framing than quizzes.
- Creator curriculum now surfaces lightweight **exam outcome reporting** per course exam:
  - enrolled learners
  - pending learners (no pass yet / no active failure state)
  - passed learners
  - failed learners
  - in-progress learners
- Exam reporting is derived in the main course DTO from course enrollments plus each learner's latest course-exam attempt state, and is shown in both the curriculum sidebar and the exam editor.
- Added a focused mapper test to lock the exam-reporting aggregation behavior.
- Exam editor UX now surfaces validation failures clearly:
  - toast feedback on failed create/update
  - inline danger alert in the exam dialog
  - friendlier parsing of nested Zod validation issues such as missing question text
- Exam dialog dirty-state tracking now follows the same usable intent as the module form:
  - save stays disabled until the form is both dirty and valid
  - explicit reset-key syncing fixed the stale RHF baseline problem after async exam payload loads
- Exam authoring interaction now matches quiz authoring semantics:
  - `multiple_choice` uses radio selection
  - `true_false` uses radio selection
  - `multi_select` remains checkbox-based

### Partially done

- **Milestone reporting** now exists in lightweight creator form inside curriculum, but creator/admin reporting is still not yet a dedicated exam-results surface or analytics page.
- **Policy** exists for attempts, cooldown, and reset, but the surrounding admin tooling is still minimal.
- **Verification** exists for the new core routes and flows, but not yet as broad regression coverage across the full app.

### Still pending

- Dedicated **creator/admin reporting** for exam outcomes, pending vs passed counts, and milestone visibility as a first-class reporting concept.
- Broader **automated verification** once the repo’s unrelated pre-existing TypeScript and test issues are cleaned up enough to run wider gates confidently.
- Decision on whether to later introduce a shared **assessment abstraction** across quizzes and exams, or keep the two-shape model long-term.
- Any advanced exam-only capabilities still intentionally out of scope:
  - manual grading
  - question banks / random pools
  - release windows / scheduling
  - proctoring / identity checks
  - advanced analytics and permissions

---

**Project:** [[Projects/Experts/Experts App/Plans & Sessions|Experts App — Plans & Sessions]]
