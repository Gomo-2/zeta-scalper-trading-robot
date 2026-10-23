import time

from .config import StrategyConfig
from .data import fetch_market_data
from .strategy import generate_signals, decide_trade


def run_live_strategy(config: StrategyConfig, broker):
    print(f"Starting live strategy for {config.symbol} on {config.broker_name} (testnet={config.broker_testnet})")
    if config.dry_run:
        print("Live mode is running in DRY RUN mode. No real order will be sent.")

    while True:
        try:
            latest_data = fetch_market_data(
                symbol=config.symbol,
                timeframe=config.timeframe,
                limit=200,
                use_mock=False,
            )
            signals = generate_signals(latest_data, config)
            action = decide_trade(signals, config)
            price_response = broker.get_prices(config.symbol)
            last_price = float(price_response["price"])

            if action == "BUY":
                if config.dry_run:
                    print(f"[DRY RUN] BUY signal at {last_price}")
                else:
                    qty = config.live_trade_quantity or (config.initial_cash * config.risk_per_trade / max(last_price, 1e-6))
                    broker.place_market_order(config.symbol, "BUY", qty)
                    print(f"Executed BUY order at {last_price}, qty={qty}")
            elif action == "SELL":
                if config.dry_run:
                    print(f"[DRY RUN] SELL signal at {last_price}")
                else:
                    qty = config.live_trade_quantity or (config.initial_cash * config.risk_per_trade / max(last_price, 1e-6))
                    broker.place_market_order(config.symbol, "SELL", qty)
                    print(f"Executed SELL order at {last_price}, qty={qty}")
            else:
                print(f"No action. Last price: {last_price} | Status: {action}")

            time.sleep(30)
        except KeyboardInterrupt:
            print("Stopping live strategy.")
            break
        except Exception as exc:
            print(f"Live bot error: {exc}")
            time.sleep(15)
