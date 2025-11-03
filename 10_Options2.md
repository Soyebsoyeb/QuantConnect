# 🛡️ SPY Put Protection Strategy using VIX Rank (QuantConnect / Lean)

This repository contains a **systematic SPY downside-protection algorithm** that dynamically buys **OTM put options** based on **volatility conditions** (VIX rank).

The strategy maintains a **core long SPY position (90%)** and hedges it only during high-volatility environments.

---

## 📌 Strategy Overview

| Component | Details |
|----------|--------|
Underlying | SPY 💹 |
Resolution | Minute data |
Hedge | OTM Put Options |
Hedge Trigger | VIX rank > 50% |
Hedge Horizon | ~25 Days to Expiry |
Exit Rule | Liquidate puts 2 days before expiration |
Portfolio | 90% SPY stock + dynamic puts |
Data | CBOE VIX custom feed |

---

## 🎯 Trading Logic

### ✅ Long SPY Exposure
- Maintain **90% capital** long SPY at all times

### ✅ When to Hedge
Buy puts only when:

> `VIX Rank > 0.5`  
(high relative volatility ⇒ crash protection needed)

### ✅ Put Selection Rules
| Filter | Condition |
|--------|----------|
Option Type | Put |
Strike | ~1% OTM |
DTE | 25 days ± 8 days |
Hedge Ratio | 1 contract per ~90 SPY shares |

### ✅ Exit Hedge Conditions
| Condition | Action |
|----------|--------|
2 days before expiration | Sell put |
VIX cools off | No new hedge |

---

## 🔬 VIX Rank Calculation

> **IV Rank = (Current VIX − Lowest) / (Highest − Lowest)** over last 150 days

Measures where current fear level sits relative to past range.

---

## 💻 Code

```python
from datetime import timedelta
from QuantConnect.Data.Custom.CBOE import *

class OptionChainProviderPutProtection(QCAlgorithm):
    # full code here...
(Full code is inside this repo — plug directly into QuantConnect Lean IDE)
```

📊 Plots
This strategy plots:

VIX percentile vs threshold

SPY price

Active hedge strike price

Useful for visualizing hedging moments.

▶️ How To Run
🖥️ QuantConnect Cloud
Create new algorithm

Paste code

Run backtest ✅

💻 Lean CLI Local
```bash
Copy code
lean init
lean backtest SPY-Put-Hedge
```
⚠️ Notes & Risks
This model protects during volatility spikes / crashes

Hedging reduces drawdowns, but can lower performance during calm bull markets

Always test with live option data before production

📎 Useful Concepts
Concept	Used Here
Options Chain Provider	✅ Manual contract selection
VIX Index	✅ CBOE custom data
IV Rank	✅ Volatility timing
Dynamic Hedge Ratio	✅ Based on stock shares
Scheduled Tasks	✅ Daily indicator updates

🧠 Why This Strategy?
Equity curve smoother vs 100% SPY

Tail-risk hedge during crashes (think 2020)

Systematic + rules-based, removes emotion

⭐ Contribution
Pull requests welcome — ideas like:

Rolling puts criteria

Using skew instead of VIX

Ladder hedge ratios

Adding ATR downside triggers

📞 Support
If this helped you:

⭐ Star this repo

🔁 Fork to your repo

✅ Connect for options research

Stay hedged, trade smart 🛡️📈
