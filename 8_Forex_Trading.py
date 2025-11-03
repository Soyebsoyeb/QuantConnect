from System.Drawing import Color

class ForexBollingerBandBot(QCAlgorithm):

    def Initialize(self):
        # Set backtest period
        self.SetStartDate(2015, 1, 1)
        self.SetEndDate(2021, 1, 1)

        # Starting portfolio value
        self.SetCash(100000)

        # Add EUR/USD forex pair
        self.pair = self.AddForex("EURUSD", Resolution.Daily, Market.Oanda).Symbol

        # --------------------------------------------------------------------
        # BOLLINGER BAND INITIALIZATION
        # --------------------------------------------------------------------
      
        # BB(period=20, std=2) means:
        # Middle Band = 20-period simple moving average (SMA)
        # Upper Band  = SMA + (2 * Standard Deviation)
        # Lower Band  = SMA - (2 * Standard Deviation)
        #
        # Standard deviation measures volatility:
        # - Bands widen during high volatility
        # - Bands contract during low volatility
        #
        # Trading logic in this strategy:
        # Buy when price falls below lower band (oversold zone)
        # Sell when price rises above upper band (overbought zone)
        # Exit when price returns to middle band
        #
        # This is a mean-reversion strategy expecting price to revert back to the middle band.
        # --------------------------------------------------------------------
        
        self.bb = self.BB(self.pair, 20, 2)
        

        # Create a chart for trade markers
        stockPlot = Chart('Trade Plot')
        stockPlot.AddSeries(Series('Buy', SeriesType.Scatter, '$', Color.Green, ScatterMarkerSymbol.Triangle))
        stockPlot.AddSeries(Series('Sell', SeriesType.Scatter, '$', Color.Red, ScatterMarkerSymbol.TriangleDown))
        stockPlot.AddSeries(Series('Liquidate', SeriesType.Scatter, '$', Color.Blue, ScatterMarkerSymbol.Diamond))
        self.AddChart(stockPlot)

    def OnData(self, data):
        # Wait until Bollinger bands are fully calculated with enough data
        if not self.bb.IsReady:
            return

        price = data[self.pair].Price

        # Plot current price and Bollinger Bands on chart
        self.Plot("Trade Plot", "Price", price)
        self.Plot("Trade Plot", "MiddleBand", self.bb.MiddleBand.Current.Value)
        self.Plot("Trade Plot", "UpperBand", self.bb.UpperBand.Current.Value)
        self.Plot("Trade Plot", "LowerBand", self.bb.LowerBand.Current.Value)

        # Entry conditions
        if not self.Portfolio.Invested:

            # BUY signal: price moves below lower BB band (oversold)
            if price < self.bb.LowerBand.Current.Value:
                self.SetHoldings(self.pair, 1)
                self.Plot("Trade Plot", "Buy", price)

            # SELL signal: price moves above upper BB band (overbought)
            elif price > self.bb.UpperBand.Current.Value:
                self.SetHoldings(self.pair, -1)
                self.Plot("Trade Plot", "Sell", price)

        # Exit conditions
        else:

            # If long and price crosses above middle band, exit
            if self.Portfolio[self.pair].IsLong:
                if price > self.bb.MiddleBand.Current.Value:
                    self.Liquidate()
                    self.Plot("Trade Plot", "Liquidate", price)

            # If short and price crosses below middle band, exit
            else:
                if price < self.bb.MiddleBand.Current.Value:
                    self.Liquidate()
                    self.Plot("Trade Plot", "Liquidate", price)
