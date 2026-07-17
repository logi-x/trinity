---
title: "Course Classification Guide"
date: "2026-04-11"
tags: ["project/experts", "topic/course-classification-guide", "topic/guides"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs/guides/guides-index|Guides index]]

# Course Classification Guide

step-by-step implementation guide for adding the optional course classification layer:

General Learning

Professional Training

Academic Program

The goal is to make it useful now, while keeping the door open for future institutional features like university partnerships, professional boards, and CPD/CME-style recognition.

Step-by-Step Guide: Course Recognition Type System

1. Define the purpose clearly

This feature is not the same as instructor certification level.

Instructor certification answers:

who the instructor is

whether they are verified

whether they are academically certified

Course recognition type answers:

what kind of learning offering this course is

what kind of outcome or recognition it may lead to

So the first rule is:

Keep instructor certification and course recognition type as separate concepts.

1. Decide the three course recognition types

Start with these three only.

General Learning

For:

hobby learning

personal development

practical non-accredited education

public educational content

Examples:

Intro to React

Beginner Photography

Time Management Basics

Professional Training

For:

workplace learning

skill development

internal training

non-academic but career-relevant education

Examples:

Project Management for Teams

Customer Service Excellence

Digital Marketing Fundamentals

Academic Program

For:

academically oriented instruction

institution-linked courses

courses that may later tie into formal credentials or recognized academic pathways

Examples:

Electrical Engineering Foundations

Introduction to Clinical Research

Advanced Educational Psychology

1. Define the initial business rule

For now, keep the rule simple:

Unverified Instructor can publish only General Learning

Verified Instructor can publish General Learning and Professional Training

Academic Instructor can publish all three, including Academic Program

That gives real meaning to certification levels without blocking growth too hard.

1. Decide certificate behavior early

This is the most important rule to lock.

Recommended first version:

General Learning

Can issue: platform completion record only

Cannot issue: academic/professional certificate

Professional Training

Can issue: instructor/platform training completion certificate

Cannot imply formal academic accreditation unless separately approved

Academic Program

Can issue: academic/professional completion certificate

Only if instructor is Academic Certified

Optionally requires manual admin approval later

This prevents legal and trust problems.

1. Add the database fields

You’ll want a course-level classification field.

Example idea:

enum CourseRecognitionType {
GENERAL_LEARNING
PROFESSIONAL_TRAINING
ACADEMIC_PROGRAM
}

In your Course model, add something like:

recognitionType CourseRecognitionType @default(GENERAL_LEARNING)

You may also want a separate certificate behavior field later, but you can avoid that initially by deriving it from recognition type + instructor certification level.

1. Add eligibility logic at the backend

Create one centralized permission rule.

Example logic:

function canInstructorUseRecognitionType(
instructorLevel: "UNVERIFIED" | "VERIFIED" | "ACADEMIC",
recognitionType: "GENERAL_LEARNING" | "PROFESSIONAL_TRAINING" | "ACADEMIC_PROGRAM"
): boolean {
if (recognitionType === "GENERAL_LEARNING") return true;
if (recognitionType === "PROFESSIONAL_TRAINING") {
return instructorLevel === "VERIFIED" || instructorLevel === "ACADEMIC";
}
if (recognitionType === "ACADEMIC_PROGRAM") {
return instructorLevel === "ACADEMIC";
}
return false;
}

This rule should be enforced:

on create

on update

on publish

Do not rely on frontend only.

1. Add it to the course creation flow

In the course creation/edit form, add a new field:

Recognition Type

Options:

General Learning

Professional Training

Academic Program

But show only allowed options depending on instructor level.

You can:

hide unavailable options

or show them disabled with explanation

Recommended UX:

disabled option

short helper text like “Requires Academic Instructor certification”

That’s better for discoverability.

1. Add explanation text in the UI

Each option should have clear meaning.

Example:

General Learning

For public educational content focused on personal or practical learning.

Professional Training

For career-oriented or workplace-focused learning that demonstrates professional development.

Academic Program

