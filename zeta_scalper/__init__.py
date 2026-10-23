# Zeta Scalper Trading Robot

A broker-ready Python trading robot for education and safe deployment testing.

## Included strategies
- EMA + RSI (default)
- ICT-style breakout / market-structure detection
- SMC-style BOS / structure-break logic

## Features
- EMA + RSI scalping strategy
- ICT-style strategy mode
- SMC-style strategy mode
- Backtesting engine
- Paper trading mode
- Binance Futures broker adapter
- Dry-run and testnet protection
- Environment-based credentials setup

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Setup credentials

Create a `.env` file or export environment variables:

```bash
export BROKER_API_KEY="your_api_key"
export BROKER_API_SECRET="your_api_secret"
export BROKER_NAME="binance"
export BROKER_TESTNET="true"
```

Example:

```bash
cp .env.example .env
```

## Basic usage

### Backtest using EMA + RSI strategy

```bash
python -m zeta_scalper.cli --mode backtest --strategy ema_rsi --symbol BTCUSDT --limit 500 --use_mock
```

### Backtest using ICT strategy

```bash
python -m zeta_scalper.cli --mode backtest --strategy ict --symbol BTCUSDT --limit 500 --use_mock
```

### Backtest using SMC strategy

```bash
python -m zeta_scalper.cli --mode backtest --strategy smc --symbol BTCUSDT --limit 500 --use_mock
```

### Paper trade

```bash
python -m zeta_scalper.cli --mode paper --strategy smc --symbol BTCUSDT --limit 500 --use_mock
```

### Live / testnet-safe mode

```bash
python -m zeta_scalper.cli --mode live --broker binance --strategy ict --symbol BTCUSDT --testnet --dry-run
```

This will check the exchange connection and run the strategy without sending real orders.

### Real order mode

Use only when you are ready and understand the risks:

```bash
python -m zeta_scalper.cli --mode live --broker binance --strategy smc --symbol BTCUSDT --live-trading --dry-run=false --testnet
```

## Important warnings
- This project is educational and not a guaranteed profit system.
- Real trading involves market risk.
- Always validate with testnet before live execution.
- Separate key permissions and account monitoring are strongly recommended.

## Broker support
Current implementation supports Binance Futures with a clean adapter pattern that can be extended for other brokers.
