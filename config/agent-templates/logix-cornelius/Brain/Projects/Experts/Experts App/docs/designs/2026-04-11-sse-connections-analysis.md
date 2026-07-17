---
title: "SSE Connections Analysis"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/sse-connections-analysis"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# SSE Connections Analysis

## Current Active SSE Connections

### 1. **Community Page** (`/community`)

- **Hook**: `useFeedEvents`
- **Endpoint**: `/api/events/stream?channels=feed:posts`
- **Connection**: 1 SSE connection
- **Subscribes to**: `feed:posts` channel
- **Purpose**: Real-time updates for posts list (likes, comments, views, updates)
- **Status**: ✅ **ACTIVE** (used in `apps/experts-app/src/app/community/page.tsx`)

### 2. **Post Detail Page** (`/community/[id]`)

- **Hook**: `usePostEvents` (✅ **CONSOLIDATED**)
- **Endpoint**: `/api/events/stream?channels=post:${postId}:events,likes:post:${postId}`
- **Connection**: 1 SSE connection per post
- **Subscribes to**:
  - `post:${postId}:events` channel
  - `likes:post:${postId}` channel
- **Purpose**: Real-time updates for specific post (likes, comments, updates)
- **Status**: ✅ **ACTIVE** (used in `apps/experts-app/src/app/community/[id]/page.tsx`)
- **Note**: ✅ Now uses unified `/api/events/stream` endpoint instead of dedicated `/api/posts/${postId}/events`

## Unused SSE Hooks (Not Currently Used)

### 3. **useLikesStream**

- **Endpoint**: `/api/events/stream?channels=likes:${contentType}:${contentId}`
- **Status**: ❌ **NOT USED** (defined but not imported/used anywhere)
- **Purpose**: Real-time like updates for specific content

### 4. **useViewsStream**

- **Endpoint**: `/api/events/stream?channels=views:${contentType}:${contentId}`
- **Status**: ❌ **NOT USED** (defined but not imported/used anywhere)
- **Purpose**: Real-time view count updates for specific content

### 5. **usePresenceStream**

- **Endpoint**: `/api/events/stream?channels=presence:user:${userId1},presence:user:${userId2},...`
- **Status**: ❌ **NOT USED** (defined but not imported/used anywhere)
- **Purpose**: Real-time presence updates for multiple users

### 6. **useFeedStream**

- **Endpoint**: `/api/events/stream?channels=feed:posts,feed:courses,feed:events`
- **Status**: ❌ **NOT USED** (defined but not imported/used anywhere)
- **Purpose**: Real-time feed updates for multiple feed types

## Connection Count Summary

### Per User Session (Single Tab)

- **Community Page**: 1 connection
- **Post Detail Page**: 1 connection
- **Total**: **1-2 connections** depending on which page is open

### Per User Session (Multiple Tabs)

- **Tab 1 (Community)**: 1 connection
- **Tab 2 (Post Detail)**: 1 connection
- **Tab 3 (Another Post)**: 1 connection
- **Total**: **N connections** (one per tab/page)

### Maximum Theoretical Connections

- If user has 10 tabs open (5 community pages + 5 post detail pages):
  - **5 × 1** (community) + **5 × 1** (post detail) = **10 connections**

## Optimization Opportunities

### 1. ✅ **Consolidate Feed Events** (COMPLETED)

- ✅ `usePostEvents` now uses unified `/api/events/stream` endpoint
- ✅ Post detail page subscribes to multiple channels in a single connection
- ✅ Removed dependency on dedicated `/api/posts/${postId}/events` endpoint

### 2. **Remove Unused Hooks**

- Consider removing `useLikesStream`, `useViewsStream`, `usePresenceStream`, `useFeedStream` if not needed
- Or document them for future use

### 3. **Connection Pooling**

- Consider using a single SSE connection per page that subscribes to multiple channels
- The `/api/events/stream` endpoint already supports multiple channels

### 4. **Smart Connection Management**

- Close connections when page is not visible (Page Visibility API)
- Reconnect when page becomes visible again

## Current Architecture

```
User Browser
├── Tab 1: Community Page
│   └── SSE Connection 1: /api/events/stream?channels=feed:posts
│
├── Tab 2: Post Detail Page (Post A)
│   └── SSE Connection 2: /api/posts/post-a-id/events
│       └── Subscribes to: post:post-a-id:events, likes:post:post-a-id
│
└── Tab 3: Post Detail Page (Post B)
    └── SSE Connection 3: /api/posts/post-b-id/events
        └── Subscribes to: post:post-b-id:events, likes:post:post-b-id
```

## Recommendations

1. **✅ Current Setup is Good**: 1-2 connections per user is reasonable
2. **Consider Consolidation**: Post detail page could use `/api/events/stream` with multiple channels instead of dedicated endpoint
3. **Monitor Connection Count**: Track active SSE connections in production
4. **Implement Connection Limits**: Add server-side limits to prevent abuse
