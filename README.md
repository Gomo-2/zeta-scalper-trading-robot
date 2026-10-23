# Zeta Scalper Trading Robot

This project is a Python-based educational scalping trading bot with a mock market-data backtester and a broker/exchange interface for future live deployment.

## Features
- EMA + RSI scalping logic
- Backtesting engine
- Paper trading mode
- Broker adapter framework for live exchange APIs
- Binance Future API adapter
- Risk and order controls

## Installation

```bash
pip install -r requirements.txt
```

## Quick start

### Backtest mode

```bash
python -m zeta_scalper.cli --mode backtest --symbol BTCUSDT --limit 500 --use_mock
```

### Paper trading mode

```bash
python -m zeta_scalper.cli --mode paper --symbol BTCUSDT --limit 500 --use_mock
```

### Live trading mode

Set your broker credentials before running live mode:

```bash
export BROKER_API_KEY="your_api_key"
export BROKER_API_SECRET="your_api_secret"
python -m zeta_scalper.cli --mode live --broker binance --symbol BTCUSDT --live-trading --dry-run --testnet
```

Important:
- `--dry-run` prevents live order placement.
- `--live-trading` enables actual order sending only when you are ready.
- Testnet is enabled by default for safety.

## Broker support

The adapter is designed to work with Binance Futures endpoints. You can extend it to other brokers by creating a new implementation of `BrokerAdapter`.

## Risk warning

This project is for learning and evaluation only. It is not a guaranteed money-making system. Real trading carries market risk and should only be done with a clear risk plan, testnet validation, and responsible capital allocation.
