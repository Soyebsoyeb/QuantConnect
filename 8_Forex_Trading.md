# 📈 Forex Bollinger Band Trading Bot (QuantConnect / Lean)

This repository contains a **Forex Bollinger Band Trading Bot** built using **QuantConnect Lean Algorithmic Trading Engine**.

The strategy trades **EUR/USD** using a **mean-reversion approach** based on **Bollinger Bands**.

---

## 🎯 Strategy Overview

### 📊 Indicators Used
| Indicator | Description |
|----------|------------|
| **Bollinger Bands (20, 2)** | Uses a 20-period SMA with 2-standard deviations |

- ✅ **Buy** when price drops below lower band (oversold)
- ✅ **Sell** when price rises above upper band (overbought)
- ✅ **Exit** when price returns to the middle band
- 🎯 Goal: Profit from price reverting back to the SMA

---

## 🧠 Trading Logic

| Condition | Action |
|----------|--------|
| Price < Lower Band & no position | **Go Long** |
| Price > Upper Band & no position | **Go Short** |
| Long position & price > Middle Band | **Exit** |
| Short position & price < Middle Band | **Exit** |

The bot also plots:
- Price 📈  
- Upper / Middle / Lower Bollinger Bands 🎯  
- Buy / Sell / Close markers ✅

---

## 💻 Code Snippet

```python
from System.Drawing import Color

class ForexBollingerBandBot(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 1, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)

        self.pair = self.AddForex("EURUSD", Resolution.Daily, Market.Oanda).Symbol
        self.bb = self.BB(self.pair, 20, 2)

        stockPlot = Chart('Trade Plot')
        stockPlot.AddSeries(Series('Buy', SeriesType.Scatter, '$', Color.Green, ScatterMarkerSymbol.Triangle))
        stockPlot.AddSeries(Series('Sell', SeriesType.Scatter, '$', Color.Red, ScatterMarkerSymbol.TriangleDown))
        stockPlot.AddSeries(Series('Liquidate', SeriesType.Scatter, '$', Color.Blue, ScatterMarkerSymbol.Diamond))
        self.AddChart(stockPlot)

    def OnData(self, data):
        if not self.bb.IsReady:
            return

        price = data[self.pair].Price
        self.Plot("Trade Plot", "Price", price)
        self.Plot("Trade Plot", "MiddleBand", self.bb.MiddleBand.Current.Value)
        self.Plot("Trade Plot", "UpperBand", self.bb.UpperBand.Current.Value)
        self.Plot("Trade Plot", "LowerBand", self.bb.LowerBand.Current.Value)

        if not self.Portfolio.Invested:
            if price < self.bb.LowerBand.Current.Value:
                self.SetHoldings(self.pair, 1)
                self.Plot("Trade Plot", "Buy", price)
            elif price > self.bb.UpperBand.Current.Value:
                self.SetHoldings(self.pair, -1)
                self.Plot("Trade Plot", "Sell", price)
        else:
            if self.Portfolio[self.pair].IsLong and price > self.bb.MiddleBand.Current.Value:
                self.Liquidate()
                self.Plot("Trade Plot", "Liquidate", price)
            elif self.Portfolio[self.pair].IsShort and price < self.bb.MiddleBand.Current.Value:
                self.Liquidate()
                self.Plot("Trade Plot", "Liquidate", price)
```
🏗️ Requirements
Tool	Version
QuantConnect Lean	Latest
Python	✔
Forex data (EUR/USD)	✔

🚀 How to Run
Option 1: QuantConnect Web IDE
Create a new algorithm

Paste the code

Run backtest ✅

Option 2: Local Lean CLI
```bash
Copy code
lean init
lean cloud pull
lean backtest <project>
```
⚠️ Disclaimer
This project is for educational purposes only.
Trading forex involves risk. 💡 Always test before live deployment.

⭐ Support & Feedback
If you like this project:

⭐ Star the repo

🔁 Fork & modify

📝 Share improvements

Happy trading! 📊💹🚀
