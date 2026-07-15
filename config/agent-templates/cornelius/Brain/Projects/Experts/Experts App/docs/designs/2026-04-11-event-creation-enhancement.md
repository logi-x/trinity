---
title: "EVENT CREATION ENHANCEMENT"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/event-creation-enhancement"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# EVENT CREATION ENHANCEMENT

Q: I had an idea, not fully implemented yet, where in create event form

General details title description…etc.

Then hosts are selected (can be existing user or manually added? )

Then fill in agendas based on selected hosts, and add an option for manually adding speakers details

Could you solidify the idea for me

A: That’s a very solid idea, and you’re actually converging on a pattern used by mature event platforms (Hopin, Webex, internal CMS tools).

Let me solidify it into a clean mental model + data model + UX flow, without over-engineering.

Core principle (this unlocks everything)

Hosts define authority.
Speakers define presentation.
Agenda binds time + speaker (not authority).

Once you accept this, the whole flow becomes obvious.

1️⃣ Conceptual separation (important)
EventHost (already correct)

Who is officially hosting the event:

permissions

publishing rights

revenue share

visibility on event page

"Who owns / runs this event?"

Speaker (new concept, lightweight)

Who speaks in agenda items:

can be a host

can be a user

can be external

can be manual

"Who is talking at this moment?"

EventAgenda

When + what + which speaker

"At 10:30, Ahmed speaks about X"

2️⃣ Proposed flow (UX-first, very clean)
Step 1: General Event Info

Nothing changes here.

title

description

category

dates

price

etc.

Step 2: Hosts (Authority layer)

UI:

Select existing users

Assign role: primary / co / guest

Revenue share

Visibility toggle

Rules:

At least one primary host

Hosts must be users (no manual typing here)

This step answers:

“Who is responsible for this event?”

Step 3: Speakers (Presentation layer)

This is the missing layer you intuited 👍

UI:

List of speakers

“Add speaker” button

For each speaker:

🔘 Select from hosts

🔘 Select from users

🔘 Add manually

Speaker fields:

name (required)

avatar (optional)

title / role (optional)

userId? (optional, if internal)

This step answers:

“Who is allowed to speak?”

Step 4: Agenda (Time + Speaker binding)

Now the agenda form becomes elegant.

For each agenda item:

title

description

start time

end time

speaker (dropdown from speakers list)

optional “multiple speakers” later

No typing speaker names again.
No duplication.
No ambiguity.

3️⃣ Data model (minimal, scalable)
EventHost (unchanged ✅)
model EventHost {
eventId String
userId String
role HostRole
// authority fields
}

Speaker (NEW, lightweight)
model EventSpeaker {
id String @id @default(dbgenerated("gen_random_uuid()"))
eventId String
userId String? // null = external
name String
avatarUrl String?
title String?

event Event @relation(fields: [eventId], references: [id], onDelete: Cascade)
user User? @relation(fields: [userId], references: [id], onDelete: SetNull)

@@index([eventId])
}

Why this is good:

no hard coupling to hosts

supports external speakers

supports internal users

survives deletions

reusable across agenda items

EventAgenda (clean + focused)
model EventAgenda {
id String
eventId String
speakerId String?

title String
description String?
startTime String // HH:mm
endTime String // HH:mm
position Int

speaker EventSpeaker? @relation(fields: [speakerId], references: [id], onDelete: SetNull)
}

Agenda now:

does not care if speaker is host/user/external

only cares about display + time

4️⃣ UX details that make this feel “premium”
✨ Smart defaults

When hosts are selected → auto-create speakers for them

Primary host pre-selected as first speaker

✨ Visual clarity

Speaker chips:

🟢 Host

🔵 Internal user

⚪ External

✨ Validation rules

Agenda item must have:

time range

title

speaker (optional if you want flexibility)

✨ Future-proofing (without implementing now)

Panel discussions (multiple speakers per agenda)

Speaker bios page

Reusable speaker profiles across events

5️⃣ Why this design is correct

✔ No redundancy
✔ No over-normalization
✔ Clear ownership vs presentation
✔ Works for webinars, panels, workshops
✔ Matches how real events work
✔ Avoids fake users
✔ Avoids tight coupling

You avoided a very common trap by not linking agenda → host directly.

6️⃣ TL;DR (the essence)

Hosts = authority & money

Speakers = presentation

Agenda = time + speaker

Manual speakers are first-class citizens

Hosts can be speakers, but not all speakers are hosts

Your idea is not only valid — it’s the right abstraction.
