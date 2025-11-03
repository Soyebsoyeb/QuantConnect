# Import necessary libraries available inside QuantConnect
import json
import numpy as np
from tensorflow.keras.models import Sequential

class MeasuredYellowBarracuda(QCAlgorithm):

    def Initialize(self):
        # Set backtest start and end dates
        self.SetStartDate(2018, 1, 1)
        self.SetEndDate(2020, 1, 1)

        # -------------------------------------------------------------
        # Load the saved Keras model from ObjectStore
        # -------------------------------------------------------------

        # This must match the key you used while saving the model config
        model_key = 'bitcoin_price_predictor'

        # Check if the model exists in ObjectStore
        if self.ObjectStore.ContainsKey(model_key):

            # Read the stored JSON text
            model_str = self.ObjectStore.Read(model_key)

            # Extract 'config' field from JSON string
            config = json.loads(model_str)['config']

            # Rebuild Keras model from saved config
            self.model = Sequential.from_config(config)

        else:
            # Fail early if model not found
            self.Debug("Model not found in Object Store. Upload first.")
            raise Exception("Keras model not found")

        # -------------------------------------------------------------
        # QuantConnect Brokerage and Cash setup
        # -------------------------------------------------------------
        self.SetBrokerageModel(BrokerageName.Bitfinex, AccountType.Margin)
        self.SetCash(100000)

        # Add BTCUSD crypto data
        self.symbol = self.AddCrypto("BTCUSD", Resolution.Daily).Symbol

        # Set benchmark to BTC itself
        self.SetBenchmark(self.symbol)

    # -------------------------------------------------------------
    # Called every time new market data comes in
    # -------------------------------------------------------------
    def OnData(self, data):
        # Only act when model gives a direction
        prediction = self.GetPrediction()

        if prediction == "Up":
            # Go long the asset if model predicts upward price move
            self.SetHoldings(self.symbol, 1)
        else:
            # Short the asset if down
            self.SetHoldings(self.symbol, -0.5)

    # -------------------------------------------------------------
    # Prepare input sequence, run through model, and interpret output
    # -------------------------------------------------------------
    def GetPrediction(self):

        # Pull 40 bars of OHLCV history
        df = self.History(self.symbol, 40).loc[self.symbol]

        # We need percent change training format (same as training pipeline)
        df_change = df[["open", "high", "low", "close", "volume"]].pct_change().dropna()

        # Collect last 30 rows as input window
        model_input = []
        for index, row in df_change.tail(30).iterrows():
            model_input.append(np.array(row))

        # Convert to numpy array and add batch dimension
        model_input = np.array([model_input])

        # Predict using the loaded Keras model
        pred = self.model.predict(model_input)[0][0]

        # Round output: 1 = Up, 0 = Down
        if round(pred) == 0:
            return "Down"
        return "Up"
