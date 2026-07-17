---
title: "Server-Sent Events (SSE) Implementation Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/sse-implementation"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Server-Sent Events (SSE) Implementation Guide

## Overview

We've implemented a unified Server-Sent Events (SSE) system for real-time updates across the Experts platform. This replaces polling with efficient, real-time push notifications using Redis pub/sub.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client (Browser)                          │
│  useEventStream, useLikesStream, useViewsStream, etc.        │
└───────────────────┬─────────────────────────────────────────┘
                    │ SSE (EventSource)
                    ▼
┌─────────────────────────────────────────────────────────────┐
│              /api/events/stream (SSE Endpoint)               │
│  - Subscribes to multiple Redis channels                     │
│  - Streams events to clients                                 │
└───────────────────┬─────────────────────────────────────────┘
                    │ Redis Pub/Sub
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    Redis Channels                            │
│  - likes:post:123                                           │
│  - views:course:456                                         │
│  - ratings:course:789                                       │
│  - presence:user:abc                                        │
│  - feed:posts, feed:courses, feed:events                    │
└───────────────────┬─────────────────────────────────────────┘
                    │ publishEvent()
                    ▼
┌─────────────────────────────────────────────────────────────┐
│              API Routes (POST/PUT/DELETE)                    │
│  - /api/likes → publishLikeEvent()                          │
│  - /api/views/track → publishViewEvent()                    │
│  - /api/ratings → publishRatingEvent()                      │
│  - /api/presence/heartbeat → publishPresenceEvent()         │
│  - /api/posts → publishFeedEvent()                          │
└─────────────────────────────────────────────────────────────┘
```

## Available Channels

### 1. Likes (`likes:{contentType}:{contentId}`)

**Events:**

- `like_added` - User liked content
- `like_removed` - User unliked content
- `reaction_changed` - User changed reaction type

**Example:**

```typescript
// Channel: likes:post:123e4567-e89b-12d3-a456-426614174000
useLikesStream("post", postId);
```

**Hook:** `useLikesStream(contentType, contentId)`

### 2. Views (`views:{contentType}:{contentId}`)

**Events:**

- `view_count_updated` - View count incremented

**Example:**

```typescript
// Channel: views:course:123e4567-e89b-12d3-a456-426614174000
useViewsStream("course", courseId);
```

**Hook:** `useViewsStream(contentType, contentId)`

### 3. Ratings (`ratings:{contentType}:{contentId}`)

**Events:**

- `rating_added` - New rating submitted
- `rating_updated` - Rating updated
- `rating_removed` - Rating removed

**Example:**

```typescript
// Channel: ratings:course:123e4567-e89b-12d3-a456-426614174000
useEventStream([`ratings:course:${courseId}`], {
  eventHandlers: {
    rating_added: (event) => {
      // Handle new rating
      mutate(`/api/ratings/course/${courseId}`);
    },
  },
});
```

### 4. Presence (`presence:user:{userId}`)

**Events:**

- `user_online` - User came online
- `user_offline` - User went offline
- `user_active` - User activity update

**Example:**

```typescript
// Channel: presence:user:123e4567-e89b-12d3-a456-426614174000
usePresenceStream([userId1, userId2, userId3]);
```

**Hook:** `usePresenceStream(userIds[])`

### 5. Feed Updates (`feed:{feedType}`)

**Events:**

- `item_added` - New post/course/event created
- `item_updated` - Post/course/event updated

**Feed Types:**

- `feed:posts` - New posts feed
- `feed:courses` - New courses feed
- `feed:events` - New events feed

**Example:**

```typescript
// Channels: feed:posts, feed:courses, feed:events
useFeedStream(["posts", "courses", "events"]);
```

**Hook:** `useFeedStream(feedTypes[])`

### 6. Post Events (`post:{postId}:events`)

**Events:**

- `comment_added` - New comment on post
- `comment_deleted` - Comment deleted
- `post_updated` - Post updated
- `post_deleted` - Post deleted

**Example:**

```typescript
// Channel: post:123e4567-e89b-12d3-a456-426614174000:events
usePostEvents(postId, (event) => {
  if (event.type === "comment_added") {
    mutateComments();
  }
});
```

**Hook:** `usePostEvents(postId, callback)` (already implemented)

## Usage Examples

### 1. Real-time Like Updates

```typescript
import {useLikesStream} from "@/hooks/use-likes-stream";

function PostCard({postId}: {postId: string}) {
  // Automatically invalidates /api/likes/post/{postId} on like events
  useLikesStream("post", postId);

  const {data: likes} = useApiQuery(`/api/likes/post/${postId}`);

  return <div>Likes: {likes?.totalLikes}</div>;
}
```

### 2. Real-time View Count Updates

```typescript
import {useViewsStream} from "@/hooks/use-views-stream";

function CoursePage({courseId}: {courseId: string}) {
  // Automatically invalidates view count cache
  useViewsStream("course", courseId);

  const {data: course} = useApiQuery(`/api/courses/${courseId}`);

  return <div>Views: {course?.viewCount}</div>;
}
```

### 3. Real-time Presence Updates

```typescript
import {usePresenceStream} from "@/hooks/use-presence-stream";
import {useBatchPresence} from "@/hooks/use-presence";

