# -------------------------------
# Import required libraries
# -------------------------------
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import model_from_json
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import json

# Initialize QuantBook to access market data
qb = QuantBook()

# -------------------------------
# Load historical BTCUSD data
# -------------------------------
symbol = qb.AddCrypto("BTCUSD", Resolution.Daily).Symbol

start = datetime(2020,1,1)
end   = datetime(2022,1,1)

# Request historical price data
history = qb.History(symbol, start, end).loc[symbol]

# --------------------------------
# Feature engineering: percent changes
# --------------------------------
# We use price % changes to make model learn movement direction instead of absolute prices
df = history[["open","high","low","close","volume"]].pct_change().dropna()

# Replace infinite values (can occur when dividing by zero) with valid max volume
df["volume"].replace([np.inf, -np.inf], np.nan, inplace=True)
df["volume"].fillna(df["volume"].max(), inplace=True)

# --------------------------------
# Build sequences of 30 days (lookback window) for ML model input
# --------------------------------
n_steps = 30
features, labels = [], []

for i in range(len(df) - n_steps):
    # Collect 30 recent rows as input feature sequence
    features.append(df.iloc[i:i+n_steps].values)

    # Output label: 1 = next price change up, 0 = down
    label = 1 if df["close"].iloc[i+n_steps] > 0 else 0
    labels.append(label)

# Convert to numpy arrays for training
features = np.array(features)
labels   = np.array(labels)

# Split dataset into train and test
train_size = int(len(features) * 0.7)
X_train, X_test = features[:train_size],  features[train_size:]
y_train, y_test = labels[:train_size],    labels[train_size:]

# --------------------------------
# Build the neural network model
# --------------------------------
model = Sequential([
    Dense(30, activation="relu", input_shape=X_train[0].shape),
    Dense(20, activation="relu"),
    Flatten(),
    Dense(1, activation="sigmoid")  # output probability of upward price move
])

# Compile with binary classification settings
model.compile(loss="binary_crossentropy", optimizer=Adam(), metrics=["accuracy"])

# Train the model for a few epochs
model.fit(X_train, y_train, epochs=5, verbose=1)

# --------------------------------
# Serialize model to save into ObjectStore
# --------------------------------
model_json = model.to_json()
model_key = "bitcoin_price_predictor"   # This string is the model's storage name

# Save model architecture into ObjectStore
qb.ObjectStore.Save(model_key, model_json)

print("Model saved with key:", model_key)
