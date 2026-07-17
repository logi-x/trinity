Two layers: **BullMQ retries** on failure, and **re-enqueue** for stuck docs. Use the paths below in prod.

## 1. Worker must be running

The worker only consumes Redis; it does not poll Postgres by itself.

```bash
docker ps --filter name=experts-prd-zatca-worker
docker logs -f experts-prd-zatca-worker --tail 50
```

After a job is enqueued you should see `active` / processor logs.

## 2. Automatic BullMQ retries (on failure)

When `executeZatca` throws, BullMQ retries the **same** job:

- **12 attempts**
- **Exponential backoff**, base **30s** (`zatca.jobs.ts`)

No extra step if the job is still in the queue and retrying.

## 3. Reconciliation sweep (recommended for your stuck invoices)

Every **10 minutes** production cron calls:

`POST /api/v1/internal/zatca/reconciliation`  
(with `Authorization: Bearer <CRON_SECRET>`)

It selects docs with `reportedAt` null, `updatedAt` older than **5 minutes**, and `nextRetryAt` null or due, then calls **`enqueueZatcaDocument`** (full context + `EXECUTE_ZATCA`, job id `zatca_<documentId>`).

**Trigger now** (from the cron container or anywhere that can reach the app with the secret):

```bash
# From production compose dir, if cron has curl + auth config:
docker exec experts-prd-cron curl -fsS -X POST \
  --config /run/curl-auth.conf \
  "http://experts-prd-app:3025/api/v1/internal/zatca/reconciliation"

# Or from host (replace URL + secret):
curl -fsS -X POST \
  -H "Authorization: Bearer $(cat ~/experts/docker/production/secrets/cron_secret.txt)" \
  "https://app.experts.com.sa/api/v1/internal/zatca/reconciliation"
```

Response shape: `{ ok, reenqueued, failed, scanned }`.

Your two stuck docs (`3f6bbfe5-…`, `fc78e6df-…`) match this sweep once certs/config are good and **`getZatcaContext`** succeeds (app must use **`APP_ENV=production`** / **`ZATCA_DEFAULT_ENV=production`** and an active **production** `SellerZatcaProfile`).

## 4. Admin retry API — do not use as-is

`POST /api/v1/admin/zatca/retry` (admin session) enqueues **`{ kind: "ZATCA_DOCUMENT" }`** and job id **`zatca:<uuid>`**, but the worker only accepts **`EXECUTE_ZATCA`** with a context snapshot and stable id **`zatca_<uuid>`**. That route is out of date relative to the current worker.

**Use reconciliation** (or a one-off that calls `enqueueZatcaDocument`) until retry is fixed to match `zatca-queue.service.ts`.

## 5. If re-enqueue does nothing

| Symptom | What to check |
|--------|----------------|
| `reenqueued: 0`, `scanned: 0` | Doc `updatedAt` within last 5 minutes → wait or touch `updatedAt` / wait for stale window |
| `failed` > 0 | App logs / `system_events` for `zatca.document.enqueue.error` or `zatca.reconcile.row_failed` (e.g. wrong ZATCA env / missing profile) |
| Job not picked up | Redis URL same for app and worker; worker logs |
| “Job already exists” | Old BullMQ job with same `jobId` in completed/failed set — remove failed job for `zatca_<id>` in Redis/BullMQ or wait until evicted |

## 6. Verify end-to-end

1. Run reconciliation once → `reenqueued >= 1`.
2. Tail ZATCA worker logs during the run.
3. DB: `billing.zatca_documents` → `status` → `reported`, `reported_at` set.

```sql
SELECT id, status, last_error, attempts, signed_at, reported_at, updated_at
FROM billing.zatca_documents
WHERE id IN (
  '3f6bbfe5-c97e-4089-b45e-383b539b8502',
  'fc78e6df-e017-4a4f-957b-a9a60fe73ef0'
);
```

I can patch `admin/zatca/retry` to call `enqueueZatcaDocument` and align job ids with the worker if you want a manual admin button without waiting for cron.