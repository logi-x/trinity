---
title: "NOTIFICATION SYSTEM IMPLEMENTATION"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/notification-system-implementation"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]
  this is how modern platforms (Slack, GitHub, Linear, Notion) actually do it.

📣 Experts Notification System — Architecture & Implementation Guide
🎯 Goals

The notification system must:

Be real-time

Be reliable

Scale with users

Support multiple delivery channels

Never block UX

Degrade gracefully

Be auditable (for important events)

🧠 Core Design Philosophy

Notifications are event-driven, user-targeted, and async.

Key principles:

Notifications ≠ SSE events

SSE is a delivery mechanism, not the source of truth

Notifications must be persisted

Delivery must be best-effort

UI must always work without real-time

🧩 High-Level Architecture
[Domain Event]
↓
[Notification Generator]
↓
[Database (notifications table)]
↓
[Redis Pub/Sub]
↓
[SSE → authenticated clients]
↓
[UI Notification Center]

🧱 Tech Stack (Recommended)
Core

Next.js App Router

PostgreSQL (persistent notifications)

Prisma ORM

Redis

Pub/Sub (real-time)

Optional queues later

SSE (real-time delivery)

NextAuth (authentication)

Optional (later)

Email (Postmark / SES)

Push notifications (FCM / APNs)

Background workers (BullMQ)

🗃️ Database Schema
notifications table
CREATE TABLE notifications (
id UUID PRIMARY KEY,
user_id UUID NOT NULL,
type TEXT NOT NULL,
title TEXT NOT NULL,
body TEXT,
entity_type TEXT,
entity_id UUID,
is_read BOOLEAN DEFAULT FALSE,
created_at TIMESTAMP DEFAULT NOW()
);

Why DB-backed?

Inbox persistence

Read/unread state

Offline users

Auditing

Replays

🔔 Notification Types (Experts-specific)
🎓 Learning & Courses
Event When
Course enrolled User enrolls
Course completed User finishes course
Certificate issued Certificate generated
New lesson released Instructor publishes lesson
Course updated Major content change
👩‍🏫 Instructor
Event When
New enrollment User enrolls in course
Course review User submits review
Question asked Comment/question posted
Event registration User registers for event
Payout processed Revenue payout
💬 Community
Event When
Post liked Someone likes your post
Post commented New comment
Reply to comment Reply on your comment
Mentioned @username
Post featured Highlighted by admins
📅 Events
Event When
Event reminder Before start
Event starting Live now
Event canceled Instructor cancels
Event updated Schedule change
🔐 System & Account
Event When
Password changed Security
New login New device
Subscription renewed Billing
Payment failed Billing issue
Admin message Platform notice
🧠 Notification Generation Strategy
Never generate notifications in UI

❌ Client → Notification
✅ Domain event → Notification

Example:

// user enrolls
await enrollUser();

await createNotification({
userId: instructorId,
type: "course.enrollment",
title: "New student enrolled",
entityId: courseId,
});

🔧 Notification Service (Server-side)
async function createNotification(data) {
const notification = await prisma.notification.create({ data });

redis.publish(
`notifications:user:${data.userId}`,
JSON.stringify(notification)
);
}

📡 Real-Time Delivery (SSE)
Authenticated SSE endpoint
GET /api/events/notifications

Rules:

Requires NextAuth session

One connection per tab

User-specific stream

SSE channel
notifications:user:{userId}

🖥️ Client-side Flow
Notification Center

Fetch initial notifications (HTTP)

Subscribe to SSE for live updates

Merge new notifications into list

Increment unread count

Example
useSWR("/api/notifications");
useNotificationsSSE();

🔐 Authentication Rules
Stream Auth
Notifications ✅ Required
Viewer counts ❌ Public
Likes count ❌ Public
Feed updates ❌ Public

Never expose notification SSE publicly.

🧪 Failure Handling
If SSE fails:

Notifications still stored in DB

User sees them on refresh

No UI blocking

If Redis fails:

DB still records notifications

Real-time temporarily disabled

If DB fails:

Event should fail (important)

🧠 Read / Unread Logic

is_read flag

Mark as read on click

Bulk mark supported

Never delete automatically

Optional later:

Archive

Snooze

Priority levels

📈 Scaling Strategy
Phase 1 (now)

DB + Redis Pub/Sub

SSE

Phase 2 (growth)

Redis Streams or BullMQ

Email fan-out

Push notifications

Retry queues

Phase 3 (large scale)

Event bus (Kafka-like)

Notification preferences

Rate limiting

🚫 What NOT to Do

❌ Notifications only via SSE
❌ No persistence
❌ UI-generated notifications
❌ One SSE per notification
❌ Polling every few seconds
❌ Storing notifications only in Redis

🧭 Summary

✔ DB = source of truth
✔ Redis = delivery
✔ SSE = real-time UX
✔ NextAuth = security
✔ Notifications ≠ presence
✔ Notifications ≠ likes

This architecture:

scales

survives failures

keeps UX smooth

matches industry leaders
