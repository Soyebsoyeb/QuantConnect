# TREND-FOLLOWING ASSET ALLOCATION STRATEGY

<div align="center">

## SYSTEMATIC EQUITY-BOND ROTATION ALGORITHM

### Dynamic Portfolio Allocation Based on Moving Average Trends

![Trading Strategy](https://img.shields.io/badge/Strategy-Trend_Following-blue)
![Python](https://img.shields.io/badge/Python-3.6%2B-green)
![Platform](https://img.shields.io/badge/Platform-QuantConnect-orange)
![Assets](https://img.shields.io/badge/Assets-Equity__Bond-yellow)
![Rebalance](https://img.shields.io/badge/Rebalance-Monthly-purple)

</div>

---

## TABLE OF CONTENTS

1. [Strategy Overview](#strategy-overview)
2. [Configuration Settings](#configuration-settings)
3. [Technical Implementation](#technical-implementation)
4. [Trading Logic](#trading-logic)
5. [Portfolio Management](#portfolio-management)
6. [Installation & Usage](#installation--usage)
7. [Risk Management](#risk-management)
8. [Customization Options](#customization-options)

---

## STRATEGY OVERVIEW

### CORE CONCEPT
A **systematic trend-following algorithm** that dynamically allocates capital between equities (SPY) and bonds (BND) based on Simple Moving Average signals:

- 📊 **Technical Trend Identification** using SMA
- ⚖️ **Dynamic Asset Allocation** between risk-on and risk-off assets
- 📅 **Systematic Rebalancing** with time-based controls
- 🛡️ **Risk-Managed Exposure** during market downturns

### TRADING LOGIC TABLE

| Market Condition | SPY Allocation | BND Allocation | Signal Trigger |
|------------------|----------------|----------------|----------------|
| **Uptrend** 📈 | 80% | 20% | SPY Price ≥ 30-day SMA |
| **Downtrend** 📉 | 20% | 80% | SPY Price < 30-day SMA |
| **Neutral** ⚪️ | Current Allocation | Current Allocation | Within 30-day lockout |

---

## CONFIGURATION SETTINGS

### BACKTEST PERIOD
```python
self.SetStartDate(2018, 1, 1)   # Start Date
self.SetEndDate(2021, 1, 1)     # End Date (3-year period)
self.SetCash(100000)            # Initial Capital: $100,000
```
TRADING INSTRUMENTS
```python
self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
self.bnd = self.AddEquity("BND", Resolution.Daily).Symbol
```
Primary Equity: SPY (S&P 500 ETF)

Primary Bond: BND (Total Bond Market ETF)

Resolution: Daily Data

PARAMETER CONFIGURATION
```python
length = self.GetParameter("sma_length")
length = 30 if length is None else int(length)
self.sma = self.SMA(self.spy, length, Resolution.Daily)
```
SMA Period: Configurable via parameter (default: 30 days)

Flexible Setup: Easy parameter optimization without code changes

TECHNICAL IMPLEMENTATION
MOVING AVERAGE SETUP
```python
self.sma = self.SMA(self.spy, length, Resolution.Daily)
```
STATE MANAGEMENT VARIABLES
```python
self.rebalanceTime = datetime.min   # Next allowed rebalance timestamp
self.uptrend = True                 # Current market regime flag
```
DATA VALIDATION
```python
if not self.sma.IsReady or self.spy not in data or self.bnd not in data:
    return
```
Ensures indicator readiness before trading

Validates data availability for both assets

Prevents execution on incomplete information

TRADING LOGIC
TREND IDENTIFICATION
```python
price = data[self.spy].Price
sma_value = self.sma.Current.Value

# Uptrend condition
if price >= sma_value:
    # Execute if rebalance time reached OR trend changed
    if self.Time >= self.rebalanceTime or not self.uptrend:
        self.SetHoldings(self.spy, 0.8)
        self.SetHoldings(self.bnd, 0.2)
        self.uptrend = True
        self.rebalanceTime = self.Time + timedelta(30)

# Downtrend condition
elif self.Time >= self.rebalanceTime or self.uptrend:
    self.SetHoldings(self.spy, 0.2)
    self.SetHoldings(self.bnd, 0.8)
    self.uptrend = False
    self.rebalanceTime = self.Time + timedelta(30)
```
REBALANCE TRIGGERS
Trend Reversal: Market regime change (uptrend ↔ downtrend)

Time-Based: 30-day minimum period elapsed

Combined Logic: Prevents whipsaw while ensuring timely adjustments

PORTFOLIO MANAGEMENT
ASSET ALLOCATION STRATEGY
Growth Phase (Uptrend): 80% equities, 20% bonds

Defensive Phase (Downtrend): 20% equities, 80% bonds

Systematic Approach: Rules-based allocation removes emotion

REBALANCE DISCIPLINE
30-Day Minimum: Prevents overtrading and reduces costs

Trend-Based: Aligns allocation with market conditions

Forced Execution: Ensures adherence to strategy rules

VISUALIZATION
```python
self.Plot("Benchmark", "SMA", sma_value)
```
Tracks SMA values for performance monitoring

Provides visual reference for trend identification

INSTALLATION & USAGE
QUICK START GUIDE

python
# Copy the entire algorithm code
PASTE INTO QUANTCONNECT

Navigate to QuantConnect Algorithm Lab

Create new algorithm

Paste the code

CONFIGURE PARAMETERS

```python
# Adjust SMA period via parameters
sma_length = 50  # Test different periods

# Modify allocation ratios if desired
self.SetHoldings(self.spy, 0.9)  # More aggressive equity allocation
self.SetHoldings(self.bnd, 0.1)
```
RUN BACKTEST

Execute backtest for 2018-2021 period

Analyze performance across different market regimes

Optimize SMA period parameter

REQUIREMENTS
QuantConnect Account

Python 3.6+

Basic understanding of trend-following strategies

RISK MANAGEMENT
BUILT-IN PROTECTIONS
Automatic Risk Reduction: Increased bond allocation during downtrends

Rebalance Frequency Control: 30-day minimum prevents overtrading

Systematic Execution: Eliminates emotional decision-making

Diversified Exposure: Balanced equity-bond allocation

RISK CONSIDERATIONS
Lagging Indicator: SMA may signal trend changes late

Whipsaw Risk: Potential for frequent trades in sideways markets

Interest Rate Sensitivity: Bond allocation carries rate risk

Market Regime Changes: Strategy effectiveness varies across environments

POSITION MANAGEMENT
Maximum Equity: 80% allocation during uptrends

Minimum Equity: 20% allocation during downtrends

Holding Period: Variable based on trend persistence

Rebalance Frequency: Minimum 30-day intervals

