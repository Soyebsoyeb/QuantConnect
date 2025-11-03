📈 Financial Stocks Analysis Using QuantBook (Python)

This project demonstrates how to use QuantConnect’s QuantBook to analyze U.S. financial stocks using both fundamental and technical data, along with a linear regression forecasting model.

✅ Features
Category	Description
📊 Equity Data	JPM, BAC, MS, SCHW, GS, AXP, C
📈 Fundamental Analysis	P/E Ratio extraction & comparison
📉 Price Analytics	Returns calculation & visualization
🔗 Correlations	PE vs Returns correlation matrix
⚙️ Options Analysis	Option chain & strikes/expiry data
📐 Indicators	Bollinger Bands demonstration
🧠 Machine Learning	Linear Regression on price forecast
🧰 Requirements

QuantConnect Research Notebook (QuantBook environment)

Python libraries:

numpy
matplotlib
scikit-learn

🧠 Workflow Summary
1️⃣ Import & Initialize QuantBook
```python
import matplotlib.pyplot as plt
import numpy as np
qb = QuantBook()
```
2️⃣ Add Financial Stocks
```python
tickers = ["JPM", "BAC", "MS", "SCHW", "GS", "AXP", "C"]
symbols = [qb.AddEquity(ticker, Resolution.Daily).Symbol for ticker in tickers]
```
3️⃣ Fetch PE Ratio Fundamentals
```python
pe_ratios = qb.GetFundamental(
    symbols, "ValuationRatios.PERatio",
    datetime(2021,1,1), datetime(2022,1,1)
)

pe_ratios.columns = [
    "American Express","JPMorgan","Goldman Sachs",
    "Morgan Stanley","Bank of America","Schwab","Citigroup"
]
```
4️⃣ Price Data & Returns
```python
history = qb.History(
    symbols,
    datetime(2021,1,1), datetime(2022,1,1),
    Resolution.Daily
).close.unstack(level=0)

returns_over_time = ((history.pct_change()[1:] + 1).cumprod() - 1)
```
5️⃣ Correlation & Scatter
```python
np.corrcoef(returns_over_time.tail(1), pe_ratios.mean())
plt.scatter(returns_over_time.tail(1), pe_ratios.mean())
```
6️⃣ Options Chain
```python
bac = qb.AddOption("BAC")
bac.SetFilter(-5, 5, timedelta(20), timedelta(50))
option_history = qb.GetOptionHistory(bac.Symbol, datetime(2021,1,1), datetime(2021,1,10))
```
7️⃣ Bollinger Bands Indicator
```python
bb = BollingerBands(30, 2)
bbdf = qb.Indicator(bb, "BAC", 360, Resolution.Daily, Field.Open)
```
8️⃣ Linear Regression Forecasting
```python
from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg.fit(train_X, train_Y)
prices_pred = reg.predict(test_X)
```
📂 Outputs

**Time-series charts for PE ratios

** Cumulative return performance chart

** Scatter: Return vs PE Ratio

** Bollinger Band visualization

** Linear regression prediction chart
