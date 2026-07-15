---
title: "Ai Tools"
date: "2026-07-15"
updated: "2026-07-15"
tags: ["inbox", "legacy"]
category: "inbox/legacy"
source: "migrated"
source_id: "Inbox/Legacy Random/ai-tools.md"
---
Based on the codebase, here are the strongest candidates ranked by impact vs effort:

Tier 1 — Near-zero effort, reuse exact same pattern

1. Learning outcomes & requirements generator
   Both courses and events already have learningOutcomes and requirements as string[] fields. The AiSuggestButton pattern works as-is — just add a new fieldType: "outcomes" | "requirements" to the API and a multi-value button that generates a bullet list and appends to the array rather than replacing a single field.

Why high impact: Instructors skip this because it's tedious. Outcomes improve conversion and SEO.

1. Tag / keyword suggestions
   Courses have a tags: string[] field. Same button, new fieldType: "tags" — returns a comma-separated list of 5–8 SEO-relevant keywords based on title + category + description.

Why high impact: Tags directly affect search ranking and discoverability on the platform.

Tier 2 — One extra API route, moderate UI work 3. Quiz question generator
Given a lesson's content (markdown), generate N multiple-choice questions with correct answers and distractors. The quiz domain already exists (src/lib/courses/quizzes/). The AI generates the JSON structure, you pre-fill the form.

Why high impact: Creating quizzes is the most time-consuming part of course creation. Most instructors skip it entirely.

1. Lesson content outline
   A "Draft for me" button in the curriculum lesson editor — given the lesson title and module name, generate a structured markdown outline. Same editor, same onChange handler.

Why high impact: Reduces blank-page paralysis. The lesson editor is already a MarkdownEditor.

Tier 3 — New capability, higher effort but high ROI 5. Translation assist
A "Translate to Arabic/Spanish" button on any text field. Sends the existing English value to the API with fieldType: "translate" + targetLocale. Since the platform is trilingual and most instructors write in English, this removes the biggest barrier to multi-language publishing.

1. Event agenda builder
   Given event title, type, and duration, suggest a full agenda with time-boxed items and descriptions. The EventAgendaSection already has the form structure — AI pre-fills it.

What I'd do first
Learning outcomes + tags — they're a copy-paste of the work already done, touch no new files, and together they cover the two biggest SEO/conversion levers for instructors. You'd be done in under an hour.

Quiz generator after that — highest raw impact, and it unlocks engagement features (completion certificates, assessments) that are blocked today because instructors don't create quizzes.

Want me to start with any of these?

---

I had an idea of course/event/lesson content outline generator/builder, where a user can input the title and description and the AI will generate a structured outline of the content.

The outline should be a list of topics and subtopics, and each topic and subtopic should have a description.

The outline should be in a structured format, so that it can be easily converted to a markdown document.

The outline should be in a format that can be easily converted to a JSON object, so that it can be easily parsed and used in the application.

The outline should be in a format that can be easily converted to a HTML document, so that it can be easily displayed in the application.

The outline should be in a format that can be easily converted to a PDF document, so that it can be easily printed and used in the application.

---

Let's start with adding AI button to markdown editor's toolbar as icon only, and make it optional, because we don't want to be allowed every where, only for specified context

@experts/apps/experts-app/app/(i18n)/\_shared/creator/courses/[id]/curriculum/sections/lesson-dialog.tsx:1150-1186

---

I want to focus on /creator/courses/[id]/curriculum

It's messed up now, and needs a lot of work, I want to implement the same logic as attached image "Lesson content types and assesments", we can start simplified, like since we didn't implement anything related to assigment/survays, we will skip these for now

---

I want to focus on /creator/courses/[id]/curriculum

It's messed up now, and needs a lot of work, I want to implement the same logic as attached image "Lesson content types and assesments", we can start simplified, like since we didn't implement anything related to assigment/survays, we will skip these for now

Two important notes:

- -selecting a Lesson format card should replace cards section with back and focus content type's window
- And this select sould be removed "Lesson format \*"

---

from the changes you made and
/home/logix/experts/apps/experts-app/app/(i18n)/\_shared/creator/courses/[id]/curriculum/sections/curriculum-builder-shell.tsx

there's a duplicate logic

---

let's move things around, I don't like how action buttons are placed

plan:
let's move add module button to the end of the Curriculum list similar to the image
let's add "add lesson" button at the end of each existing module
"add lesson" button should open the lesson content-type picker view similar to the image
clicking on a lesson content-type card should focus the content-type's window

---

I want to make quizzes support image uploads and file uploads, like we have for lessons

plan:
let's add a new field to the quiz form "resources" of type "resource[]"
let's add a new component to the quiz form "resource-panel"
let's add a new route to the api to handle the resource-panel
let's add a new component to the lesson-dialog to handle the resource-panel
let's add a new component to the quiz-dialog to handle the resource-panel
let's add a new component to the curriculum-builder-shell to handle the resource-panel
let's add a new component to the curriculum-list to handle the resource-panel
let's add a new component to the curriculum-item to handle the resource-panel

---

Let's' start with Exams and assessment section separate from main content-types

plan:
let's add a new route to the api to handle the exam and assessment
let's add a new component to the lesson-dialog to handle the exam and assessment
let's add a new component to the quiz-dialog to handle the exam and assessment
let's add a new component to the curriculum-builder-shell to handle the exam and assessment
let's add a new component to the curriculum-list to handle the exam and assessment
let's add a new component to the curriculum-item to handle the exam and assessment

---

audio recorder component

plan:
let's add a new component to the lesson-dialog to handle the audio recorder
let's add a new component to the quiz-dialog to handle the audio recorder
let's add a new component to the curriculum-builder-shell to handle the audio recorder
let's add a new component to the curriculum-list to handle the audio recorder
let's add a new component to the curriculum-item to handle the audio recorder

---

let's add a new component to the lesson-dialog to handle the video recorder
