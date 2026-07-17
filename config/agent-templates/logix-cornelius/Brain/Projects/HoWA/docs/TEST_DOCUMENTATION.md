---
title: "Payment Testing Documentation"
date: "2026-04-11"
tags: ["project/howa", "docs/howa"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Payment Testing Documentation

## Overview

This document describes the comprehensive test suite for taxable/non-taxable payment scenarios, course enrollments, service orders, and manual invoice generation with payment links.

## Test Structure

### 1. Enrollment Payment Tests

#### `Enrollment/Payment/EnrollmentPaymentTest.php`

Original test file for basic enrollment payment scenarios.

**Coverage:**

- Noon payment processing
- Tabby payment processing
- Failed payment handling

#### `Enrollment/Payment/TaxableEnrollmentPaymentTest.php` ✨ NEW

Comprehensive tests for taxable and non-taxable course enrollments.

**Test Cases:**

1. `test_can_process_taxable_course_enrollment_with_noon_payment`
   - Verifies taxable course enrollment via Noon payment
   - Validates 15% tax calculation
   - Confirms invoice tax fields are correct

2. `test_can_process_non_taxable_course_enrollment_with_noon_payment`
   - Verifies non-taxable course enrollment via Noon payment
   - Confirms zero tax amount
   - Validates tax_rate is 0

3. `test_can_process_taxable_course_enrollment_with_tabby_payment`
   - Verifies taxable course enrollment via Tabby installments
   - Validates tax calculation with installment payment
   - Confirms payment_type is 'installment'

4. `test_can_process_non_taxable_course_enrollment_with_tabby_payment`
   - Verifies non-taxable course enrollment via Tabby
   - Confirms zero tax for installment payments

5. `test_tax_calculation_is_correct_for_taxable_course`
   - Unit test for tax math (15% = SAR 135 on SAR 1000)

6. `test_tax_is_zero_for_non_taxable_course`
   - Unit test confirming zero tax calculation

**Key Validations:**

- ✅ Enrollment record creation
- ✅ Invoice generation with correct tax
- ✅ Tax rate (15% for taxable, 0% for non-taxable)
- ✅ Payment method tracking (noon/tabby)
- ✅ Database integrity

---

### 2. Service Order Payment Tests

#### `Services/ServiceOrderPaymentTest.php` ✨ NEW

Tests for service order payments with tax variations.

**Test Cases:**

1. `test_can_process_taxable_service_order_with_noon_payment`
   - Service order with 15% VAT via Noon
   - Validates order and invoice creation
   - Confirms tax calculations

2. `test_can_process_non_taxable_service_order_with_noon_payment`
   - Service order without tax via Noon
   - Validates zero tax handling

3. `test_can_process_taxable_service_order_with_tabby_payment`
   - Service order with tax via Tabby installments
   - Confirms installment payment type

4. `test_can_process_non_taxable_service_order_with_tabby_payment`
   - Service order without tax via Tabby

5. `test_service_order_creates_invoice_items_correctly`
   - Validates invoice_items table records
   - Confirms service_id linkage

6. `test_tax_calculation_is_correct_for_taxable_service`
   - Unit test for service tax math

**Key Features:**

- Service categories and types setup
- Order record creation
- Invoice with invoice_type = 'service'
- Service-specific tax handling

---

### 3. Manual Invoice & Payment Link Tests (Admin)

#### `admin/tests/Invoices/ManualInvoicePaymentLinkTest.php` ✨ NEW

Tests for admin-generated manual invoices and payment links.

**Test Cases:**

##### Manual Invoice Creation

1. `test_can_generate_manual_invoice_for_taxable_course`
   - Admin creates invoice for taxable course
   - Validates tax calculation and invoice fields

2. `test_can_generate_manual_invoice_for_non_taxable_course`
   - Admin creates invoice without tax
   - Confirms zero tax handling

##### Payment Link Generation (Noon)

3. `test_can_generate_noon_payment_link_for_taxable_course`
   - Generates Noon payment link with tax
   - Validates response structure
   - Confirms payment URL generation

4. `test_can_generate_noon_payment_link_for_taxable_service`
   - Generates Noon payment link for service with tax

##### Payment Link Generation (Tabby)

5. `test_can_generate_tabby_payment_link_for_non_taxable_service`
   - Generates Tabby payment link without tax
   - Validates installment configuration

##### Tax Validation

6. `test_payment_link_includes_correct_tax_for_taxable_items`
   - Validates tax calculation in payment links
   - Confirms total = subtotal + tax

7. `test_payment_link_has_zero_tax_for_non_taxable_items`
   - Validates zero tax in payment links
   - Confirms total = subtotal

**Key Features:**

- Admin user authentication
- Manual invoice generation
- Payment link creation for both Noon and Tabby
- Tax calculation validation
- Response structure validation

---

## Database Factories

### New Factories Created

1. **ServiceFactory.php**
   - Creates test Service records
   - Fields: title, description, type_id

2. **ServiceFeeFactory.php**
   - Creates service fee records
   - States: `taxable()`, `nonTaxable()`, `free()`
   - Default: is_taxable = true, price = 1000

3. **ServiceCategoryFactory.php**
   - Creates service categories
   - Used for service hierarchy

4. **ServiceTypeFactory.php**
   - Creates service types
   - Links to categories

5. **OrderFactory.php**
   - Creates service order records
   - Links users to services

6. **Updated CourseFeeFactory.php**
   - Added `is_taxable` and `is_free` fields
   - Added states: `taxable()`, `nonTaxable()`, `free()`

---

## Tax Calculation Logic

### Saudi Arabia VAT Rate: 15%

**Taxable Items:**

```php
$subtotal = 1000.00;
$tax = $subtotal * 0.15; // 150.00
$total = $subtotal + $tax; // 1150.00
```

**Non-Taxable Items:**

```php
$subtotal = 1000.00;
$tax = 0;
$total = $subtotal; // 1000.00
```

### Database Schema

```sql
-- Invoices
taxable BOOLEAN DEFAULT true
tax_rate DECIMAL(5,2) DEFAULT 15.00
tax DECIMAL(10,2)
subtotal DECIMAL(10,2)
total DECIMAL(10,2)

-- Course/Service Fees
is_taxable BOOLEAN DEFAULT true
is_free BOOLEAN DEFAULT false
```

---

## Running Tests

### Run All Payment Tests

```bash
cd /home/logix/howa/apps/client
php artisan test --filter Payment
```

### Run Specific Test Files

```bash
# Taxable enrollment tests
php artisan test tests/Enrollment/Payment/TaxableEnrollmentPaymentTest.php

# Service order tests
php artisan test tests/Services/ServiceOrderPaymentTest.php

# Manual invoice tests (admin)
cd /home/logix/howa/apps/admin
php artisan test tests/Invoices/ManualInvoicePaymentLinkTest.php
```

### Run Specific Test Methods

```bash
php artisan test --filter test_can_process_taxable_course_enrollment_with_noon_payment
```

---

## Test Coverage Summary

| Scenario                 | Noon | Tabby | Tax | No Tax |
| ------------------------ | ---- | ----- | --- | ------ |
| Course Enrollment        | ✅   | ✅    | ✅  | ✅     |
| Service Order            | ✅   | ✅    | ✅  | ✅     |
| Manual Invoice (Course)  | ✅   | ✅    | ✅  | ✅     |
| Manual Invoice (Service) | ✅   | ✅    | ✅  | ✅     |

**Total Test Cases: 20**

- Enrollment: 6 tests
- Service Orders: 6 tests
- Manual Invoices & Payment Links: 8 tests

---

## Key Assertions

### Invoice Validation

```php
$this->assertDatabaseHas('invoices', [
    'user_id' => $user->id,
    'status' => 'paid',
    'taxable' => true,
    'tax_rate' => 15,
    'invoice_type' => 'course', // or 'service'
]);
```

### Enrollment Validation

```php
$this->assertDatabaseHas('enrollments', [
    'user_id' => $user->id,
    'course_id' => $course->id,
    'status' => 'paid',
]);
```

### Order Validation

```php
$this->assertDatabaseHas('orders', [
    'user_id' => $user->id,
    'service_id' => $service->id,
    'status' => 'paid',
]);
```

### Tax Calculation Validation

```php
$invoice = Invoice::find($id);
$this->assertTrue($invoice->taxable);
$this->assertEquals(15, $invoice->tax_rate);
$this->assertGreaterThan(0, $invoice->tax);
$this->assertEquals($subtotal + $tax, $invoice->total);
```

---

## HTTP Mocking

All tests use HTTP fakes to avoid real payment gateway calls:

```php
Http::fake([
    '*/noon/order/*' => Http::response($mockNoonResponse, 200),
    '*/tabby/payment/*' => Http::response($mockTabbyResponse, 200),
    '*/api/zatca-v2/sign-invoice' => Http::response(['status' => 'success'], 200),
    '*/api/invoice/generate-pdf' => Http::response(['status' => 'success'], 200)
]);
```

---

## Migration Changes

### Added to Course Fees Table

```php
$table->boolean('is_taxable')->default(true);
$table->boolean('is_free')->default(false);
```

### Added to Service Fees Table

```php
$table->boolean('is_taxable')->default(true);
$table->boolean('is_free')->default(false);
```

---

## Future Enhancements

1. **Coupon Integration**
   - Test tax calculation with coupons
   - Discount applied before/after tax

2. **Multi-Currency**
   - Test tax with different currencies
   - Currency conversion with tax

3. **Tax Exemption Certificates**
   - User-specific tax exemptions
   - Document upload and validation

4. **Partial Payments**
   - Tax allocation on partial payments
   - Installment-specific tax handling

---

## Troubleshooting

### Test Failures

**Issue: "Table not found" errors**

```bash
# Solution: Run migrations
php artisan migrate:fresh
```

**Issue: "Factory not found" errors**

```bash
# Solution: Ensure composer autoload is up to date
composer dump-autoload
```

**Issue: "Route not found" errors**

```bash
# Solution: Check route definitions in routes/web.php
php artisan route:list
```

---

## Contact & Support

For questions about these tests:

1. Review test code comments
2. Check TEST_DOCUMENTATION.md (this file)
3. Review actual controller implementations
4. Check database migrations

**Last Updated:** October 19, 2025
**Test Suite Version:** 2.0
**Coverage:** Taxable/Non-Taxable Payment Scenarios