For academically credentialed learning delivered by Academic Certified instructors and suitable for formal or institution-aligned recognition.

This reduces support tickets later.

1. Add publish-time validation

Even if someone somehow edits payloads manually, publishing should fail if the recognition type is not allowed.

At publish time validate:

instructor certification level

recognition type

certificate rules

any future institutional requirements

Example publish error:
“Academic Program courses require Academic Instructor certification.”

1. Add certificate issuance rules

You already want:
“Only Academic Certified instructors can issue certificates upon course completion.”

Now refine it with recognition type:

Rule set

GENERAL_LEARNING → completion record only

PROFESSIONAL_TRAINING → training certificate allowed if verified or academic

ACADEMIC_PROGRAM → certificate allowed only for academic instructors

Later you can split:

platform-issued certificate

instructor-issued certificate

institution-issued certificate

But you do not need that complexity yet.

1. Reflect it on the public course page

Show the recognition type on the course page.

Examples:

General Learning

Professional Training

Academic Program

This helps:

learners understand expectations

institutions trust the catalog

future filtering/search

It also makes the platform look more structured and premium.

1. Add search/filter support early

Even if you do not expose it immediately, structure the backend so you can filter by recognition type later.

Useful future filters:

General Learning

Professional Training

Academic Program

Academic Certified instructors only

This will matter a lot when catalog grows.

1. Add admin moderation support

Create admin visibility for:

instructor certification level

course recognition type

whether recognition type is allowed

whether certificate issuance is enabled

Later, admin can manually override or approve sensitive cases.

Especially useful for:

medicine

engineering

psychology

legal training

healthcare

1. Add a migration-safe rollout plan

Do not force this onto all existing courses immediately.

Recommended rollout:

Phase 1

add field to DB

default all old courses to GENERAL_LEARNING

Phase 2

show field in creator UI for new/editable courses

Phase 3

enforce recognition type validation on publish

Phase 4

introduce certificate rules tied to recognition type

Phase 5

add admin moderation / approval for Academic Program if needed

This keeps rollout safe.

1. Prepare for future institutional extensions

This is where the feature becomes strategic.

Later, ACADEMIC_PROGRAM can support extra metadata such as:

awarding institution

board approval number

credit hours

CPD points

CME hours

recognition body

expiration date of approval

Do not build all of this now.

Just design your current model so these can be added later without breaking the system.

A future table could hold optional academic/program metadata instead of bloating the main course model.

1. Keep wording legally safe

This matters a lot.

Avoid promising:

official accreditation

government recognition

licensed qualification

Unless that is truly verified.

Prefer wording like:

Academic Program

Professional Training

Certificate of Completion

Instructor credential verified by platform

That keeps trust high without overclaiming.

1. Suggested implementation order

Here’s the exact order I’d implement it:

Phase A — Foundation

Add recognitionType enum to DB

Default existing courses to GENERAL_LEARNING

Add backend validation helper

Phase B — Creator Flow

Add Recognition Type field in creator form

Show gated options based on instructor certification

Add helper text and disabled states

Phase C — Publishing Rules

Enforce validation on create/update/publish

Block invalid publish attempts

Add audit/admin visibility

Phase D — Learner Experience

Show recognition type on public course page

Add internal search/filter support

Adjust certificate behavior based on type

Phase E — Future Expansion

Add institutional metadata for Academic Program

Add moderation/approval workflow for sensitive fields

Add CPD/CME/board-credit support later

1. Recommended minimal v1 rules

To keep implementation simple, start with this exact v1:

Every course has one recognition type

Default is GENERAL_LEARNING

Only Academic instructors can choose ACADEMIC_PROGRAM

Only Verified and Academic instructors can choose PROFESSIONAL_TRAINING

Only Academic instructors can issue academic-style completion certificates

Existing courses remain General Learning unless manually changed

That is enough for a strong first version.

1. Example policy mapping

A clean mapping could be:

Instructor Level General Learning Professional Training Academic Program
Unverified Yes No No
Verified Yes Yes No
Academic Yes Yes Yes

