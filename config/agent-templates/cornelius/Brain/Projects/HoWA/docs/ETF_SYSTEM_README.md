---
title: "Internal ETF (Investment Fund) System"
date: "2026-04-11"
tags: ["project/howa", "docs/howa"]
category: "docs/howa"
updated: "2026-07-15"
---

## Links

- [[Entities/Projects/HoWA]]

# Internal ETF (Investment Fund) System

## 📊 Overview

A complete NAV-based investment tracking system that allows you to manage an internal fund backed by your platform's daily revenue. Investors can buy shares based on the current NAV, and their holdings grow (or shrink) with the platform's performance.

---

## 🗃️ Database Structure

### Tables Created

1. **`etf_nav_history`** - Daily NAV values with OHLC data
   - `nav_per_share` - Net Asset Value per share
   - `total_aum` - Total Assets Under Management
   - `total_shares` - Total issued shares
   - `opening_nav`, `closing_nav`, `high_nav`, `low_nav` - Candlestick data
   - `daily_revenue`, `daily_expenses`, `net_daily_income`

2. **`etf_investors`** - Investor/shareholder records
   - `name`, `email`, `phone`
   - `total_shares`, `total_invested`, `current_value`
   - `total_return`, `return_percentage`
   - Tracks portfolio performance automatically

3. **`etf_share_transactions`** - Buy/sell/redeem transactions
   - `transaction_type` - buy, sell, redeem, dividend
   - `shares`, `nav_per_share`, `amount`
   - `fee`, `net_amount` - Transaction costs
   - Links to investors via foreign key

4. **`etf_daily_revenue`** - Platform revenue tracking
   - `gross_revenue`, `total_expenses`, `net_revenue`
   - `enrollment_revenue`, `service_revenue`
   - Breakdown by source (enrollments, services, etc.)

---

## 🎯 Core Concept

### How It Works

1. **Initial Setup:**
   - Start with initial NAV = SAR 10.00/share
   - AUM (Assets Under Management) = SAR 0
   - Total Shares = 0

2. **Investor Joins:**

   ```
   Investor deposits SAR 10,500
   Current NAV = 10.50/share
   → Receives 1,000 shares (10,500 / 10.50)
   New AUM = 10,500
   Total Shares = 1,000
   ```

3. **Daily Revenue Added:**

   ```
   Platform earns SAR 5,000 (net)
   Previous AUM = 10,500
   New AUM = 15,500
   NAV = 15,500 / 1,000 = SAR 15.50/share

   Investor's portfolio:
   - Shares: 1,000
   - Value: 1,000 × 15.50 = SAR 15,500
   - Return: +47.6%
   ```

4. **Investor Redeems:**

   ```
   Investor redeems 500 shares
   Current NAV = 15.50/share
   Amount = 500 × 15.50 = SAR 7,750
   Fee (1%) = 77.50
   Net payout = SAR 7,672.50
   ```

---

## 🚀 API Endpoints

### Dashboard & Data

- `GET /etf/dashboard` - Main ETF dashboard
- `GET /etf/nav-chart-data` - NAV history for charts
- `GET /etf/statistics` - Current ETF statistics

### NAV Management

- `POST /etf/process-daily-nav` - Calculate & store daily NAV

  ```json
  {
    "date": "2025-10-20",
    "revenue": 5000.0,
    "expenses": 1000.0
  }
  ```

### Transactions

- `POST /etf/buy-shares` - Investor purchases shares

  ```json
  {
    "investor_id": 1,
    "amount": 10000.0,
    "date": "2025-10-20"
  }
  ```

- `POST /etf/redeem-shares` - Investor redeems shares

  ```json
  {
    "investor_id": 1,
    "shares": 500,
    "date": "2025-10-20"
  }
  ```

### Portfolio

- `GET /etf/investor/{id}/portfolio` - View investor's holdings

---

## 💻 Frontend Components

### 1. ETF NAV Chart (`etf-nav-chart.tsx`)

Stock-like candlestick chart showing:

- Daily NAV with OHLC (Open, High, Low, Close)
- Volume indicators (transaction count)
- Multiple timeframes (7D, 30D, 90D, 1Y, All)
- Performance indicators
- Responsive and theme-aware

### 2. ETF Dashboard (`Pages/etf/dashboard.tsx`)

Complete dashboard with:

- Current NAV with change indicators
- Total AUM and share count
- Active investors count
- YTD and monthly returns
- Interactive NAV chart
- Top investors table
- Recent transactions feed

---

## 📝 Usage Examples

### 1. Initial Fund Setup

```php
// Create first investor
$investor = EtfInvestor::create([
    'name' => 'Founding Partner',
    'email' => 'partner@company.com',
    'investor_type' => 'partner',
    'total_shares' => 0,
]);

// Initialize NAV at 10.00
EtfNavHistory::create([
    'date' => today(),
    'nav_per_share' => 10.00,
    'total_aum' => 0,
    'total_shares' => 0,
]);
```

