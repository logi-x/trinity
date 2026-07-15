---
title: "Transaction Seeder Guide"
date: "2026-04-11"
tags: ["project/howa", "docs/howa"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Transaction Seeder Guide

## 📦 What Was Created

### 3 New Seeders for Enrollments & Orders

1. **EnrollmentInvoiceSeeder** - Simple enrollment seeder
2. **OrderInvoiceSeeder** - Simple order seeder
3. **TransactionSeeder** ⭐ RECOMMENDED - Complete solution with stats

---

## 🚀 Quick Start

### Option 1: Use TransactionSeeder (Recommended)

Creates both enrollments and orders with full statistics:

```bash
php artisan db:seed --class=TransactionSeeder
```

**Output:**

```
🔄 Creating transactions (enrollments & orders) with invoices...

📊 Transaction Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Course Enrollments:
  Total: 150
  - Paid: 128
  - Refunded: 22
  - Taxable: 105
  - Non-taxable: 45
  - With Coupon: 30

🔧 Service Orders:
  Total: 60
  - Paid: 48
  - Refunded: 12
  - Taxable: 42
  - Non-taxable: 18
  - With Coupon: 9
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Total transactions created: 210
```

### Option 2: Seed Separately

```bash
# Just enrollments
php artisan db:seed --class=EnrollmentInvoiceSeeder

# Just orders
php artisan db:seed --class=OrderInvoiceSeeder
```

---

## 🎯 What Gets Created

### For Each Enrollment

✅ Enrollment record (user → course → timing)  
✅ Invoice record with proper tax calculation  
✅ Invoice item record  
✅ Payment method (Noon/Tabby/Cash)  
✅ Card type (VISA/MASTERCARD/MADA/AMEX)  
✅ Status (85-90% paid, 10-15% refunded)

### For Each Order

✅ Order record (user → service)  
✅ Invoice record with tax  
✅ Invoice item record  
✅ Payment references  
✅ Proper tax handling  
✅ Coupon support (15-20% have coupons)

---

## 📊 Distribution Stats

### Enrollment Distribution

- **50 users** × **1-4 courses each** = ~150 enrollments
- **85% Paid** | 15% Refunded
- **70% Taxable** | 30% Non-taxable
- **20% with Coupons**

### Order Distribution

- **30 users** × **1-3 services each** = ~60 orders
- **80% Paid** | 20% Refunded
- **70% Taxable** | 30% Non-taxable
- **15% with Coupons**

### Payment Methods

- **55% Noon** (full payment)
- **30% Tabby** (installments)
- **15% Cash**

### Card Types

- **40% VISA**
- **30% MASTERCARD**
- **25% MADA**
- **5% AMEX**

---

## 💡 Usage Examples

### Full Database Setup

```bash
# Complete setup from scratch
php artisan migrate:fresh
php artisan db:seed --class=UserSeeder
php artisan db:seed --class=CourseSeeder
php artisan db:seed --class=ServiceSeeder
php artisan db:seed --class=TransactionSeeder
```

### Quick Test Data

```bash
# Just add transactions to existing data
php artisan db:seed --class=TransactionSeeder
```

### Verify Data

```bash
php artisan tinker
>>> Enrolment::count()  # Should show ~150
>>> Order::count()      # Should show ~60
>>> Invoice::where('status', 'paid')->count()
>>> Invoice::where('taxable', true)->sum('tax')
```

---

## 🔍 Data Features

### Realistic Invoices

- Sequential invoice numbers starting from last invoice
- Unique payment references (PAY-xxxxx)
- Proper tax calculation (15% for taxable items)
- Coupon discounts applied before tax
- Random dates within last year
- Payment method tracking

### Tax Handling

```php
// Taxable item
Subtotal: SAR 1,000
Tax (15%): SAR 150
Total: SAR 1,150

// Non-taxable item
Subtotal: SAR 1,000
Tax (0%): SAR 0
Total: SAR 1,000

// With coupon (10% off)
Original: SAR 1,000
Discount: SAR 100
Subtotal: SAR 900
Tax (15%): SAR 135
Total: SAR 1,035
```

### Invoice Items

Each invoice gets proper line items:

- Course/Service title
- Description (limited to 250 chars)
- Quantity (always 1)
- Original price
- Discounted price

---

## 🎨 Customization

### Change Quantities

```php
// In TransactionSeeder.php

// More enrollments per user
$numEnrollments = rand(1, 10); // Instead of rand(1, 4)

// More orders per user
$numOrders = rand(1, 5); // Instead of rand(1, 3)
```

### Adjust Paid/Refunded Ratio

```php
// More refunds
$status = rand(1, 100) <= 70 ? 'paid' : 'refunded'; // 70% paid instead of 85%
```

### Change Coupon Usage

```php
// More coupons
$coupon = (rand(1, 100) <= 50 && $coupons->isNotEmpty()) ? $coupons->random() : null; // 50% instead of 20%
```

### Modify Payment Method Distribution

```php
private function randomPaymentMethod(): string
{
    $rand = rand(1, 100);

    if ($rand <= 70) return 'noon';  // 70% Noon
    if ($rand <= 90) return 'tabby'; // 20% Tabby
    return 'cash';                   // 10% Cash
}
```

---

## 🔧 Troubleshooting

### Issue: "No users found"

```bash
# Solution: Run UserSeeder first
php artisan db:seed --class=UserSeeder
```

### Issue: "No courses found"

```bash
# Solution: Run CourseSeeder first
php artisan db:seed --class=CourseSeeder
```

### Issue: "No services found"

```bash
# Solution: Run ServiceSeeder first
php artisan db:seed --class=ServiceSeeder
```

### Issue: Duplicate invoice numbers

```bash
# Solution: Truncate invoices table first
php artisan tinker
>>> Invoice::truncate();
```

### Recommended Seeding Order

```bash
1. php artisan db:seed --class=UserSeeder
2. php artisan db:seed --class=CourseSeeder
3. php artisan db:seed --class=ServiceSeeder
4. php artisan db:seed --class=TransactionSeeder
```

---

## 📈 Statistics & Analytics

After seeding, your dashboard will show:

- Revenue trends (daily/weekly/monthly)
- Tax collection totals
- Course vs Service revenue
- Payment method breakdown
- Refund statistics
- User engagement metrics

### Check Results

```bash
php artisan tinker

# Enrollment stats
>>> Enrolment::where('status', 'paid')->count()
>>> Invoice::where('invoice_type', 'course')->sum('total')
>>> Invoice::where('invoice_type', 'course')->where('taxable', true)->sum('tax')

# Order stats
>>> Order::where('status', 'paid')->count()
>>> Invoice::where('invoice_type', 'service')->sum('total')
>>> Invoice::where('invoice_type', 'service')->where('taxable', true)->sum('tax')

# Payment methods
>>> Invoice::select('payment_method', DB::raw('count(*) as count'))->groupBy('payment_method')->get()
```

---

## 🎯 Use Cases

### 1. Development Dashboard Testing

Populate dashboard with realistic revenue data.

### 2. Analytics Testing

Test charts, graphs, and statistical calculations.

### 3. Tax Reporting

Verify tax calculation logic with real data.

### 4. Demo Presentations

Show clients realistic transaction history.

### 5. Load Testing

Generate thousands of transactions for performance testing.

### 6. Export Testing

Test invoice PDF generation and exports.

---

## 📝 Database Schema

### Enrollments Table

- Links: User → Course → Timing → Fee
- Status: paid/refunded
- Payment method tracking

### Orders Table

- Links: User → Service → Type → Category → Fee
- Status: paid/refunded
- Payment reference tracking

### Invoices Table

- Links to Enrollment OR Order
- Tax calculation fields
- Payment details
- Coupon tracking

### Invoice Items Table

- Line items for each invoice
- Quantity and pricing
- Links to course or service

---

**Created:** October 19, 2025  
**Purpose:** Generate realistic transaction data  
**Seeders:** 3 (EnrollmentInvoiceSeeder, OrderInvoiceSeeder, TransactionSeeder)  
**Status:** ✅ Ready to use
