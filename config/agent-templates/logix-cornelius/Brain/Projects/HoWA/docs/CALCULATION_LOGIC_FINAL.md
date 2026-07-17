---
title: "Final Calculation Logic"
date: "2026-04-24"
tags: ["project/howa", "docs/howa"]
category: "docs/howa"
updated: "2026-07-15"
---

> ↑ [[Entities/Projects/HoWA|HoWA]]

# Final Calculation Logic - All Components Aligned ✅

## Executive Summary

All dashboard statistics and charts are now using **semantically correct** calculations where:

- **Total Sales** = Gross revenue (what customers initially paid)
- **Total Paid** = Net revenue (what we actually kept after ALL refunds)
- **Net Profit** = Total Paid - Total Taxes

## 🎯 Final Accurate Values

```
╔══════════════════════════════════════════════════════════════════╗
║                   SEMANTICALLY CORRECT VALUES                    ║
╠══════════════════════════════════════════════════════════════════╣
║  Total Sales:        3,432,732.56 SAR (gross billing)           ║
║  Total Paid:         3,303,115.59 SAR (net after refunds)       ║
║  Total Refunds:        129,616.97 SAR (86 refunds)              ║
║                                                                  ║
║  Total Taxes:          446,383.71 SAR ✅                        ║
║  Net Profit:         2,856,731.88 SAR ✅                        ║
║                                                                  ║
║  Total Taxable:      3,035,297.89 SAR ✅                        ║
║  Total Non-Taxable:          0.00 SAR ✅                        ║
╚══════════════════════════════════════════════════════════════════╝
```

## 📊 Calculation Formulas

### Main Dashboard Statistics

#### Total Paid (Updated)

```php
// Now uses ALL refunds (partial + full)
$netEnrollmentsPaid = $grossEnrollmentsPaid - $allEnrollmentRefunds;
$netOrdersPaid = $grossOrdersPaid - $allOrderRefunds;
$totalPaid = $netEnrollmentsPaid + $netOrdersPaid;

// Result: 3,303,115.59 SAR
```

#### Total Taxable/Non-Taxable (Updated)

```php
// Now uses refunds filtered by tax status
$totalTaxable = $grossTaxable - $taxableRefunds;
$totalNonTaxable = $grossNonTaxable - $nonTaxableRefunds;

// Result: 3,035,297.89 SAR (taxable)
```

#### Total Taxes (Unchanged - Still Correct)

```php
// Only uses PARTIAL refund tax (fully refunded already excluded by SQL)
$netTax = $grossTax - $partialRefundTax;

// Result: 446,383.71 SAR
```

#### Net Profit (Updated via Total Paid)

```php
// Automatically correct since Total Paid is now correct
$netProfit = $totalPaid - $totalTaxes;

// Result: 2,856,731.88 SAR
```

### Chart Data (Already Correct)

Charts were already using the correct logic:

```php
// In getRefundsByInterval()
$completedRefunds = InvoiceRefund::where('status', 'completed')->get();
// ✅ No filter - returns ALL refunds (partial + full)

// In chart tooltip
net_profit = subtotal - (total_refunds + refunds_tax)
// ✅ Subtracts ALL refunds from subtotal
```

## 🔍 Detailed Breakdown

### Enrollments

```
Gross Paid:      3,164,914.86 SAR
- All Refunds:     129,616.97 SAR (86 refunds: 85 full + 1 partial)
─────────────────────────────────
Net Paid:        3,035,297.89 SAR ✅

Gross Tax:         412,813.91 SAR
- Partial Tax:          58.57 SAR (1 partial refund only)
─────────────────────────────────
Net Tax:           412,755.34 SAR ✅

Net Profit:      2,622,542.55 SAR ✅
```

### Orders

```
Gross Paid:        267,817.70 SAR
- All Refunds:           0.00 SAR (no refunds)
─────────────────────────────────
Net Paid:          267,817.70 SAR ✅

Gross Tax:          33,628.37 SAR
- Partial Tax:           0.00 SAR (no partial refunds)
─────────────────────────────────
Net Tax:            33,628.37 SAR ✅

Net Profit:        234,189.33 SAR ✅
```

### Total