### 2. Daily NAV Calculation

```php
// Record daily revenue
EtfDailyRevenue::create([
    'date' => today(),
    'enrollment_revenue' => 15000.00,
    'service_revenue' => 8000.00,
    'operating_expenses' => 5000.00,
    'marketing_expenses' => 2000.00,
]);

// Process NAV
$controller = new EtfController();
$controller->processDailyNav(new Request([
    'date' => today(),
    'revenue' => 23000.00, // 15k + 8k
    'expenses' => 7000.00,  // 5k + 2k
]));
// → NAV automatically calculated and updated
```

### 3. Investor Transactions

```php
// Buy shares
EtfShareTransaction::processBuy(
    investorId: 1,
    amount: 50000.00,
    date: today()
);

// Redeem shares
EtfShareTransaction::processRedeem(
    investorId: 1,
    shares: 1000,
    date: today()
);
```

---

## 📈 Chart Data Format

The NAV chart expects data in this format:

```typescript
interface NavDataPoint {
  x: string; // Date: "2025-10-20"
  y: number; // NAV value: 10.5000
  open: number; // Opening NAV
  close: number; // Closing NAV
  high: number; // Highest NAV
  low: number; // Lowest NAV
  volume: number; // Transaction count
}
```

---

## ⚙️ Model Methods

### EtfNavHistory

```php
// Calculate NAV for a date
EtfNavHistory::calculateNAV('2025-10-20', 5000.00);

// Get chart data
EtfNavHistory::getChartData(
    startDate: '2025-01-01',
    endDate: '2025-12-31',
    interval: 'daily'
);
```

### EtfInvestor

```php
$investor->updateCurrentValue();        // Update portfolio value
$investor->getPortfolioSummary();       // Get performance metrics
$investor->transactions();              // Get all transactions
```

### EtfShareTransaction

```php
// Automatic calculations handle:
// - Share quantity based on NAV
// - Transaction fees (1%)
// - Investor balance updates
// - AUM adjustments
EtfShareTransaction::processBuy($investorId, $amount);
EtfShareTransaction::processRedeem($investorId, $shares);
```

---

## 🎨 UI Features

### Dashboard Stats Cards

- **Current NAV** - With daily change %
- **Total AUM** - With share count
- **Active Investors** - Portfolio holders
- **YTD Return** - Annual performance

### Interactive Chart

- Candlestick visualization
- Reference line at initial NAV (10.00)
- Volume bars
- Timeframe selection
- Hover tooltips with OHLC data

### Tables

- **Top Investors** - By portfolio value
- **Recent Transactions** - Latest activity

---

## 🔒 Legal Considerations

⚠️ **Important:** This is an **internal private system** for tracking profit-sharing among partners/investors.

**Cannot be used as:**

- Public ETF or mutual fund
- Regulated investment product
- Marketed to retail investors

**Suitable for:**

- Private equity-like structures
- Partner profit-sharing
- Internal company investment pools
- Tokenized revenue sharing (private)

**Compliance:**

- Requires proper legal structure
- May need CMA licensing in Saudi Arabia if public
- Consult legal/financial advisors before use

---

## 🚦 Next Steps

1. **Visit Dashboard:**

   ```
   http://your-domain.com/etf/dashboard
   ```

2. **Create Sample Data:**
   - Create investors
   - Initialize NAV
   - Record daily revenue
   - Process transactions

3. **Monitor Performance:**
   - Track NAV growth
   - View investor returns
   - Generate reports

4. **Integrate Revenue:**
   - Automate daily revenue recording
   - Link to enrollment/service payments
   - Calculate expenses

---

## 📊 Example Scenario

### Month 1: Fund Launch

```
Day 1: Initialize NAV at SAR 10.00
Day 2: Partner A invests SAR 100,000 → 10,000 shares
Day 3: Platform earns SAR 5,000 net → NAV = 10.50
Day 10: Partner B invests SAR 52,500 → 5,000 shares
Day 30: Total AUM = SAR 195,000, NAV = SAR 13.00
        Partner A: 10,000 shares = SAR 130,000 (+30% return)
        Partner B: 5,000 shares = SAR 65,000 (+23.8% return)
```

---

## 🛠️ Technical Stack

- **Backend:** Laravel 10+ (PHP 8.1+)
- **Frontend:** React + TypeScript + Inertia.js
- **UI:** HeroUI + TailwindCSS
- **Charts:** Recharts
- **Database:** MySQL/MariaDB

---

## 📞 Support

For questions or customizations, refer to:

- Laravel Documentation
- Recharts Documentation
- HeroUI Components

---

**Built with ❤️ for transparent, fair profit-sharing**
