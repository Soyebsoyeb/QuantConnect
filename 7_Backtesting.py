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
        # Equivalent manual alternative that you commented:
        # self.sma = self.SMA(self.spy, 30, Resolution.Daily)

        # Initialize variables to control rebalancing frequency and trend status
        self.rebalanceTime = datetime.min   # next allowed rebalance time
        self.uptrend = True                 # tracks whether price is above SMA

    def OnData(self, data):
        # Ensure SMA is ready and both SPY & BND have data available
        if not self.sma.IsReady or self.spy not in data or self.bnd not in data:
            return

        # Debug or benchmark comparison (optional)
        # If uncommented, this forces 100% SPY exposure and exits logic
        # self.SetHoldings(self.spy, 1)
        # return
        
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
