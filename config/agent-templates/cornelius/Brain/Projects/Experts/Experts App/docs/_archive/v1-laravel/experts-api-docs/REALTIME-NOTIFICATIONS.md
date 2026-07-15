---
title: "🔔 Real-Time Notifications Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/experts-api-docs"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🔔 Real-Time Notifications Guide

Complete guide for implementing real-time notifications with Laravel Reverb and Next.js.

---

## ✅ What's Already Set Up

- ✅ Laravel Reverb WebSocket server running on port 3020
- ✅ Pusher client configured for Reverb
- ✅ Private channel authentication
- ✅ UUID-based channel authorization
- ✅ Automatic toast notifications

---

## 🚀 Quick Start

### 1. Add Notification Provider to Layout

```tsx
// apps/experts-app/src/app/layout.tsx or (portal)/portal/layout.tsx
import { NotificationProvider } from "@providers/notification-provider";

export default function Layout({ children }) {
  return <NotificationProvider>{children}</NotificationProvider>;
}
```

### 2. Send Notification from Laravel

```php
use App\Events\PrivateMessageEvent;

// Send to specific user
event(new PrivateMessageEvent(
    uuid: $user->uuid,
    message: 'Your order has been confirmed!',
    type: 'success'
));
```

### 3. User Sees Toast Notification

The notification automatically appears as a toast in the browser!

---

## 📚 Event Types

### Public Events (No Auth Required)

```php
// apps/experts-api/app/Events/AnnouncementEvent.php
class AnnouncementEvent implements ShouldBroadcastNow
{
    public function broadcastOn(): array
    {
        return [new Channel('announcements')];
    }

    public function broadcastAs(): string
    {
        return 'announcement';
    }
}
```

**Frontend:**

```tsx
const channel = pusherService.subscribe("announcements");
channel.bind("announcement", (data) => {
  console.log("Announcement:", data);
});
```

### Private Events (User-Specific)

```php
// apps/experts-api/app/Events/PrivateMessageEvent.php
class PrivateMessageEvent implements ShouldBroadcastNow
{
    public function __construct(
        public string $uuid,  // User UUID
        public string $message,
        public string $type = 'info'
    ) {}

    public function broadcastOn(): array
    {
        return [new PrivateChannel("user.{$this->uuid}")];
    }
}
```

**Frontend:** Handled automatically by `NotificationProvider`!

### Presence Channels (Online Users)

```php
// apps/experts-api/app/Events/UserJoinedEvent.php
class UserJoinedEvent implements ShouldBroadcastNow
{
    public function broadcastOn(): array
    {
        return [new PresenceChannel('chat-room')];
    }
}
```

**Channel Authorization (routes/channels.php):**

```php
Broadcast::channel('chat-room', function ($user) {
    return [
        'uuid' => $user->uuid,
        'name' => $user->name,
    ];
});
```

**Frontend:**

```tsx
const channel = pusherService.subscribe("presence-chat-room");

channel.bind("pusher:subscription_succeeded", (members) => {
  console.log("Online users:", members.count);
  members.each((member) => {
    console.log(member.info); // {uuid, name}
  });
});

channel.bind("pusher:member_added", (member) => {
  console.log("User joined:", member.info);
});

channel.bind("pusher:member_removed", (member) => {
  console.log("User left:", member.info);
});
```

---

## 🎯 Common Use Cases

### 1. Course Enrollment Notification

**Laravel:**

```php
// When user enrolls in a course
event(new PrivateMessageEvent(
    uuid: $user->uuid,
    message: "You've been enrolled in {$course->title}!",
    type: 'success'
));
```

**Result:** User sees toast notification immediately!

### 2. Assignment Graded

**Laravel:**

```php
event(new PrivateMessageEvent(
    uuid: $student->uuid,
    message: "Your assignment '{$assignment->title}' has been graded: {$grade}%",
    type: $grade >= 70 ? 'success' : 'warning'
));
```

### 3. Live Course Updates

**Laravel:**

```php
// Broadcast to all students in a course
event(new CourseUpdateEvent(
    courseUuid: $course->uuid,
    message: "Instructor started a live session!",
    url: "/courses/{$course->uuid}/live"
));
```

**Frontend:**

