from QuantConnect.Indicators import MovingAverageType

class CreativeRedHornet(QCAlgorithm):

    def Initialize(self):
        # Backtest date range
        self.SetStartDate(2019, 1, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(100000)

        # Prevent full portfolio usage, keep buffer
        self.Settings.FreePortfolioValuePercentage = 0.05

        # Each trade position size (in USD)
        self.positionSizeUSD = 5000

        # RSI Entry/Exit parameters
        self.rsiEntryThreshold = 70      # Enter long if RSI crosses above this
        self.rsiExitThreshold = 60       # Exit long if RSI crosses below this

        # Volume threshold: avoid low liquidity coins
        self.minimumVolume = 1_000_000

        # Crypto universe
        universe = [
            'BTCUSD','LTCUSD','ETHUSD','ETCUSD','RRTUSD','ZECUSD','XMRUSD','XRPUSD','EOSUSD',
            'SANUSD','OMGUSD','NEOUSD','ETPUSD','BTGUSD','SNTUSD','BATUSD','FUNUSD','ZRXUSD',
            'TRXUSD','REQUSD','LRCUSD','WAXUSD','DAIUSD','BFTUSD','ODEUSD','ANTUSD','XLMUSD',
            'XVGUSD','MKRUSD','KNCUSD','LYMUSD','UTKUSD','VEEUSD','ESSUSD','IQXUSD','ZILUSD',
            'BNTUSD','XRAUSD','VETUSD','GOTUSD','XTZUSD','MLNUSD','PNKUSD','DGBUSD','BSVUSD',
            'ENJUSD','PAXUSD'
        ]

        # Create objects for all crypto pairs
        self.pairs = [CryptoPair(self, ticker, self.minimumVolume) for ticker in universe]

        # Use BTC as benchmark reference
        self.SetBenchmark("BTCUSD")

        # Warm up indicators (RSI & Bollinger need history)
        self.SetWarmup(30)

    def OnData(self, data):

        for pair in self.pairs:

            # Indicators must be ready before trading
            if not pair.rsi.IsReady or not pair.bb.IsReady:
                continue

            symbol = pair.symbol
            rsi = pair.rsi.Current.Value
            price = self.Securities[symbol].Price

            # Retrieve Bollinger values
            lower = pair.bb.LowerBand.Current.Value
            upper = pair.bb.UpperBand.Current.Value
            middle = pair.bb.MiddleBand.Current.Value

            # If position already held, manage exit
            if self.Portfolio[symbol].Invested:

                # Exit if volume drops
                if not pair.Investable():
                    self.Liquidate(symbol, "Volume dropped below threshold")
                    continue

                # Exit if RSI falls below threshold
                if rsi < self.rsiExitThreshold:
                    self.Liquidate(symbol, "RSI exit condition triggered")
                    continue

                # Exit if price closes below middle band (trend weakening)
                if price < middle:
                    self.Liquidate(symbol, "Price dropped below Bollinger mid-band")
                    continue

            # Do not enter if coin fails liquidity requirements
            if not pair.Investable():
                continue

            # Entry signal: RSI overbought AND price breaks above upper band (trend breakout)
            if rsi > self.rsiEntryThreshold and price > upper and self.Portfolio.MarginRemaining > self.positionSizeUSD:
                quantity = self.positionSizeUSD / price
                self.Buy(symbol, quantity)


class CryptoPair:
    """
    Handles tracking indicators and filtering conditions per asset
    """

    def __init__(self, algorithm, ticker, minimumVolume):
        # Add crypto from Bitfinex exchange
        self.symbol = algorithm.AddCrypto(ticker, Resolution.Daily, Market.Bitfinex).Symbol

        # RSI for momentum measure
        self.rsi = algorithm.RSI(self.symbol, 14, MovingAverageType.Simple, Resolution.Daily)

        # Bollinger Bands: 20-period SMA, 2 std deviation
        self.bb = algorithm.BB(self.symbol, 20, 2, MovingAverageType.Simple, Resolution.Daily)

        # 30-day average dollar volume = SMA(volume) * SMA(price)
        self.volume = IndicatorExtensions.Times(
            algorithm.SMA(self.symbol, 30, Resolution.Daily, Field.Volume),
            algorithm.SMA(self.symbol, 30, Resolution.Daily, Field.Close)
        )

        # Required liquidity threshold
        self.minimumVolume = minimumVolume

    def Investable(self):
        # True if average dollar volume exceeds requirement
        return self.volume.Current.Value > self.minimumVolume
