from dataclasses import dataclass, field


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

    # broker integration settings
    broker_name: str = "binance"
    broker_testnet: bool = True
    api_key: str = ""
    api_secret: str = ""
    live_trading: bool = False
    live_trade_quantity: float = 0.0
    order_timeout_seconds: int = 30
    dry_run: bool = True
    alert_channel: str = "console"
    market_data_source: str = "mock"
    extra: dict = field(default_factory=dict)
