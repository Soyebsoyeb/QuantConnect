# 📈 BREAKOUT TRADING STRATEGY WITH MOVING AVERAGE & 52-WEEK FILTERS 📉

<div align="center">

## 🚀 **QUANTCONNECT ALGORITHM** 🚀

### *Advanced Breakout Detection System with Custom Indicators*

![Trading Strategy](https://img.shields.io/badge/Strategy-Breakout_Trading-blue)
![Python](https://img.shields.io/badge/Python-3.6%2B-green)
![Platform](https://img.shields.io/badge/Platform-QuantConnect-orange)

</div>

---

## 📋 **TABLE OF CONTENTS** 📋

1. [🎯 Strategy Overview](#-strategy-overview)
2. [⚙️ Configuration Settings](#️-configuration-settings)
3. [🔧 Technical Implementation](#-technical-implementation)
4. [📊 Trading Logic](#-trading-logic)
5. [🛠️ Installation & Usage](#️-installation--usage)
6. [📈 Performance Monitoring](#-performance-monitoring)
7. [⚡ Risk Management](#-risk-management)
8. [🎨 Customization Options](#-customization-options)

---

## 🎯 **STRATEGY OVERVIEW** 🎯

### 🔥 **CORE CONCEPT**
A **sophisticated breakout trading algorithm** that combines trend-following and momentum strategies using multiple technical indicators:

- 🎯 **Custom 30-day Simple Moving Average (SMA)**
- 📅 **52-week high/low breakout filters**
- 📊 **Price momentum confirmation**
- ⚡ **Real-time position management**

### 🎪 **TRADING LOGIC TABLE**

| Position | Conditions | Signal Strength |
|----------|------------|-----------------|
| **LONG** 🟢 | Price ≥ 95% of 52-week high **AND** Price > SMA | 🚀 STRONG BULLISH |
| **SHORT** 🔴 | Price ≤ 105% of 52-week low **AND** Price < SMA | 📉 STRONG BEARISH |
| **FLAT** ⚪️ | Conditions not met - Exit positions | 🛑 NEUTRAL |

---

## ⚙️ **CONFIGURATION SETTINGS** ⚙️

### 📅 **BACKTEST PERIOD**
```python
self.SetStartDate(2020, 1, 1)   # 🗓️ Start Date
self.SetEndDate(2021, 1, 1)     # 🗓️ End Date
self.SetCash(100000)            # 💰 Initial Capital: $100,000
```
📊 TRADING INSTRUMENTS
```python
self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
Primary Asset: SPY (S&P 500 ETF) 🏆
```
Resolution: Daily 📈

Market: US Equities 🇺🇸

🔧 TECHNICAL IMPLEMENTATION 🔧
📉 CUSTOM SMA INDICATOR
```python
class CustomSimpleMovingAverage(PythonIndicator):
    def __init__(self, name, period):
        self.Name = name
        self.Value = 0
        self.period = period
        self.queue = deque(maxlen=period)
```
🔄 INDICATOR FEATURES
✅ Sliding window buffer using deque

✅ Real-time updates with each new bar

✅ Automatic ready state detection

✅ Efficient memory usage

📈 BREAKOUT FILTERS
52-Week High Calculation: hist["high"].max()

52-Week Low Calculation: hist["low"].min()

Historical Data: 365 days of daily prices

📊 TRADING LOGIC 📊
🟢 LONG ENTRY CONDITIONS
```python
if price >= 0.95 * high and price > self.sma.Current.Value:
    self.SetHoldings(self.spy, 1)  # 100% Long
```
🔴 SHORT ENTRY CONDITIONS
```python
elif price <= 1.05 * low and price < self.sma.Current.Value:
    self.SetHoldings(self.spy, -1)  # 100% Short
```
⚪️ EXIT CONDITIONS
python
else:
    self.Liquidate()  # Close all position
