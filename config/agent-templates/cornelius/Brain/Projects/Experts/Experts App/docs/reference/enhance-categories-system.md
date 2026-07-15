---
title: "ENHANCE CATEGORIES SYSTEM"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/enhance-categories-system"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# ENHANCE CATEGORIES SYSTEM

Q: How can I enhance Category without overcomplicating things ?

current

model Category {
id String @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
name String @db.VarChar(255)
position Int @default(0)
createdAt DateTime @default(now()) @map("created_at") @db.Timestamptz(6)

    @@map("categories")
    @@schema("public")

}

and it's not linked to anything yet, as seen here

model Course {
id String @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
processingEntityId String @map("processing_entity_id") @db.Uuid
title String @db.VarChar(255)
description String?
shortDescription String? @map("short_description") @db.VarChar(500)
thumbnailUrl String? @map("thumbnail_url")
category String? @db.VarChar(255)
level String @default("Beginner") @db.VarChar(50)
price Decimal @default(0) @db.Decimal(10, 2)
isPublished Boolean @default(false) @map("is_published")
isFeatured Boolean @default(false) @map("is_featured")
duration String? @db.VarChar(50)
totalLessons Int @default(0) @map("total_lessons")
students Int @default(0)
learningOutcomes Json? @map("learning_outcomes")
requirements Json?
detailedDescription String? @map("detailed_description")
tags String[] @default([])

    publishingStatus PublishingStatus @default(draft) @map("publishing_status")
    createdAt        DateTime         @default(now()) @map("created_at") @db.Timestamptz(6)
    updatedAt        DateTime         @default(now()) @updatedAt @map("updated_at") @db.Timestamptz(6)

    businessEntity BusinessEntity     @relation(fields: [processingEntityId], references: [id], onDelete: Restrict)
    instructors    CourseInstructor[]
    enrollments    Enrollment[]
    certificates   Certificate[]
    lessonProgress LessonProgress[]
    modules        Module[]
    invoices       Invoice[]

    @@index([category])
    @@index([isPublished])
    @@index([processingEntityId])
    @@index([publishingStatus])
    @@map("courses")
    @@schema("public")

}

model Event {
id String @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
processingEntityId String @map("processing_entity_id") @db.Uuid
title String @db.VarChar(255)
description String?
shortDescription String? @map("short_description") @db.VarChar(500)
thumbnailUrl String? @map("thumbnail_url")
eventType String @default("webinar") @map("event_type") @db.VarChar(50)
category String? @db.VarChar(255)
scheduleType String @default("single") @map("schedule_type") @db.VarChar(50)
recurringDays String[] @map("recurring_days")
startDate DateTime @map("start_date") @db.Timestamptz(6)
endDate DateTime? @map("end_date") @db.Timestamptz(6)
timezone String @default("Asia/Riyadh") @db.VarChar(50)
locationType String @default("online") @map("location_type") @db.VarChar(50)
locationDetails String? @map("location_details")
meetingUrl String? @map("meeting_url")
maxAttendees Int? @map("max_attendees")
price Decimal @default(0) @db.Decimal(10, 2)
isFree Boolean @default(true) @map("is_free")
isPublished Boolean @default(false) @map("is_published")
isFeatured Boolean @default(false) @map("is_featured")
learningOutcomes Json? @map("learning_outcomes")
requirements Json?
detailedDescription String? @map("detailed_description")
tags String[] @default([])
publishingStatus PublishingStatus @default(draft) @map("publishing_status")
createdAt DateTime @default(now()) @map("created_at") @db.Timestamptz(6)
updatedAt DateTime @default(now()) @updatedAt @map("updated_at") @db.Timestamptz(6)

    agenda        EventAgenda[]
    registrations EventRegistration[]
    slots         EventSlot[]

    processingEntity BusinessEntity @relation(fields: [processingEntityId], references: [id], onDelete: Restrict)
    hosts            EventHost[]
    invoices         Invoice[]

    @@index([startDate])
    @@index([processingEntityId])
    @@index([publishingStatus])
    @@map("events")
    @@schema("public")

}

A: I’ll give you a progressive enhancement path that:

fixes the current inconsistencies

adds real value

stays boring and reversible

avoids “category hell”

First: what’s wrong with the current state (gently)

Right now you have:

Course.category String?
Event.category String?
Category.name String

This creates three problems:

❌ No referential integrity

❌ Typos / casing differences ("AI" vs "Ai" vs "Artificial Intelligence")

❌ Category table is unused → dead schema

But you also don’t need:

deep trees

polymorphic joins

tagging engines

SEO taxonomies

So we’ll fix it with the smallest useful step.

The correct goal (keep this in mind)

Categories are curated, finite, and platform-owned
Tags are free-form, user-owned, and many

You already did this right by having:

tags String[]

So don’t turn categories into tags.

Step 1 — Make Category real, but keep it simple (recommended)
Enhance Category just enough
model Category {
id String @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
slug String @unique @db.VarChar(100)
name String @db.VarChar(255)
position Int @default(0)
isActive Boolean @default(true)
createdAt DateTime @default(now()) @map("created_at") @db.Timestamptz(6)

@@index([position])
@@map("categories")
@@schema("public")
}

Why these fields:

slug → stable, URL-safe, API-safe

position → curated ordering

isActive → soft hide without breaking data

No parents. No trees. No magic.

Step 2 — Link Course & Event via categoryId (not string)
Course (clean)
model Course {
...
categoryId String? @map("category_id") @db.Uuid

category Category? @relation(fields: [categoryId], references: [id])

@@index([categoryId])
}

Event (same pattern)
model Event {
...
categoryId String? @map("category_id") @db.Uuid

category Category? @relation(fields: [categoryId], references: [id])

@@index([categoryId])
}