And for certificates:

Recognition Type Completion Record Training Certificate Academic Certificate
General Learning Yes No No
Professional Training Yes Yes No
Academic Program Yes Yes Yes, if Academic instructor 20. Final architecture principle

The cleanest long-term design is:

Instructor Certification Level controls trust and eligibility

Course Recognition Type controls course category and certificate behavior

Certificate Policy controls what learners receive on completion

Three separate concerns.
That separation will save you a lot of pain later.

---

a clean, scalable schema for the entire instructor certification system for Experts, covering:

certification levels

applications

review workflow

badges

fields/specializations

verification evidence

certificate issuance eligibility

I’ll keep it implementation-oriented and Prisma-friendly.

Design goals

This schema is designed to support:

A gated instructor certification path
Unverified → Verified Instructor → Academic Instructor

Multiple applications over time
including re-application and upgrades

Review workflow with auditability

Flexible evidence submissions
files, links, text statements, licenses, degrees, portfolios, etc.

Badge rendering on public profiles

Course eligibility rules later
such as who can publish Academic Programs or issue certificates

Core model structure

You can think of the system in 6 layers:

Instructor certification state

Certification applications

Application review decisions

Submitted evidence

Fields / specializations

Badge projection / public status

Recommended enums
enum InstructorCertificationLevel {
UNVERIFIED
VERIFIED
ACADEMIC
}

enum CertificationApplicationType {
VERIFIED
ACADEMIC
}

enum CertificationApplicationStatus {
DRAFT
SUBMITTED
UNDER_REVIEW
NEEDS_INFO
APPROVED
REJECTED
WITHDRAWN
EXPIRED
}

enum CertificationEvidenceType {
IDENTITY_DOCUMENT
PROFESSIONAL_PROFILE
PORTFOLIO
WORK_SAMPLE
INTRO_VIDEO
EMPLOYMENT_PROOF
DEGREE
LICENSE
CERTIFICATE
INSTITUTIONAL_AFFILIATION
SUPPORTING_DOCUMENT
WEBSITE
OTHER
}

enum CertificationEvidenceStatus {
PENDING
ACCEPTED
REJECTED
NEEDS_INFO
}

enum CertificationReviewDecisionType {
SUBMIT
REQUEST_INFO
APPROVE
REJECT
WITHDRAW
EXPIRE
}

enum BadgeType {
VERIFIED_FIELD
ACADEMIC_FIELD
}

enum VerificationSourceType {
PLATFORM_REVIEW
MANUAL_ADMIN
EXTERNAL_PROVIDER
INSTITUTIONAL_CONFIRMATION
}

1. Instructor certification state

This is the current effective state on the user/instructor profile.

You can keep some of this on User, but I strongly recommend a separate profile-level table so you don’t clutter the user model.

model InstructorCertificationProfile {
id String @id @default(cuid())
userId String @unique

currentLevel InstructorCertificationLevel @default(UNVERIFIED)
currentFieldId String?
currentBadgeId String?

verifiedAt DateTime?
academicCertifiedAt DateTime?

certificateIssuanceEnabled Boolean @default(false)
accreditationEnabled Boolean @default(false)

lastApplicationId String?
notesInternal String?

createdAt DateTime @default(now())
updatedAt DateTime @updatedAt

user User @relation(fields: [userId], references: [id], onDelete: Cascade)
currentField CertificationField? @relation("CurrentCertificationField", fields: [currentFieldId], references: [id])
currentBadge CertificationBadge? @relation("CurrentCertificationBadge", fields: [currentBadgeId], references: [id])
applications CertificationApplication[]

@@index([currentLevel])
@@index([currentFieldId])
}
Why this exists

This gives you one place to read:

current certification level

current field label

whether the instructor can issue certificates

public trust state

1. Certification fields / specializations

This allows badges like:

Verified Marketing Instructor

Academic Electrical Engineering Instructor

