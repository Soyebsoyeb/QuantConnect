# region imports
from AlgorithmImports import *
# endregion

class AdaptableSkyBlueCat(QCAlgorithm):
   
    def Initialize(self):
        # Set backtest dates
        self.SetStartDate(2019, 1, 1)
        self.SetEndDate(2021, 1, 1)

        # Initial capital
        self.SetCash(100000)

        # Next rebalance date tracker
        self.rebalanceTime = datetime.min
        
        # Store active stocks
        self.activeStocks = set()

        # Add universe selection with coarse + fine filters
        self.AddUniverse(self.CoarseFilter, self.FineFilter)

        # Set resolution for universe data
        self.UniverseSettings.Resolution = Resolution.Hour
        
        # Will hold desired target portfolio weights
        self.portfolioTargets = []

    # ---------------- Coarse Universe Filter ----------------
    def CoarseFilter(self, coarse):
        # Only rebalance once per month (~30 days)
        if self.Time <= self.rebalanceTime:
            return self.Universe.Unchanged
        
        # Set next rebalance time
        self.rebalanceTime = self.Time + timedelta(30)
        
        # Sort by dollar volume (liquid stocks first)
        sortedByDollarVolume = sorted(
            coarse, key=lambda x: x.DollarVolume, reverse=True
        )

        # Filter stocks with price > $10 and fundamental data available
        return [
            x.Symbol for x in sortedByDollarVolume 
            if x.Price > 10 and x.HasFundamentalData
        ][:200]  # take top 200 by liquidity

    # ---------------- Fine Universe Filter ----------------
    def FineFilter(self, fine):
        # Sort by MarketCap ascending (picking smaller market caps first)
        sortedByPE = sorted(fine, key=lambda x: x.MarketCap)

        # Keep only stocks with valid MarketCap > 0, take top 10
        return [x.Symbol for x in sortedByPE if x.MarketCap > 0][:10]

    # ---------------- Universe Change Handler ----------------
    def OnSecuritiesChanged(self, changes):
        # Liquidate stocks removed from universe
        for x in changes.RemovedSecurities:
            self.Liquidate(x.Symbol)
            if x.Symbol in self.activeStocks:
                self.activeStocks.remove(x.Symbol)

        # Add new stocks to active set
        for x in changes.AddedSecurities:
            self.activeStocks.add(x.Symbol)   

        # Equal-weight target allocation
        if len(self.activeStocks) > 0:
            self.portfolioTargets = [
                PortfolioTarget(symbol, 1 / len(self.activeStocks)) 
                for symbol in self.activeStocks
            ]

    # ---------------- OnData: Execute Rebalance ----------------
    def OnData(self, data):

        # If no targets set, nothing to do
        if self.portfolioTargets == []:
            return
        
        # Ensure all active stocks have valid data
        for symbol in self.activeStocks:
            if symbol not in data:
                return

        # Execute portfolio rebalance (equal weights)
        self.SetHoldings(self.portfolioTargets)
        
        # Reset targets so we don't buy every bar
        self.portfolioTargets = []
