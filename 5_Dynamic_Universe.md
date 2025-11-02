# 📊 SMALL-CAP MOMENTUM STRATEGY - UNIVERSE SELECTION 📈

<div align="center">

## 🚀 **QUANTCONNECT ALGORITHM** 🚀

### *Monthly Rebalanced Small-Cap Momentum Portfolio*

![Trading Strategy](https://img.shields.io/badge/Strategy-SmallCap_Momentum-blue)
![Python](https://img.shields.io/badge/Python-3.6%2B-green)
![Platform](https://img.shields.io/badge/Platform-QuantConnect-orange)
![Rebalance](https://img.shields.io/badge/Rebalance-Monthly-yellow)

</div>

---

## 📋 **TABLE OF CONTENTS** 📋

1. [🎯 Strategy Overview](#-strategy-overview)
2. [⚙️ Configuration Settings](#️-configuration-settings)
3. [🔧 Universe Selection Process](#-universe-selection-process)
4. [📊 Portfolio Construction](#-portfolio-construction)
5. [🔄 Rebalancing Logic](#-rebalancing-logic)
6. [🛠️ Installation & Usage](#️-installation--usage)
7. [⚡ Risk Management](#-risk-management)
8. [🎨 Customization Options](#-customization-options)

---

## 🎯 **STRATEGY OVERVIEW** 🎯

### 🔥 **CORE CONCEPT**
A **sophisticated small-cap momentum strategy** that uses a two-stage filtering process to identify promising small-cap stocks with high liquidity:

- 📊 **Two-Stage Universe Filtering** (Coarse + Fine)
- 🏢 **Small-Cap Focus** (Market Cap Based Selection)
- 💧 **Liquidity Screening** (Dollar Volume Filter)
- 📅 **Monthly Rebalancing** (Systematic Portfolio Updates)

### 🎪 **STRATEGY PHILOSOPHY**

| Component | Approach | Rationale |
|-----------|----------|-----------|
| **Universe** | Top 200 liquid stocks → Top 10 small-caps | Balance liquidity with small-cap exposure |
| **Selection** | Market Cap Sorting | Small-cap anomaly premium capture |
| **Rebalancing** | Monthly | Capture momentum while controlling turnover |
| **Allocation** | Equal Weight | Diversification across selected names |

---

## ⚙️ **CONFIGURATION SETTINGS** ⚙️

### 📅 **BACKTEST PERIOD**
```python
self.SetStartDate(2019, 1, 1)   # 🗓️ Start Date
self.SetEndDate(2021, 1, 1)     # 🗓️ End Date (2-year period)
self.SetCash(100000)            # 💰 Initial Capital: $100,000
```
📊 DATA SETTINGS
```python
self.AddUniverse(self.CoarseFilter, self.FineFilter)
self.UniverseSettings.Resolution = Resolution.Hour
```
Universe Type: Dynamic Stock Universe 🔄

Data Resolution: Hourly 📊

Rebalance Frequency: Monthly 📅

🔧 UNIVERSE SELECTION PROCESS 🔧
🎯 TWO-STAGE FILTERING SYSTEM
1. COARSE FILTER STAGE 📊
```python
def CoarseFilter(self, coarse):
    # Monthly rebalancing check
    if self.Time <= self.rebalanceTime:
        return self.Universe.Unchanged
    self.rebalanceTime = self.Time + timedelta(30)
    
    # Liquidity and price filters
    sortedByDollarVolume = sorted(coarse, key=lambda x: x.DollarVolume, reverse=True)
    return [x.Symbol for x in sortedByDollarVolume if x.Price > 10
                                            and x.HasFundamentalData][:200]
```
Coarse Filter Criteria:

✅ Monthly Rebalance Timer ⏰

✅ Price > $10 (Penny Stock Exclusion) 💰

✅ Has Fundamental Data 📈

✅ Top 200 by Dollar Volume 💧

2. FINE FILTER STAGE 🔍
```python
def FineFilter(self, fine):
    sortedByPE = sorted(fine, key=lambda x: x.MarketCap)
    return [x.Symbol for x in sortedByPE if x.MarketCap > 0][:10]
Fine Filter Criteria:
```
✅ Market Cap > 0 (Valid Companies) 🏢

✅ Sorted by Market Cap (Ascending - Smallest First) 📊

✅ Top 10 Smallest Companies 🎯

📊 PORTFOLIO CONSTRUCTION 📊
⚖️ EQUAL WEIGHT ALLOCATION
```python
self.portfolioTargets = [PortfolioTarget(symbol, 1/len(self.activeStocks)) 
                    for symbol in self.activeStocks]
```
Allocation Logic:

🎯 Equal Weight across all selected stocks

🔢 Dynamic Position Sizing based on universe count

💰 10 Stocks = 10% each, 8 Stocks = 12.5% each, etc.

🔄 ACTIVE STOCKS MANAGEMENT
```python
self.activeStocks = set()  # Tracks current portfolio holdings
```
🔄 REBALANCING LOGIC 🔄
📅 MONTHLY REBALANCE SCHEDULE
```python
# Rebalance timing control
self.rebalanceTime = datetime.min

# Monthly check in CoarseFilter
if self.Time <= self.rebalanceTime:
    return self.Universe.Unchanged
self.rebalanceTime = self.Time + timedelta(30)
```
🎯 SECURITIES CHANGE HANDLING
```python
def OnSecuritiesChanged(self, changes):
    # Remove liquidated securities
    for x in changes.RemovedSecurities:
        self.Liquidate(x.Symbol)
        self.activeStocks.remove(x.Symbol)

    # Add new securities to tracking
    for x in changes.AddedSecurities:
        self.activeStocks.add(x.Symbol)

    # Recalculate portfolio targets
    self.portfolioTargets = [PortfolioTarget(symbol, 1/len(self.activeStocks)) 
                        for symbol in self.activeStocks]

```
⏰ EXECUTION TIMING
```python
def OnData(self, data):
    # Wait for all symbols to have data
    if self.portfolioTargets == []:
        return
    
    for symbol in self.activeStocks:
        if symbol not in data:
            return
    
    # Execute portfolio rebalance
    self.SetHoldings(self.portfolioTargets)
    self.portfolioTargets = []  # Reset targets after execution
```

🛠️ INSTALLATION & USAGE 🛠️
📥 QUICK START GUIDE
COPY THE CODE 📋

```python
# Copy the entire algorithm code
PASTE INTO QUANTCONNECT 🖥️

Navigate to QuantConnect Algorithm Lab

Create new algorithm

Paste the code

CONFIGURE PARAMETERS ⚙️

python
# Adjust these values as needed:
self.SetStartDate(2019, 1, 1)    # Change backtest period
self.SetCash(100000)             # Adjust capital
# Modify universe size:
return [x.Symbol for x in sortedByDollarVolume if x.Price > 10 and x.HasFundamentalData][:100]  # Top 100
RUN BACKTEST 🚀

Click "Backtest"

Analyze small-cap momentum performance
```
Optimize parameters
`
🔧 REQUIREMENTS
✅ QuantConnect Account

✅ Python 3.6+

✅ Understanding of universe selection

⚡ RISK MANAGEMENT ⚡
🛡️ BUILT-IN PROTECTIONS
✅ Liquidity Screening (High Dollar Volume) 💧

✅ Price Floor (>$10 eliminates penny stocks) 💰

✅ Equal Weight Diversification 📊

✅ Monthly Rebalancing Discipline 📅

⚠️ RISK CONSIDERATIONS
Small-Cap Volatility: Higher price swings expected 📈📉

Liquidity Risk: Despite screening, small-caps can be less liquid 💧

Sector Concentration: May overweight certain sectors 🏢

Market Cap Drift: Stocks may grow out of small-cap range 🔄

💼 POSITION MANAGEMENT
Maximum Stocks: 10 positions

Allocation: Equal weight (10% each typically)

Holding Period: Approximately 1 month

Turnover: 100% monthly (complete rebalance)

