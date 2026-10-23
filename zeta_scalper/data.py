import numpy as np
import pandas as pd
import requests


def generate_mock_candles(symbol: str, points: int = 500, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    close = np.empty(points)
    open_prices = np.empty(points)
    high = np.empty(points)
    low = np.empty(points)
    volume = np.empty(points)

    close[0] = 100.0
    open_prices[0] = 100.0 * (1 + rng.normal(0.0, 0.002))

    for i in range(1, points):
        drift = 0.0008 + rng.normal(0.0, 0.004)
        close[i] = close[i - 1] * (1 + drift)
        open_prices[i] = close[i - 1] * (1 + rng.normal(0.0, 0.003))
        high[i] = max(open_prices[i], close[i]) * (1 + rng.uniform(0.001, 0.02))
        low[i] = min(open_prices[i], close[i]) * (1 - rng.uniform(0.001, 0.02))
        volume[i] = max(1.0, rng.integers(500, 5000))

    data = pd.DataFrame(
        {
            "Symbol": symbol,
            "Open": open_prices,
            "High": high,
            "Low": low,
            "Close": close,
            "Volume": volume,
        }
    )
    data.index = pd.date_range(end=pd.Timestamp.utcnow(), periods=points, freq="min")
    return data


def fetch_binance_klines(symbol: str, interval: str = "1m", limit: int = 500) -> pd.DataFrame:
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    rows = response.json()

    columns = ["OpenTime", "Open", "High", "Low", "Close", "Volume", "CloseTime", "QuoteAssetVolume", "NumberOfTrades", "TakerBuyBaseVolume", "TakerBuyQuoteVolume", "Ignore"]
    raw = pd.DataFrame(rows, columns=columns)
    raw["Open"] = raw["Open"].astype(float)
    raw["High"] = raw["High"].astype(float)
    raw["Low"] = raw["Low"].astype(float)
    raw["Close"] = raw["Close"].astype(float)
    raw["Volume"] = raw["Volume"].astype(float)
    raw["OpenTime"] = pd.to_datetime(raw["OpenTime"], unit="ms")
    raw.set_index("OpenTime", inplace=True)
    raw = raw[["Open", "High", "Low", "Close", "Volume"]]
    raw.columns = ["Open", "High", "Low", "Close", "Volume"]
    return raw


def fetch_market_data(symbol: str, timeframe: str = "1m", limit: int = 500, use_mock: bool = True) -> pd.DataFrame:
    if use_mock:
        return generate_mock_candles(symbol=symbol, points=limit)
    try:
        return fetch_binance_klines(symbol=symbol, interval=timeframe, limit=limit)
    except Exception:
        return generate_mock_candles(symbol=symbol, points=limit)


def load_csv_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path, parse_dates=[0])
    data = data.rename(columns={data.columns[0]: "OpenTime"})
    data = data.set_index("OpenTime")
    return data