```
Total Paid:      3,303,115.59 SAR ✅
Total Taxes:       446,383.71 SAR ✅
─────────────────────────────────
Net Profit:      2,856,731.88 SAR ✅
```

## 💡 Why This Makes Sense

### Before (Confusing)

```
Total Sales:  3,432,732.56 SAR (gross)
Total Paid:   3,432,283.56 SAR (gross - partial only)
Difference:          449.00 SAR (only 1 partial refund)

❌ Problem: 85 full refunds (129,167.97 SAR) not subtracted!
❌ "Total Paid" included money we refunded
```

### After (Clear & Accurate)

```
Total Sales:  3,432,732.56 SAR (what customers paid initially)
Total Paid:   3,303,115.59 SAR (what we actually kept)
Difference:      129,616.97 SAR (all 86 refunds)

✅ "Total Paid" = money in our account
✅ "Total Sales" = gross billing volume
✅ Clear distinction between gross and net
```

## 🎯 Semantic Clarity

| Metric                | Meaning           | Calculation                             |
| --------------------- | ----------------- | --------------------------------------- |
| **Total Sales**       | Gross billing     | All paid invoices                       |
| **Total Paid**        | Net revenue       | Gross - ALL refunds                     |
| **Total Refunds**     | Money returned    | All refund amounts                      |
| **Total Taxes**       | Net tax liability | Gross tax - Partial refund tax          |
| **Net Profit**        | Actual profit     | Total Paid - Total Taxes                |
| **Total Taxable**     | Taxable revenue   | Gross taxable - Taxable refunds         |
| **Total Non-Taxable** | Exempt revenue    | Gross non-taxable - Non-taxable refunds |

## ✅ Components Updated

### 1. HomeController.php

- ✅ Updated `getStats()` - Total Paid uses ALL refunds
- ✅ Updated `getStatsDebug()` - Total Paid uses ALL refunds
- ✅ Added `course_taxable_refunds`, `course_non_taxable_refunds` to refund stats
- ✅ Updated Total Taxable/Non-Taxable calculations
- ✅ Updated all comments and documentation

### 2. Validation Commands

- ✅ `ValidateTotalPaid.php` - Now validates ALL refunds
- ✅ `ValidateNetProfit.php` - Now validates ALL refunds
- ✅ Updated display messages to show "Total Refunds" instead of "Partial Refunds"
- ✅ All commands passing with new logic

### 3. Charts (Already Correct)

- ✅ `chart.tsx` - Already using ALL refunds
- ✅ `averages-chart.tsx` - Already using ALL refunds
- ✅ Chart data preparation - Already using ALL refunds
- ✅ No changes needed!

### 4. Documentation

- ✅ Updated PHPDoc comments
- ✅ Updated inline code comments
- ✅ Created comprehensive docs in `/docs` portal

## 🧪 Test Results

All tests passing:

```
✅ DashboardStatisticsAccuracyTest - 5 scenarios
✅ InvoiceRefundCalculationsTest - 11 scenarios
✅ Total: 16 scenarios, 87 assertions - ALL PASSING
```

Validation commands:

```
✅ validate:total-paid - EXACT MATCH
✅ validate:total-taxes - EXACT MATCH
✅ validate:net-profit - EXACT MATCH
✅ validate:all-calculations - ALL PASSING
```

## 🎊 Final Verification

Run these commands to verify everything:

```bash
# Verify all calculations
php artisan validate:all-calculations --detailed

# Check test suite
php artisan test --filter=Statistics

# View updated stats
curl http://localhost:8001/api/v1/stats-debug --insecure | jq
```

## 📖 Related Documentation

- `VALIDATED_CALCULATION_FORMULAS.md` - Core formulas
- `TAX_CALCULATION_GUIDE.md` - Tax calculations
- `VALIDATION_COMMANDS_README.md` - Validation commands
- `/docs/statistics-accuracy-report` - Accuracy report (in docs portal)
- `/docs/validated-calculation-formulas` - Formulas (in docs portal)

---

**🎉 ALL CALCULATIONS ARE SEMANTICALLY CORRECT AND VALIDATED! 🎉**

_Last Updated: October 26, 2025_
_All components aligned and production-ready_
