---
title: "ETF System Accuracy Update"
date: "2026-04-11"
tags: ["project/howa", "docs/howa"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# ETF System Accuracy Update

## Summary

The ETF system has been successfully migrated to the new `invoice_refunds` table system and now **perfectly matches** the dashboard Net Profit calculations with **0.00 SAR difference**.

---

## Changes Made

### 1. **Updated ETF Sync Command** (`SyncEtfNavFromPlatformData.php`)

#### Refund Grouping

**Before:** Refunds were grouped by `completed_at` (when refund was processed)

```php
->whereBetween('completed_at', [$startDate, $endDate])
->groupBy(DB::raw('DATE(completed_at)'))
```

**After:** Refunds are grouped by invoice `created_at` (when sale occurred)

```php
->join('invoices', 'invoice_refunds.invoice_id', '=', 'invoices.id')
->whereBetween('invoices.created_at', [$startDate, $endDate])
->groupBy(DB::raw('DATE(invoices.created_at)'))
```

**Why:** This ensures refunds are attributed to the same period as the original sale, matching the dashboard chart logic.

---

#### NAV Calculation Formula

**Before:**

```php
$netRevenue = $grossRevenue - (float) $day->total_tax;
$refunds = (float) ($day->total_refunds ?? 0);
$netDailyIncome = $netRevenue - $refunds - $operatingExpenses;
```

**After:**

```php
// Calculate gross revenue (tax-inclusive, from paid invoices)
$grossRevenue = (float) $day->total_revenue;

// Calculate total refunds (tax-inclusive, returned to customers)
$totalRefunds = (float) ($day->total_refunds ?? 0);

// Calculate NET tax (tax paid to government minus tax credits from refunds)
$grossTax = (float) $day->total_tax;
$refundTax = (float) ($day->total_tax_refund ?? 0);
$netTax = $grossTax - $refundTax;

// Calculate total paid (gross revenue minus all refunds)
$totalPaid = $grossRevenue - $totalRefunds;

// Calculate net revenue (total paid minus net taxes to government)
// This matches dashboard "Net Profit" calculation
$netRevenue = $totalPaid - $netTax;

// Calculate operating expenses (percentage of net revenue)
$operatingExpenses = $netRevenue * $expenseRatio;

// Calculate net daily income (what actually adds to fund AUM)
// = Net Revenue - Operating Expenses
// Refunds are already accounted for in totalPaid calculation
$netDailyIncome = $netRevenue - $operatingExpenses;
```

**Why:** This matches the exact calculation used in the dashboard:

- Total Paid = Gross Revenue - ALL Refunds
- Net Profit = Total Paid - NET Taxes

---

### 2. **Updated Metadata Storage**

**Added fields to metadata:**

```json
{
  "gross_revenue": 3432732.56,
  "total_refunds": 129616.97,
  "total_paid": 3303115.59,
  "gross_tax": 447290.84,
  "refund_tax": 17755.06,
  "net_tax": 429535.78,
  "refund_count": 17,
  "operating_expenses": 0,
  "net_profit": 2873579.81
}
```

---

### 3. **Updated Revenue Record Breakdown**

**Added detailed breakdown for transparency:**

```json
{
  "calculation": "Gross Revenue - Total Refunds - Net Taxes - Operating Expenses",
  "gross_revenue": 3432732.56,
  "minus_refunds": 129616.97,
  "equals_total_paid": 3303115.59,
  "minus_net_tax": 429535.78,
  "equals_net_profit": 2873579.81,
  "minus_operating_expenses": 0,
  "equals_net_daily_income": 2873579.81,
  "refund_count": 17,
  "refund_tax_credit": 17755.06,
  "operating_expense_ratio": "0%"
}
```

---

## Validation Results

### Command Run

```bash
php artisan etf:sync-nav --fresh --expense-ratio=0
```

### ETF Fund Results

```
📊 ETF FUND:
  Total AUM:         SAR 3,873,579.81
  Seed Capital:      SAR 1,000,000.00
  Net Profit:        SAR 2,873,579.81
```

### Dashboard Results

```
💰 DASHBOARD:
  Total Sales:       SAR 3,432,732.56
  Total Refunds:     SAR   129,616.97
  Total Paid:        SAR 3,303,115.59
  Total Taxes:       SAR   429,535.78
  Net Profit:        SAR 2,873,579.81
```

### Accuracy Check

```
✅ ACCURACY CHECK:
  Difference:        SAR 0.00 ✅ PERFECT MATCH!
```

---

## Breakdown by Component

| Component         | Dashboard (SAR) | ETF (SAR)    | Difference | Status |
| ----------------- | --------------- | ------------ | ---------- | ------ |
| **Total Sales**   | 3,432,732.56    | 3,432,732.56 | 0.00       | ✅     |
| **Total Refunds** | 129,616.97      | 129,616.97   | 0.00       | ✅     |
| **Total Paid**    | 3,303,115.59    | 3,303,115.59 | 0.00       | ✅     |
| **Total Taxes**   | 429,535.78      | 429,535.78   | 0.00       | ✅     |
| **Net Profit**    | 2,873,579.81    | 2,873,579.81 | 0.00       | ✅     |

---

## Key Formulas Aligned

### 1. Total Paid

```
Total Paid = Gross Revenue - Total Refunds (including tax)
           = 3,432,732.56 - 129,616.97
           = 3,303,115.59 SAR
```

### 2. Net Tax

```
Net Tax = Gross Tax - Refund Tax
        = 447,290.84 - 17,755.06
        = 429,535.78 SAR
```

### 3. Net Profit

```
Net Profit = Total Paid - Net Tax
           = 3,303,115.59 - 429,535.78
           = 2,873,579.81 SAR
```

### 4. Total AUM (ETF)

```
Total AUM = Seed Capital + Net Profit
          = 1,000,000.00 + 2,873,579.81
          = 3,873,579.81 SAR
```

---

## Tax Calculation

The ETF now correctly uses the **tax-inclusive formula** aligned with the dashboard:

```
Tax = Total × (1 - 1/1.15)
    = Total × 0.130434782...
    = Total × 15/115
```

This ensures consistent tax calculations across:

- Dashboard statistics
- ETF NAV calculations
- Refund processing
- ZATCA reporting

---

## NAV Performance (as of 2025-10-25)

```
📈 NAV PERFORMANCE
├─ Current NAV:    SAR 38.7358
├─ Starting NAV:   SAR 10.0620
├─ Total Growth:   284.97%
├─ Trading Days:   654
└─ Seed Shares:    100,000
```

**Calculation:**

```
NAV per Share = Total AUM ÷ Total Shares
              = 3,873,579.81 ÷ 100,000
              = SAR 38.7358
```

---

## Files Modified

1. `/apps/admin/app/Console/Commands/SyncEtfNavFromPlatformData.php`
   - Updated `getDailyDataWithSeparateRefunds()` method
   - Updated `calculateNavProgression()` method
   - Enhanced metadata and revenue record structure

2. `/apps/admin/app/Console/Commands/EtfStatus.php`
   - Updated detailed breakdown to read from metadata JSON
   - Added proper JSON extraction for refunds and taxes

---

## Next Steps

### 1. With Operating Expenses (Optional)

If you want to add a 0.5% operating expense ratio:

```bash
php artisan etf:sync-nav --fresh --expense-ratio=0.005
```

### 2. With Seed Capital Adjustment

To reflect the academy's actual seed capital:

```bash
php artisan etf:sync-nav --fresh --initial-aum=1000000 --initial-shares=100000
```

### 3. Production Sync

Run the sync command in production to update live data:

```bash
php artisan etf:sync-nav  # Without --fresh to append new data
```

---

## Accuracy Guarantee

✅ **100% Accurate** - The ETF system now:

- Uses the same refund table as dashboard
- Groups refunds by invoice creation date (not refund completion date)
- Calculates taxes using the same formula (1 - 1/1.15)
- Subtracts ALL refunds (partial + full) from gross revenue
- Accounts for refund tax credits properly
- Matches dashboard Net Profit to the cent: **SAR 2,873,579.81**

---

**Last Updated:** October 26, 2025  
**System Version:** ETF v2.0 (Invoice Refunds Migration)  
**Data Integrity:** ✅ Validated  
**Calculation Accuracy:** ✅ 100% Match
