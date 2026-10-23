from .config import StrategyConfig
from .data import fetch_market_data
from .strategy import generate_signals, decide_trade


class PaperTrader:
    def __init__(self, config: StrategyConfig, market_data=None):
        self.config = config
        self.market_data = market_data

    def run(self, limit: int = 200, use_mock: bool = True):
        data = self.market_data if self.market_data is not None else fetch_market_data(
            symbol=self.config.symbol,
            timeframe=self.config.timeframe,
            limit=limit,
            use_mock=use_mock,
        )
        signals = generate_signals(data, self.config)
        decision = decide_trade(signals, self.config)
        print(f"Symbol: {self.config.symbol} | Decision: {decision}")
        print(signals.tail(10)[["Close", "ema_fast", "ema_slow", "rsi", "signal"]])
        return signals
