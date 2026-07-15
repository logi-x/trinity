---
title: "Polling Migration Fixes - Complete Summary"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/polling-migration-fixes-summary"]
category: "docs/experts-designs"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Polling Migration Fixes - Complete Summary

**Date**: December 22, 2025
**Status**: ✅ All Issues Resolved

## Overview

Successfully migrated from Server-Sent Events (SSE) to polling-based real-time sync system. Fixed multiple critical issues related to polling not working and UI glitches during like/unlike actions.

---

## Issue 1: Broken ETag Caching (Polling Stuck at 304)

### Problem

- Polling endpoint **always returned "304 Not Modified"** without querying the database
- Likes and comments were not syncing across tabs
- Server console showed constant 304 responses even when new likes were added

### Root Cause

The ETag was set to the cursor value:

```typescript
const etag = `"${cursor || "initial"}"`;
const ifNoneMatch = req.headers.get("If-None-Match");
if (ifNoneMatch === etag && cursor) {
  return new NextResponse(null, { status: 304 }); // ❌ Returns 304 without checking DB!
}
```

This meant every request with the same cursor would return 304 **without querying the database** for new events.

### Fix

**File**: `app/api/realtime/sync/route.ts` (lines 29-33)

Removed ETag logic entirely:

```typescript
// ✅ FIX: Remove broken ETag logic
// The ETag was set to the cursor value, which meant every request with the same cursor
// would return 304 without checking for new events. This prevented likes from syncing.
// ETag should only be used if we actually know there are no new events (after querying).
// For now, we'll remove it and always query. In production, use Redis Streams for better caching.
```

Added proper cache control headers:

```typescript
headers: {
  "Cache-Control": "no-cache, no-store, must-revalidate",
}
```

---

## Issue 2: Infinite Re-render Loop

### Problem

- Console logs showed **hundreds of "[usePostEvents] Subscribing:" messages per second**
- Caused excessive CPU usage and performance degradation
- Polling transport was constantly recreating subscriptions

### Root Cause

The `channels` array and `eventHandlers` object were recreated on every render:

```typescript
// ❌ BEFORE (causes infinite re-renders):
export function usePostEvents(postId: string | null, options?: {enabled?: boolean}) {
  const channels = postId && enabled
    ? [`post:${postId}:events`, `likes:post:${postId}`] // ← New array every render!
    : null;

  const {isConnected} = useRealtime(channels, {
    eventHandlers: { // ← New object every render!
      like_added: (event) => { ... },
    },
  });
}
```

This caused `useRealtime` to detect "new" channels/handlers on every render, triggering constant resubscriptions.

### Fix

**File**: `src/hooks/use-post-events.ts` (lines 42-92)

Wrapped both `channels` and `eventHandlers` in `useMemo`:

```typescript
// ✅ AFTER (fixed - memoized to prevent re-renders):
export function usePostEvents(
  postId: string | null,
  options?: { enabled?: boolean },
) {
  const enabled = options?.enabled !== false;

  // ✅ FIX: Memoize channels array to prevent infinite re-renders
  const channels = useMemo(
    () =>
      postId && enabled
        ? [`post:${postId}:events`, `likes:post:${postId}`]
        : null,
    [postId, enabled],
  );

  // ✅ FIX: Memoize event handlers to prevent infinite re-renders
  const eventHandlers = useMemo(
    () => ({
      like_added: (event: RealtimeEvent) => {
        // SWR's dedupingInterval (default 2000ms) prevents excessive revalidations
        if (postId) {
          mutate(`/api/posts/${postId}`);
        }
      },
      like_removed: (event: RealtimeEvent) => {
        if (postId) {
          mutate(`/api/posts/${postId}`);
        }
      },
      // ... other handlers
    }),
    [postId],
  );

  const { isConnected } = useRealtime(channels, {
    enabled,
    eventHandlers,
  });
}
```

---

## Issue 3: Future Cursor Bug (Cursor Jumped to Jan 2026)

### Problem

