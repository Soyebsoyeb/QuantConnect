# region imports
from AlgorithmImports import *
# endregion

class AdaptableSkyBlueCat(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020,9,23)
        self.SetEndDate(2021,1,1)
        self.SetCash(100000)

        spy = self.AddEquity("SPY",Resolution.Daily)
        # We can add other asset classes
        # self.AddForex , self.AddFuture ...

        spy.SetDataNormalizationMode(DataNormalizationMode.Raw)


        # Holds more data than Ticker and No place for ambiguity
        self.spy = spy.Symbol

        
        self.SetBenchmark("SPY")
        
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage , AccountType.Margin )

        self.entryPrice = 0
        self.period = timedelta(31)
        self.nextEntryTime = self.Time



    def OnData(self, data):

        bar = data.Bars.get(self.spy)
        if bar is None:
            return

        price = bar.Close

        if not self.Portfolio.Invested:
            if self.nextEntryTime <= self.Time:
                self.SetHoldings(self.spy, 1)
                # 1 specifies , We will allocate 100 percent to our portfolio SPY   
                
                # self.MarketOrder(self.spy , int(self.Portfolio.Cash / price))


                self.Log(f"BUY SPY @ {price}")
                self.entryPrice = price
            
            elif self.entryPrice*1.1 < price or self.entryPrice*0.9 > price:
                self.Liquidate()
                self.Log(f"SELL SPY @ {price}")
                self.nextEntryTime = self.Time + self.period
