---
title: "Tax Calculation Guide - Saudi VAT (Tax-Inclusive Pricing)"
date: "2026-04-11"
tags: ["project/howa", "docs/howa"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Tax Calculation Guide - Saudi VAT (Tax-Inclusive Pricing)

## Overview

In Saudi Arabia, VAT is 15% and prices are typically displayed as **tax-inclusive**. This means the displayed price already includes the tax.

## The Correct Formula

### ✅ CORRECT: Tax-Inclusive Pricing

When you have a **total price (tax-inclusive)** and need to extract the tax:

```php
// Given: Total = 1150 SAR (tax-inclusive)
Subtotal = Total / 1.15 = 1150 / 1.15 = 1000 SAR
Tax = Total - Subtotal = 1150 - 1000 = 150 SAR

// Or directly:
Tax = Total × (1 - 1/1.15) = Total × (0.15/1.15) = 1150 × 0.130434... = 150 SAR
```

### ❌ INCORRECT: Tax-Exclusive Formula

```php
// This is WRONG for tax-inclusive pricing:
Tax = Total × 0.15 = 1150 × 0.15 = 172.50 SAR ❌
```

## Mathematical Proof

If the subtotal is 1000 SAR and tax rate is 15%:

- **Tax**: 1000 × 0.15 = 150 SAR
- **Total**: 1000 + 150 = 1150 SAR

Now, to extract tax from the total (reverse calculation):

- **Tax**: 1150 × (0.15 / 1.15) = 1150 × 0.130434... = 150 SAR ✅
- **NOT**: 1150 × 0.15 = 172.50 SAR ❌

## Implementation Across the App

### 1. When Calculating FROM Subtotal (Tax-Exclusive Base)

```php
// You have: Subtotal (excl. tax)
// You need: Tax amount

$tax = $subtotal * 0.15;
$total = $subtotal + $tax;
```

**Example**: `GenerateInvoiceController::calculateTax()` receives a subtotal and returns tax.

### 2. When Calculating FROM Total (Tax-Inclusive)

```php
// You have: Total (incl. tax)
// You need: Subtotal and Tax

$subtotal = $total / 1.15;
$tax = $total - $subtotal;
// Or: $tax = $total * (0.15 / 1.15);
```

**Example**: `RefundService::calculateRefundBreakdown()` receives a total refund amount and extracts subtotal and tax.

### 3. When Displaying to Users

```php
// Always show tax-inclusive total as the main price
$displayPrice = $subtotal * 1.15; // Total including tax

// Breakdown (optional):
echo "Subtotal (excl. VAT): " . $subtotal . " SAR\n";
echo "VAT (15%): " . ($subtotal * 0.15) . " SAR\n";
echo "Total (incl. VAT): " . $displayPrice . " SAR\n";
```

## Files That Are Correctly Implemented

✅ **`app/Services/RefundService.php`**

```php
$taxRate = $invoice->tax / $invoice->subtotal;
$taxDivisor = 1 + $taxRate; // e.g., 1.15
$refundSubtotal = $refundAmount / $taxDivisor;
$taxRefund = $refundAmount - $refundSubtotal;
```

✅ **`app/Http/Controllers/Invoices/GenerateInvoiceController.php`**

```php
// Extracts subtotal from tax-inclusive total
$subtotal = $discountedAmount / 1.15;
// Then calculates tax from subtotal
$tax = $subtotal * 0.15;
```

## Common Scenarios

### Scenario 1: User Pays 1150 SAR (Tax-Inclusive)

```php
$totalPaid = 1150; // What user paid (tax-inclusive)
$subtotal = $totalPaid / 1.15; // 1000 SAR
$tax = $subtotal * 0.15; // 150 SAR
```

### Scenario 2: Partial Refund of 460 SAR

```php
$refundTotal = 460; // Total to refund (tax-inclusive)
$refundSubtotal = $refundTotal / 1.15; // 400 SAR
$refundTax = $refundSubtotal * 0.15; // 60 SAR
```

### Scenario 3: Invoice Creation from Base Price

```php
$basePrice = 1000; // Subtotal (tax-exclusive)
$tax = $basePrice * 0.15; // 150 SAR
$total = $basePrice + $tax; // 1150 SAR (tax-inclusive)
```

## ZATCA Compliance

For ZATCA (Saudi Tax Authority) reporting:

- **Invoice Total**: Always tax-inclusive
- **Subtotal (TaxExclusiveAmount)**: Calculated as `Total / 1.15`
- **Tax Amount (TaxAmount)**: Calculated as `Subtotal × 0.15`
- **Line Items**: Also use subtotal × 0.15 for tax

## Testing

The formula is validated in `InvoiceRefundCalculationsTest.php`:

```php
// Test both directions
$expectedTax = $invoice->subtotal * 0.15; // From subtotal
$expectedTaxFromTotal = $invoice->total * (0.15 / 1.15); // From total
```

Both should give the same result: **150 SAR**

## Quick Reference

| Given           | Formula                    | Result          |
| --------------- | -------------------------- | --------------- |
| Subtotal = 1000 | Tax = Subtotal × 0.15      | Tax = 150       |
| Subtotal = 1000 | Total = Subtotal × 1.15    | Total = 1150    |
| Total = 1150    | Subtotal = Total / 1.15    | Subtotal = 1000 |
| Total = 1150    | Tax = Total × (0.15/1.15)  | Tax = 150       |
| Total = 1150    | Tax = Total - (Total/1.15) | Tax = 150       |

## Constants

```php
const TAX_RATE = 0.15; // 15%
const TAX_MULTIPLIER = 1.15; // 1 + TAX_RATE
const TAX_DIVISOR = 1.15; // For extracting subtotal from total
const TAX_EXTRACTION_RATE = 0.130434782608696; // 0.15 / 1.15
```

## Summary

- **Tax-Inclusive**: `Tax = Total × (0.15 / 1.15)` ✅
- **Tax-Exclusive**: `Tax = Subtotal × 0.15` ✅
- **NOT**: `Tax = Total × 0.15` ❌

Always identify whether you're working with:

1. **Subtotal** (tax-exclusive base) → Multiply by 0.15
2. **Total** (tax-inclusive) → Multiply by (0.15 / 1.15) or divide by 1.15 first

This ensures accurate tax calculations for ZATCA compliance and correct financial reporting.
