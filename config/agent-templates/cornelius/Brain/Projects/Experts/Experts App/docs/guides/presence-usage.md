---
title: "User Presence System - Usage Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v4", "topic/presence", "topic/api"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

# User Presence System - Usage Guide

The presence system tracks whether users are online or offline, and when they were last seen. It includes:

- **Automatic heartbeat**: Updates user's online status every 2 minutes
- **Activity detection**: Updates presence on user interactions
- **Auto-offline**: Automatically marks users offline after 5 minutes of inactivity
- **Real-time updates**: Presence status refreshes every 30 seconds

## Links

- [[Projects/Experts/Experts App/docs]]

## Components

### 1. PresenceProvider (Global Setup)

The `PresenceProvider` is already integrated in the root layout. It automatically tracks the current user's presence when they're authenticated.

**Location**: `src/app/providers.tsx`

No additional setup needed - it's already configured!

### 2. PresenceIndicator Component

Display a user's online/offline status with a visual indicator.

**Basic Usage**:

```tsx
import {PresenceIndicator} from "@/components/PresenceIndicator";

// Simple dot indicator
<PresenceIndicator userId={user.id} />

// With custom size and variant
<PresenceIndicator
  userId={user.id}
  size="lg"
  variant="ring"
  showTooltip={true}
/>
```

**Props**:

- `userId`: User ID to show presence for
- `size`: `"sm" | "md" | "lg"` (default: `"md"`)
- `variant`: `"dot" | "ring" | "badge"` (default: `"dot"`)
- `showTooltip`: Show tooltip with last seen time (default: `true`)
- `className`: Additional CSS classes

### 3. AvatarWithPresence Component

Display a user avatar with a presence indicator badge.

**Usage**:

```tsx
import { AvatarWithPresence } from "@/components/PresenceIndicator";
<AvatarWithPresence
  userId={user.id}
  name={user.name}
  avatarUrl={user.avatarUrl}
  size="md"
  showTooltip={true}
/>;
```

**Props**:

- `userId`: User ID to show presence for
- `name`: User's name (for fallback initials)
- `avatarUrl`: User's avatar image URL
- `size`: `"sm" | "md" | "lg"` (default: `"md"`)
- `showTooltip`: Show tooltip with last seen time (default: `true`)
- `className`: Additional CSS classes

### 4. Hooks

#### usePresence()

Manages the current user's presence with automatic heartbeat. Already used in `PresenceProvider`, but you can use it directly if needed.

```tsx
import { usePresence } from "@/hooks/use-presence";

function MyComponent() {
  const { isActive } = usePresence();
  // isActive indicates if presence tracking is active
}
```

#### useUserPresence(userId)

Get a specific user's presence status.

```tsx
import { useUserPresence } from "@/hooks/use-presence";

function UserCard({ userId }: { userId: string }) {
  const { presence, isLoading, error } = useUserPresence(userId);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading presence</div>;

  return (
    <div>
      <p>Status: {presence?.isOnline ? "Online" : "Offline"}</p>
      <p>Last seen: {presence?.lastSeenAt}</p>
    </div>
  );
}
```

#### useBatchPresence(userIds)

Get presence status for multiple users at once (efficient for lists).

```tsx
import { useBatchPresence } from "@/hooks/use-presence";

function UserList({ userIds }: { userIds: string[] }) {
  const { presenceMap, getPresence } = useBatchPresence(userIds);

  return (
    <div>
      {userIds.map((userId) => {
        const presence = getPresence(userId);
        return (
          <div key={userId}>
            User {userId}: {presence?.isOnline ? "Online" : "Offline"}
          </div>
        );
      })}
    </div>
  );
}
```

## Examples

### Example 1: User Profile Page

```tsx
import { AvatarWithPresence } from "@/components/PresenceIndicator";
import { useUserPresence } from "@/hooks/use-presence";

function UserProfile({ user }: { user: User }) {
  const { presence } = useUserPresence(user.id);

  return (
    <div>
      <AvatarWithPresence
        userId={user.id}
        name={user.name}
        avatarUrl={user.avatarUrl}
        size="lg"
      />
      <h1>{user.name}</h1>
      <p>{presence?.isOnline ? "🟢 Online" : "⚫ Offline"}</p>
    </div>
  );
}
```

### Example 2: User List with Presence

