# 🚀 Crypto RSI + Bollinger Breakout Strategy (QuantConnect / Lean)

This strategy trades a large crypto universe using **RSI momentum confirmation** and **Bollinger Band breakouts**, with strong **volume-based liquidity filtering**.  
Designed for spot crypto on **Bitfinex**.

---

## 📌 Strategy Summary

| Category | Details |
|---|---|
Universe | 50+ Bitfinex crypto pairs |
Indicators | RSI(14), Bollinger Bands (20, 2σ), SMA volume |
Timeframe | Daily candles |
Position Size | $5,000 per trade |
Benchmark | BTCUSD |
Warmup | 30 days |
Risk Control | Volume screen + exit rules |
Portfolio Buffer | 5% free capital always reserved |

---

## 🎯 Trading Rules

### ✅ Entry Conditions (LONG only)
Enter long when:

- RSI > **70** (*strong momentum / overbought breakout*)
- Price > **Upper Bollinger Band** (*volatility breakout*)
- 30-day average **dollar volume > $1M**
- Sufficient portfolio margin available

> **Idea:** Overbought can signal momentum continuation in crypto (trend-following).

### ✅ Exit Conditions
Exit long position if:

| Condition | Reason |
|---|---|
Volume drops below threshold | Avoid illiquid markets |
RSI < 60 | Momentum weakening |
Price < Middle Bollinger Band | Trend losing strength |

---

## 📊 Indicators Used

| Indicator | Purpose |
|---|---|
**RSI(14)** | Measures momentum strength |
**Bollinger Bands (20, 2σ)** | Detects volatility breakouts & trend fades |
**30-Day Avg Dollar Volume** = SMA(volume) × SMA(price) | Filters out low-liquidity assets |

---

## 💡 Universe Coverage

Trades all major Bitfinex USD crypto pairs such as:

BTC, ETH, XRP, LTC, XMR, EOS, ZEC, TRX, OMG, NEO, BAT, XLM, KNC, MKR, DAI, ENJ, BNT, VET, BSV, ZIL, ETC, and others.

---

## 🧠 Strategy Philosophy

- **Crypto momentum tends to continue after breakouts**
- Focus on **liquid assets only** (institutional mindset)
- Avoids mean-reversion; this is a **trend-following breakout model**
- Modular design via `CryptoPair` class for clean expansion

---

## 🧮 Risk Management

| Component | Method |
|---|---|
Capital Allocation | Fixed $5,000 per asset |
Portfolio reserve | 5% idle cash buffer |
Liquidity filter | $1M avg daily dollar volume |
Position exit signals | Multi-factor weakening triggers |

---

## 📦 Code Structure

/CreativeRedHornet
├── main algorithm (QCAlgorithm)
└── CryptoPair helper class

yaml
Copy code

Handles:

- RSI
- Bollinger Bands
- Dollar-volume filter
- Per-asset trading logic

---

## ▶️ Running the Strategy

### 🖥️ In QuantConnect Web IDE
1. Create new Python algorithm
2. Paste strategy code
3. Run backtest ✅

### 💻 With Lean CLI
```bash
lean init
lean backtest CreativeRedHornet
```
📁 Output & Metrics You Can Add
Daily P&L

Win rate

Max drawdown

Sortino / Sharpe

Exposure breakdown by asset

Let me know if you want me to add these into your code.

✨ Customization Ideas
Enhancement	Benefit
ATR stop-loss	Better downside control
Dynamic RSI filter	Adapt to volatility regimes
Rank universe by momentum	Trade top 10 strongest coins only
Portfolio volatility cap	Stable returns in bear markets
Leverage settings	For futures/margin trading models

📞 Support
If this repo helps you:

⭐ Star the project

🔁 Fork and build on it

📧 Message for custom research or live deployment help

Trade smart. Protect capital. Let momentum work for you ⚡