function CommentList({comments}: {comments: Comment[]}) {
  const userIds = comments.map((c) => c.author_uuid).filter(Boolean);

  // Real-time presence updates
  usePresenceStream(userIds);

  // Fetch presence data
  const {presenceMap} = useBatchPresence(userIds);

  return (
    <div>
      {comments.map((comment) => {
        const presence = presenceMap.get(comment.author_uuid);
        return (
          <div key={comment.id}>
            <span>{comment.author_name}</span>
            {presence?.isOnline && <span>🟢 Online</span>}
          </div>
        );
      })}
    </div>
  );
}
```

### 4. Real-time Feed Updates

```typescript
import {useFeedStream} from "@/hooks/use-feed-stream";

function HomePage() {
  // Listen to all feed updates
  useFeedStream(["posts", "courses", "events"]);

  const {data: posts} = useApiQuery("/api/posts");
  const {data: courses} = useApiQuery("/api/courses?published=true");
  const {data: events} = useApiQuery("/api/events");

  return (
    <div>
      <PostList posts={posts} />
      <CourseList courses={courses} />
      <EventList events={events} />
    </div>
  );
}
```

### 5. Custom Event Handling

```typescript
import {useEventStream} from "@/hooks/use-event-stream";
import {mutate} from "swr";

function CustomComponent({contentId}: {contentId: string}) {
  useEventStream([`custom:${contentId}`], {
    eventHandlers: {
      custom_event: (event) => {
        // Custom handling
        console.log("Custom event received:", event);
        mutate(`/api/custom/${contentId}`);
      },
    },
  });

  return <div>Listening for custom events...</div>;
}
```

## API Functions

### Publishing Events (Server-Side)

```typescript
import {
  publishEvent,
  publishLikeEvent,
  publishRatingEvent,
  publishViewEvent,
  publishPresenceEvent,
  publishFeedEvent,
} from "@/lib/redis";

// Generic event
await publishEvent("custom:channel", "event_type", { data: "value" });

// Like event
await publishLikeEvent("post", postId, "like_added", {
  userId,
  reactionType: "like",
});

// Rating event
await publishRatingEvent("course", courseId, "rating_added", {
  userId,
  rating: 5,
});

// View event
await publishViewEvent("post", postId, { viewCount: 100 });

// Presence event
await publishPresenceEvent(userId, "user_active", {
  lastActivityAt: new Date().toISOString(),
});

// Feed event
await publishFeedEvent("posts", "item_added", { postId, title: "New Post" });
```

## Implementation Checklist

### ✅ Completed

- [x] Unified SSE endpoint (`/api/events/stream`)
- [x] Redis pub/sub integration
- [x] Generic `useEventStream` hook
- [x] Specialized hooks: `useLikesStream`, `useViewsStream`, `usePresenceStream`, `useFeedStream`
- [x] Like events integration
- [x] View count events integration
- [x] Rating events integration
- [x] Presence events integration
- [x] Feed events integration (posts, courses, events)
- [x] Post comments events (existing)

### 🔄 Future Enhancements

- [ ] Add SSE for lesson progress updates
- [ ] Add SSE for enrollment notifications
- [ ] Add SSE for certificate generation status
- [ ] Add connection status indicator in UI
- [ ] Add reconnection strategy configuration
- [ ] Add event filtering on client-side
- [ ] Add analytics for SSE usage

## Performance Considerations

1. **Connection Limits**: Each SSE connection uses one server connection. Consider connection pooling for high-traffic scenarios.

2. **Redis Channels**: Each client subscribes to specific channels. Too many channels can impact performance.

3. **Heartbeat**: 30-second heartbeat keeps connections alive and helps detect disconnections.

4. **Cache Invalidation**: SSE events trigger SWR cache invalidation, which automatically refetches data. This is efficient compared to polling.

5. **Graceful Degradation**: If SSE fails, fall back to SWR's built-in polling (`refreshInterval`).

## Testing

To test SSE functionality:

1. Open multiple browser tabs/devices
2. Perform an action (like, view, rate, etc.)
3. Verify all tabs receive updates in real-time
4. Check browser console for SSE connection logs
5. Check server logs for Redis pub/sub activity

## Troubleshooting

### SSE Not Connecting

1. Check Redis connection: `curl http://localhost:3025/api/debug/redis`
2. Check SSE endpoint: `curl http://localhost:3025/api/events/stream?channels=test:channel`
3. Check browser console for EventSource errors
4. Verify `REDIS_URL` environment variable is set

### Events Not Received

1. Verify Redis pub/sub is working
2. Check channel names match exactly
3. Verify `publishEvent()` is being called
4. Check server logs for publish errors

### Too Many Connections

1. Implement connection pooling
2. Use fewer SSE subscriptions per page
3. Combine related channels when possible
4. Consider WebSockets for high-frequency updates
