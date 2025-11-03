# Trend-Following Portfolio Strategy (SPY & BND)

This project implements a simple trend-following asset allocation strategy using the QuantConnect Lean framework. The algorithm rotates between equities (SPY) and bonds (BND) based on the relationship between SPY's price and its Simple Moving Average (SMA).

## Strategy Overview

This strategy uses:

- **SPY** — S&P 500 ETF (equity exposure)
- **BND** — Vanguard Total Bond Market ETF (bond exposure)
- **Simple Moving Average (SMA)** as a trend indicator
- **Monthly rebalance lock** to avoid frequent trades

### Trading Logic

1. Compute SMA for SPY (default 30-day, can be overridden via parameter `sma_length`).
2. If SPY's price is **above** the SMA (uptrend):
   - Allocate **80% SPY**
   - Allocate **20% BND**
3. If SPY's price is **below** the SMA (downtrend):
   - Allocate **20% SPY**
   - Allocate **80% BND**
4. Rebalance only every **30 days** or when the trend flips.

This approach blends trend-following with tactical asset allocation to reduce whipsaw trading.

---

## Code

```python
class CrawlingYellowGreenJackal(QCAlgorithm):

    def Initialize(self):
        # Set backtest period and initial cash
        self.SetStartDate(2018, 1, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)

        # Add SPY (equity) and BND (bond ETF) to the algorithm
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol
        self.bnd = self.AddEquity("BND", Resolution.Daily).Symbol

        # Read SMA length from parameters if supplied, else default to 30
        length = self.GetParameter("sma_length")
        length = 30 if length is None else int(length)

        # Create a Simple Moving Average indicator for SPY
        self.sma = self.SMA(self.spy, length, Resolution.Daily)

        # Initialize variables to control rebalancing frequency and trend status
        self.rebalanceTime = datetime.min   # next allowed rebalance time
        self.uptrend = True                 # tracks whether price is above SMA

    def OnData(self, data):
        # Ensure SMA is ready and both SPY & BND have data available
        if not self.sma.IsReady or self.spy not in data or self.bnd not in data:
            return

        price = data[self.spy].Price
        sma_value = self.sma.Current.Value

        # If SPY price is above its SMA, this indicates an uptrend
        if price >= sma_value:
            # Rebalance if:
            # (1) It's time to rebalance OR
            # (2) Trend changed from downtrend to uptrend
            if self.Time >= self.rebalanceTime or not self.uptrend:
                # Allocate 80% to equity, 20% to bonds during uptrend
                self.SetHoldings(self.spy, 0.8)
                self.SetHoldings(self.bnd, 0.2)

                self.uptrend = True
                # Prevent rebalancing for the next 30 days
                self.rebalanceTime = self.Time + timedelta(30)

        # If SPY price falls below SMA, this is a downtrend condition
        elif self.Time >= self.rebalanceTime or self.uptrend:
            # Allocate only 20% to equity, 80% to bonds during downtrend
            self.SetHoldings(self.spy, 0.2)
            self.SetHoldings(self.bnd, 0.8)

            self.uptrend = False
            # Lock rebalancing for 30 days
            self.rebalanceTime = self.Time + timedelta(30)

        # Plot SMA for visual benchmark
        self.Plot("Benchmark", "SMA", sma_value)
```
Parameters
Parameter	Default	Description
sma_length	30	SMA lookback period for SPY (days)

Example usage in QuantConnect:

ini
Copy code
sma_length=50
Key Features
Rule-based trend following

Low trading frequency (30-day rebalance lock)

Dual asset rotation (stocks vs. bonds)

SMA driven market regime switching

Simple and robust portfolio logic

How To Run
In QuantConnect IDE
Create a new Python algorithm

Paste this code into main.py

Add parameter if desired

Run backtest and analyze results

Backtest Period
2018-01-01 to 2021-01-01

Starting Capital: $100,000

Improvements To Explore
Dynamic risk budgeting

Multi-asset universe (commodities, gold, international equities)

Different lookback SMA periods

Stop-loss or volatility filter

Rebalancing frequency experimentation