model CertificationField {
id String @id @default(cuid())
slug String @unique
name String
description String?
isActive Boolean @default(true)
sortOrder Int @default(0)

createdAt DateTime @default(now())
updatedAt DateTime @updatedAt

applications CertificationApplication[]
badges CertificationBadge[]
profilesCurrent InstructorCertificationProfile[] @relation("CurrentCertificationField")
}

Examples:

software-development

electrical-engineering

psychology

digital-marketing

finance

law

You could later add parent/child taxonomy, but v1 does not need it.

1. Certification applications

This is the heart of the workflow.

Each instructor can submit multiple applications over time:

first Verified application

later Academic upgrade

re-apply after rejection

re-submit after needs info

model CertificationApplication {
id String @id @default(cuid())
userId String
certificationProfileId String
type CertificationApplicationType
status CertificationApplicationStatus @default(DRAFT)

targetFieldId String
title String?
summary String?

fullLegalName String?
countryCode String?
phoneNumber String?
professionalHeadline String?
yearsOfExperience Int?
institutionName String?
graduationYear Int?
licenseNumber String?
portfolioUrl String?
linkedinUrl String?
websiteUrl String?

submittedAt DateTime?
reviewedAt DateTime?
decidedAt DateTime?
expiresAt DateTime?

currentReviewerId String?
finalDecisionReason String?
internalNotes String?

createdAt DateTime @default(now())
updatedAt DateTime @updatedAt

user User @relation(fields: [userId], references: [id], onDelete: Cascade)
certificationProfile InstructorCertificationProfile @relation(fields: [certificationProfileId], references: [id], onDelete: Cascade)
targetField CertificationField @relation(fields: [targetFieldId], references: [id])

currentReviewer User? @relation("CertificationCurrentReviewer", fields: [currentReviewerId], references: [id])

evidences CertificationEvidence[]
reviews CertificationReviewDecision[]
badgeAssignments CertificationBadgeAssignment[]

@@index([userId, type])
@@index([status])
@@index([targetFieldId])
@@index([currentReviewerId])
@@index([submittedAt])
}
Why this model is important

It lets you:

track draft and submitted forms

support upgrades from Verified to Academic

preserve application history

display progress in the UI

1. Verification evidence

This model stores all evidence attached to an application.

Keep evidence generic and typed rather than making a separate table for each document type.

model CertificationEvidence {
id String @id @default(cuid())
applicationId String

type CertificationEvidenceType
status CertificationEvidenceStatus @default(PENDING)

label String?
description String?

fileUrl String?
fileName String?
fileMimeType String?
fileSizeBytes Int?

externalUrl String?
textValue String?

issuedBy String?
issuedAt DateTime?
expiresAt DateTime?

reviewerNotes String?
reviewedAt DateTime?
reviewedById String?

createdAt DateTime @default(now())
updatedAt DateTime @updatedAt

application CertificationApplication @relation(fields: [applicationId], references: [id], onDelete: Cascade)
reviewedBy User? @relation("CertificationEvidenceReviewer", fields: [reviewedById], references: [id])

@@index([applicationId])
@@index([type])
@@index([status])
}
Supports things like

passport / ID

degree PDF

portfolio link

LinkedIn URL

employer verification letter

intro video

license certificate

work sample attachment

1. Review workflow decisions

This is the audit trail.

Do not rely only on application.status.
You need a decision log.

model CertificationReviewDecision {
id String @id @default(cuid())
applicationId String
reviewerId String

decisionType CertificationReviewDecisionType
fromStatus CertificationApplicationStatus?
toStatus CertificationApplicationStatus?

reason String?
notesInternal String?
notesVisibleToUser String?

createdAt DateTime @default(now())

application CertificationApplication @relation(fields: [applicationId], references: [id], onDelete: Cascade)
reviewer User @relation("CertificationReviewReviewer", fields: [reviewerId], references: [id])

@@index([applicationId])
@@index([reviewerId])
@@index([createdAt])
}
Example events

user submits application

reviewer requests more info

reviewer approves

reviewer rejects

application expires

This makes support, compliance, and admin debugging much easier.

1. Badge definitions