```tsx
import { useBatchPresence } from "@/hooks/use-presence";
import { PresenceIndicator } from "@/components/PresenceIndicator";

function UserList({ users }: { users: User[] }) {
  const userIds = users.map((u) => u.id);
  const { getPresence } = useBatchPresence(userIds);

  return (
    <ul>
      {users.map((user) => {
        const presence = getPresence(user.id);
        return (
          <li key={user.id} className="flex items-center gap-2">
            <PresenceIndicator userId={user.id} size="sm" />
            <span>{user.name}</span>
            {presence?.isOnline && (
              <span className="text-green-500">Online</span>
            )}
          </li>
        );
      })}
    </ul>
  );
}
```

### Example 3: Chat/Messaging Interface

```tsx
import { AvatarWithPresence } from "@/components/PresenceIndicator";

function ChatHeader({ recipient }: { recipient: User }) {
  return (
    <div className="flex items-center gap-2">
      <AvatarWithPresence
        userId={recipient.id}
        name={recipient.name}
        avatarUrl={recipient.avatarUrl}
        size="sm"
      />
      <div>
        <h3>{recipient.name}</h3>
        <p className="text-muted-foreground text-sm">
          {presence?.isOnline ? "Online" : "Last seen recently"}
        </p>
      </div>
    </div>
  );
}
```

## API Endpoints

The presence system includes these API endpoints:

### POST `/api/v1/internal/presence/heartbeat`

Updates the current user's presence status. Called automatically by `usePresence()` hook.

**Response**:

```json
{
  "success": true,
  "isOnline": true,
  "lastSeenAt": "2025-12-13T10:30:00.000Z",
  "lastActivityAt": "2025-12-13T10:30:00.000Z"
}
```

### GET `/api/v1/internal/presence/[userId]`

Get a specific user's presence status.

**Response**:

```json
{
  "userId": "uuid",
  "isOnline": true,
  "lastSeenAt": "2025-12-13T10:30:00.000Z",
  "lastActivityAt": "2025-12-13T10:30:00.000Z"
}
```

### GET `/api/v1/internal/presence/batch?userIds=id1,id2,id3`

Get presence status for multiple users.

**Response**:

```json
{
  "presence": [
    {
      "userId": "uuid1",
      "isOnline": true,
      "lastSeenAt": "2025-12-13T10:30:00.000Z",
      "lastActivityAt": "2025-12-13T10:30:00.000Z"
    },
    {
      "userId": "uuid2",
      "isOnline": false,
      "lastSeenAt": "2025-12-13T09:15:00.000Z",
      "lastActivityAt": "2025-12-13T09:15:00.000Z"
    }
  ]
}
```

## Configuration

### Timeouts

- **Heartbeat Interval**: 2 minutes (updates presence every 2 minutes)
- **Presence Timeout**: 5 minutes (user marked offline after 5 minutes of inactivity)
- **Refresh Interval**: 30 seconds (UI refreshes presence status every 30 seconds)

These can be adjusted in:

- `src/hooks/use-presence.ts` - Hook configuration
- `src/app/api/v1/internal/presence/*/route.ts` - API timeout constants

## Database Schema

The presence system uses these fields in the `users` table:

- `is_online`: Boolean indicating if user is currently online
- `last_seen_at`: Timestamp of when user was last seen
- `last_activity_at`: Timestamp of user's last activity

## Best Practices

1. **Use batch queries for lists**: When displaying presence for multiple users, use `useBatchPresence` instead of multiple `useUserPresence` calls.

2. **Handle loading states**: Always check `isLoading` before displaying presence status.

3. **Cache presence data**: The hooks use SWR for automatic caching and revalidation.

4. **Respect privacy**: Only show presence status to users who have permission to see it.

5. **Optimize for performance**: Presence indicators are lightweight, but avoid rendering hundreds at once.

## Troubleshooting

### Presence not updating

- Check that `PresenceProvider` is in the root layout
- Verify user is authenticated
- Check browser console for errors
- Verify API endpoints are accessible

### Users showing as offline when online

- Check the presence timeout (default 5 minutes)
- Verify heartbeat is being sent (check Network tab)
- Check database for `is_online` and `last_seen_at` values

### Performance issues

- Use `useBatchPresence` for multiple users
- Reduce refresh interval if needed
- Check database indexes are created
