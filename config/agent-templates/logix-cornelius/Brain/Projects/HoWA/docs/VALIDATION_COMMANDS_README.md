---
title: "Dashboard Statistics Validation Commands"
date: "2026-04-11"
tags: ["project/howa", "docs/howa"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Dashboard Statistics Validation Commands

## Overview

Four Artisan commands have been created to validate dashboard statistics calculations against actual database records. These commands help ensure data accuracy and can be run anytime to verify calculations.

## Available Commands

### 1. Validate Total Paid

```bash
php artisan validate:total-paid
```

Validates that `Total Paid` is correctly calculated as:

```
Total Paid = (Gross Enrollment Paid - Partial Enrollment Refunds)
           + (Gross Order Paid - Partial Order Refunds)
```

**Flags:**

- `--detailed` : Show detailed breakdown by enrollments and orders
- `--json` : Output results as JSON

**Example:**

```bash
# Basic validation
php artisan validate:total-paid

# With detailed breakdown
php artisan validate:total-paid --detailed

# JSON output
php artisan validate:total-paid --json
```

---

### 2. Validate Total Taxes

```bash
php artisan validate:total-taxes
```

Validates that `Total Taxes` is correctly calculated as:

```
Total Taxes = (Gross Enrollment Tax - Partial Enrollment Refund Tax)
            + (Gross Order Tax - Partial Order Refund Tax)
```

**Flags:**

- `--detailed` : Show detailed breakdown with refund information
- `--json` : Output results as JSON

**Example:**

```bash
# Basic validation
php artisan validate:total-taxes

# With detailed breakdown
php artisan validate:total-taxes --detailed

# JSON output for CI/CD
php artisan validate:total-taxes --json
```

---

### 3. Validate Net Profit

```bash
php artisan validate:net-profit
```

Validates that `Net Profit` is correctly calculated as:

```
Net Profit = Total Paid - Total Taxes
```

Also performs alternative verification using subtotals:

```
Net Profit = (Gross Subtotal - Partial Refund Subtotal)
```

**Flags:**

- `--detailed` : Show both calculation methods and breakdown by type
- `--json` : Output results as JSON

**Example:**

```bash
# Basic validation
php artisan validate:net-profit

# With detailed breakdown showing both methods
php artisan validate:net-profit --detailed
```

---

### 4. Validate All Calculations

```bash
php artisan validate:all-calculations
```

Runs all three validations in sequence and provides a summary report.

**Flags:**

- `--detailed` : Show detailed breakdown for all validations
- `--json` : Output combined results as JSON

**Example:**

```bash
# Quick validation of all calculations
php artisan validate:all-calculations

# Comprehensive report
php artisan validate:all-calculations --detailed

# For monitoring/alerting systems
php artisan validate:all-calculations --json
```

---

## Usage Examples

### Daily Verification

```bash
# Quick check (recommended for daily use)
php artisan validate:all-calculations
```

### Detailed Investigation

```bash
# If you notice discrepancies
php artisan validate:total-paid --detailed
php artisan validate:total-taxes --detailed
php artisan validate:net-profit --detailed
```

### CI/CD Integration

```bash
# Add to deployment pipeline
php artisan validate:all-calculations --json | jq '.all_passed'
```

### Monitoring

```bash
# Create a cron job to alert on discrepancies
0 */6 * * * cd /home/logix/howa/apps/admin && php artisan validate:all-calculations || mail -s "Stats Discrepancy Alert" admin@howa.edu.sa
```

## Understanding the Output

### Exit Codes

- `0` : All calculations are accurate
- `1` : Discrepancies detected

### Success Indicators

- ✅ **EXACT MATCH** : Difference < 0.01 SAR (perfect)
- ✅ **ACCURATE** : Difference < 1 SAR (acceptable rounding)
- ❌ **DISCREPANCY** : Difference ≥ 1 SAR (needs investigation)

### Sample Output

```
╔══════════════════════════════════════════════════════════════════════╗
║                      TOTAL PAID VALIDATION                           ║
╚══════════════════════════════════════════════════════════════════════╝

  Calculated from DB: 3,432,283.56 SAR
  API Value: 3,432,283.56 SAR
  Difference: 0.00 SAR

✅ EXACT MATCH - Total Paid is 100% accurate!
```

## What Each Command Validates

### validate:total-paid

- ✅ Queries all paid invoices (status = 'paid')
- ✅ Calculates gross paid amounts
- ✅ Subtracts partial refund amounts only
- ✅ Compares with API /stats-debug endpoint
- ✅ Returns enrollment, order, and total breakdowns

### validate:total-taxes

- ✅ Queries all taxable paid invoices
- ✅ Calculates gross tax amounts
- ✅ Subtracts partial refund taxes only (not full refunds)
- ✅ Validates tax-inclusive pricing formulas
- ✅ Compares with API values

### validate:net-profit

- ✅ Uses validated Total Paid and Total Taxes
- ✅ Calculates: Total Paid - Total Taxes
- ✅ Alternative validation using subtotals
- ✅ Shows breakdown by enrollment and order types
- ✅ Verifies both methods give same result (within rounding)

### validate:all-calculations

- ✅ Runs all three validations sequentially
- ✅ Provides comprehensive summary
- ✅ Single command for complete verification
- ✅ Returns 0 only if ALL calculations are accurate

## Troubleshooting

### If discrepancies are detected

1. **Check database consistency:**

   ```bash
   php artisan tinker
   DB::table('invoices')->where('status', 'paid')->count();
   ```

2. **Clear cache:**

   ```bash
   php artisan optimize:clear
   ```

3. **Run with detailed flag:**

   ```bash
   php artisan validate:total-taxes --detailed
   ```

4. **Check logs:**

   ```bash
   tail -100 storage/logs/core.howa.edu.sa-$(date +%Y-%m-%d).log
   ```

5. **Run test suite:**

   ```bash
   php artisan test --filter=InvoiceRefundCalculationsTest
   ```

## Related Documentation

- `VALIDATED_CALCULATION_FORMULAS.md` - Core formulas and methodology
- `TAX_CALCULATION_GUIDE.md` - Saudi VAT tax-inclusive pricing
- `FINAL_CALCULATION_SUMMARY.md` - Complete implementation summary
- `tests/Feature/Statistics/` - Comprehensive test suite (16 scenarios, 87 assertions)

## Technical Details

### Data Sources

- **Database Tables**: `invoices`, `invoice_refunds`
- **API Endpoint**: `/api/v1/stats-debug`
- **Calculation Method**: Direct SQL queries matching HomeController logic

### Validation Criteria

- Exact match (0.00 SAR difference) ✅
- Acceptable variance (< 1 SAR) ✅
- Rounding tolerance (< 0.01% of total)

### Performance

- Fast execution (~1-2 seconds)
- Direct database queries
- Minimal memory usage
- Can be run frequently

---

**💡 Tip**: Run `php artisan validate:all-calculations` after any changes to refund logic or invoice processing to ensure accuracy!
