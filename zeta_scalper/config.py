from dataclasses import dataclass


@dataclass
class StrategyConfig:
    symbol: str = "BTCUSDT"
    timeframe: str = "1m"
    initial_cash: float = 10_000.0
    max_position_ratio: float = 0.25
    stop_loss_pct: float = 0.015
    take_profit_pct: float = 0.03
    risk_per_trade: float = 0.01
    fast_ema: int = 9
    slow_ema: int = 21
    rsi_period: int = 14
    rsi_buy_threshold: float = 45.0
    rsi_sell_threshold: float = 55.0
    slippage_pct: float = 0.0005
