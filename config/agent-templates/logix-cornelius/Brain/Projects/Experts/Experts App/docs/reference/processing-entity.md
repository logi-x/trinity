---
title: "PROCESSING ENTITY"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/processing-entity"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  Q: 4️⃣ Enforce “instructor must belong to entity”
  I agree with you in this point, but it's too restrictive, the business model as per the client is that anyone can teach create events, and not everyone can belong or own an entity as an entity requires legal docs

A: Perfect — this clarification changes the model in an important (and very common) way.
You’re right: the earlier rule is too restrictive for your business model.

Let’s realign the design with the actual business reality 👇

First, restate the real business rules (corrected)

From what you said, the true rules are:

BusinessEntity

Requires legal docs

Owned/managed by a limited set of users

Acts as a publisher / organizer / fiscal umbrella

User (Instructor)

Anyone can be an instructor

Does not need to own or belong to an entity

Can create courses/events freely

Course / Event

Must be published under exactly one entity

Entity handles:

branding

payments

invoices (ZATCA)

liability

Relationship

Instructor is a contributor, not a member

Entity is a sponsor / publisher, not the author

This is very similar to:

Udemy

Eventbrite

YouTube MCNs

Medium publications

So your instinct is correct 👍

The key shift in mindset
❌ Old (too strict)

Instructor must belong to entity

✅ New (correct)

Entity publishes content created by instructors

That means:

No membership required

Explicit publishing agreement per course/event

The correct abstraction: Publishing / Attribution

Instead of “membership”, think:

This entity agrees to publish this content

That agreement is content-scoped, not user-scoped.

Updated winning model (clean + flexible)
1️⃣ Course/Event belongs to an entity (still true)

This does not change.

model Course {
id String @id @default(dbgenerated("gen_random_uuid()"))
businessEntityId String @map("business_entity_id") @db.Uuid

title String
description String?

entity BusinessEntity @relation(fields: [businessEntityId], references: [id])

instructors CourseInstructor[]
}

Same for Event.

2️⃣ Instructor assignment does NOT require membership

Your pivot stays, but the rule changes.

model CourseInstructor {
courseId String @map("course_id") @db.Uuid
userId String @map("user_id") @db.Uuid
businessEntityId String @map("business_entity_id") @db.Uuid

role String @default("primary") // primary, co, guest
revenueShare Decimal? @db.Decimal(5,2)
isVisible Boolean @default(true)

course Course @relation(fields: [courseId], references: [id], onDelete: Cascade)
user User @relation(fields: [userId], references: [id], onDelete: Cascade)
entity BusinessEntity @relation(fields: [businessEntityId], references: [id])

@@id([courseId, userId])
}

Important difference:
There is no requirement that userId appears in BusinessMembership.

3️⃣ Replace “membership enforcement” with publishing approval

This is the crucial replacement for step 4️⃣.

Add a publishing status
model Course {
...
publishingStatus String @default("draft")
// draft | submitted | approved | rejected | published
}

Flow

Instructor creates course → draft

Chooses entity to publish under

Submits → submitted

Entity admin reviews

Approves → published

This:

protects the entity legally

allows open instructor participation

matches your client’s model

4️⃣ Entity permissions move to approval, not authorship

Only these users can approve:

entity owners

entity admins

const canApprove = await prisma.businessMembership.findFirst({
where: {
userId: approverId,
businessEntityId,
role: { in: ["owner", "admin"] },
},
});

if (!canApprove) throw new Error("Not allowed to approve content");

Instructor never needs membership.

5️⃣ Revenue, invoices, payouts (why this still works)

Even with no membership:

Payments go to BusinessEntity

Entity issues invoices

Entity pays instructors later (payout system)

Instructor revenue is derived from CourseInstructor.revenueShare

This aligns perfectly with:

ZATCA

your affiliate/commission system

future payouts

6️⃣ Why isInstructor still matters

Keep it — but reinterpret it correctly.

User.isInstructor === true

Means:

This user is allowed to create educational content

It does not imply:

entity affiliation

publishing rights

revenue rights

Those come from content-level agreements.

7️⃣ Optional (but very smart): PublishingAgreement table

If you want to be legally precise:

model PublishingAgreement {
id String @id @default(dbgenerated("gen_random_uuid()"))
userId String
businessEntityId String
courseId String?

termsVersion String
acceptedAt DateTime

@@unique([userId, businessEntityId, courseId])
}

