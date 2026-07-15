---
title: "TIMELINE IMPLEMENTATION"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/timeline-implementation"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  🧵 Experts User Timeline / Activity Feed System
  🎯 Goals

Build a system that:

Shows recent user activities across the platform

Supports public profiles (/@username)

Supports follow / unfollow

Powers:

Home feed

Profile feed

Instructor feed

Is real-time capable

Is privacy-aware

Scales cleanly

🧠 Core Design Philosophy

Activities are immutable events. Feeds are materialized views.

Key principles:

Activity ≠ Notification

Activity ≠ Audit log

Activity ≠ Analytics

Activities are public-facing, human-readable events

Feed queries must be fast

🧱 High-Level Architecture
[Domain Action]
↓
[Activity Generator]
↓
[activities table] ← source of truth
↓
[Feed Queries / Materialization]
↓
[HTTP fetch + SSE updates]

🗃️ Database Schema
users
id
username (unique)
display_name
avatar_url
is_private

follows
follower_id
following_id
created_at

PRIMARY KEY (follower_id, following_id)

activities
id UUID
actor_id UUID
type TEXT
entity_type TEXT
entity_id UUID
metadata JSONB
visibility TEXT -- public | followers | private
created_at TIMESTAMP

Why JSON metadata?

Avoids schema churn

Supports future activity types

Keeps feed flexible

🧾 Activity Types (Experts-specific)
🎓 Learning

course.completed

lesson.completed

certificate.issued

course.enrolled

👩‍🏫 Teaching

course.published

lesson.published

event.created

💬 Community

post.created

post.commented

comment.replied

post.liked (optional)

📅 Events

event.attended

event.started

👥 Social

user.followed

profile.updated

🔒 Visibility Rules
Activity Visibility
Course completed Public / Followers
Post created Public
Commented Public
Attended event Followers
Profile updated Followers
Private course Private

Never store hidden activities — just filter at query time.

🧠 Activity Creation Strategy
Activities are generated server-side only
await createActivity({
actorId,
type: "post.commented",
entityType: "post",
entityId: postId,
metadata: {
postTitle,
},
});

Never generate from UI.

🔧 Activity Service
async function createActivity(data) {
return prisma.activity.create({ data });
}

Later enhancements:

batch insert

fan-out caching

dedupe rules

📰 Feed Types
1️⃣ Home Feed (Following)
SELECT \*
FROM activities
WHERE actor_id IN (
SELECT following_id FROM follows WHERE follower_id = :me
)
AND visibility IN ('public', 'followers')
ORDER BY created_at DESC
LIMIT 50;

2️⃣ Profile Feed (/@username)
SELECT \*
FROM activities
WHERE actor_id = :userId
AND visibility = 'public'
ORDER BY created_at DESC;

3️⃣ Instructor Feed

Teaching activities

Enrollment events

Reviews

Revenue (private)

📡 Real-Time Updates (Optional but recommended)
SSE Feed Updates
Channel: feed:user:{userId}

Flow:

New activity created

Publish to Redis

SSE pushes to followers

Public feeds:

No auth required

Personal feed:

Auth required

🔔 Feed ≠ Notifications
Feature Feed Notifications
Persistence Yes Yes
Audience Many Single user
Importance Low–Medium High
Delivery Pull + SSE Push + SSE
Real-time required Optional Yes
👤 Public Profiles (/@username)
Route
/@{username}

Shows:

Avatar

Bio

Follow button

Activity feed

Courses / events (optional)

Follow Button Logic

Logged-out → prompt login

Logged-in → follow/unfollow

Private profile → request flow (optional)

🔄 Follow / Unfollow Implementation
POST /api/follow
DELETE /api/follow

Creates:

follows record

user.followed activity (optional)

Notification to followed user

🧪 Performance Strategy
Indexing (critical)
INDEX (actor_id, created_at)
INDEX (type)
INDEX (visibility)

Pagination

Cursor-based (created_at + id)

Never offset-based

🚫 What NOT to Do

❌ Build feed from notifications
❌ Generate activities in client
❌ Store rendered strings in DB
❌ Hardcode feed logic
❌ Overuse real-time

🧭 UX Best Practices

Human-readable strings generated in UI

Show relative time

Collapse similar events

Hide spammy actions

Never notify on likes (optional)

🧠 Summary

✔ Activity feed = public history
✔ Notifications = personal alerts
✔ Activities are immutable
✔ Feeds are filtered views
✔ Follow graph drives feed
✔ SSE enhances UX but not required

This design:

matches modern social platforms

is flexible for Experts’ growth

avoids overengineering

remains easy to reason about
