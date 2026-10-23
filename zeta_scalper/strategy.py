import os
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
    strategy_name: str = "ema_rsi"
    swing_lookback: int = 20

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

    def validate(self):
        if not self.symbol:
            raise ValueError("symbol cannot be empty")
        if self.initial_cash <= 0:
            raise ValueError("initial_cash must be > 0")
        if self.stop_loss_pct <= 0 or self.take_profit_pct <= 0:
            raise ValueError("stop_loss_pct and take_profit_pct must be > 0")
        if self.live_trading and not self.api_key and not os.getenv("BROKER_API_KEY"):
            raise ValueError("Live trading requires BROKER_API_KEY or StrategyConfig.api_key")
        if self.live_trading and not self.api_secret and not os.getenv("BROKER_API_SECRET"):
            raise ValueError("Live trading requires BROKER_API_SECRET or StrategyConfig.api_secret")
        valid_names = {"ema_rsi", "ict", "smc"}
        if self.strategy_name not in valid_names:
            raise ValueError(f"Unsupported strategy_name '{self.strategy_name}'. Choose one of {sorted(valid_names)}")

    def apply_env(self):
        self.api_key = self.api_key or os.getenv("BROKER_API_KEY", "")
        self.api_secret = self.api_secret or os.getenv("BROKER_API_SECRET", "")
        self.broker_name = self.broker_name or os.getenv("BROKER_NAME", "binance")
        self.broker_testnet = self.broker_testnet if os.getenv("BROKER_TESTNET") is None else os.getenv("BROKER_TESTNET", "true").lower() == "true"