- Server logs showed cursor date of **"2026-01-20T04:36:45.530Z"** (1.5 months in the future)
- All activity records showed `isAfterCursor: false` despite being recent
- Polling couldn't detect any events because cursor was ahead of current time
- User message: _"same thingg"_ with server console logs showing future cursor

### Root Cause

Some database record had a `createdAt` timestamp in the future, which advanced the cursor ahead:

```typescript
// ❌ BEFORE:
const nextCursor =
  events.length > 0 ? Math.max(...events.map((e) => e.ts)).toString() : cursor;
```

If any event had a future timestamp (due to clock skew or bad data), the cursor would jump to that future time permanently.

### Diagnosis

Server logs revealed:

```
cursorTimestamp: 1768883805530  // Jan 20, 2026
now: 1766363829103              // Dec 22, 2025
cursorDate: '2026-01-20T04:36:45.530Z'
```

### Fix

**File**: `app/api/realtime/sync/route.ts` (lines 68-76)

Added cursor sanitization to detect and reset future cursors:

```typescript
// ✅ FIX: Protect against future timestamps
// If cursor is in the future (bad data), reset to current time
const now = Date.now();
const sanitizedCursorTimestamp = cursorTimestamp > now ? now : cursorTimestamp;
const cursorDate = new Date(sanitizedCursorTimestamp);

if (
  sanitizedCursorTimestamp !== cursorTimestamp &&
  process.env.NODE_ENV === "development"
) {
  console.warn(
    `[Sync] Cursor was in the future! Resetting from ${new Date(cursorTimestamp).toISOString()} to ${cursorDate.toISOString()}`,
  );
}
```

**User confirmation**: _"Yes, now it works... finally."_

---

## Issue 4: Cursor Not Advancing Correctly

### Problem

- First like synced successfully, but subsequent likes didn't sync
- User message: _"We are almost there, it worked once, but subsecuent likes added/remomved didn't work..."_
- Cursor jumped to `Date.now()` when no events, permanently skipping events created during that gap

### Root Cause

```typescript
// ❌ BEFORE (broken):
const nextCursor =
  events.length > 0
    ? Math.max(...events.map((e) => e.ts)).toString()
    : Date.now().toString(); // ← Jumped ahead even with no events!
```

This caused the cursor to skip forward to the current time even when there were no events, missing any events that occurred between the old cursor and now.

### Fix

**File**: `app/api/realtime/sync/route.ts` (lines 396-398)

Only advance cursor when events actually exist:

```typescript
// ✅ FIX: Make cursor "exclusive" by adding 1ms to prevent missing events
const nextCursor =
  events.length > 0
    ? (Math.max(...events.map((e) => e.ts)) + 1).toString()
    : cursor; // Keep same cursor if no new events
```

---

## Issue 5: Events at Exact Cursor Timestamp Missed

### Problem

- Some events created at the exact millisecond as the cursor were missed
- Query used `gt` (greater than) instead of `gte` (greater than or equal)

### Root Cause

```typescript
// ❌ BEFORE:
where: {
  createdAt: {
    gt: cursorDate; // ← Misses events at exactly cursorDate!
  }
}
```

If an event was created at exactly `T` and cursor was `T`, the query would miss it.

### Fix

**File**: `app/api/realtime/sync/route.ts` (lines 117, 175, 269)

Changed all queries from `gt` to `gte` and made cursor exclusive by adding +1ms:

```typescript
// ✅ AFTER:
where: {
  createdAt: {
    gte: cursorDate; // ✅ Use gte since cursor is now exclusive (T+1)
  }
}

// Cursor advancement with +1ms for exclusivity:
const nextCursor =
  events.length > 0
    ? (Math.max(...events.map((e) => e.ts)) + 1).toString()
    : cursor;
```

This ensures:

1. Cursor represents the **exclusive** boundary (events after T, not at T)
2. Queries use `gte` to include events at exactly the cursor time
3. Cursor advances by +1ms to prevent re-fetching same events

---

## Issue 6: Transport Recreation Race Condition

### Problem

