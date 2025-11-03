from AlphaModel import *

class VerticalTachyonRegulators(QCAlgorithm):  # Define the algorithm class that inherits QCAlgorithm

    def Initialize(self):  # Initialization method, runs once at start
        self.SetStartDate(2020, 1, 1)  # Set backtest start date
        self.SetEndDate(2021, 1, 1)    # Set backtest end date
        self.SetCash(100000)           # Set initial capital to $100,000

        # === Universe Selection Variables ===
        self.month = 0                 # Track last rebalance month
        self.num_coarse = 500          # Limit coarse universe size to top 500 by volume

        self.UniverseSettings.Resolution = Resolution.Daily  # Apply daily resolution to universe data

        # Add universe selection with two steps: coarse + fine filters
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)

        # === Alpha Model ===
        self.AddAlpha(FundamentalFactorAlphaModel())  # Add fundamental alpha factors strategy

        # === Portfolio Construction ===
        # Equal weighting + rebalance schedule based on our custom rebalance function
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel(self.IsRebalanceDue))
        
        # === Risk Management ===
        self.SetRiskManagement(NullRiskManagementModel())  # Disable risk controls (no hedging/limits)

        # === Order Execution ===
        self.SetExecution(ImmediateExecutionModel())  # Execute trades immediately upon signal


    def IsRebalanceDue(self, time):  # Function to check if rebalancing should occur
        # Only rebalance on first month of each quarter (Jan, Apr, Jul, Oct)
        # Also skip if rebalance already done in this month
        if time.month == self.month or time.month not in [1, 4, 7, 10]:
            return None  # No rebalance this time
        
        self.month = time.month  # Update last rebalance month
        return time              # Return the timestamp: triggers rebalance


    def CoarseSelectionFunction(self, coarse):  # First universe filter layer
        # If rebalance is not due, keep universe unchanged
        if not self.IsRebalanceDue(self.Time): 
            return Universe.Unchanged

        # Filter: must have fundamental data + price above $5
        filtered = [c for c in coarse if c.HasFundamentalData and c.Price > 5]

        # Sort stocks by Dollar Volume (liquidity), descending
        selected = sorted(filtered, key=lambda c: c.DollarVolume, reverse=True)

        # Return only the top N symbols by liquidity
        return [s.Symbol for s in selected[:self.num_coarse]]


    def FineSelectionFunction(self, fine):  # Second universe filter layer (fundamentals)
        # Define eligible sectors
        sectors = [
            MorningstarSectorCode.FinancialServices,
            MorningstarSectorCode.RealEstate,
            MorningstarSectorCode.Healthcare,
            MorningstarSectorCode.Utilities,
            MorningstarSectorCode.Technology
        ]

        # Filter based on multiple conditions:
        # - IPO older than 5 years
        # - Belongs to selected sectors
        # - Positive Return on Equity (profitable)
        # - Positive Net Margin (profitable)
        # - Positive PE ratio (no weird negative earnings valuation)
        filtered_fine = [
            f.Symbol for f in fine
            if f.SecurityReference.IPODate + timedelta(365*5) < self.Time
            and f.AssetClassification.MorningstarSectorCode in sectors
            and f.OperationRatios.ROE.Value > 0
            and f.OperationRatios.NetMargin.Value > 0
            and f.ValuationRatios.PERatio > 0
        ]

        # Return final stock list for alpha model to generate signals on
        return filtered_fine
