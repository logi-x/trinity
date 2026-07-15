---
title: "Refund Processing Migration Plan"
date: "2026-04-11"
tags: ["project/howa", "docs/howa"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Refund Processing Migration Plan

## 🎯 Objective

Migrate refund processing from the old system (direct invoice status updates) to the new `invoice_refunds` table system with proper workflow, ZATCA compliance, and comprehensive testing.

---

## 📊 Current State Analysis

### Old System (What We're Migrating From)

**Backend:**

- `PaymentWebhooksController.php` - Directly updates invoice status to 'refunded'
- `CreditNotesController.php` - Creates credit notes and updates invoice status
- `EnrollmentPaymentController.php` - Updates payment status directly
- No separate refund records
- No refund workflow (pending → approved → completed)
- Limited refund tracking

**Frontend:**

- Credit note tabs trigger webhook refunds
- Payment control tabs manage refund UI
- No partial refund support
- No refund status tracking

### New System (What We're Migrating To)

**Database:**

- `invoice_refunds` table with workflow states
- Computed fields on invoices (`has_refunds`, `fully_refunded`, `total_refunded`)
- Proper audit trail

**Backend Services:**

- `RefundService` - Business logic for refunds
- `InvoiceRefundController` - API endpoints
- `InvoiceRefundPolicy` - Authorization
- `InvoiceRefundObserver` - ETF NAV triggers

---

## 🔄 Migration Strategy

### Phase 1: Backend - Webhook Integration ✅ (CRITICAL)

**Files to Update:**

1. **`PaymentWebhooksController.php`**
   - `tabbyWebhook()` method
   - `noonWebhook()` method
   - Create `InvoiceRefund` record instead of direct invoice update
   - Keep ZATCA integration
   - Update credit note creation

2. **`CreditNotesController.php`**
   - `store()` method - Create `InvoiceRefund` when creating credit note
   - `handleCnReported()` - Update `InvoiceRefund` status
   - Link credit notes to refund records

3. **`EnrollmentPaymentController.php`**
   - `updatePaymentStatus()` - Use `RefundService` to create refund

**Changes:**

```php
// OLD WAY (Direct update)
$invoice->update([
    'status' => 'refunded',
    'refunded_amount' => $amount,
    'refunded_at' => now()
]);

// NEW WAY (Create refund record)
$refund = InvoiceRefund::create([
    'invoice_id' => $invoice->id,
    'refund_amount' => $breakdown['refund_amount'],
    'tax_refund' => $breakdown['tax_refund'],
    'net_refund' => $breakdown['net_refund'],
    'refund_reason' => 'Payment gateway refund',
    'refund_type' => $breakdown['is_full_refund'] ? 'full' : 'partial',
    'refunded_by' => auth()->id() ?? 'system',
    'status' => 'completed', // Webhook refunds are auto-completed
    'requested_at' => now(),
    'completed_at' => now(),
    'payment_gateway_ref' => $paymentReference,
]);

// Observer automatically updates invoice status
```

---

### Phase 2: Frontend - Refund UI Enhancement

**Files to Update:**

1. **Enrollment Credit Note Tab** (`apps/admin/resources/js/Pages/courses/course/enrollment/tabs/credit-note-tab.tsx`)
2. **Enrollment Payment Controls** (`apps/admin/resources/js/Pages/courses/course/enrollment/tabs/payment-controls-tab.tsx`)
3. **Service Credit Note Tab** (`apps/admin/resources/js/Pages/services/service/order/tabs/credit-note-tab.tsx`)
4. **Service Payment Controls** (`apps/admin/resources/js/Pages/services/service/order/tabs/payment-controls-tab.tsx`)

**Changes:**

- Update API endpoints to use new refund system
- Add partial refund support
- Display refund status (pending/approved/completed)
- Show refund history
- Add refund reason input

---

### Phase 3: New Refund Workflow API Endpoints

**Create New Endpoints:**

```php
// For manual/admin-initiated refunds
POST   /api/refunds/request         - Request a refund
POST   /api/refunds/{id}/approve    - Approve a refund
POST   /api/refunds/{id}/reject     - Reject a refund
POST   /api/refunds/{id}/complete   - Complete a refund
GET    /api/refunds/pending         - List pending refunds
GET    /api/refunds/{invoice_id}    - Get refund history
```

---

### Phase 4: Testing Strategy

**Unit Tests:**

- `RefundServiceTest` - ✅ Already exists
- `InvoiceRefundModelTest` - Test relationships and computed fields
- `InvoiceRefundObserverTest` - Test observer triggers

**Feature Tests:**

- `WebhookRefundWorkflowTest` - Test Tabby/Noon webhooks
- `ManualRefundWorkflowTest` - Test admin-initiated refunds
- `PartialRefundTest` - Test multiple partial refunds
- `CreditNoteRefundIntegrationTest` - Test credit note creation with refunds

**Integration Tests:**

- Full refund flow: webhook → refund → credit note → ZATCA
- Partial refund flow: multiple refunds on same invoice
- ETF NAV impact test

---

## 📝 Detailed Implementation Plan

### Step 1: Update `PaymentWebhooksController.php`

**Current Flow:**

1. Webhook received (Tabby/Noon)
2. Update invoice status directly to 'refunded'
3. Create credit note
4. Report to ZATCA
5. Send notification

**New Flow:**

1. Webhook received (Tabby/Noon)
2. **Create InvoiceRefund record** with status='completed'
3. **Observer automatically updates invoice status**
4. Create credit note linked to refund
5. Report to ZATCA
6. Send notification

**Code Changes:**

```php
// In processTabbyRefund() and processNoonRefund()
private function processTabbyRefund(Invoice $invoice, Request $request): array
{
    $lastRefund = last($request->refunds);
    $refundAmount = $lastRefund['amount'] ?? 0;

    // Calculate refund breakdown
    $breakdown = app(RefundService::class)->calculateRefundBreakdown(
        $invoice,
        $refundAmount
    );

    // Create refund record (observer will update invoice)
    $refund = InvoiceRefund::create([
        'id' => Str::uuid(),
        'invoice_id' => $invoice->id,
        'refund_amount' => $breakdown['refund_amount'],
        'tax_refund' => $breakdown['tax_refund'],
        'net_refund' => $breakdown['net_refund'],
        'refund_reason' => 'Tabby payment gateway refund',
        'refund_type' => $breakdown['is_full_refund'] ? 'full' : 'partial',
        'refund_percentage' => $breakdown['refund_percentage'],
        'refunded_by' => 'system',
        'status' => 'completed',
        'requested_at' => now(),
        'approved_at' => now(),
        'completed_at' => now(),
        'payment_gateway_ref' => $invoice->payment_reference,
        'refund_notes' => 'Auto-processed via Tabby webhook',
    ]);

    // Rest of the flow (credit note, ZATCA) remains similar
    // ...
}
```

---

### Step 2: Update `CreditNotesController.php`

**store() method:**

```php
public function store(Request $request)
{
    $originalInvoice = Invoice::find($request->original_invoice_id);

    // Create refund record first
    $breakdown = app(RefundService::class)->calculateRefundBreakdown(
        $originalInvoice,
        $originalInvoice->subtotal
    );

    $refund = InvoiceRefund::create([
        'id' => Str::uuid(),
        'invoice_id' => $originalInvoice->id,
        'refund_amount' => $breakdown['refund_amount'],
        'tax_refund' => $breakdown['tax_refund'],
        'net_refund' => $breakdown['net_refund'],
        'refund_reason' => $request->reason ?? 'Manual credit note generation',
        'refund_type' => 'full',
        'refunded_by' => auth()->id(),
        'status' => 'completed',
        'requested_at' => now(),
        'completed_at' => now(),
    ]);

    // Create credit note
    $creditNote = CreditNote::create([
        'id' => $request->id,
        'invoice_id' => $originalInvoice->id,
        'invoice_refund_id' => $refund->id, // Link to refund
        // ... other fields
    ]);

    // Observer handles invoice status update
}
```

---

### Step 3: Create Webhook Refund Tests

**tests/Feature/Webhooks/TabbyRefundWebhookTest.php:**

```php
<?php

namespace Tests\Feature\Webhooks;

use Tests\TestCase;
use App\Models\Invoice\Invoice;
use App\Models\Invoice\InvoiceRefund;
use Illuminate\Foundation\Testing\RefreshDatabase;

class TabbyRefundWebhookTest extends TestCase
{
    use RefreshDatabase;

    #[Test]
    public function it_creates_refund_record_on_tabby_webhook()
    {
        $invoice = Invoice::factory()->paid()->create();

        $response = $this->postJson('/api/webhooks/tabby', [
            'id' => $invoice->payment_reference,
            'amount' => $invoice->paid,
            'refunds' => [
                ['amount' => $invoice->paid]
            ]
        ]);

        $response->assertStatus(200);

        // Assert refund record created
        $this->assertDatabaseHas('invoice_refunds', [
            'invoice_id' => $invoice->id,
            'status' => 'completed',
        ]);

        // Assert invoice updated
        $invoice->refresh();
        $this->assertTrue($invoice->fully_refunded);
        $this->assertEquals('refunded', $invoice->status);
    }

    #[Test]
    public function it_handles_partial_refund_via_webhook()
    {
        $invoice = Invoice::factory()->paid()->create([
            'subtotal' => 1000,
            'tax' => 150,
            'paid' => 1150,
        ]);

        $partialAmount = 500;

        $response = $this->postJson('/api/webhooks/tabby', [
            'id' => $invoice->payment_reference,
            'amount' => $partialAmount,
            'refunds' => [
                ['amount' => $partialAmount]
            ]
        ]);

        $invoice->refresh();
        $this->assertFalse($invoice->fully_refunded);
        $this->assertTrue($invoice->has_refunds);
        $this->assertEquals('paid', $invoice->status);
    }
}
```

---

## 🔍 Key Considerations

### 1. **Backward Compatibility**

- Keep old webhook signatures
- Gradual migration of existing refunded invoices
- Support both systems during transition

### 2. **ZATCA Integration**

- Credit notes must still be reported
- Link credit notes to refund records
- Maintain compliance

### 3. **ETF NAV Impact**

- Observer triggers ETF recalculation
- Only trigger on completed refunds
- Test impact on investor shares

### 4. **Notification System**

- Update email templates to show refund details
- Include refund status and timeline
- Partial refund notifications

### 5. **Payment Gateway Integration**

- Tabby webhook support
- Noon webhook support
- Store gateway transaction IDs

---

## ✅ Success Criteria

1. ✅ All webhooks create `InvoiceRefund` records
2. ✅ Invoice status updates automatically via observer
3. ✅ Credit notes linked to refund records
4. ✅ ZATCA compliance maintained
5. ✅ Partial refunds supported
6. ✅ Full test coverage (>90%)
7. ✅ No breaking changes to existing flows
8. ✅ ETF NAV updates correctly
9. ✅ Frontend displays refund status
10. ✅ Admin can manage refunds

---

## 🚀 Implementation Order

1. **Update `PaymentWebhooksController`** (Tabby & Noon methods)
2. **Update `CreditNotesController`** (store & handleCnReported)
3. **Update `EnrollmentPaymentController`**
4. **Create webhook refund tests**
5. **Test manually with staging webhooks**
6. **Update frontend components**
7. **Create admin refund management UI**
8. **Deploy to production**

---

## 🔗 Related Files

**Backend:**

- `app/Http/Controllers/api/PaymentWebhooksController.php`
- `app/Http/Controllers/CreditNotes/CreditNotesController.php`
- `app/Http/Controllers/Courses/Course/EnrollmentPaymentController.php`
- `app/Services/RefundService.php`
- `app/Observers/InvoiceRefundObserver.php`

**Frontend:**

- `apps/admin/resources/js/Pages/courses/course/enrollment/tabs/credit-note-tab.tsx`
- `apps/admin/resources/js/Pages/courses/course/enrollment/tabs/payment-controls-tab.tsx`
- `apps/admin/resources/js/Pages/services/service/order/tabs/credit-note-tab.tsx`
- `apps/admin/resources/js/Pages/services/service/order/tabs/payment-controls-tab.tsx`

**Tests:**

- `tests/Feature/Webhooks/TabbyRefundWebhookTest.php` (NEW)
- `tests/Feature/Webhooks/NoonRefundWebhookTest.php` (NEW)
- `tests/Feature/Invoice/CreditNoteRefundTest.php` (NEW)
- `tests/Unit/RefundServiceTest.php` (✅ EXISTS)

---

## 📌 Notes

- **CRITICAL**: Test thoroughly in staging before production
- **IMPORTANT**: Coordinate with payment gateway testing
- **REMINDER**: Update API documentation
- **TODO**: Create admin dashboard for refund management
- **TODO**: Add refund analytics and reporting

---

_This is a living document. Update as implementation progresses._
