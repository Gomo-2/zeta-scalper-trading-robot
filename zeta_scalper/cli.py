import pandas as pd

from .config import StrategyConfig
from .indicators import ema, rsi


def _compute_swing_levels(df: pd.DataFrame, lookback: int = 20):
    recent_high = df["High"].rolling(window=lookback, min_periods=lookback).max()
    recent_low = df["Low"].rolling(window=lookback, min_periods=lookback).min()
    return recent_high, recent_low


def generate_ema_rsi_signals(df: pd.DataFrame, config: StrategyConfig) -> pd.DataFrame:
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


def generate_ict_signals(df: pd.DataFrame, config: StrategyConfig) -> pd.DataFrame:
    working = df.copy()
    working["ema_fast"] = ema(working["Close"], config.fast_ema)
    working["ema_slow"] = ema(working["Close"], config.slow_ema)
    working["rsi"] = rsi(working["Close"], config.rsi_period)
    swing_high, swing_low = _compute_swing_levels(working, config.swing_lookback)
    working["swing_high"] = swing_high
    working["swing_low"] = swing_low
    working["signal"] = 0

    for i in range(1, len(working)):
        prev = working.iloc[i - 1]
        curr = working.iloc[i]
        bullish_ict = (
            curr["Close"] > curr["swing_high"] and
            curr["rsi"] > config.rsi_buy_threshold and
            curr["ema_fast"] > curr["ema_slow"]
        )
        bearish_ict = (
            curr["Close"] < curr["swing_low"] and
            curr["rsi"] < config.rsi_sell_threshold and
            curr["ema_fast"] < curr["ema_slow"]
        )

        if bullish_ict:
            working.at[working.index[i], "signal"] = 1
        elif bearish_ict:
            working.at[working.index[i], "signal"] = -1

    return working


def generate_smc_signals(df: pd.DataFrame, config: StrategyConfig) -> pd.DataFrame:
    working = df.copy()
    working["ema_fast"] = ema(working["Close"], config.fast_ema)
    working["ema_slow"] = ema(working["Close"], config.slow_ema)
    working["rsi"] = rsi(working["Close"], config.rsi_period)
    swing_high, swing_low = _compute_swing_levels(working, config.swing_lookback)
    working["swing_high"] = swing_high
    working["swing_low"] = swing_low
    working["signal"] = 0

    for i in range(1, len(working)):
        prev = working.iloc[i - 1]
        curr = working.iloc[i]

        bullish_bos = prev["Close"] <= prev["swing_high"] and curr["Close"] > curr["swing_high"]
        bearish_bos = prev["Close"] >= prev["swing_low"] and curr["Close"] < curr["swing_low"]

        bullish_smc = bullish_bos and curr["ema_fast"] > curr["ema_slow"] and curr["rsi"] > config.rsi_buy_threshold
        bearish_smc = bearish_bos and curr["ema_fast"] < curr["ema_slow"] and curr["rsi"] < config.rsi_sell_threshold

        if bullish_smc:
            working.at[working.index[i], "signal"] = 1
        elif bearish_smc:
            working.at[working.index[i], "signal"] = -1

    return working


def generate_signals(df: pd.DataFrame, config: StrategyConfig) -> pd.DataFrame:
    strategy_name = getattr(config, "strategy_name", "ema_rsi")
    if strategy_name == "ict":
        return generate_ict_signals(df, config)
    if strategy_name == "smc":
        return generate_smc_signals(df, config)
    return generate_ema_rsi_signals(df, config)


def decide_trade(df: pd.DataFrame, config: StrategyConfig) -> str:
    if df.empty:
        return "HOLD"
    last = df.iloc[-1]
    if last["signal"] > 0:
        return "BUY"
    if last["signal"] < 0:
        return "SELL"
    return "HOLD"
