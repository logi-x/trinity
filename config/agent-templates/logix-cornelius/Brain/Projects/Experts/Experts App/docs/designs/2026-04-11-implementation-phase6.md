---
title: "IMPLEMENTATION PHASE6"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/implementation-phase6"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  Short answer (opinionated, but proven)

Do NOT show an entity dropdown by default.
Let the system decide the default, and expose entity selection only when it’s relevant.

That keeps UX clean, prevents legal mistakes, and still supports your business model.

The guiding principle (this is the anchor)

Choosing a processing entity is a legal/financial decision, not a content decision.

Most instructors:

don’t understand entities

don’t care about VAT / ZATCA

just want to publish content

So we optimize for safe defaults, not maximum choice.

Recommended UX model (exact flow)
🟢 Default path (90% of users)

System decides automatically

When user creates a course/event:

processingEntityId = Experts

No dropdown

No questions

No friction

Always valid legally

This is your happy path.

🟡 Advanced path (explicit intent required)

User opts in to choosing another entity

Instead of a dropdown, use an explicit action:

🔘 “Publish under a different organization”

Only when clicked:

Show entity selector

Show explanation text

Trigger approval flow

This avoids accidental misuse.

What should determine the default entity?
✅ Rule #1 — Platform default

If nothing else is explicitly chosen:

processingEntity = Experts

Always.

This guarantees:

payments work

invoices are issued

no orphan content

legal safety

✅ Rule #2 — Explicit user choice overrides default

Only if the user actively selects an entity:

and that entity exists

and the user has a valid relationship with it

and approval is granted

Then:

processingEntity = SelectedEntity
publishingStatus = submitted

When should the dropdown appear?
✅ Show entity selector ONLY if:

user clicks “Publish under an organization”

OR user already has approved publishing rights with an entity

OR user is editing an already-approved entity-backed draft

❌ Do NOT show it:

on first draft creation

on basic “Create Event” flow

to new instructors

to casual users

How to decide which entities appear in the selector?

Only show entities where one of these is true:

User has an approved BusinessMembership

User has previously published content under that entity

Entity explicitly invited the user to publish (future feature)

Never show:

all entities

entities user has no relation to

UX copy matters a lot here

Instead of “Processing Entity”, say:

Published under

Experts Company Ltd (default)

And when changing:

⚠️ Publishing under another organization requires approval and affects invoicing and payouts.

This sets expectations correctly.

Backend enforcement (important)

Even if UI hides it, backend must still:

if (!processingEntityId) {
processingEntityId = DEFAULT_ENTITY_ID;
}

UI is convenience. Backend is authority.

TL;DR (clear rules)

✅ System decides default entity (Experts)

❌ No dropdown on initial creation

✅ Explicit opt-in to choose another entity

✅ Approval required for non-default entity

✅ Backend always enforces a valid entity

❌ Never rely on user “guessing” correctly

Why this is the right choice for Experts

This approach:

matches your legal constraints

reduces user confusion

avoids accidental ZATCA issues

keeps UX clean

scales to future entities

mirrors how real platforms work (Udemy, Eventbrite, Gumroad)
