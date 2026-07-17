---
title: "PDF Queue Troubleshooting"
date: "2026-04-11"
tags: ["project/experts", "docs/v2", "topic/pdf-queue-troubleshooting"]
category: "docs/experts-reference"
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# PDF Queue Troubleshooting

## Common Issues

### 1. "SASL: SCRAM-SERVER-FIRST-MESSAGE: client password must be a string"

**Problem:** The worker can't connect to PostgreSQL because `DATABASE_URL` is not set or invalid.

**Solution:**

```bash
# Make sure DATABASE_URL is set in your environment
# For test environment:
NODE_ENV=test dotenv -e .env.test -- pnpm worker:pdf

# Or use the test worker script:
pnpm worker:pdf:test
```

**Check:**

```bash
# Verify DATABASE_URL is set
echo $DATABASE_URL

# Or check in your .env.test file
cat .env.test | grep DATABASE_URL
```

### 2. Worker Not Processing Jobs

**Symptoms:**

- Jobs are enqueued but stay in "waiting" state
- Worker shows no activity

**Check:**

1. Is the worker running?

   ```bash
   pnpm worker:pdf
   ```

2. Is Redis connected?

   ```bash
   # Check REDIS_URL is set
   echo $REDIS_URL
   ```

3. Check queue stats:

   ```typescript
   import { pdfQueue } from "@/queue/queues";
   const waiting = await pdfQueue.getWaitingCount();
   const active = await pdfQueue.getActiveCount();
   console.log({ waiting, active });
   ```

### 3. Jobs Failing Immediately

**Check worker logs:**

- Look for error messages in the worker output
- Check if DATABASE_URL and REDIS_URL are set correctly

**Common causes:**

- Missing environment variables
- Database connection issues
- Redis connection issues
- Invalid invoice ID

### 4. Testing Queue in Different Environments

**Development:**

```bash
# Start worker with dev environment
dotenv -e .env -- pnpm worker:pdf
```

**Test:**

```bash
# Start worker with test environment
pnpm worker:pdf:test
```

**Production:**

```bash
# Worker should be started with production environment variables
# Usually managed by process manager (PM2, systemd, etc.)
```

## Debugging Steps

1. **Verify Environment Variables:**

   ```bash
   # Check all required vars
   echo "DATABASE_URL: ${DATABASE_URL:+SET}"
   echo "REDIS_URL: ${REDIS_URL:+SET}"
   ```

2. **Test Queue Connection:**

   ```bash
   pnpm test:pdf:queue [invoice-id]
   ```

3. **Check Worker Logs:**
   - Worker should log "Processing PDF job" when it picks up a job
   - Check for any error messages

4. **Verify Redis Connection:**

   ```bash
   redis-cli -u $REDIS_URL ping
   ```

5. **Check Database Connection:**

   ```bash
   # Test PostgreSQL connection
   psql $DATABASE_URL -c "SELECT 1;"
   ```

## Environment Setup

Make sure your `.env.test` file has:

```env
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://host:port
```

For the worker to work, it needs access to the same environment variables as your test script.