Badges should be defined once and assigned separately.

model CertificationBadge {
id String @id @default(cuid())
slug String @unique
type BadgeType

fieldId String?
displayName String
shortLabel String?
description String?

iconKey String?
colorToken String?

isActive Boolean @default(true)

createdAt DateTime @default(now())
updatedAt DateTime @updatedAt

field CertificationField? @relation(fields: [fieldId], references: [id])
assignments CertificationBadgeAssignment[]
currentProfiles InstructorCertificationProfile[] @relation("CurrentCertificationBadge")

@@index([type])
@@index([fieldId])
}

Examples:

verified-software-development

verified-digital-marketing

academic-electrical-engineering

academic-psychology

1. Badge assignments

Never just mutate profile badge without history.
Keep assignments explicit.

model CertificationBadgeAssignment {
id String @id @default(cuid())
userId String
applicationId String?
badgeId String

assignedAt DateTime @default(now())
revokedAt DateTime?
revokeReason String?

assignedById String?
verificationSource VerificationSourceType @default(PLATFORM_REVIEW)

createdAt DateTime @default(now())

user User @relation(fields: [userId], references: [id], onDelete: Cascade)
application CertificationApplication? @relation(fields: [applicationId], references: [id], onDelete: SetNull)
badge CertificationBadge @relation(fields: [badgeId], references: [id])
assignedBy User? @relation("CertificationBadgeAssignedBy", fields: [assignedById], references: [id])

@@index([userId, revokedAt])
@@index([badgeId])
@@index([applicationId])
}
Why this matters

Later you may need:

badge history

revoked certification

institution-issued badge

admin override

Optional but highly recommended models 8. Application step progress

Useful if your UI has a guided wizard and autosave.

model CertificationApplicationProgress {
id String @id @default(cuid())
applicationId String @unique

baselineCompleted Boolean @default(false)
identityCompleted Boolean @default(false)
expertiseCompleted Boolean @default(false)
academicCompleted Boolean @default(false)
reviewReady Boolean @default(false)

updatedAt DateTime @updatedAt

application CertificationApplication @relation(fields: [applicationId], references: [id], onDelete: Cascade)
} 9. Structured reviewer checklist

Very useful if multiple admins review applications consistently.

model CertificationReviewChecklist {
id String @id @default(cuid())
applicationId String @unique

identityConsistencyScore Int?
expertiseClarityScore Int?
evidenceCredibilityScore Int?
fieldAlignmentScore Int?

hasFraudConcern Boolean @default(false)
hasMissingDocuments Boolean @default(false)
recommendsApproval Boolean?

notes String?

updatedAt DateTime @updatedAt

application CertificationApplication @relation(fields: [applicationId], references: [id], onDelete: Cascade)
}
Full Prisma schema draft

Here’s the full schema in one place for easier copy/use.

enum InstructorCertificationLevel {
UNVERIFIED
VERIFIED
ACADEMIC
}

enum CertificationApplicationType {
VERIFIED
ACADEMIC
}

enum CertificationApplicationStatus {
DRAFT
SUBMITTED
UNDER_REVIEW
NEEDS_INFO
APPROVED
REJECTED
WITHDRAWN
EXPIRED
}

enum CertificationEvidenceType {
IDENTITY_DOCUMENT
PROFESSIONAL_PROFILE
PORTFOLIO
WORK_SAMPLE
INTRO_VIDEO
EMPLOYMENT_PROOF
DEGREE
LICENSE
CERTIFICATE
INSTITUTIONAL_AFFILIATION
SUPPORTING_DOCUMENT
WEBSITE
OTHER
}

enum CertificationEvidenceStatus {
PENDING
ACCEPTED
REJECTED
NEEDS_INFO
}

enum CertificationReviewDecisionType {
SUBMIT
REQUEST_INFO
APPROVE
REJECT
WITHDRAW
EXPIRE
}

enum BadgeType {
VERIFIED_FIELD
ACADEMIC_FIELD
}

