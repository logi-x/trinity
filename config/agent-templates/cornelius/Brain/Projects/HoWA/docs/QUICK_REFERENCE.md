---
title: "Quick Reference Card - Factories & Seeders"
date: "2026-04-11"
tags: ["project/howa", "docs/howa"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Quick Reference Card - Factories & Seeders

## 🚀 Quick Commands

### Seeders

```bash
# Run all seeders
php artisan migrate:fresh
php artisan db:seed --class=CourseSeeder
php artisan db:seed --class=ServiceSeeder
php artisan db:seed --class=PaymentTestDataSeeder

# Quick reset with test data
php artisan migrate:fresh && \
php artisan db:seed --class=PaymentTestDataSeeder
```

### Test Data Access

```php
// Get test users
$testUser = User::where('email', 'testuser@example.com')->first();
$adminUser = User::where('email', 'admin@example.com')->first();

// Get test courses
$taxableCourse = Course::where('title', 'LIKE', '[TEST] Taxable%')->first();
$nonTaxableCourse = Course::where('title', 'LIKE', '[TEST] Non-Taxable%')->first();

// Get test services
$taxableService = Service::where('title', 'LIKE', '[TEST] Taxable%')->first();
$freeService = Service::where('title', 'LIKE', '[TEST] Free%')->first();
```

---

## 💡 Factory States

### Course

```php
Course::factory()->featured()->create();
Course::factory()->popular()->create();
Course::factory()->bestseller()->create();
Course::factory()->online()->create();
Course::factory()->soldOut()->create();
```

### Course Fee

```php
CourseFee::factory()->taxable()->create();      // 15% VAT
CourseFee::factory()->nonTaxable()->create();   // 0% VAT
CourseFee::factory()->free()->create();         // Free
```

### Service

```php
Service::factory()->active()->create();
Service::factory()->inactive()->create();
Service::factory()->private()->create();
Service::factory()->popular()->create();
Service::factory()->new()->create();
```

### Service Fee

```php
ServiceFee::factory()->taxable()->create();     // 15% VAT
ServiceFee::factory()->nonTaxable()->create();  // 0% VAT
ServiceFee::factory()->free()->create();        // Free
ServiceFee::factory()->premium()->create();     // 10K-30K
ServiceFee::factory()->budget()->create();      // 250-1K
ServiceFee::factory()->onlineOnly()->create();  // Noon/Tabby
ServiceFee::factory()->cashOnly()->create();    // Cash
```

---

## 📊 Test Data Summary

### Test Users

| Email                  | Password | Role  | Phone         |
| ---------------------- | -------- | ----- | ------------- |
| <testuser@example.com> | password | user  | +966530111111 |
| <admin@example.com>    | password | admin | +966530222222 |

### Test Courses (4)

| Title                           | Price     | Tax | Payment |
| ------------------------------- | --------- | --- | ------- |
| [TEST] Taxable Course - Noon    | SAR 1,000 | 15% | Noon    |
| [TEST] Non-Taxable - Tabby      | SAR 1,000 | 0%  | Tabby   |
| [TEST] Taxable - Manual Invoice | SAR 1,500 | 15% | Manual  |
| [TEST] Free Test Course         | SAR 0     | 0%  | Free    |

### Test Services (4)

| Title                         | Price      | Tax | Payment |
| ----------------------------- | ---------- | --- | ------- |
| [TEST] Taxable Service - Noon | SAR 2,000  | 15% | Noon    |
| [TEST] Non-Taxable - Tabby    | SAR 2,000  | 0%  | Tabby   |
| [TEST] Premium Taxable        | SAR 10,000 | 15% | Premium |
| [TEST] Free Consultation      | SAR 0      | 0%  | Free    |

---

## 🧮 Tax Calculation

### Formula

```
Taxable: Total = Subtotal + (Subtotal × 0.15)
Non-Taxable: Total = Subtotal
```

### Examples

```
Taxable SAR 1,000:
  Subtotal: 1,000
  Tax (15%): 150
  Total: 1,150

Non-Taxable SAR 1,000:
  Subtotal: 1,000
  Tax (0%): 0
  Total: 1,000
```

---

## 🎯 Common Test Scenarios

### 1. Taxable Course with Noon

```php
$course = Course::where('title', 'LIKE', '[TEST] Taxable%Noon%')->first();
$user = User::where('email', 'testuser@example.com')->first();
// Test Noon payment flow
```

### 2. Non-Taxable Service with Tabby

```php
$service = Service::where('title', 'LIKE', '[TEST] Non-Taxable%')->first();
$user = User::where('email', 'testuser@example.com')->first();
// Test Tabby installment flow
```

### 3. Manual Invoice Generation

```php
$course = Course::where('title', 'LIKE', '%Manual Invoice%')->first();
$admin = User::where('email', 'admin@example.com')->first();
// Test manual invoice creation
```

---

## 📝 Factory Usage in Tests

### Basic Usage

```php
public function test_example()
{
    $course = Course::factory()->create();
    $course->fee()->create(
        CourseFee::factory()->taxable()->make()->toArray()
    );

    // Your assertions
}
```

### With Relationships

```php
$category = ServiceCategory::factory()->create();
$type = ServiceType::factory()->create(['category_id' => $category->id]);
$service = Service::factory()->active()->create(['type_id' => $type->id]);
$service->fee()->create(
    ServiceFee::factory()->premium()->taxable()->make()->toArray()
);
```

---

## 🔍 Verification Commands

```bash
# Check seeded counts
php artisan tinker
>>> Course::count()
>>> Service::count()
>>> User::where('email', 'LIKE', '%example.com')->count()

# Check tax distribution
>>> Course::whereHas('fee', fn($q) => $q->where('is_taxable', true))->count()
>>> Service::whereHas('fee', fn($q) => $q->where('is_taxable', false))->count()
```

---

## 📚 Documentation Files

| File                                 | Description              |
| ------------------------------------ | ------------------------ |
| **QUICK_REFERENCE.md**               | This file - Quick access |
| **FACTORIES_AND_SEEDERS_SUMMARY.md** | Complete overview        |
| **SEEDER_DOCUMENTATION.md**          | Detailed seeder docs     |
| **TESTING_SUMMARY.md**               | Payment tests overview   |
| **TEST_DOCUMENTATION.md**            | Comprehensive test guide |

---

## 🆘 Troubleshooting

### Issue: Unique constraint error

```bash
# Solution: Clean and reseed
php artisan migrate:fresh
php artisan db:seed --class=PaymentTestDataSeeder
```

### Issue: Factory not found

```bash
composer dump-autoload
```

### Issue: No test data found

```bash
# Reseed payment test data
php artisan db:seed --class=PaymentTestDataSeeder
```

---

**Last Updated:** October 19, 2025  
**Quick Access:** Keep this file handy for daily development
