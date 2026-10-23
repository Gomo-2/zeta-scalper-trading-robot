import pandas as pd

from .config import StrategyConfig
from .indicators import ema, rsi


def run_backtest(data: pd.DataFrame, config: StrategyConfig):
    df = data.copy()
    df["ema_fast"] = ema(df["Close"], config.fast_ema)
    df["ema_slow"] = ema(df["Close"], config.slow_ema)
    df["rsi"] = rsi(df["Close"], config.rsi_period)

    cash = config.initial_cash
    position_size = 0.0
    position_price = 0.0
    entry_price = None
    trade_log = []
    pnl_history = []

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]
        price = float(row["Close"])

        bullish_signal = (
            prev["ema_fast"] <= prev["ema_slow"]
            and row["ema_fast"] > row["ema_slow"]
            and row["rsi"] >= config.rsi_buy_threshold
        )
        bearish_signal = (
            prev["ema_fast"] >= prev["ema_slow"]
            and row["ema_fast"] < row["ema_slow"]
            and row["rsi"] <= config.rsi_sell_threshold
        )

        if position_size == 0 and bullish_signal:
            max_trade_value = cash * config.max_position_ratio
            risk_value = cash * config.risk_per_trade
            trade_value = min(max_trade_value, risk_value / max(config.stop_loss_pct, 1e-6))
            if trade_value > 0 and cash >= trade_value:
                position_size = trade_value / price
                entry_price = price
                cash -= trade_value
                trade_log.append({"type": "BUY", "price": price, "size": position_size})

        elif position_size > 0:
            stop_price = entry_price * (1 - config.stop_loss_pct)
            take_profit = entry_price * (1 + config.take_profit_pct)

            if bearish_signal or price <= stop_price or price >= take_profit:
                exit_value = position_size * price
                pnl = exit_value - (position_size * entry_price)
                cash += exit_value
                pnl_history.append(pnl)
                trade_log.append({"type": "SELL", "price": price, "size": position_size, "pnl": pnl})
                position_size = 0.0
                entry_price = None

    final_value = cash + position_size * df["Close"].iloc[-1]
    total_pnl = final_value - config.initial_cash

    num_wins = sum(1 for item in trade_log if item.get("pnl", 0) > 0)
    num_losses = sum(1 for item in trade_log if item.get("pnl", 0) < 0)
    total_trades = len([t for t in trade_log if t["type"] == "SELL"])

    metrics = {
        "initial_cash": config.initial_cash,
        "final_value": final_value,
        "total_pnl": total_pnl,
        "return_pct": (final_value / config.initial_cash - 1.0) * 100,
        "total_trades": total_trades,
        "wins": num_wins,
        "losses": num_losses,
        "win_rate": (num_wins / total_trades) * 100 if total_trades else 0.0,
    }
    return metrics, trade_log, df