- When channels updated, the polling transport was completely recreated
- Caused race conditions where old transport still polled with stale channels
- Led to inconsistent polling behavior

### Root Cause

```typescript
// ❌ BEFORE (broken):
private updateTransportChannels() {
  const oldTransport = this.transport;
  const wasRunning = oldTransport.isConnected();
  oldTransport.stop();

  this.transport = new PollingTransport(...); // ← New instance causes race
  this.transport.onEvent((ev) => { ... });

  if (wasRunning && this.coordinator.isLeader()) {
    this.transport.start();
  }
}
```

### Fix

**File**: `src/lib/realtime/global-coordinator.ts` (lines 156-183)

Made channels dynamically updateable without recreating transport:

```typescript
// ✅ AFTER (fixed - updates in-place):
private updateTransportChannels() {
  if (!this.transport || !this.coordinator) return;

  const allChannelsArray = Array.from(this.allChannels);

  // ✅ FIX: Update channels dynamically instead of recreating transport
  // This prevents race condition where old transport still polling with stale channels
  this.transport.setChannels(allChannelsArray);

  // ✅ FIX: If transport is not running but we're leader, start it
  if (this.coordinator.isLeader() && !this.transport.isConnected()) {
    this.transport.start();
  }
}
```

**File**: `src/lib/realtime/polling-transport.ts` (lines 29, 47-59)

Added methods to update channels dynamically:

```typescript
private channels: string[] = []; // ← Now mutable

constructor(
  private readonly url: string,
  private readonly getIntervalMs: () => number,
  initialChannels?: string[],
) {
  this.channels = initialChannels || [];
}

setChannels(channels: string[]): void {
  this.channels = channels;
}

getChannels(): string[] {
  return [...this.channels];
}

resetCursor(newCursor?: string | null): void {
  this.cursor = newCursor || null;
}
```

---

## Issue 7: Glitchy Like Button (UI Flash)

### Problem

- When liking a comment, the like count **flashed**: "1 like" → "" → "1 like"
- User message: _"When liking a comment, it sort of flashes the text '1 like' -> '' -> '1 like' in milliseconds, which make it feel glitchy"_
- Made the UI feel unresponsive and broken
- User provided video showing the glitchy behavior
- User message after multiple attempts: _"stilll glitchy"_

### Root Cause

**ANY cache mutation** (even with `{revalidate: false}`) caused React re-renders that temporarily reverted props to stale values, interrupting the optimistic state:

```typescript
// ❌ BEFORE (caused flash):
onLikeSuccess={async (result) => {
  await mutatePost(
    (currentPost) => {
      if (!currentPost) return currentPost;
      return {
        ...currentPost,
        comments: currentPost.comments?.map((c) =>
          c.id === comment.id
            ? {
                ...c,
                likesCount: result.stats.totalLikes, // ← Updating cache
                isLiked: result.liked,
                userReaction: result.reactionType,
              }
            : c
        ),
      };
    },
    {revalidate: false} // ← Still causes re-render!
  );
}}
```

Timeline of the flash:

1. User clicks like button
2. Optimistic state shows "1 like" immediately
3. API call completes
4. `mutatePost` updates cache → triggers parent re-render
5. During re-render, props briefly revert to old values
6. Component shows "" or "0" for a frame
7. Props catch up, shows "1 like" again
8. Result: visible flash

### Attempted Fixes (All Failed)

1. ❌ Removed `{revalidate: true}` - User: _"still flashes..."_
2. ❌ Optimistically updated post cache with calculated delta - User: _"There miight be something else we,re doinng wrong"_
3. ❌ Updated post cache with actual API result - User: _"stilll glitchy"_
4. ❌ Added 300ms debounced clearing of optimistic state - User: _"still having the same glitchy issue"_

### Final Fix (✅ WORKS)

**File**: `app/community/[id]/page.tsx` (lines 606-611)

**Removed ALL cache updates** from the `onLikeSuccess` callback:

