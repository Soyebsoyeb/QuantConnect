# region imports
from AlgorithmImports import *
from collections import deque
# endregion

"""
Breakout strategy using:
- Custom 30-day Simple Moving Average (SMA)
- 52-week (1-year) high/low breakout filter
Logic:
    Long  when price is near yearly high and above SMA
    Short when price is near yearly low and below SMA
    Otherwise remain flat
"""

class AdaptableSkyBlueCat(QCAlgorithm):

    def Initialize(self):
        # Backtest period
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2021, 1, 1)

        # Initial cash
        self.SetCash(100000)

        # Add SPY (S&P 500 ETF) daily resolution
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol


        #     : Non-Custom Indicator:

        #    self.sma = self.SMA(self.spy, 30, Resolution.Daily)
        # History warm up for shortcut helper SMA indicator
        #    closing_prices = self.History(self.spy, 30, Resolution.Daily)["close"]
        #    for time, price in closing_prices.loc[self.spy].items():
        #        self.sma.Update(time, price)



        # Create and register custom SMA indicator
        self.sma = CustomSimpleMovingAverage("CustomSMA", 30)
        self.RegisterIndicator(self.spy, self.sma, Resolution.Daily)

        self.Debug("Strategy initialized")


    def OnData(self, data):
        # Ensure SMA has enough data before trading
        if not self.sma.IsReady:
            return

        # Get 1-year historical data
        hist = self.History(self.spy, 365, Resolution.Daily)
        if hist.empty:
            return

        # Compute 52-week high/low
        low = hist.loc[self.spy]["low"].min()
        high = hist.loc[self.spy]["high"].max()

        # Current price
        price = self.Securities[self.spy].Price

        # Trading rules

        # Long entry: price near yearly high and above SMA (uptrend breakout)
        if price >= 0.95 * high and price > self.sma.Current.Value:
            if not self.Portfolio[self.spy].IsLong:
                self.Debug(f"Going LONG at {price}")
                self.SetHoldings(self.spy, 1)

        # Short entry: price near yearly low and below SMA (downtrend breakdown)
        elif price <= 1.05 * low and price < self.sma.Current.Value:
            if not self.Portfolio[self.spy].IsShort:
                self.Debug(f"Going SHORT at {price}")
                self.SetHoldings(self.spy, -1)

        # Exit: when trend conditions break
        else:
            if self.Portfolio[self.spy].Invested:
                self.Debug(f"Exiting position at {price}")
            self.Liquidate()

        # Plot levels for visualization
        self.Plot("Benchmark", "52w-High", high)
        self.Plot("Benchmark", "52w-Low", low)
        self.Plot("Benchmark", "SMA-30", self.sma.Current.Value)



# Custom SMA indicator
class CustomSimpleMovingAverage(PythonIndicator):

    def __init__(self, name, period):
        self.Name = name
        self.Time = datetime.min
        self.Value = 0
        self.period = period
        self.queue = deque(maxlen=period)  # sliding window buffer

    def Update(self, input):
        # Add new closing price
        self.queue.appendleft(input.Close)

        # Update timestamp
        self.Time = input.EndTime

        # Calculate average
        count = len(self.queue)
        self.Value = sum(self.queue) / count

        # Indicator ready when queue is full
        return count == self.period
