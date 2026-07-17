---
title: "Experts App v1.1.6 — release candidate"
date: "2026-04-17"
updated: "2026-04-17"
tags: ["project/experts", "project/experts-app", "topic/release", "docs/changelog"]
category: "Projects/Experts/Experts App/reports"
source: "generated"
source_id: "Projects/Experts/Experts App/reports/release-v1.1.6.md"
---

# Experts App v1.1.6 (release candidate)

**Status:** Release candidate (as of **2026-04-17**).  
**Window (changelog):** **14 April 2026** → **17 April 2026**.

## Links

- [[Entities/Projects/Experts App|Experts App (entity hub)]]
- [Google Docs — V1.1.6 tab](https://docs.google.com/document/d/1oJb9RHMSWVPRfXk0o43Y-YH1Pn46u7SUL0Kw73v0gkU/edit?tab=t.l0gusvlyetr)
- **Canonical technical log:** `` `apps/experts-app/public/reports/CHANGELOG_RAW.md` `` (**monorepo root**)
- **Published / client-readable changelog:** `` `apps/experts-app/public/reports/CHANGELOG.md` `` (**monorepo root**)

## Summary (stakeholder-facing)

- **Platform & quality:** `tsconfig` excludes `src/generated/**` and `coverage/**`; remaining type errors cleared; certification overview and console tests refreshed (`proofOfExpertise`, needs-info checkpoint, queue tests); clone dialogs now use **`entityType`** not `entityLabel`; Admin payments tabs simplified; error components and creator lifecycle copy localized in **EN / AR / ES**.
- **Curriculum:** New **`CourseAssetsPanel`** in **`CurriculumBuilderShell`** for images, video, files, and links with clearer upload feedback; lessons get **voice notes** in **`LessonDialog`** (**`AudioRecorder`** / **`AudioWavePlayer`**), Markdown editor integration, audio-friendly upload API, **drag-and-drop** ordering for lessons / quizzes, duration **`NumberField`**; leaner module selection (**`effectiveSelectedModuleId`**) and broader i18n on the curriculum screen.
- **Exams, quizzes & AI:** **`QuestionAssetUploader`** in exam and quiz dialogs with localized failures; full create/edit via **`ExamDialog`** (replaces stub); **multi-select** quiz type with ≥ 2-correct validation; **`AiSuggestButton`** / **`AiSuggestListButton`** and hooks for question generation; sample env hygiene (**`OPENAI_SECRET`** commented where appropriate); strings in **EN / AR / ES**.
- **Home:** Stats include **total events**; courses and events sections + empty states refined.
- **Learn workspace:** **`useCoursePlayer`** + view-model for lesson/quiz **accessibility**, **progress**, **unlock reasons**, **up-next / resume**; **`LessonPlayer`** resources; **`LearnerWorkspaceLayout`** and toolbar; **`CertModal`**, **`LessonList`**, **`ModuleOverview`**, loading and progress UI.
- **Courses, events & visual polish:** **`ValidationTracker`** on course forms surfaces required-field issues; event overview completion uses clearer progress feedback; legacy `CourseCardV2` / `EventCardV2` removed; **muted / surface** tokens and testimonials aligned with the design system; event pricing validation stricter by selection.
- **Staging & launch readiness (internal):** Core pillars (certification, payments, HeroUI, auth, subscriptions, courses/events, admin, i18n, ZATCA, Docker) largely in place; **certification-gated publishing** and **subscription content gating** still need final wiring; aggressive staging realistic after build/type strictness and follow-ups (image **`remotePatterns`**, Phase-13 **Noon** webhook audit). **Mid-July 2026** soft-launch target noted with client-side risks (brand assets, categories, sample course, instructor ToS) flagged.
- **Tooling & docs:** Package versions bumped to **1.1.6**; **brain-vault Obsidian** Cursor rule and **experts-rule-guide** cross-links; Claude skill docs expanded (**`experts-ecosystem`**, **experts-orbit**, **experts-cosmos**).

## Institutional memory

Decisions and deep dives for this work should also appear on the relevant **Wiki/Concepts/** pages (e.g. [[Wiki/Concepts/Curriculum]], [[Wiki/Concepts/Instructor Certification|Certification]], [[Wiki/Concepts/Assessments|Quizzes]], [[Wiki/Concepts/AI Features|AI]], [[Wiki/Concepts/i18n]], [[Wiki/Concepts/Design System]]) when they change long-lived behaviour — not only in this release note.
