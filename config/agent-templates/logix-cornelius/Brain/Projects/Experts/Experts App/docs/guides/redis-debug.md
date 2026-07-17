---
title: "Redis Debugging Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v3", "topic/redis-debug"]
category: "docs/experts-guides"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Redis Debugging Guide

This guide explains how to debug Redis connection and operations in the Experts app.

## Quick Check

### 1. Check Redis Connection Status

Visit the debug endpoint:

```bash
curl http://localhost:3025/api/v1/internal/debug/redis
```

Or open in browser:

```
http://localhost:3025/api/v1/internal/debug/redis
```

**Expected Response:**

```json
{
  "connected": true,
  "status": "ready",
  "ping": "PONG",
  "cacheTest": true,
  "pubsubTest": true,
  "host": "redis://localhost:6379",
  "timestamp": "2025-01-XX..."
}
```

### 2. Test Cache Operations

Test posts cache:

```bash
curl -X POST http://localhost:3025/api/v1/internal/debug/redis \
  -H "Content-Type: application/json" \
  -d '{"action": "test-cache", "postId": "test-123"}'
```

Test comments cache:

```bash
curl -X POST http://localhost:3025/api/v1/internal/debug/redis \
  -H "Content-Type: application/json" \
  -d '{"action": "test-comments-cache", "postId": "test-123"}'
```

### 3. Test Pub/Sub (SSE Events)

Test publishing an event:

```bash
curl -X POST http://localhost:3025/api/v1/internal/debug/redis \
  -H "Content-Type: application/json" \
  -d '{"action": "test-pubsub", "postId": "test-123"}'
```

## Server Logs

Check your server console for Redis connection events:

**✅ Good Signs:**

```
✅ Redis connected successfully
🔌 SSE client connected for post: xxx
📡 SSE subscribed to Redis channel: post:xxx:events
📡 Published comment_added event to post:xxx:events (2 subscribers)
📨 SSE received event on post:xxx:events: comment_added
```

**❌ Problem Signs:**

```
❌ Redis connection error (cache will be disabled): ...
⚠️ Redis connection closed
🔄 Redis reconnecting in 1000ms...
```

## Browser Console

Open browser DevTools and check console when viewing a post:

**✅ Good Signs:**

```
SSE connected for post: xxx
```

**❌ Problem Signs:**

```
SSE connection error: ...
```

## Network Tab

1. Open DevTools → Network tab
2. Filter by "events" or "EventStream"
3. Look for `/api/v1/internal/posts/[id]/events`
4. Click on it and check:
   - **Status**: Should be `200` or `200 (pending)`
   - **Type**: Should be `eventsource` or `text/event-stream`
   - **Messages tab**: Should show `connected` event

## Redis CLI (Direct Connection)

If you have Redis CLI installed:

```bash
# Connect to Redis
redis-cli

# Or with connection string
redis-cli -u redis://localhost:6379

# Check connection
PING
# Should return: PONG

# Check if any keys exist
KEYS *

# Check specific cache keys
KEYS post:*
KEYS comments:post:*

# Monitor pub/sub (in one terminal)
PSUBSCRIBE post:*:events

# Publish test event (in another terminal)
PUBLISH post:test-123:events '{"type":"test","postId":"test-123"}'
```

## Common Issues

### Issue: Redis Not Connecting

**Symptoms:**

- `connected: false` in debug endpoint
- Error logs: "Redis connection error"

**Solutions:**

1. Check if Redis is running:

   ```bash
   redis-cli ping
   ```

2. Check `REDIS_URL` environment variable:

   ```bash
   echo $REDIS_URL
   # Should be: redis://localhost:6379 (or your Redis URL)
   ```

3. Check Redis server logs

### Issue: SSE Not Receiving Events

**Symptoms:**

- SSE connects but no events received
- Events published but not received

**Solutions:**

1. Check if events are being published:
   - Look for: `📡 Published comment_added event...` in server logs
   - Check subscriber count in logs

2. Test pub/sub manually:

   ```bash
   curl -X POST http://localhost:3025/api/v1/internal/debug/redis \
     -H "Content-Type: application/json" \
     -d '{"action": "test-pubsub", "postId": "YOUR_POST_ID"}'
   ```

3. Check browser console for SSE errors

### Issue: Cache Not Working

**Symptoms:**

- Cache test returns `false`
- Always fetching from database

**Solutions:**

1. Check Redis connection (see above)
2. Test cache operations via debug endpoint
3. Check Redis keys exist:

   ```bash
   redis-cli
   KEYS post:*
   GET post:YOUR_POST_ID
   ```

## Environment Variables

Make sure these are set:

```env
REDIS_URL=redis://localhost:6379
# Or for production:
REDIS_URL=redis://your-redis-host:6379
```

## Monitoring in Production

For production monitoring, consider:

1. Redis monitoring tools (RedisInsight, etc.)
2. Application performance monitoring (APM)
3. Log aggregation (check for Redis errors)
4. Health check endpoint that includes Redis status
