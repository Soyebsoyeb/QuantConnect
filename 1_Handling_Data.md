# QuantConnect LEAN Price Access Example

This project demonstrates correct methods to access asset prices in the LEAN engine without causing `NoneType` errors.

## ✅ Summary

| Method | Safe | Use |
|-------|------|-----|
`self.Securities[symbol].Close` | ✅ | Always available (recommended) |
`data.Bars.get(symbol).Close` | ✅ | Slice-dependent, check first |
`data[symbol].Close` | ❌ | Causes NoneType errors, avoid |

---

## 📌 Example Strategy (`main.py`)

```python
# region imports
from AlgorithmImports import *
# endregion

class PriceAccessExample(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 5, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)

        equity = self.AddEquity("SPY", Resolution.Daily)
        equity.SetDataNormalizationMode(DataNormalizationMode.Raw)
        self.spy = equity.Symbol

        self.SetBenchmark("SPY")
        self.entry_price = None

    def OnData(self, data):

        # ✅ Safe slice price access
        bar = data.Bars.get(self.spy)
        if bar is None:
            return

        price_slice = bar.Close

        # ✅ Safe always-available price
        price_security = self.Securities[self.spy].Close

        # Choose one:
        price = price_security  # recommended

        if not self.Portfolio.Invested:
            self.SetHoldings(self.spy, 1)
            self.entry_price = price
            self.Log(f"BUY SPY @ {price}")
        else:
            if price > self.entry_price * 1.1 or price < self.entry_price * 0.9:
                self.Liquidate()
                self.Log(f"SELL SPY @ {price}")
```

---

## 🛑 Avoid This

```python
price = data[self.spy].Close   # ❌ can throw NoneType error
```

---

## 🚀 Run with LEAN CLI

```bash
lean backtest
```

---

## 📎 Docs & Support

- Docs: https://www.quantconnect.com/docs/
- Forums: https://www.quantconnect.com/forum/