```typescript
// ✅ FIX: Don't update post cache at all - causes re-render flash
onLikeSuccess={async (result) => {
  // Just let polling sync the changes within 5-10 seconds
  // The optimistic UI in LikeButton handles immediate feedback
  // This prevents ANY cache-related re-renders that could cause flash
}}
```

**File**: `src/components/likes/LikeButton.tsx` (lines 95-135)

Simplified optimistic state clearing with debouncing:

```typescript
// ✅ FIX: Clear optimistic state ONLY when props match AND are stable
// Use a debounced approach to prevent clearing during temporary prop reverts
useEffect(() => {
  if (optimisticCount === null && optimisticReaction === null) {
    return;
  }

  const usingAggregatedData =
    initialLikesCount !== undefined || initialIsLiked !== undefined;
  if (!usingAggregatedData) {
    return;
  }

  // Debounce clearing - wait for props to be stable
  const timeoutId = setTimeout(() => {
    let shouldClearCount = false;
    let shouldClearReaction = false;

    if (optimisticCount !== null && initialLikesCount !== undefined) {
      shouldClearCount = initialLikesCount >= optimisticCount;
    }

    if (optimisticReaction !== null && initialIsLiked !== undefined) {
      const optimisticIsLiked = optimisticReaction === "like";
      shouldClearReaction = initialIsLiked === optimisticIsLiked;
    }

    if (shouldClearCount) {
      setOptimisticCount(null);
    }
    if (shouldClearReaction) {
      setOptimisticReaction(null);
    }
  }, 300); // Debounce: wait 300ms for props to stabilize

  return () => clearTimeout(timeoutId);
}, [initialLikesCount, initialIsLiked, optimisticCount, optimisticReaction]);
```

### Why This Works

1. **No parent re-renders** - Not updating post cache means no parent component re-renders
2. **Optimistic UI preserved** - LikeButton's internal optimistic state is never interrupted
3. **Eventual consistency** - Polling syncs changes within 5-10 seconds
4. **Smooth UX** - User sees instant feedback (optimistic) → no flash → eventual sync

**User confirmation**: _"YES, fixed..."_

---

## Architecture Overview

### Polling Flow

```
1. GlobalCoordinator.subscribe(channels, onEvent)
   ↓
2. Leader election via BroadcastChannel
   ↓
3. Only leader starts PollingTransport
   ↓
4. PollingTransport polls /api/realtime/sync every 5-10s
   ↓
5. Server queries Activity table for events since cursor
   ↓
6. Events broadcasted to all tabs via BroadcastChannel
   ↓
7. Each tab's useRealtime hook receives events
   ↓
8. Event handlers trigger SWR mutations
   ↓
9. UI updates via SWR cache
```

### Like Button Flow (Optimistic UI)

```
1. User clicks like button
   ↓
2. LikeButton sets optimistic state (count++, reaction="like")
   ↓
3. UI immediately shows "1 like" (optimistic)
   ↓
4. API call to /api/likes/{contentType}/{contentId}
   ↓
5. Server creates Activity record (like_added)
   ↓
6. API returns {liked: true, stats: {totalLikes: 1}}
   ↓
7. LikeButton updates local cache with result
   ↓
8. onLikeSuccess callback does NOTHING (no parent cache update)
   ↓
9. Polling detects Activity record within 5-10s
   ↓
10. usePostEvents triggers SWR mutation
   ↓
11. Post cache updates with new like count
   ↓
12. LikeButton's debounced useEffect clears optimistic state
   ↓
13. Props take over, showing "1 like" (from cache)
```

---

## Files Modified

### Server-Side (Polling Endpoint)

- ✅ `app/api/realtime/sync/route.ts`
  - Removed broken ETag logic
  - Added cursor sanitization for future timestamps
  - Fixed cursor advancement (only when events exist)
  - Changed queries from `gt` to `gte`
  - Added extensive debug logging

### Client-Side (Polling Transport)

- ✅ `src/lib/realtime/polling-transport.ts`
  - Made channels dynamically updateable
  - Added `setChannels()`, `getChannels()`, `resetCursor()` methods

