
# Import required libraries
# matplotlib: used for plotting graphs and visualizing data
# numpy: used for numerical operations and matrix calculations
import matplotlib.pyplot as plt 
import numpy as np

# Initialize QuantBook environment to access market data inside QuantConnect Research
qb = QuantBook()

# -----------------------------------------------------------
# Load financial sector equity data
# -----------------------------------------------------------

# List of U.S. financial sector stocks for analysis
tickers = ["JPM", "BAC", "MS", "SCHW", "GS", "AXP", "C"]

# Add each equity to QuantBook and store Symbol objects
symbols = [qb.AddEquity(ticker, Resolution.Daily).Symbol for ticker in tickers]

# -----------------------------------------------------------
# Retrieve PE Ratio Fundamental Data
# -----------------------------------------------------------

# Request Price-to-Earnings (PE) ratio data from financial fundamentals
pe_ratios = qb.GetFundamental(
    symbols,
    "ValuationRatios.PERatio",
    datetime(2021, 1, 1),
    datetime(2022, 1, 1)
)

# Preview dataset
pe_ratios.head()

# Rename columns to readable company names
pe_ratios.columns = [
    "American Express", "JPMorgan", "Goldman Sachs",
    "Morgan Stanley", "Bank of America", "Schwab", "Citigroup"
]

# -----------------------------------------------------------
# Plot PE Ratios over time
# -----------------------------------------------------------

pe_ratios.plot(figsize=(16, 8), title="PE Ratio Over Time")
plt.xlabel("Time")
plt.ylabel("Price-to-Earnings Ratio")
plt.show()

# Compute average PE ratio for comparison across companies
mean_pe = pe_ratios.mean()

# Display sorted PE ratios (ascending)
mean_pe.sort_values()

# -----------------------------------------------------------
# Retrieve Price Data for Return Calculation
# -----------------------------------------------------------

history = qb.History(
    symbols,
    datetime(2021, 1, 1),
    datetime(2022, 1, 1),
    Resolution.Daily
).close.unstack(level=0)

# Rename columns to human readable names
history.columns = [
    "American Express", "JPMorgan", "Goldman Sachs", 
    "Morgan Stanley", "Bank of America", "Schwab", "Citigroup"
]

history.head()

# -----------------------------------------------------------
# Compute and Plot Returns
# -----------------------------------------------------------

# Calculate cumulative returns over time
returns_over_time = ((history.pct_change()[1:] + 1).cumprod() - 1)

returns_over_time.plot(figsize=(16, 8), title="Returns Over Time")
plt.grid()
plt.ylabel("Cumulative Return")
plt.show()

# -----------------------------------------------------------
# Study relationship between valuation and performance
# -----------------------------------------------------------

# Calculate correlation between PE ratios and returns
np.corrcoef(returns_over_time.tail(1), mean_pe)

# Scatter plot to visualize return vs valuation relationship
plt.figure(figsize=(10,7))
plt.scatter(returns_over_time.tail(1), mean_pe)
plt.title("2021 Returns vs Mean Price/Earnings Ratio")
plt.xlabel("2021 Returns")
plt.ylabel("Mean PE Ratio 2021")
plt.grid()
plt.show()

# -----------------------------------------------------------
# Options Data Example: BAC Options
# -----------------------------------------------------------

# Add BAC options chain
bac = qb.AddOption("BAC")

# Set filter for options only near money and near expiration
bac.SetFilter(-5, 5, timedelta(20), timedelta(50))

# Fetch option history data
option_history = qb.GetOptionHistory(
    bac.Symbol,
    datetime(2021, 1, 1),
    datetime(2021, 1, 10)
)

# Print available strikes and expiration dates
print(option_history.GetStrikes())
print(option_history.GetExpiryDates())

# View complete option dataset
option_history.GetAllData()

# -----------------------------------------------------------
# Technical Indicator: Bollinger Bands
# -----------------------------------------------------------

# Initialize Bollinger Bands indicator
bb = BollingerBands(30, 2)

# Compute indicator values on BAC open price over past 360 periods
bbdf = qb.Indicator(bb, "BAC", 360, Resolution.Daily, Field.Open)

# Plot raw output including extra fields
bbdf.plot(figsize=(16, 8), title="BAC Bollinger Bands", grid=1)

# Remove statistical extras for clean plot
bbdf = bbdf.drop(["standarddeviation", "percentb", "bandwidth"], axis=1)

# Plot simplified Bollinger Band lines
bbdf.plot(figsize=(16, 8), title="BAC Bollinger Bands", grid=1)

# -----------------------------------------------------------
# Linear Regression Forecasting: Price vs Bollinger Middle Band
# -----------------------------------------------------------

from sklearn.linear_model import LinearRegression

# Fetch last 60 days of BAC price history
history = qb.History(qb.Symbol("BAC"), 60, Resolution.Daily)
history = history.reset_index(level=0, drop=True)

# Extract closing prices
prices = list(history["close"])

# Prepare training data: Bollinger mid-band vs closing price (first 30)
train_X = np.asarray(bbdf["middleband"][-60:-30]).reshape(30, 1)
train_Y = prices[:30]

# Train regression model
reg = LinearRegression()
reg.fit(train_X, train_Y)

# Prepare test input data: last 60 mid-band values
test_X = np.asarray(bbdf["middleband"][-60:]).reshape(60, 1)

# Predict closing prices using model
prices_pred = reg.predict(test_X)

# -----------------------------------------------------------
# Plot regression training and prediction results
# -----------------------------------------------------------

plt.figure(figsize=(10,7))
plt.scatter(bbdf["middleband"][-60:-30], prices[:30], color="blue", label="Training Data")
plt.scatter(bbdf["middleband"][-30:], prices[30:60], color="green", label="Test Data")
plt.plot(bbdf["middleband"][-60:], prices_pred, color="red", linewidth=1, label="Predicted Price")
plt.xlabel("Bollinger Middle Band")
plt.ylabel("Closing Price")
plt.title("Linear Regression: Bollinger Band vs BAC Closing Price")
plt.legend()
plt.grid()
plt.show()