enum VerificationSourceType {
PLATFORM_REVIEW
MANUAL_ADMIN
EXTERNAL_PROVIDER
INSTITUTIONAL_CONFIRMATION
}

model InstructorCertificationProfile {
id String @id @default(cuid())
userId String @unique

currentLevel InstructorCertificationLevel @default(UNVERIFIED)
currentFieldId String?
currentBadgeId String?

verifiedAt DateTime?
academicCertifiedAt DateTime?

certificateIssuanceEnabled Boolean @default(false)
accreditationEnabled Boolean @default(false)

lastApplicationId String?
notesInternal String?

createdAt DateTime @default(now())
updatedAt DateTime @updatedAt

user User @relation(fields: [userId], references: [id], onDelete: Cascade)
currentField CertificationField? @relation("CurrentCertificationField", fields: [currentFieldId], references: [id])
currentBadge CertificationBadge? @relation("CurrentCertificationBadge", fields: [currentBadgeId], references: [id])
applications CertificationApplication[]

@@index([currentLevel])
@@index([currentFieldId])
}

model CertificationField {
id String @id @default(cuid())
slug String @unique
name String
description String?
isActive Boolean @default(true)
sortOrder Int @default(0)

createdAt DateTime @default(now())
updatedAt DateTime @updatedAt

applications CertificationApplication[]
badges CertificationBadge[]
profilesCurrent InstructorCertificationProfile[] @relation("CurrentCertificationField")
}

model CertificationApplication {
id String @id @default(cuid())
userId String
certificationProfileId String
type CertificationApplicationType
status CertificationApplicationStatus @default(DRAFT)

targetFieldId String
title String?
summary String?

fullLegalName String?
countryCode String?
phoneNumber String?
professionalHeadline String?
yearsOfExperience Int?
institutionName String?
graduationYear Int?
licenseNumber String?
portfolioUrl String?
linkedinUrl String?
websiteUrl String?

submittedAt DateTime?
reviewedAt DateTime?
decidedAt DateTime?
expiresAt DateTime?

currentReviewerId String?
finalDecisionReason String?
internalNotes String?

createdAt DateTime @default(now())
updatedAt DateTime @updatedAt

user User @relation(fields: [userId], references: [id], onDelete: Cascade)
certificationProfile InstructorCertificationProfile @relation(fields: [certificationProfileId], references: [id], onDelete: Cascade)
targetField CertificationField @relation(fields: [targetFieldId], references: [id])
currentReviewer User? @relation("CertificationCurrentReviewer", fields: [currentReviewerId], references: [id])

evidences CertificationEvidence[]
reviews CertificationReviewDecision[]
badgeAssignments CertificationBadgeAssignment[]
progress CertificationApplicationProgress?
checklist CertificationReviewChecklist?

@@index([userId, type])
@@index([status])
@@index([targetFieldId])
@@index([currentReviewerId])
@@index([submittedAt])
}

model CertificationEvidence {
id String @id @default(cuid())
applicationId String

type CertificationEvidenceType
status CertificationEvidenceStatus @default(PENDING)

label String?
description String?

fileUrl String?
fileName String?
fileMimeType String?
fileSizeBytes Int?

externalUrl String?
textValue String?

issuedBy String?
issuedAt DateTime?
expiresAt DateTime?

reviewerNotes String?
reviewedAt DateTime?
reviewedById String?

createdAt DateTime @default(now())
updatedAt DateTime @updatedAt

application CertificationApplication @relation(fields: [applicationId], references: [id], onDelete: Cascade)
reviewedBy User? @relation("CertificationEvidenceReviewer", fields: [reviewedById], references: [id])

@@index([applicationId])
@@index([type])
@@index([status])
}

model CertificationReviewDecision {
id String @id @default(cuid())
applicationId String
reviewerId String

decisionType CertificationReviewDecisionType
fromStatus CertificationApplicationStatus?
toStatus CertificationApplicationStatus?

reason String?
notesInternal String?
notesVisibleToUser String?

createdAt DateTime @default(now())

application CertificationApplication @relation(fields: [applicationId], references: [id], onDelete: Cascade)
reviewer User @relation("CertificationReviewReviewer", fields: [reviewerId], references: [id])

@@index([applicationId])
@@index([reviewerId])
@@index([createdAt])
}