- ✅ `src/lib/realtime/global-coordinator.ts`
  - Update channels in-place instead of recreating transport
  - Fixed leader check on transport start

### React Hooks

- ✅ `src/hooks/use-post-events.ts`
  - Memoized `channels` array
  - Memoized `eventHandlers` object
  - Fixed infinite re-render loop

### UI Components

- ✅ `src/components/likes/LikeButton.tsx`
  - Simplified optimistic state clearing logic
  - Added debounced useEffect (300ms delay)
  - Modified `onLikeSuccess` callback signature to pass API result

- ✅ `app/community/[id]/page.tsx`
  - Removed ALL cache updates from `onLikeSuccess` callback
  - Let polling handle eventual consistency

---

## Testing Checklist

### Polling Functionality

- ✅ Polling starts when first hook subscribes
- ✅ Polling uses aggregated channels from all hooks
- ✅ Leader election works correctly (only one tab polls)
- ✅ Followers receive events via BroadcastChannel
- ✅ Cursor advances correctly when events exist
- ✅ Cursor stays same when no events
- ✅ Future cursors are sanitized to current time
- ✅ Queries use `gte` with exclusive cursor (+1ms)
- ✅ No infinite re-render loops
- ✅ No 304 responses (always queries database)

### Like Button Functionality

- ✅ Clicking like shows "1 like" immediately (optimistic)
- ✅ NO flashing or glitching
- ✅ Unliking returns to "" or "0" smoothly
- ✅ Changes sync to other tabs within 5-10 seconds via polling
- ✅ Multiple rapid clicks handled correctly
- ✅ Reaction picker works flawlessly (no flash)

---

## Performance Characteristics

### Polling Intervals

- **Post/Comment channels**: 5 seconds
- **Other channels**: 10 seconds
- **Leadership heartbeat**: 5 seconds

### Optimistic UI

- **Immediate feedback**: 0ms (instant)
- **API response**: ~100-500ms (typical)
- **Polling sync**: 5-10 seconds (eventual consistency)
- **Debounced clearing**: 300ms delay

### Resource Usage

- **Network**: 1 request per 5-10 seconds (per leader tab)
- **Memory**: Minimal (shared BroadcastChannel)
- **CPU**: Low (no infinite loops, memoized hooks)

---

## Key Insights

1. **ETag Caching**: HTTP caching mechanisms like ETag must be carefully implemented with polling to avoid returning 304 without database queries

2. **React Memoization**: In hooks that create arrays/objects, ALWAYS use `useMemo` to prevent infinite re-renders

3. **Cursor Management**:
   - Use exclusive cursors (T+1) with `gte` queries to prevent missing events
   - Sanitize cursors to prevent future timestamps
   - Only advance cursor when events exist

4. **Optimistic UI**:
   - Parent cache updates during optimistic state cause re-render flashes
   - Best approach: Let child component handle optimistic state entirely
   - Rely on polling for eventual consistency (5-10s is acceptable UX)

5. **Debugging**: Extensive logging during development is crucial for diagnosing polling issues (cursor values, timestamps, event counts)

---

## Future Improvements

### Short-term

- Monitor for any database records with future `createdAt` timestamps
- Consider adding cursor validation on write (prevent future timestamps)
- Add metrics/monitoring for polling performance

### Long-term

- Migrate to Redis Streams for better performance and scalability
- Implement proper ETag/caching once Redis Streams in place
- Consider WebSocket fallback for users who need <1s latency
- Add circuit breaker for failed polling requests

---

## Conclusion

All polling migration issues have been successfully resolved:

- ✅ Polling works reliably across multiple tabs
- ✅ Likes and comments sync within 5-10 seconds
- ✅ No infinite re-render loops
- ✅ No UI glitching or flashing
- ✅ Optimistic UI feels instant and smooth
- ✅ Future cursor bugs prevented
- ✅ Cursor advancement works correctly

The system now provides a solid foundation for real-time updates via polling, with excellent UX through optimistic updates and eventual consistency.
