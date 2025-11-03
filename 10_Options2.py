from datetime import timedelta
from QuantConnect.Data.Custom.CBOE import *

class OptionChainProviderPutProtection(QCAlgorithm):

    def Initialize(self):
        # --------------------------------------------------------------
        # Backtest Parameters
        # --------------------------------------------------------------
        self.SetStartDate(2017, 10, 1)
        self.SetEndDate(2020, 10, 1)
        self.SetCash(100000)

        # --------------------------------------------------------------
        # Add underlying equity (SPY), Minute data, RAW prices
        # --------------------------------------------------------------
        self.equity = self.AddEquity("SPY", Resolution.Minute)
        self.equity.SetDataNormalizationMode(DataNormalizationMode.Raw)
        self.symbol = self.equity.Symbol

        # --------------------------------------------------------------
        # Add VIX Index to measure implied volatility environment
        # Used for volatility timing indicator (VIX Rank)
        # --------------------------------------------------------------
        self.vix = self.AddData(CBOE, "VIX").Symbol

        # Initialize state variables
        self.rank = 0                    # VIX percentile rank indicator
        self.contract = str()           # stores current put contract symbol
        self.contractsAdded = set()     # avoid repeated subscription

        # --------------------------------------------------------------
        # User Parameters / Strategy Inputs
        # --------------------------------------------------------------
        self.DaysBeforeExp = 2      # exit puts 2 days before expiration
        self.DTE = 25               # target 25 days to expiration
        self.OTM = 0.01             # 1% out-of-the-money put strike target
        self.lookbackIV = 150       # lookback days for IV rank
        self.IVlvl = 0.5            # enter hedge when VIX rank > 50% level
        self.percentage = 0.9       # allocate 90% capital to SPY shares
        self.options_alloc = 90     # 1 option per 90 shares (hedge ratio)

        # --------------------------------------------------------------
        # Scheduled Functions
        # Run after market open daily for indicator + plotting
        # --------------------------------------------------------------
        self.Schedule.On(
            self.DateRules.EveryDay(self.symbol),
            self.TimeRules.AfterMarketOpen(self.symbol, 30),
            self.Plotting
        )

        self.Schedule.On(
            self.DateRules.EveryDay(self.symbol),
            self.TimeRules.AfterMarketOpen(self.symbol, 30),
            self.VIXRank
        )

        # Warm-up period for VIX rank data
        self.SetWarmUp(timedelta(self.lookbackIV)) 


    def VIXRank(self):
        # --------------------------------------------------------------
        # Compute IV Rank = (Current VIX - Lowest) / (Highest - Lowest)
        #
        # Higher rank = volatility high → hedge more likely
        # --------------------------------------------------------------
        history = self.History(CBOE, self.vix, self.lookbackIV, Resolution.Daily)

        self.rank = (
            (self.Securities[self.vix].Price - min(history["low"])) /
            (max(history["high"]) - min(history["low"]))
        )
 
 
    def OnData(self, data):
        # Block until warm-up finishes
        if self.IsWarmingUp:
            return
        
        # --------------------------------------------------------------
        # Core Logic
        #
        # 1. Hold 90% SPY equity position
        # 2. Buy put hedge only when VIX rank > threshold
        # 3. Exit hedge before expiration
        # --------------------------------------------------------------

        # Allocate portfolio to SPY stock if not already invested
        if not self.Portfolio[self.symbol].Invested:
            self.SetHoldings(self.symbol, self.percentage)
        
        # If volatility high → buy OTM put protection
        if self.rank > self.IVlvl:
            self.BuyPut(data)
        
        # Close hedge before expiration
        if self.contract:
            if (self.contract.ID.Date - self.Time) <= timedelta(self.DaysBeforeExp):
                self.Liquidate(self.contract)
                self.Log("Closed: too close to expiration")
                self.contract = str()


    def BuyPut(self, data):
        # Get best put contract matching filters
        if self.contract == str():
            self.contract = self.OptionsFilter(data)
            return
        
        # Execute hedge if data is added and not already hedged
        if not self.Portfolio[self.contract].Invested and data.ContainsKey(self.contract):
            # Hedge ratio: shares / 90 ≈ 1 contract covers ~90 shares
            self.Buy(self.contract, round(self.Portfolio[self.symbol].Quantity / self.options_alloc))


    def OptionsFilter(self, data):
        # --------------------------------------------------------------
        # Manually choose put contract using OptionChainProvider
        # Filter OTM puts near target DTE window
        # --------------------------------------------------------------
        contracts = self.OptionChainProvider.GetOptionContractList(self.symbol, data.Time)
        self.underlyingPrice = self.Securities[self.symbol].Price

        # Filter:
        # - Put options
        # - Strike slightly below spot (OTM)
        # - Exp near 25 days (±8 days tolerance)
        otm_puts = [
            i for i in contracts
            if i.ID.OptionRight == OptionRight.Put and
               self.underlyingPrice - i.ID.StrikePrice > self.OTM * self.underlyingPrice and
               self.DTE - 8 < (i.ID.Date - data.Time).days < self.DTE + 8
        ]

        if len(otm_puts) > 0:
            # Sort by DTE proximity then strike
            contract = sorted(
                sorted(otm_puts, key=lambda x: abs((x.ID.Date - self.Time).days - self.DTE)),
                key=lambda x: self.underlyingPrice - x.ID.StrikePrice
            )[0]

            # Subscribe to option data once
            if contract not in self.contractsAdded:
                self.contractsAdded.add(contract)
                self.AddOptionContract(contract, Resolution.Minute)

            return contract

        return str()


    def Plotting(self):
        # Plot VIX rank and entry threshold
        self.Plot("Vol Chart", "Rank", self.rank)
        self.Plot("Vol Chart", "lvl", self.IVlvl)

        # Plot SPY price
        self.Plot("Data Chart", self.symbol, self.Securities[self.symbol].Close)

        # Plot strike price of active put hedge
        option_invested = [x.Key for x in self.Portfolio 
                           if x.Value.Invested and x.Value.Type == SecurityType.Option]
        
        if option_invested:
            self.Plot("Data Chart", "strike", option_invested[0].ID.StrikePrice)


    def OnOrderEvent(self, orderEvent):
        # Print order execution events
        self.Log(str(orderEvent))
