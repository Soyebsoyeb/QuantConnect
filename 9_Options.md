# 🚀 MSFT Breakout Call Option Strategy (QuantConnect / Lean)

This repository contains an algorithmic **bullish breakout options strategy** for **MSFT** using the QuantConnect Lean engine.

The bot buys **near-ATM call options** when **Microsoft (MSFT)** breaks above a **21-day high**, signaling strong momentum.

---

## 📌 Strategy Summary

| Feature | Description |
|--------|-------------|
| Asset | MSFT (Equity & Options) |
| Resolution | 1-minute |
| Option Type | Call Options Only |
| Universe Filter | ±3 strikes | 
| Expiry Filter | 20–40 days out |
| Breakout Trigger | Price ≥ 21-day high |
| Position Size | 5% portfolio per trade |
| Exit | 4 days before expiry or option exercise |

---

## 🎯 Strategy Logic

### ✅ Entry Condition
Buy **call option** when:

> 📈 MSFT breaks above its **21-day high**

Meaning: bullish breakout, momentum continuation expected.

### ✅ Exit Conditions
| Condition | Action |
|----------|--------|
< 4 days to expiration | Close position |
Option exercised | Liquidate underlying immediately |

---

## 🧠 Why This Works

This is a **momentum breakout + options leverage** strategy:

- Uses **raw intraday minute price** to detect breakout
- Uses **daily 21-day highest high** as resistance level
- Buys call options closest to ATM
- Takes contracts **furthest expiration within 20-40 days**
- Avoids **gamma crush** near expiration

---

## 💻 Code

```python
class BreakoutCallBuy(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018, 1, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)

        equity = self.AddEquity("MSFT", Resolution.Minute)
        equity.SetDataNormalizationMode(DataNormalizationMode.Raw)
        self.equity = equity.Symbol

        self.SetBenchmark(self.equity)
        
        option = self.AddOption("MSFT", Resolution.Minute)
        option.SetFilter(-3, 3, timedelta(20), timedelta(40))

        self.high = self.MAX(self.equity, 21, Resolution.Daily, Field.High)
    
    
    def OnData(self, data):
        if not self.high.IsReady:
            return
        
        option_invested = [x.Key for x in self.Portfolio
                           if x.Value.Invested and x.Value.Type == SecurityType.Option]
        
        if option_invested:
            if self.Time + timedelta(4) > option_invested[0].ID.Date:
                self.Liquidate(option_invested[0], "Too close to expiration")
            return
        
        if self.Securities[self.equity].Price >= self.high.Current.Value:
            for i in data.OptionChains:
                self.BuyCall(i.Value)


    def BuyCall(self, chains):
        expiry = sorted(chains, key=lambda x: x.Expiry, reverse=True)[0].Expiry
        calls = [i for i in chains if i.Expiry == expiry and i.Right == OptionRight.Call]
        call_contracts = sorted(calls, key=lambda x: abs(x.Strike - x.UnderlyingLastPrice))
        
        if len(call_contracts) == 0: return
        
        self.call = call_contracts[0]
        quantity = self.Portfolio.TotalPortfolioValue / self.call.AskPrice
        quantity = int(0.05 * quantity / 100)
        self.Buy(self.call.Symbol, quantity)


    def OnOrderEvent(self, orderEvent):
        order = self.Transactions.GetOrderById(orderEvent.OrderId)
        if order.Type == OrderType.OptionExercise:
            self.Liquidate()
```
▶️ How To Run
🔹 Option 1 — QuantConnect Web IDE
Create new algorithm

Paste code

Run backtest ✅

🔹 Option 2 — Lean CLI (Local)
```bash
Copy code
lean init
lean research
lean backtest <project>
```
⚠️ Disclaimer
This project is for educational purposes only.
Options trading is risky. 📉 Always test before live trading.

⭐ Show Support
If this helped you:

✔️ Star the repo
🔁 Fork it
🧠 Suggest improvements

Happy coding & profitable trading! 💹🚀
