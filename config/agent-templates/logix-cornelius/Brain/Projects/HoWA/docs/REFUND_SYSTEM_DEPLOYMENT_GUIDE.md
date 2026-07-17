---
title: "🚀 Refund System Deployment Guide"
date: "2026-04-11"
tags: ["project/howa", "docs/howa"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# 🚀 Refund System Deployment Guide

## 📋 Prerequisites

### **Required Services**

For the refund system to work properly, you need **all three services** running:

1. ✅ **Laravel Backend** (apps/admin)
   - Port: 80/443 (nginx)
   - Handles: Database, business logic, webhooks

2. ✅ **Node.js API Server** (apps/server)
   - Port: 4000 (or configured port)
   - Handles: Payment gateway API calls (Tabby, Noon)
   - **CRITICAL**: Refunds won't work without this!

3. ✅ **Frontend** (apps/admin/resources)
   - Port: 5174 (Vite dev server)
   - Handles: UI, user interactions

---

## 🔧 Starting the Services

### **Development Environment**

```bash
# Terminal 1: Laravel Backend
cd /home/logix/howa/apps/admin
php artisan serve
# OR if using nginx, just ensure it's running

# Terminal 2: Node.js API Server ⚠️ REQUIRED FOR REFUNDS
cd /home/logix/howa/apps/server
npm install
npm start
# Should output: Server running on port 4000

# Terminal 3: Frontend (Vite)
cd /home/logix/howa/apps/admin
npm run dev
```

### **Production Environment**

```bash
# Node.js API Server (use PM2 or similar)
cd /home/logix/howa/apps/server
pm2 start npm --name "howa-api-server" -- start
pm2 save

# Laravel (ensure queue workers are running)
php artisan queue:work --queue=admin_notifications,etf-updates
```

---

## 🔍 Troubleshooting

### **Issue: "Network Error" when processing refund**

**Cause:** Node.js API server not running

**Solution:**

```bash
cd /home/logix/howa/apps/server
npm start
```

**Verify it's running:**

```bash
curl http://localhost:4000/health
# OR
curl http://localhost:3052/health
```

---

### **Issue: "Webhook failed" error**

**Cause:** Laravel backend not receiving webhook calls from Node server

**Check:**

1. Is Laravel backend running?
2. Is the `CORE_DEV_URL` in `/apps/server/.env` correct?
3. Check firewall rules

**Solution:**

```bash
# In apps/server/.env, verify:
CORE_DEV_URL=http://localhost:8001
CORE_STAGING_URL=https://staging-core.howa.edu.sa
CORE_PROD_URL=https://core.howa.edu.sa
```

---

### **Issue: Refund created but ZATCA not reported**

**Cause:** ZATCA API connection issue

**Check:**

```bash
# Test ZATCA endpoint
curl -X POST http://localhost:8001/api/v2/zatca/sign \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

**Solution:**

- ZATCA failures are non-blocking - refund will still be processed
- Credit note will show "Not Reported" status
- Can be manually reported later

---

## 📊 Refund Flow Architecture

```
Frontend (Vite)
    ↓ POST /api/refund-tabby-order
Node.js API Server (apps/server)
    ↓ 1. POST /api/v1/payment/webhook/tabby (internal webhook)
Laravel Backend (apps/admin)
    ├─ Create InvoiceRefund record
    ├─ Observer updates invoice
    └─ Respond to Node server
    ↓ 2. POST to Tabby API (external)
Tabby Payment Gateway
    └─ Process actual refund
    ↓
Laravel Webhook (apps/admin)
    └─ Receive confirmation (if configured)
```

---

## ⚠️ Critical Dependencies

### **Node.js Server Environment Variables**

Required in `/apps/server/.env`:

```env
# App Config
APP_ENV=local|staging|production
PORT=4000

# Laravel Backend URLs
CORE_DEV_URL=http://localhost:8001
CORE_STAGING_URL=https://staging-core.howa.edu.sa
CORE_PROD_URL=https://core.howa.edu.sa

# Tabby
TABBY_PAYMENT_ENDPOINT=https://api.tabby.ai/api/v2/payments
TABBY_SECRET_KEY=your_secret_key

# Noon
NOON_PAYMENT_BUSINESS_ID=your_business_id
NOON_PAYMENT_APP_NAME=your_app_name
NOON_PAYMENT_APP_KEY=your_app_key
NOON_PAYMENT_API=https://api-test.noonpayments.com/payment/v1
NOON_PAYMENT_SECRET=your_secret
```

---

## ✅ Deployment Checklist

### **Before Deploying:**

- [ ] All migrations run: `php artisan migrate`
- [ ] Node.js dependencies installed: `cd apps/server && npm install`
- [ ] Frontend built: `cd apps/admin && npm run build`
- [ ] Environment variables configured in all `.env` files
- [ ] SSL certificates valid for all domains
- [ ] CORS configured properly
- [ ] Queue workers running
- [ ] Node.js server configured with PM2 or systemd

### **After Deploying:**

- [ ] Test Tabby refund flow
- [ ] Test Noon refund flow
- [ ] Test manual credit note creation
- [ ] Verify ZATCA reporting
- [ ] Check refund history displays correctly
- [ ] Verify email notifications sent
- [ ] Check ETF NAV updates correctly
- [ ] Monitor logs for errors

---

## 📝 Testing Refund Flow

### **Test in Development:**

```bash
# 1. Create a test enrollment with Tabby payment
# 2. Go to enrollment confirmation page
# 3. Click "Payment Controls" tab
# 4. Click "Process Refund"
# 5. Select partial/full refund
# 6. Enter reason
# 7. Click "Refund Transaction"
# 8. Verify:
#    - Refund appears in "Refund History"
#    - Invoice status updates
#    - Credit note created
#    - ETF NAV recalculated (if applicable)
```

### **Check Logs:**

```bash
# Laravel logs
tail -f /home/logix/howa/apps/admin/storage/logs/laravel-*.log

# Node.js server logs
# If using PM2:
pm2 logs howa-api-server

# Browser console
# Should show: "✅ Order has been refunded successfully"
```

---

## 🔐 Security Notes

1. **API Authentication**: The Node.js server doesn't require authentication (it's internal)
2. **CORS**: Ensure Node server allows requests from your frontend domain
3. **Webhook Verification**: Tabby/Noon webhooks should verify signatures (if available)
4. **Audit Trail**: All refunds are logged with user ID and timestamps

---

## 📊 Monitoring

### **What to Monitor:**

1. **Refund Processing Time**
   - Should complete within 30 seconds
   - If longer, check Node server performance

2. **Failed Refunds**
   - Check `invoice_refunds` table for `status = 'failed'`
   - Monitor payment gateway API errors

3. **ZATCA Reporting**
   - Check `credit_notes` table for `reported = false`
   - These need manual intervention

4. **ETF NAV Updates**
   - Verify NAV recalculates after refunds
   - Check `etf_nav_history` table

---

## 🆘 Emergency Procedures

### **If Node.js Server Crashes:**

1. Refunds will fail with "Network Error"
2. **Immediate Action:**

   ```bash
   cd /home/logix/howa/apps/server
   pm2 restart howa-api-server
   # OR
   npm start
   ```

3. **Long-term Fix:**
   - Set up auto-restart with PM2
   - Configure monitoring alerts

### **If Refunds Stuck in "Processing":**

1. Check `invoice_refunds` table:

   ```sql
   SELECT * FROM invoice_refunds WHERE status = 'processing';
   ```

2. Manually complete:

   ```php
   $refund = InvoiceRefund::find('refund-id');
   $refund->update(['status' => 'completed', 'completed_at' => now()]);
   ```

3. Observer will auto-update invoice

---

## 📌 Important Notes

1. **Two-Step Refund Process:**
   - Internal webhook creates refund record FIRST
   - Then actual payment gateway refund
   - This ensures data integrity even if gateway fails

2. **Partial Refunds:**
   - Multiple partial refunds are supported
   - Invoice stays "paid" until fully refunded
   - Remaining amount calculated automatically

3. **ZATCA Compliance:**
   - Credit notes auto-generated for all refunds
   - Reporting happens asynchronously
   - Failures are logged but don't block refunds

---

**For questions or issues, check the logs and verify all services are running!**
