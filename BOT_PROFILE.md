# Zeta Scalper Bot Profile

## Bot Name
Zeta Scalper

## Purpose
Zeta Scalper is an educational algorithmic trading bot designed for short-term market structure and momentum-based execution. It is built to scan price action, identify trade setups, and manage entries, exits, and risk in a structured, rules-based manner.

## Trading Style
- Scalping / short-term trend following
- Intraday swing and momentum logic
- Structure-based decision making using ICT and SMC-inspired concepts
- Multi-strategy support: EMA + RSI, ICT, and SMC

## Supported Strategies
1. EMA + RSI
   - Trend confirmation via moving averages
   - RSI momentum filter
   - Suitable for fast directional scalping

2. ICT-style strategy
   - Structure and liquidity awareness
   - Breakout and retracement confirmation patterns
   - Useful for intraday directional setups

3. SMC-style strategy
   - BOS / break-of-structure detection
   - Trend continuation and reversal confirmation
   - Helps identify market structure shifts

## Markets
- Crypto pairs such as BTC/USDT, ETH/USDT, and other liquid symbols
- Compatible with exchange-style market data sources
- Designed for futures-style trading environments, but adaptable to other market feeds

## Risk Control
- Max position ratio caps
- Stop-loss and take-profit logic
- Risk-per-trade sizing
- Dry-run and testnet default protection
- Broker credential validation before live execution

## Execution Modes
- Backtest mode
- Paper trading mode
- Live broker-ready mode with safety constraints
- Testnet-first deployment workflow

## Broker Compatibility
- Binance Futures adapter included
- Broker abstraction allows extension to other APIs
- Safe defaults prevent live order execution without explicit approval

## Operational Profile
- Runs as a Python-based automation bot
- Uses a modular architecture for data, strategy, execution, and live broker integration
- Designed to be configurable through CLI arguments and environment variables

## Recommended Use
- Research and optimization
- Strategy backtesting
- Paper-trading validation
- Testnet trade simulation before live deployment

## Disclaimer
This bot is for educational and research purposes only. It does not guarantee profitability and should not be treated as financial advice. Real-money trading carries significant risk and should only be done with clear risk management, proper testing, and responsible account controls.

## Summary
Zeta Scalper is a modular, broker-ready trading robot that blends classic technical indicators with ICT/SMC-inspired market structure logic. It is built to support testing, validation, and safe execution workflows while emphasizing controlled risk and strategy transparency.