🚨 Important

Remove:

category String?

This is the biggest correctness win with the least complexity.

Step 3 — How this should behave in the product
Who controls categories?

Platform admins only

Not instructors

Not entities

This keeps:

search clean

filters meaningful

analytics reliable

Instructor experience

Select one category from dropdown

Optional (can be null)

No creation

No editing

UX copy

Category (optional)
Used to help learners discover your content

Step 4 — Querying stays dead simple
Courses by category
where: { category: { slug: "ai" } }

Featured categories
orderBy: { position: "asc" }

No joins explosion
No recursive trees
No polymorphism
What NOT to add (yet)

❌ parentId (hierarchies explode fast)
❌ many-to-many categories
❌ polymorphic category tables
❌ “subcategories”
❌ SEO taxonomies

You can always add hierarchy later without breaking this design.

If you want ONE future-proofing hook (optional)

If you suspect categories may diverge later:

type CategoryScope = "course" | "event" | "both"

scope String @default("both")

But this is optional — don’t add unless needed.

Migration strategy (safe)

Add Category.slug

Backfill categories

Add categoryId to Course/Event

Migrate existing category strings → IDs

Drop old category string fields

No downtime required.

TL;DR (the “don’t overcomplicate” answer)

✅ Keep categories curated and finite

✅ Use a real FK (categoryId)

✅ Add slug, position, isActive

❌ Don’t add hierarchy yet

❌ Don’t let instructors create categories

✅ Tags stay free-form

This gives you:

clean filtering

stable analytics

future extensibility

zero conceptual overhead

---

Q: "decide when/if to add subcategories" I've tried this before, and turned into a nightmare LOL..
how to align this with search & recommendations ?

A: 😂 you’re not wrong — subcategory trees are where good schemas go to die.
The fact you’ve already felt that pain is exactly why this question matters.

I’ll give you a battle-tested way to align categories + search + recommendations without ever introducing subcategories, and still get 95% of the benefit.

The core insight (this is the unlock)

Categories are for navigation.
Search & recommendations should NOT depend on category hierarchies.

Most systems fail because they try to make categories do everything.

Instead:

Category = coarse intent

Tags + text = fine intent

Behavior = relevance

Once you accept this, subcategories become unnecessary.

The winning model (simple + powerful)
1️⃣ Category = single, curated, flat

You already landed here (good):

One category per course/event

Admin-curated

Small set (10–30 max)

Examples:

AI

Business

Design

Programming

Health

Leadership

This is not a taxonomy — it’s a shelf.

2️⃣ Tags = expressive, user-driven, multi-valued

You already have:

tags String[]

This is where “subcategories” actually belong.

Examples:

ai, llm, chatgpt, prompt-engineering

react, nextjs, typescript

marketing, seo, ads

Tags do what subcategories pretend to do — but better.

How search should work (very important)
🔍 Search input → ranked signals

When a user searches "chatgpt for marketing":

Rank by multiple signals, not structure:

Full-text match

title

description

tags

Category boost

if category = AI or Marketing

Behavioral signals

enrollments

views

completion

Freshness

Entity trust / featured

No tree traversal. No recursion. No joins nightmare.

Example (pseudo-ranking)
score =
textMatch _0.5 +
categoryMatch_ 0.2 +
popularity _0.2 +
freshness_ 0.1

Categories are just one signal, not the backbone.

Recommendations (this is where people overthink)
Rule #1 (pin this)

Recommendations are behavior-first, not taxonomy-first

Categories only help you filter the candidate pool.

Example recommendation flow

“Users who viewed this also liked…”

Start with:

same category

Narrow by:

overlapping tags

Rank by:

conversion rate

rating

recency

That’s it.

No subcategories needed.

Example query logic (conceptual)
where: {
categoryId: current.categoryId,
tags: { hasSome: current.tags }
}
orderBy: [
{ popularity: "desc" },
{ averageRating: "desc" }
]

This gives much better results than a tree ever will.

When (and only when) subcategories become necessary

There are only two valid triggers:

✅ Trigger 1 — Category exceeds ~40% of catalog

Example:

“Programming” contains 60% of all courses

Then you don’t add subcategories — you split the category:

Programming → Frontend / Backend / Mobile

Flat, still curated.

✅ Trigger 2 — Search logs prove confusion

If users consistently search:

“AI → Prompt Engineering”

“Design → UI UX”

Then:

promote common tags

add tag-based filters

maybe surface “Popular topics” UI

Still not hierarchy.

How to simulate subcategories without schema changes

This is the trick you’ll like.

Curated “topic clusters” (purely at query/UI level)

Example:

AI category
├─ Prompt Engineering (tag cluster)
├─ LLMs
├─ Computer Vision

But:

no DB hierarchy

no FK

no recursion

no migrations

Just saved queries / configs.

Why this avoids your previous nightmare
Old approach This approach
Recursive joins Flat filters
Rigid structure Flexible tags
Schema migrations UI logic
Hard to change Easy to iterate
Breaks analytics Improves analytics
What I’d recommend you do right now
✅ Lock this rule in your head:

Categories never nest. Ever.

✅ Use categories to:

build nav

filter browse pages

seed recommendations

✅ Use tags to:

refine search

power “related content”

adapt to trends

❌ Never use categories as a tree
TL;DR (the “learned the hard way” version)

You’re right: subcategories are a nightmare

You don’t need them for search

You don’t need them for recommendations

Flat categories + tags + behavior > any hierarchy

If a category grows too big → split it

If a topic emerges → promote a tag

You already have the right instincts — this approach lets you move fast without reopening old wounds.