model CertificationBadge {
id String @id @default(cuid())
slug String @unique
type BadgeType

fieldId String?
displayName String
shortLabel String?
description String?

iconKey String?
colorToken String?

isActive Boolean @default(true)

createdAt DateTime @default(now())
updatedAt DateTime @updatedAt

field CertificationField? @relation(fields: [fieldId], references: [id])
assignments CertificationBadgeAssignment[]
currentProfiles InstructorCertificationProfile[] @relation("CurrentCertificationBadge")

@@index([type])
@@index([fieldId])
}

model CertificationBadgeAssignment {
id String @id @default(cuid())
userId String
applicationId String?
badgeId String

assignedAt DateTime @default(now())
revokedAt DateTime?
revokeReason String?

assignedById String?
verificationSource VerificationSourceType @default(PLATFORM_REVIEW)

createdAt DateTime @default(now())

user User @relation(fields: [userId], references: [id], onDelete: Cascade)
application CertificationApplication? @relation(fields: [applicationId], references: [id], onDelete: SetNull)
badge CertificationBadge @relation(fields: [badgeId], references: [id])
assignedBy User? @relation("CertificationBadgeAssignedBy", fields: [assignedById], references: [id])

@@index([userId, revokedAt])
@@index([badgeId])
@@index([applicationId])
}

model CertificationApplicationProgress {
id String @id @default(cuid())
applicationId String @unique

baselineCompleted Boolean @default(false)
identityCompleted Boolean @default(false)
expertiseCompleted Boolean @default(false)
academicCompleted Boolean @default(false)
reviewReady Boolean @default(false)

updatedAt DateTime @updatedAt

application CertificationApplication @relation(fields: [applicationId], references: [id], onDelete: Cascade)
}

model CertificationReviewChecklist {
id String @id @default(cuid())
applicationId String @unique

identityConsistencyScore Int?
expertiseClarityScore Int?
evidenceCredibilityScore Int?
fieldAlignmentScore Int?

hasFraudConcern Boolean @default(false)
hasMissingDocuments Boolean @default(false)
recommendsApproval Boolean?

notes String?

updatedAt DateTime @updatedAt

application CertificationApplication @relation(fields: [applicationId], references: [id], onDelete: Cascade)
}
Recommended business rules

Here are the key rules to enforce in your service layer.

Rule 1

A user can only apply for ACADEMIC if current level is VERIFIED.

Rule 2

On approval of a VERIFIED application:

profile.currentLevel = VERIFIED

profile.verifiedAt = now()

assign Verified badge for target field

Rule 3

On approval of an ACADEMIC application:

profile.currentLevel = ACADEMIC

profile.academicCertifiedAt = now()

profile.certificateIssuanceEnabled = true

assign Academic badge for target field

Rule 4

Only one active submitted/in-review application of the same type per user at a time.

Rule 5

Badge shown publicly should be the currently active highest badge.

Public badge logic

A simple display resolver:

if profile.currentLevel = ACADEMIC and active academic badge exists → show academic badge

else if profile.currentLevel = VERIFIED and active verified badge exists → show verified badge

else show nothing

Suggested v1 simplifications

To avoid overbuilding:

Allow only one targetFieldId per application

Do not support multi-field badges yet

Keep evidence generic

Keep badge assignment history even if you only show one current badge

Store files externally and keep only metadata + URL in DB

Suggested future additions

Later you may want:

institution verification requests

third-party KYC / document verification

field-specific reviewer pools

expiration / renewal for some certifications

suspension reason tracking

academic program approval tied to certification

My recommendation for your stack

Given your Experts architecture, I’d likely place:

these models in public schema or a dedicated trust schema

badges and fields as seed data

application/evidence/reviews as transactional records

final public state cached on InstructorCertificationProfile

That gives you fast reads and clean audit history.
