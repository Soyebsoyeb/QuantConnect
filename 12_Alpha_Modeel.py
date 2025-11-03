
class FundamentalFactorAlphaModel(AlphaModel):  # Define a custom alpha model inheriting from QC AlphaModel class
    
    def __init__(self):  # Constructor runs once when model is created
        self.rebalanceTime = datetime.min   # Track next rebalance time, initialize to earliest possible date
        
        # Dictionary mapping sectors to sets of securities in those sectors
        # Example: { Technology: {AAPL, MSFT}, Healthcare: {JNJ, PFE}, ... }
        self.sectors = {}


    def Update(self, algorithm, data):  # Called automatically each time new data arrives
        
        # If current time has not reached rebalance time, do nothing
        if algorithm.Time <= self.rebalanceTime:
            return []  # No insights produced
        
        # Set next rebalance time to end of current quarter
        # Ensures alpha signals match quarterly rebalance schedule
        self.rebalanceTime = Expiry.EndOfQuarter(algorithm.Time)
        
        insights = []  # List to store trading signals (insights)
        
        # Loop through each sector group in universe
        for sector in self.sectors:
            securities = self.sectors[sector]  # Get list of securities belonging to this sector

            # Sort securities by fundamental factors:

            # 1️⃣ Highest Return on Equity (ROE) is better
            sortedByROE = sorted(
                securities, 
                key=lambda x: x.Fundamentals.OperationRatios.ROE.Value, 
                reverse=True
            )

            # 2️⃣ Highest Net Profit Margin is better
            sortedByPM = sorted(
                securities, 
                key=lambda x: x.Fundamentals.OperationRatios.NetMargin.Value, 
                reverse=True
            )

            # 3️⃣ Lowest Price-to-Earnings Ratio (more value) is better
            sortedByPE = sorted(
                securities, 
                key=lambda x: x.Fundamentals.ValuationRatios.PERatio, 
                reverse=False
            )

            # Dictionary to hold score per security
            # Lower score = better fundamentals
            scores = {}

            # Score system: sum of ranks in ROE, PM, PE
            for security in securities:
                score = (
                    sortedByROE.index(security) +
                    sortedByPM.index(security) +
                    sortedByPE.index(security)
                )
                scores[security] = score  # Store combined score
            
            # Select **top 20%** fundamentally strongest stocks in each sector
            # Ensure at least **one stock** is selected per sector
            length = max(int(len(scores) / 5), 1)

            # Sort by score (lower is better) and select top candidates
            topStocks = sorted(scores.items(), key=lambda x: x[1])[:length]

            for security, score in topStocks:
                symbol = security.Symbol  # Get symbol object

                # Create a long (bullish) signal until quarter end
                insights.append(
                    Insight.Price(
                        symbol, 
                        Expiry.EndOfQuarter, 
                        InsightDirection.Up
                    )
                )
        
        return insights  # Return all generated insights


    def OnSecuritiesChanged(self, algorithm, changes):  # Called whenever universe adds/removes symbols
        
        # Remove securities that left the universe
        for security in changes.RemovedSecurities:
            for sector in self.sectors:
                if security in self.sectors[sector]:
                    self.sectors[sector].remove(security)  # Remove from correct sector grouping
        
        # Add securities that entered universe
        for security in changes.AddedSecurities:
            # Get Morningstar sector code of new stock
            sector = security.Fundamentals.AssetClassification.MorningstarSectorCode
            
            # If sector is not tracked yet, create a set for it
            if sector not in self.sectors:
                self.sectors[sector] = set()
            
            # Add security to its sector bucket
            self.sectors[sector].add(security)
