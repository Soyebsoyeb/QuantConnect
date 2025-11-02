# 📈 GAP TRADING STRATEGY - INTRADAY MEAN REVERSION 📉

<div align="center">

## 🚀 **QUANTCONNECT ALGORITHM** 🚀

### *Intraday Gap Trading Strategy with Scheduled Exit*

![Trading Strategy](https://img.shields.io/badge/Strategy-Gap_Trading-blue)
![Python](https://img.shields.io/badge/Python-3.6%2B-green)
![Platform](https://img.shields.io/badge/Platform-QuantConnect-orange)
![Timeframe](https://img.shields.io/badge/Timeframe-Intraday-yellow)

</div>

---

## 📋 **TABLE OF CONTENTS** 📋

1. [🎯 Strategy Overview](#-strategy-overview)
2. [⚙️ Configuration Settings](#️-configuration-settings)
3. [🔧 Technical Implementation](#-technical-implementation)
4. [📊 Trading Logic](#-trading-logic)
5. [🕒 Schedule Management](#-schedule-management)
6. [🛠️ Installation & Usage](#️-installation--usage)
7. [⚡ Risk Management](#-risk-management)
8. [🎨 Customization Options](#-customization-options)

---

## 🎯 **STRATEGY OVERVIEW** 🎯

### 🔥 **CORE CONCEPT**
A **sophisticated intraday gap trading strategy** that capitalizes on overnight price gaps with mean reversion principles:

- 📊 **Overnight Gap Detection** (vs previous close)
- 🔄 **Mean Reversion Logic** (fade the gap)
- 🕒 **Scheduled Position Exit** (before market close)
- ⚡ **Minute-level Precision** entry timing

### 🎪 **TRADING LOGIC TABLE**

| Gap Type | Condition | Action | Strategy |
|----------|-----------|--------|----------|
| **GAP UP** 📈 | Open ≥ 1.01 × Previous Close | **SELL** 🔴 | Mean Reversion Short |
| **GAP DOWN** 📉 | Open ≤ 0.99 × Previous Close | **BUY** 🟢 | Mean Reversion Long |
| **NO GAP** ⚪️ | Within 1% range | **FLAT** | No Trade |

---

## ⚙️ **CONFIGURATION SETTINGS** ⚙️

### 📅 **BACKTEST PERIOD**
```python
self.SetStartDate(2018, 1, 1)   # 🗓️ Start Date
self.SetEndDate(2021, 1, 1)     # 🗓️ End Date (3-year period)
self.SetCash(100000)            # 💰 Initial Capital: $100,000
```
📊 TRADING INSTRUMENTS
```python
self.symbol = self.AddEquity("SPY", Resolution.Minute).Symbol
Primary Asset: SPY (S&P 500 ETF) 🏆
```
Resolution: Minute Data ⏱️

Market: US Equities 🇺🇸

🔧 TECHNICAL IMPLEMENTATION 🔧
📊 DATA MANAGEMENT
```python
self.rollingWindow = RollingWindow[TradeBar](2)
self.Consolidate(self.symbol, Resolution.Daily, self.CustomBarHandler)
```
🔄 ROLLING WINDOW FEATURES
✅ Maintains last 2 daily bars for gap calculation

✅ Automatic data consolidation from minute to daily

✅ Real-time bar updates via custom handler

✅ Efficient memory management

🕒 PRECISE TIMING CONTROL
```python
if not (self.Time.hour == 9 and self.Time.minute == 31):
 return
```
Entry Time: 9:31 AM EST ⏰

Reason: Capture opening price after initial volatility

Avoids: Pre-market and opening auction noise

📊 TRADING LOGIC 📊
🔴 SHORT ENTRY CONDITIONS (Gap Up)
```python
if data[self.symbol].Open >= 1.01 * self.rollingWindow[0].Close:
    self.SetHoldings(self.symbol, -1)  # 100% Short
```
Condition: 1% or higher gap up 📈

Logic: Expect mean reversion downward 📉

🟢 LONG ENTRY CONDITIONS (Gap Down)
```python
elif data[self.symbol].Open <= 0.99 * self.rollingWindow[0].Close:
    self.SetHoldings(self.symbol, 1)  # 100% Long
```
Condition: 1% or lower gap down 📉

Logic: Expect mean reversion upward 📈

🕒 SCHEDULE MANAGEMENT 🕒
🎯 AUTOMATED EXIT SYSTEM
```python
self.Schedule.On(self.DateRules.EveryDay(self.symbol),
                 self.TimeRules.BeforeMarketClose(self.symbol, 15),      
                 self.ExitPositions)
```
⏰ EXIT TIMING
When: Every trading day 📅

Time: 15 minutes before market close 🕒

Action: Liquidate all positions 💰

Purpose: Avoid overnight risk 🌙

🔄 DAILY WORKFLOW
9:31 AM - Check for gaps and enter trades ⏰

Intraday - Hold position through day 📊

3:45 PM - Exit all positions before close 🏁

Overnight - Flat position, no risk 🌙

