# region imports
from AlgorithmImports import *
# endregion

# Import NLTK VADER sentiment analyzer (supported in new QC environment)
from nltk.sentiment import SentimentIntensityAnalyzer


class AdaptableSkyBlueCat(QCAlgorithm):

    def Initialize(self):
        # Set backtest range
        self.SetStartDate(2012, 11, 1)
        self.SetEndDate(2017, 1, 1)

        # Starting capital
        self.SetCash(100000)
        
        # Add TSLA stock with minute resolution
        self.tsla = self.AddEquity("TSLA", Resolution.Minute).Symbol
        
        # Add Musk tweet sentiment stream as custom data
        self.musk = self.AddData(MuskTweet, "MUSKTWTS", Resolution.Minute).Symbol

        # Schedule exit function 15 minutes before close every day
        self.Schedule.On(
            self.DateRules.EveryDay(self.tsla),
            self.TimeRules.BeforeMarketClose(self.tsla, 15),
            self.ExitPositions
        )


    def OnData(self, data):

        # Only proceed when we actually received a Musk tweet this bar
        if self.musk not in data:
            return
        
        # Extract sentiment score and tweet text
        sentiment_score = data[self.musk].Value
        tweet_text      = data[self.musk].Tweet
        
        # Trading logic:
        # If sentiment score > 0.5 → bullish → go long TSLA
        if sentiment_score > 0.5:
            self.SetHoldings(self.tsla, 1)

        # If sentiment score < -0.5 → bearish → short TSLA
        elif sentiment_score < -0.5:
            self.SetHoldings(self.tsla, -1)

        # Optional logging for strongly biased tweets
        if abs(sentiment_score) > 0.5:
            self.Log(f"Sentiment: {sentiment_score}  |  Tweet: {tweet_text}")


    def ExitPositions(self):
        # Close any open TSLA position each day before market close
        self.Liquidate()



# -------------------- Custom Data Class --------------------

class MuskTweet(PythonData):
    
    # Initialize NLTK sentiment analyzer once
    sia = SentimentIntensityAnalyzer()

    def GetSource(self, config, date, isLive):
        # CSV file containing pre-processed tweet dataset
        # (Downloaded each time by QC)
        url = "https://www.dropbox.com/s/ovnsrgg1fou1y0r/MuskTweetsPreProcessed.csv?dl=1"
        return SubscriptionDataSource(url, SubscriptionTransportMedium.RemoteFile)
    

    def Reader(self, config, line, date, isLive):

        # Skip empty or invalid lines
        if not (line.strip() and line[0].isdigit()):
            return None
    
        fields = line.split(',')
        obj = MuskTweet()

        try:
            # Assign symbol and timestamp (+1 minute offset to sync with bar)
            obj.Symbol = config.Symbol
            obj.Time   = datetime.strptime(fields[0], '%Y-%m-%d %H:%M:%S') + timedelta(minutes=1)

            # Raw tweet text
            content = fields[1]

            # Compute compound sentiment score using NLTK VADER
            sentiment = self.sia.polarity_scores(content)["compound"]

            # Only apply sentiment when tweet explicitly references Tesla
            if "tsla" in content.lower() or "tesla" in content.lower():
                obj.Value = sentiment      # store sentiment score as Value
            else:
                obj.Value = 0              # ignore irrelevant tweets

            # Store tweet text in custom member variable
            obj.Tweet = content

        except:
            return None
        
        return obj
