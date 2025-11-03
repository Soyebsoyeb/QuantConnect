class BreakoutCallBuy(QCAlgorithm):

    def Initialize(self):
        # --------------------------------------------------------------
        # Backtest period and starting capital
        # --------------------------------------------------------------
        self.SetStartDate(2018, 1, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)

        # --------------------------------------------------------------
        # Add underlying stock (MSFT) using RAW price data
        # We use minute resolution for intraday breakout detection.
        # --------------------------------------------------------------
        equity = self.AddEquity("MSFT", Resolution.Minute)
        equity.SetDataNormalizationMode(DataNormalizationMode.Raw)
        self.equity = equity.Symbol

        # Set benchmark to MSFT for comparison
        self.SetBenchmark(self.equity)
        
        # --------------------------------------------------------------
        # Add MSFT options universe
        # Filter rules:
        # - Select strikes within ±3 strike levels around spot price
        # - Only select expirations 20 to 40 days out
        #
        # This keeps liquid, near-money options with enough time value
        # --------------------------------------------------------------
        option = self.AddOption("MSFT", Resolution.Minute)
        option.SetFilter(-3, 3, timedelta(20), timedelta(40))

        # --------------------------------------------------------------
        # Calculate 21-day rolling highest price (breakout level)
        # Using daily high values to detect fresh breakout conditions.
        #
        # MAX(period=21) = Highest High over the last 21 days
        # --------------------------------------------------------------
        self.high = self.MAX(self.equity, 21, Resolution.Daily, Field.High)
    
    
    def OnData(self, data):

        # Wait until 21-day high indicator is ready
        if not self.high.IsReady:
            return
        
        # --------------------------------------------------------------
        # Check if we already hold any option positions.
        # We trade only one option at a time to control risk.
        # --------------------------------------------------------------
        option_invested = [x.Key for x in self.Portfolio 
                           if x.Value.Invested and x.Value.Type == SecurityType.Option]
        
        if option_invested:

            # ----------------------------------------------------------
            # Avoid holding options very close to expiration.
            # If less than 4 days remaining → exit trade.
            # ----------------------------------------------------------
            if self.Time + timedelta(4) > option_invested[0].ID.Date:
                self.Liquidate(option_invested[0], "Too close to expiration")
            return
        
        # --------------------------------------------------------------
        # BREAKOUT LOGIC
        #
        # Condition:
        # Current price >= 21-day highest price
        #
        # Meaning:
        # Price breaks above recent resistance → bullish breakout
        # Trigger: Buy call option
        # --------------------------------------------------------------
        if self.Securities[self.equity].Price >= self.high.Current.Value:
            for i in data.OptionChains:
                chains = i.Value
                self.BuyCall(chains)


    def BuyCall(self, chains):
        # --------------------------------------------------------------
        # Pick the furthest expiration available in the filtered set
        # This gives more time value and smoother trades
        # --------------------------------------------------------------
        expiry = sorted(chains, key=lambda x: x.Expiry, reverse=True)[0].Expiry
        
        # Filter only call contracts with this expiration
        calls = [i for i in chains if i.Expiry == expiry and i.Right == OptionRight.Call]
        
        # Sort calls by nearest strike to current price (ATM or near-ATM)
        call_contracts = sorted(calls, key=lambda x: abs(x.Strike - x.UnderlyingLastPrice))
        
        if len(call_contracts) == 0:
            return
        
        # Select closest-to-spot strike call
        self.call = call_contracts[0]
        
        # --------------------------------------------------------------
        # Position sizing:
        # 5% of total portfolio allocated to this call trade
        #
        # Options trade in 100-share contracts, hence divide by 100
        # --------------------------------------------------------------
        quantity = self.Portfolio.TotalPortfolioValue / self.call.AskPrice
        quantity = int(0.05 * quantity / 100)

        # Execute buy order for selected option contract
        self.Buy(self.call.Symbol, quantity)


    def OnOrderEvent(self, orderEvent):
        # --------------------------------------------------------------
        # If option gets exercised, liquidate underlying immediately
        # to avoid unwanted stock assignment exposure
        # --------------------------------------------------------------
        order = self.Transactions.GetOrderById(orderEvent.OrderId)
        if order.Type == OrderType.OptionExercise:
            self.Liquidate()