```tsx
// In course page
const channel = pusherService.subscribe(`course.${courseUuid}`);
channel.bind("course-update", (data) => {
  toast.info(data.message, {
    action: {
      label: "Join",
      onClick: () => router.push(data.url),
    },
  });
});
```

---

## 🔧 Advanced Features

### Custom Notification Listener

```tsx
import { notificationService } from "@services/websocket/notification-service";

function MyComponent() {
  useEffect(() => {
    // Add custom handler
    notificationService.addListener("my-handler", (notification) => {
      // Custom logic (e.g., update UI state, play sound, etc.)
      console.log("Custom handler:", notification);
    });

    return () => {
      notificationService.removeListener("my-handler");
    };
  }, []);
}
```

### Subscribe to Multiple Channels

```tsx
import { pusherService } from "@services/websocket/pusher";

function CourseRoom({ courseId }) {
  useEffect(() => {
    // Subscribe to course channel
    const courseChannel = pusherService.subscribe(`course.${courseId}`);

    courseChannel.bind("new-comment", handleNewComment);
    courseChannel.bind("instructor-joined", handleInstructorJoined);

    return () => {
      pusherService.unsubscribe(`course.${courseId}`);
    };
  }, [courseId]);
}
```

---

## 📋 Channel Naming Conventions

| Pattern                 | Example                  | Auth Required | Use Case          |
| ----------------------- | ------------------------ | ------------- | ----------------- |
| `public-*`              | `public-announcements`   | ❌ No         | Global broadcasts |
| `private-user.{uuid}`   | `private-user.abc-123`   | ✅ Yes        | User-specific     |
| `private-course.{uuid}` | `private-course.def-456` | ✅ Yes        | Course-specific   |
| `presence-*`            | `presence-chat-room`     | ✅ Yes        | Online presence   |

---

## 🛠️ Debugging

### Enable Pusher Debug Logging

```tsx
import Pusher from "pusher-js";

if (process.env.NODE_ENV === "development") {
  Pusher.logToConsole = true;
}
```

### Check Active Subscriptions

```tsx
import { pusherService } from "@services/websocket/pusher";

// In browser console
console.log(pusherService.getConnectionState());
console.log(pusherService.isConnected());
```

### Monitor Reverb Activity

```bash
docker exec -it experts-development-api php artisan reverb:start --debug
```

Watch for:

```
[DEBUG] Broadcasting to channel: private-user.abc-123
[DEBUG] Event: private-message
[DEBUG] Sent to 1 connection(s)
```

---

## 🚨 Troubleshooting

### No Messages Received

1. ✅ Check Reverb is running: `docker logs experts-development-api | grep reverb`
2. ✅ Check broadcasting driver: `BROADCAST_CONNECTION=reverb` in `.env`
3. ✅ Check browser console for connection status
4. ✅ Verify user is authenticated

### Subscription Failed

1. ✅ Check access token is present
2. ✅ Verify `/v1/broadcasting/auth` route works
3. ✅ Check channel authorization in `routes/channels.php`
4. ✅ Verify UUID matches between event and channel

### CORS Errors

1. ✅ Add origin to `allowed_origins` in `config/reverb.php`
2. ✅ Check API CORS middleware configuration

---

## 📦 Files Reference

| File                                                                            | Purpose                    |
| ------------------------------------------------------------------------------- | -------------------------- |
| `apps/experts-api/app/Events/PrivateMessageEvent.php`                           | Example private event      |
| `apps/experts-api/routes/channels.php`                                          | Channel authorization      |
| `apps/experts-api/routes/v1/api.php`                                            | Broadcasting auth endpoint |
| `apps/experts-app/src/packages/core/services/websocket/pusher.ts`               | Pusher client service      |
| `apps/experts-app/src/packages/core/services/websocket/notification-service.ts` | Notification handler       |
| `apps/experts-app/src/packages/providers/src/notification-provider.tsx`         | Auto-init provider         |

---

## 🎯 Next Steps

1. ✅ Add `NotificationProvider` to your layout
2. ✅ Create events for your use cases
3. ✅ Add channel authorization rules
4. ✅ Test with real user scenarios
5. ✅ Deploy to production

---

## 🎉 Success Checklist

- ✅ Reverb server running
- ✅ Public channels working
- ✅ Private channels working
- ✅ Channel authentication working
- ✅ UUID-based authorization working
- ✅ Toast notifications showing
- ✅ Production-ready code

**You're ready for production!** 🚀
