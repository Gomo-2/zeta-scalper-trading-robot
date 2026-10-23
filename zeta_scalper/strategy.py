import pandas as pd

from .config import StrategyConfig
from .indicators import ema, rsi


def generate_signals(df: pd.DataFrame, config: StrategyConfig) -> pd.DataFrame:
    working = df.copy()
    working["ema_fast"] = ema(working["Close"], config.fast_ema)
    working["ema_slow"] = ema(working["Close"], config.slow_ema)
    working["rsi"] = rsi(working["Close"], config.rsi_period)

    working["signal"] = 0
    for i in range(1, len(working)):
        prev = working.iloc[i - 1]
        curr = working.iloc[i]

        bullish_cross = prev["ema_fast"] <= prev["ema_slow"] and curr["ema_fast"] > curr["ema_slow"]
        bearish_cross = prev["ema_fast"] >= prev["ema_slow"] and curr["ema_fast"] < curr["ema_slow"]

        if bullish_cross and curr["rsi"] >= config.rsi_buy_threshold:
            working.at[working.index[i], "signal"] = 1
        elif bearish_cross and curr["rsi"] <= config.rsi_sell_threshold:
            working.at[working.index[i], "signal"] = -1

    return working


def decide_trade(df: pd.DataFrame, config: StrategyConfig) -> str:
    if df.empty:
        return "HOLD"
    last = df.iloc[-1]
    if last["signal"] > 0:
        return "BUY"
    if last["signal"] < 0:
        return "SELL"
    return "HOLD"
