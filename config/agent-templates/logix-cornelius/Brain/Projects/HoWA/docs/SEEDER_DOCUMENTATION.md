---
title: "Database Seeders Documentation"
date: "2026-04-11"
tags: ["project/howa", "docs/howa"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Database Seeders Documentation

## Overview

Comprehensive documentation for all database seeders including courses, services, and payment test data.

---

## Available Seeders

### 1. CourseSeeder

Seeds the database with realistic course data including various pricing and tax scenarios.

**Usage:**

```bash
php artisan db:seed --class=CourseSeeder
```

**What It Creates:**

- **50 Total Courses:**
  - 30 Regular courses (70% taxable, 30% non-taxable)
  - 5 Featured & Popular courses
  - 5 Bestseller courses
  - 3 Free courses
  - 4 Online courses (non-taxable educational)
  - 3 Sold-out premium courses

**Features:**

- Realistic Saudi Arabian course titles
- Multiple timings per course (1-5 depending on popularity)
- Varied pricing (SAR 500 - SAR 6,000)
- CPD hours allocation
- Ratings and reviews
- Keywords and metadata

**Course Categories:**

- Project Management
- Digital Marketing
- Financial Planning
- Healthcare Administration
- Software Development
- Data Science
- Business Leadership
- Cybersecurity
- Human Resources
- And more...

---

### 2. ServiceSeeder

Seeds professional services with categories, types, and fee structures.

**Usage:**

```bash
php artisan db:seed --class=ServiceSeeder
```

**What It Creates:**

- **6 Service Categories:**
  - Professional Consulting
  - Technical Services
  - Training & Development
  - Financial Services
  - Legal Services
  - Marketing Services

- **18 Service Types** (3 per category)

- **90+ Services:**
  - Regular services (3 per type)
  - Premium services (1 per type)
  - Budget services (1 per type)
  - Special services (Free consultation, VIP packages, etc.)

**Service Features:**

- Realistic business service titles
- Varied pricing (SAR 250 - SAR 50,000)
- Tax status (70% taxable, 30% non-taxable)
- Multiple payment methods
- Discount structures
- Active/inactive states

---

### 3. PaymentTestDataSeeder

Creates specific test data for payment integration testing.

**Usage:**

```bash
php artisan db:seed --class=PaymentTestDataSeeder
```

**What It Creates:**

#### Test Users (2 users)

```
1. Regular User
   - Email: testuser@example.com
   - Phone: +966530111111
   - Role: user

2. Admin User
   - Email: admin@example.com
   - Phone: +966530222222
   - Role: admin
```

#### Test Courses (4 courses)

```
1. [TEST] Taxable Course - Noon Payment
   - Price: SAR 1,000 | Discounted: SAR 900
   - Taxable: YES (15% VAT)
   - For testing: Noon payment gateway

2. [TEST] Non-Taxable Course - Tabby Payment
   - Price: SAR 1,000 | Discounted: SAR 900
   - Taxable: NO
   - For testing: Tabby installments

3. [TEST] Taxable Course - Manual Invoice
   - Price: SAR 1,500 | Discounted: SAR 1,350
   - Taxable: YES
   - For testing: Manual invoice generation

4. [TEST] Free Test Course
   - Price: SAR 0
   - Taxable: NO
   - For testing: Free enrollment
```

#### Test Services (4 services)

```
1. [TEST] Taxable Service - Noon Payment
   - Price: SAR 2,000 | Discounted: SAR 1,800
   - Taxable: YES (15% VAT)

2. [TEST] Non-Taxable Service - Tabby Payment
   - Price: SAR 2,000 | Discounted: SAR 1,800
   - Taxable: NO

3. [TEST] Premium Taxable Service
   - Price: SAR 10,000 | Discounted: SAR 9,000
   - Taxable: YES

4. [TEST] Free Consultation Service
   - Price: SAR 0
   - Taxable: NO
```

**When to Use:**

- Before running automated tests
- For manual payment gateway testing
- When demonstrating payment flows
- For QA team testing scenarios

---

## Running Seeders

### Run All Seeders

```bash
# Run all seeders defined in DatabaseSeeder
php artisan db:seed
```

### Run Specific Seeder

```bash
# Run only course seeder
php artisan db:seed --class=CourseSeeder

# Run only service seeder
php artisan db:seed --class=ServiceSeeder

# Run only payment test data
php artisan db:seed --class=PaymentTestDataSeeder
```

### Fresh Migration with Seeding

```bash
# Drop all tables, run migrations, then seed
php artisan migrate:fresh --seed
```

### Production-Safe Seeding

```bash
# Only seed if database is empty (safe for production)
php artisan db:seed --class=CourseSeeder --force
```

---

## Factory States Reference

### CourseFactory States

```php
// Featured course
Course::factory()->featured()->create();

// Popular course (high viewers & reviews)
Course::factory()->popular()->create();

// Bestseller
Course::factory()->bestseller()->create();

// Online course
Course::factory()->online()->create();

// Sold out
Course::factory()->soldOut()->create();
```

### CourseFeeFactory States

```php
// Taxable course fee (15% VAT)
CourseFee::factory()->taxable()->create();

// Non-taxable course fee
CourseFee::factory()->nonTaxable()->create();

// Free course
CourseFee::factory()->free()->create();
```

### ServiceFactory States

```php
// Active service
Service::factory()->active()->create();

// Inactive service
Service::factory()->inactive()->create();

// Private service
Service::factory()->private()->create();

// Popular service
Service::factory()->popular()->create();

// New service (recently created)
Service::factory()->new()->create();
```

### ServiceFeeFactory States

```php
// Taxable service fee
ServiceFee::factory()->taxable()->create();

// Non-taxable service fee
ServiceFee::factory()->nonTaxable()->create();

// Free service
ServiceFee::factory()->free()->create();

// Premium pricing
ServiceFee::factory()->premium()->create();

// Budget pricing
ServiceFee::factory()->budget()->create();

// No discount
ServiceFee::factory()->noDiscount()->create();

// Online payment only
ServiceFee::factory()->onlineOnly()->create();

// Cash only
ServiceFee::factory()->cashOnly()->create();
```

---

## Seeder Customization

### Modify Course Count

```php
// In CourseSeeder.php
Course::factory()
    ->count(50) // Change this number
    ->create()
    // ...
```

### Adjust Tax Ratio

```php
// Change 70% to desired percentage
$isTaxable = rand(1, 100) <= 70; // 70% taxable
```

### Customize Price Ranges

```php
// In ServiceFeeFactory.php
$price = $this->faker->randomElement([
    500, 1000, 2000, 5000, 10000 // Add/remove values
]);
```

---

## Tax Configuration

### Saudi Arabia VAT Rate: 15%

**Taxable Items:**

- Most business services
- Commercial training programs
- Consulting services
- IT services

**Non-Taxable Items:**

- Educational courses (certain categories)
- Free services
- Government-mandated services
- Healthcare services (in some cases)

### Calculating Final Price

```php
// For taxable items
$subtotal = 1000.00;
$tax = $subtotal * 0.15; // SAR 150
$total = $subtotal + $tax; // SAR 1150

// For non-taxable items
$subtotal = 1000.00;
$tax = 0;
$total = $subtotal; // SAR 1000
```

---

## Best Practices

### 1. Use Transactions

Always wrap seeder operations in transactions:

```php
DB::transaction(function () {
    // Seeding logic here
});
```

### 2. Check Before Seeding

Prevent duplicate data:

```php
if (Course::count() > 0) {
    $this->command->warn('Courses already exist!');
    return;
}
```

### 3. Display Progress

Inform users about seeding progress:

```php
$this->command->info('✅ Courses seeded successfully!');
$this->command->line('Created ' . $count . ' courses');
```

### 4. Use Realistic Data

Prefer realistic titles and descriptions over random strings.

### 5. Maintain Relationships

Always create related records together:

```php
$course = Course::factory()->create();
$course->fee()->create([...]);
$course->time()->create([...]);
```

---

## Troubleshooting

### Issue: "Class not found" Error

**Solution:**

```bash
composer dump-autoload
```

### Issue: Foreign Key Constraint Errors

**Solution:** Ensure parent records exist before creating child records, or disable foreign key checks:

```php
DB::statement('SET FOREIGN_KEY_CHECKS=0;');
// Seeding logic
DB::statement('SET FOREIGN_KEY_CHECKS=1;');
```

### Issue: Duplicate Entry Errors

**Solution:** Truncate tables before seeding:

```php
Course::truncate();
Service::truncate();
```

### Issue: Memory Limit Exceeded

**Solution:** Reduce batch sizes or increase PHP memory:

```bash
php -d memory_limit=512M artisan db:seed
```

---

## Testing Seeders

### Test Individual Seeder

```bash
php artisan db:seed --class=CourseSeeder
```

### Verify Seeded Data

```bash
# Check course count
php artisan tinker
>>> Course::count()
>>> Course::where('is_taxable', true)->count()
```

### Reseed Specific Tables

```bash
php artisan migrate:fresh --path=database/migrations/specific_migration.php
php artisan db:seed --class=CourseSeeder
```

---

## Integration with Tests

### Use Seeders in Tests

```php
public function setUp(): void
{
    parent::setUp();
    $this->seed(PaymentTestDataSeeder::class);
}
```

### Access Seeded Data in Tests

```php
$course = Course::where('title', 'LIKE', '[TEST]%')->first();
$user = User::where('email', 'testuser@example.com')->first();
```

---

## Quick Reference

| Command                                    | Description           |
| ------------------------------------------ | --------------------- |
| `php artisan db:seed`                      | Run all seeders       |
| `php artisan db:seed --class=CourseSeeder` | Run specific seeder   |
| `php artisan migrate:fresh --seed`         | Reset & seed database |
| `php artisan db:seed --force`              | Seed in production    |
| `composer dump-autoload`                   | Refresh autoloader    |

---

**Last Updated:** October 19, 2025  
**Version:** 1.0  
**Maintained by:** Development Team
