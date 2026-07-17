---
title: "Chart Data with Refunds, Taxes & Subtotals"
date: "2026-04-11"
tags: ["project/howa", "docs/howa"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Chart Data with Refunds, Taxes & Subtotals

## ✅ **Chart Data Structure - Updated**

### What Frontend Receives

Each data point in the chart now includes:

```typescript
interface ChartDataPoint {
  x: string; // Date/period (e.g., "2025-10-23", "2025-W43", "2025-10", "2025-Q4", "2025")
  y: number; // NET sales (after refunds) - THIS IS WHAT DISPLAYS
  total_txns: number; // Number of transactions
  type: "combined"; // Data type

  // NEW: Additional metrics for display
  total_refunds: number; // Total refunds for this period
  taxes: number; // Total taxes for this period
  subtotal: number; // Subtotal (excluding tax) for this period

  metadata: {
    avg_per_transaction: number;
    date: string;
    gross_amount: number; // Original amount before refunds
    refund_amount: number; // Refunds for this period
    enrollment_count: number;
    service_count: number;
    enrollment_amount: number;
    service_amount: number;
  };
}
```

---

## 📊 **Example Data**

### Daily Data Point

```javascript
{
  x: "2025-10-23",
  y: 12450.50,                  // NET sales (displayed in chart)
  total_txns: 15,
  type: "combined",
  total_refunds: 549.50,        // ← Show under "Total Sales"
  taxes: 1626.59,               // ← Show under "Total Sales"
  subtotal: 10823.91,           // ← Show under "Total Sales"
  metadata: {
    avg_per_transaction: 830.03,
    date: "2025-10-23",
    gross_amount: 13000,        // Before refunds
    refund_amount: 549.50,
    enrollment_count: 12,
    service_count: 3,
    enrollment_amount: 9800,
    service_amount: 3200
  }
}
```

### Weekly Data Point

```javascript
{
  x: "2025-W43",
  y: 65234.25,                  // NET sales
  total_txns: 78,
  type: "combined",
  total_refunds: 2765.75,       // ← Total refunds this week
  taxes: 8508.48,               // ← Total taxes this week
  subtotal: 56725.77,           // ← Total subtotal this week
  metadata: {
    gross_amount: 68000,
    refund_amount: 2765.75,
    // ...
  }
}
```

---

## 🎨 **How to Display in Frontend**

### Chart Tooltip (Updated)

```typescript
// In chart.tsx CustomTooltip component

const CustomTooltip = ({ active, payload, currency = "SAR" }: any) => {
  if (!active || !payload || !payload[0]) return null;

  const data = payload[0].payload;

  return (
    <div className="bg-white dark:bg-zinc-900 p-4 rounded-lg shadow-lg border">
      {/* Period/Date */}
      <p className="font-semibold mb-2">{data.x}</p>

      {/* Main Value - NET Sales */}
      <div className="mb-3">
        <span className="text-sm text-zinc-500">Total Sales (NET):</span>
        <p className="text-lg font-bold">
          {formatCurrency(data.y, currency)}
        </p>
      </div>

      {/* Breakdown - NEW */}
      <div className="space-y-1 text-sm border-t pt-2">
        <div className="flex justify-between">
          <span className="text-zinc-600 dark:text-zinc-400">Subtotal:</span>
          <span className="font-medium">{formatCurrency(data.subtotal, currency)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-zinc-600 dark:text-zinc-400">Taxes (15%):</span>
          <span className="font-medium">{formatCurrency(data.taxes, currency)}</span>
        </div>
        {data.total_refunds > 0 && (
          <div className="flex justify-between text-red-600 dark:text-red-400">
            <span>Refunds:</span>
            <span className="font-medium">-{formatCurrency(data.total_refunds, currency)}</span>
          </div>
        )}
        {data.metadata.gross_amount > data.y && (
          <div className="flex justify-between text-xs text-zinc-500 pt-1 border-t">
            <span>Gross:</span>
            <span>{formatCurrency(data.metadata.gross_amount, currency)}</span>
          </div>
        )}
      </div>

      {/* Transactions */}
      <div className="mt-2 pt-2 border-t text-xs text-zinc-500">
        {data.total_txns} transaction{data.total_txns !== 1 ? 's' : ''}
      </div>
    </div>
  );
};
```

### Chart Legend/Summary

```typescript
// Under the chart
<div className="mt-4 grid grid-cols-3 gap-4 text-sm">
  <div>
    <p className="text-zinc-500">Subtotal</p>
    <p className="font-semibold">
      {formatCurrency(
        chartData.reduce((sum, d) => sum + d.subtotal, 0),
        'SAR'
      )}
    </p>
  </div>

  <div>
    <p className="text-zinc-500">Taxes</p>
    <p className="font-semibold">
      {formatCurrency(
        chartData.reduce((sum, d) => sum + d.taxes, 0),
        'SAR'
      )}
    </p>
  </div>

  <div>
    <p className="text-zinc-500 text-red-600">Refunds</p>
    <p className="font-semibold text-red-600">
      -{formatCurrency(
        chartData.reduce((sum, d) => sum + d.total_refunds, 0),
        'SAR'
      )}
    </p>
  </div>
</div>
```

---

## 📈 **Chart Display Options**

### Option 1: Stacked Info Under Value (Recommended)

```typescript
<div className="text-center">
  {/* Main value */}
  <h2 className="text-3xl font-bold">{formatCurrency(data.y)}</h2>
  <p className="text-sm text-zinc-500">Total Sales (NET)</p>

  {/* Breakdown in smaller font */}
  <div className="mt-2 space-y-0.5 text-xs text-zinc-500">
    <p>Subtotal: {formatCurrency(data.subtotal)}</p>
    <p>Taxes: {formatCurrency(data.taxes)}</p>
    {data.total_refunds > 0 && (
      <p className="text-red-600">Refunds: -{formatCurrency(data.total_refunds)}</p>
    )}
  </div>
</div>
```

### Option 2: Inline With Icons

```typescript
<div className="flex items-baseline gap-2">
  {/* Main value */}
  <h2 className="text-3xl font-bold">{formatCurrency(data.y)}</h2>

  {/* Breakdown inline */}
  <div className="flex gap-3 text-xs text-zinc-500">
    <span title="Subtotal">S: {formatCurrency(data.subtotal, 'SAR', true)}</span>
    <span title="Taxes">T: {formatCurrency(data.taxes, 'SAR', true)}</span>
    {data.total_refunds > 0 && (
      <span className="text-red-600" title="Refunds">
        R: -{formatCurrency(data.total_refunds, 'SAR', true)}
      </span>
    )}
  </div>
</div>
```

### Option 3: Compact Grid

```typescript
<div className="space-y-1">
  <h2 className="text-2xl font-bold">{formatCurrency(data.y)}</h2>
  <div className="grid grid-cols-3 gap-2 text-xs">
    <div>
      <p className="text-zinc-400">Subtotal</p>
      <p className="font-medium">{formatCurrency(data.subtotal, 'SAR', true)}</p>
    </div>
    <div>
      <p className="text-zinc-400">Taxes</p>
      <p className="font-medium">{formatCurrency(data.taxes, 'SAR', true)}</p>
    </div>
    {data.total_refunds > 0 && (
      <div>
        <p className="text-red-400">Refunds</p>
        <p className="font-medium text-red-600">-{formatCurrency(data.total_refunds, 'SAR', true)}</p>
      </div>
    )}
  </div>
</div>
```

---

## 🔍 **How It Works**

### Backend Calculation

```php
// For each data point in chart
foreach ($dates as $date) {
    // 1. Get gross sales
    $grossSales = Invoices::forDate($date)->sum('paid'); // e.g., SAR 13,000

    // 2. Get refunds for this date
    $refunds = InvoiceRefund::completedOn($date)->sum('net_refund'); // e.g., SAR 549.50

    // 3. Calculate breakdown
    $subtotal = $grossSales / 1.15;   // SAR 11,304.35
    $taxes = $grossSales - $subtotal; // SAR 1,695.65

    // 4. Calculate NET
    $netSales = $grossSales - $refunds; // SAR 12,450.50

    // 5. Return data point
    return [
        'x' => $date,
        'y' => $netSales,           // ← Main chart line shows NET
        'total_refunds' => $refunds, // ← Display under value
        'taxes' => $taxes,           // ← Display under value
        'subtotal' => $subtotal,     // ← Display under value
    ];
}
```

### Frontend Display

```
Chart shows: SAR 12,450.50 (NET)
             ↓
Under value shows:
  Subtotal: SAR 11,304.35
  Taxes: SAR 1,695.65
  Refunds: -SAR 549.50
```

---

## 📊 **Data Flow**

```
Database
├─ Invoices (status='paid'):        SAR 13,000
├─ InvoiceRefunds (completed):      SAR 549.50
└─ Calculation:                     SAR 13,000 - SAR 549.50 = SAR 12,450.50

Backend Processing
├─ Gross: SAR 13,000
├─ Subtotal: SAR 11,304.35 (gross / 1.15)
├─ Taxes: SAR 1,695.65 (gross - subtotal)
├─ Refunds: SAR 549.50
└─ NET: SAR 12,450.50 (gross - refunds)

Frontend Display
├─ Chart Line: SAR 12,450.50 (NET) ← Main value
└─ Under value:
    ├─ Subtotal: SAR 11,304.35
    ├─ Taxes: SAR 1,695.65
    └─ Refunds: -SAR 549.50
```

---

## 🎯 **Available in All Intervals**

### Daily Chart

```javascript
aggregatedChartData.daily.map((point) => ({
  date: point.x, // "2025-10-23"
  netSales: point.y, // NET (what's displayed)
  subtotal: point.subtotal, // ← NEW
  taxes: point.taxes, // ← NEW
  refunds: point.total_refunds, // ← NEW
}));
```

### Weekly Chart

```javascript
aggregatedChartData.weekly.map((point) => ({
  week: point.x, // "2025-W43"
  netSales: point.y,
  subtotal: point.subtotal, // ← NEW
  taxes: point.taxes, // ← NEW
  refunds: point.total_refunds, // ← NEW
}));
```

### Monthly, Quarterly, Yearly - Same Structure

All intervals have the same structure with `subtotal`, `taxes`, and `total_refunds`.

---

## 💡 **Usage Example**

### In chart.tsx

```typescript
// Update the chart component to show breakdown
export function Chart({ data, interval, currency = "SAR" }: ChartProps) {
  return (
    <div>
      {/* Existing chart */}
      <ResponsiveContainer>
        <LineChart data={data}>
          {/* ... existing chart config */}
        </LineChart>
      </ResponsiveContainer>

      {/* NEW: Show breakdown under chart */}
      <div className="mt-4 p-4 bg-zinc-50 dark:bg-zinc-900 rounded-lg">
        <div className="grid grid-cols-4 gap-4 text-sm">
          <div>
            <p className="text-zinc-500">Total Sales (NET)</p>
            <p className="text-xl font-bold">
              {formatCurrency(data.reduce((sum, d) => sum + d.y, 0), currency)}
            </p>
          </div>

          <div>
            <p className="text-zinc-500">Subtotal</p>
            <p className="text-lg font-semibold">
              {formatCurrency(data.reduce((sum, d) => sum + d.subtotal, 0), currency)}
            </p>
          </div>

          <div>
            <p className="text-zinc-500">Taxes</p>
            <p className="text-lg font-semibold">
              {formatCurrency(data.reduce((sum, d) => sum + d.taxes, 0), currency)}
            </p>
          </div>

          <div>
            <p className="text-zinc-500 text-red-600">Refunds</p>
            <p className="text-lg font-semibold text-red-600">
              -{formatCurrency(data.reduce((sum, d) => sum + d.total_refunds, 0), currency)}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
```

### In Tooltip

```typescript
<CustomTooltip>
  {/* Main Value */}
  <p className="text-lg font-bold">{formatCurrency(data.y)}</p>
  <p className="text-xs text-zinc-500">Total Sales (NET)</p>

  {/* Breakdown - smaller font */}
  <div className="mt-2 pt-2 border-t space-y-1 text-xs">
    <div className="flex justify-between">
      <span className="text-zinc-500">Subtotal:</span>
      <span className="font-medium">{formatCurrency(data.subtotal)}</span>
    </div>
    <div className="flex justify-between">
      <span className="text-zinc-500">Taxes:</span>
      <span className="font-medium">{formatCurrency(data.taxes)}</span>
    </div>
    {data.total_refunds > 0 && (
      <div className="flex justify-between text-red-600">
        <span>Refunds:</span>
        <span className="font-medium">-{formatCurrency(data.total_refunds)}</span>
      </div>
    )}
  </div>
</CustomTooltip>
```

---

## 📊 **Calculation Details**

### For Each Period

```php
// 1. Get gross revenue
$grossRevenue = $items->sum('y'); // e.g., SAR 13,000

// 2. Get refunds for this period
$refunds = $refundsByDate[$date] ?? 0; // e.g., SAR 549.50

// 3. Calculate breakdown
$subtotal = $grossRevenue / 1.15;        // SAR 11,304.35
$taxes = $grossRevenue - $subtotal;      // SAR 1,695.65

// 4. Calculate NET
$netSales = $grossRevenue - $refunds;    // SAR 12,450.50

// 5. Return to frontend
[
    'y' => $netSales,           // ← Chart displays this
    'total_refunds' => $refunds, // ← Show in breakdown
    'taxes' => $taxes,           // ← Show in breakdown
    'subtotal' => $subtotal,     // ← Show in breakdown
]
```

---

## 🎯 **Visual Example**

### Chart Display

```
Total Sales Chart
┌──────────────────────────────────────┐
│                                      │
│         ╱╲                          │
│        ╱  ╲      ╱╲                 │
│   ╱╲  ╱    ╲    ╱  ╲                │
│  ╱  ╲╱      ╲  ╱    ╲               │
│ ╱            ╲╱      ╲              │
└──────────────────────────────────────┘
  Mon   Tue   Wed   Thu   Fri

Hover on "Wed" shows:
┌─────────────────────────┐
│ Wednesday, Oct 23       │
│                         │
│ Total Sales (NET)       │
│ SAR 12,450.50          │
│                         │
│ ─────────────────────── │
│ Subtotal:  SAR 10,823.91│
│ Taxes:     SAR  1,626.59│
│ Refunds:  -SAR    549.50│ ← Red
│ ─────────────────────── │
│ Gross:     SAR 13,000.00│
│                         │
│ 15 transactions         │
└─────────────────────────┘
```

---

## ✅ **What's Available**

### For Every Data Point

```typescript
point.y; // NET sales (after refunds) - MAIN VALUE
point.total_refunds; // Refunds for this period
point.taxes; // Taxes for this period
point.subtotal; // Subtotal for this period
point.metadata.gross_amount; // Original gross (before refunds)
```

### Aggregate Totals

```typescript
// Calculate totals for entire period
const totalSubtotal = chartData.reduce((sum, d) => sum + d.subtotal, 0);
const totalTaxes = chartData.reduce((sum, d) => sum + d.taxes, 0);
const totalRefunds = chartData.reduce((sum, d) => sum + d.total_refunds, 0);
const totalNet = chartData.reduce((sum, d) => sum + d.y, 0);
const totalGross = chartData.reduce(
  (sum, d) => sum + d.metadata.gross_amount,
  0,
);
```

---

## 🎨 **UI Recommendations**

### Color Scheme

- **NET Sales**: Primary color (blue/green)
- **Subtotal**: Neutral (zinc-600)
- **Taxes**: Neutral (zinc-600)
- **Refunds**: Red/Danger (red-600)
- **Gross**: Muted (zinc-400)

### Font Sizes

- **NET Sales**: Large (text-2xl or text-3xl)
- **Breakdown**: Small (text-xs or text-sm)
- **Labels**: Extra small (text-xs text-zinc-500)

### Visual Hierarchy

```
Total Sales: SAR 12,450.50  ← Large, bold
  Subtotal: SAR 10,823.91   ← Small, normal weight
  Taxes: SAR 1,626.59       ← Small, normal weight
  Refunds: -SAR 549.50      ← Small, red color
```

---

## ✅ **Testing**

### Verify Chart Data

```bash
php artisan tinker

# Get chart data
>>> $controller = new App\Http\Controllers\HomeController();
>>> $stats = $controller->getStats(request());
>>> $dailyData = $stats['aggregatedChartData']['daily'];

# Check first data point
>>> $dailyData[0]
=> [
  "x" => "2025-10-23",
  "y" => 12450.5,              // NET
  "total_refunds" => 549.5,    // ✅ Available
  "taxes" => 1626.59,          // ✅ Available
  "subtotal" => 10823.91,      // ✅ Available
  "metadata" => [
    "gross_amount" => 13000,   // ✅ Available
    // ...
  ]
]
```

---

## 🎯 **Summary**

### ✅ **What We Added**

**To every chart data point:**

1. ✅ `total_refunds` - Refunds for this period
2. ✅ `taxes` - Taxes for this period
3. ✅ `subtotal` - Subtotal for this period
4. ✅ `metadata.gross_amount` - Original amount

**Available in all intervals:**

- ✅ Daily
- ✅ Weekly
- ✅ Monthly
- ✅ Quarterly
- ✅ Yearly

### 🎨 **Frontend Usage**

```typescript
// Simple access
data.total_refunds; // Show under "Total Sales"
data.taxes; // Show under "Total Sales"
data.subtotal; // Show under "Total Sales"

// Display in smaller font, stacked vertically
```

**Ready to update the chart component!** 📊