This gives you:

legal audit trail

future ToS changes

dispute resolution

Final comparison (old vs new)
Concern Old model New model
Who can teach Entity members only Anyone
Legal control Membership Approval
Publishing Implicit Explicit
Scalability Low High
Marketplace-ready ❌ ✅
TL;DR (pin this)

You’re right: membership is too restrictive

Entity = publisher, not owner of instructor

Instructor = contributor

Approval replaces membership enforcement

Keep pivot tables

Add publishing workflow

This matches your client’s business reality

---

Q: I think now I understand, correct me if I'm wrong...

Any paid service (course/event/etc) must be processed by an entity no matter what, in this case we'll default to Experts as the default processing authority (even if a user doesn't belong to any entity), in theory, the user belongs to Experts by default, otherwise if the user decides to publish under another specific entity, the process goes through that entity with approval/invoicing/zatca system...

A: You’re basically correct, and your mental model is now 90% there.
I’ll just tighten a few terms so it’s precise and future-proof.

The corrected, crisp version of the model
✅ Core rule (this is the anchor)

Any paid service must be processed by exactly ONE BusinessEntity. Always. No exceptions.

That entity is responsible for:

payment processing

invoicing

VAT / ZATCA

refunds

legal liability

payouts

This is non-negotiable, and you got that exactly right.

Now let’s refine the parts you said 👇
❌ Slight correction to this sentence

“in theory, the user belongs to Experts by default”

Not quite.
The user does not belong to Experts.

✅ Correct framing

Experts is the default processing / publishing authority, not a default membership.

This distinction matters a lot later.

The clean conceptual model (final form)
1️⃣ BusinessEntity = Processing Authority

A BusinessEntity is:

a legal wrapper

a payment processor

a publisher of record

Not:

a group users must belong to

an identity the instructor “joins” by default

2️⃣ Default entity (Experts)

You can absolutely define:

DEFAULT_PROCESSING_ENTITY = Experts

Meaning:

If an instructor publishes without choosing an entity

The platform automatically assigns:

businessEntityId = Experts.id

Experts:

processes payment

issues invoice

handles VAT

later pays instructor

This is exactly how:

Udemy

Skillshare

Eventbrite

Gumroad (with platform accounts)

work.

3️⃣ Instructor does NOT belong to Experts

Instead:

Instructor is a content creator

Content is published under Experts

Relationship is content-scoped, not user-scoped

This avoids:

fake memberships

legal confusion

permission leaks

4️⃣ Publishing under another entity

If the instructor selects:

“Publish under House of Wisdom Academy”

Then:

Course/Event is created with:

businessEntityId = HoWA.id
publishingStatus = "submitted"

HoWA admins review

If approved:

HoWA becomes processor

HoWA issues invoice

HoWA handles ZATCA

If rejected:

instructor can:

revise

or fall back to Experts

This is exactly the approval model you described.

The full lifecycle (end-to-end)
Instructor creates content

No entity membership required

Must be isInstructor = true

Instructor chooses publishing option

✅ Default → Experts

🟡 Optional → another entity (approval required)

Content is published

Always under one entity

Payments always go through that entity

Revenue handling

Entity receives funds

Platform records revenue share

Instructor payout happens later

Why this model is excellent (and safe)

This gives you:

✅ Legal clarity
✅ ZATCA compliance
✅ Marketplace flexibility
✅ No fake memberships
✅ Easy default path
✅ Clean approval workflow
✅ Future multi-entity expansion

And it avoids:

“who owns this payment?” ambiguity

instructors accidentally becoming legal members

retroactive VAT disasters

One last important naming recommendation

To make this crystal clear in code, I recommend:

Avoid naming things like ownerEntity

Prefer:

processingEntityId

or publishingEntityId

This enforces the correct mental model everywhere.

TL;DR (your understanding, corrected)

✔ Any paid service must go through an entity

✔ Experts can be the default processor

❌ User does NOT belong to Experts by default

✔ User is a creator; entity is a processor

✔ Publishing under other entities requires approval

✔ ZATCA/invoicing always lives at entity level

You’re thinking about this exactly the right way now — this is platform-level architecture, not app-level, and you’ve landed on a model that scales legally, technically, and commercially.
