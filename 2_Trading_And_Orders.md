# Trailing Stop Loss Algorithm

A QuantConnect algorithm implementing a trailing stop loss strategy for QQQ (Invesco QQQ Trust) with dynamic order management.

## Strategy Overview

This algorithm employs a systematic approach to trading QQQ with risk management features:

- **Entry**: Limit orders at current market price
- **Risk Management**: 5% trailing stop loss that moves up with new highs
- **Order Management**: Automatic order updates and timing controls
- **Cooling Period**: 30-day waiting period after stop loss triggers

## Key Features

- **Trailing Stop Loss**: Automatically adjusts stop loss to 5% below the highest price achieved
- **Dynamic Order Updates**: Updates unfilled limit orders after 1 day
- **Portfolio Allocation**: 90% of portfolio allocated to QQQ positions
- **Hourly Resolution**: Uses hourly data for precise execution

## Code Structure

### Main Components

- **Initialize()**: Sets up algorithm parameters, dates, and cash
- **OnData()**: Handles real-time data processing and order management
- **OnOrderEvent()**: Processes order fill events and triggers stop loss orders

### Order Types Used

- `LimitOrder`: For entry positions
- `StopMarketOrder`: For trailing stop loss protection
- `UpdateOrderFields`: For dynamic order price adjustments

## Algorithm Logic

1. **Entry Condition**: Places limit order when not invested and no open orders exist
2. **Order Management**: Updates unfilled limit orders daily to current price
3. **Stop Loss Management**: 
   - Sets initial stop at 5% below entry
   - Trails stop loss upward as price reaches new highs
   - Maintains 5% buffer from highest price
4. **Cooling Period**: Waits 30 days after stop loss execution before re-entering

## Risk Parameters

- **Position Size**: 90% of portfolio
- **Stop Loss**: 5% trailing stop
- **Re-entry Delay**: 30 days after exit

## Requirements

- QuantConnect platform
- QQQ data subscription
- Basic understanding of algorithmic trading

## Usage

1. Clone or copy the code to QuantConnect
2. Ensure QQQ data subscription is active
3. Backtest or run live with appropriate capital
4. Monitor performance metrics and adjust parameters as needed

## Disclaimer

This algorithm is for educational purposes. Past performance does not guarantee future results. Always test strategies thoroughly before deploying with real capital.
