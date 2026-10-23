import argparse
import os

from .backtest import run_backtest
from .broker import get_broker
from .config import StrategyConfig
from .data import fetch_market_data
from .live import run_live_strategy


def build_parser():
    parser = argparse.ArgumentParser(description="Zeta Scalper trading robot")
    parser.add_argument("--mode", choices=["backtest", "paper", "live"], default="backtest")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--use_mock", action="store_true", default=True)
    parser.add_argument("--broker", choices=["binance"], default="binance")
    parser.add_argument("--live-trading", action="store_true", default=False)
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--testnet", action="store_true", default=True)
    parser.add_argument("--api-key", default=os.getenv("BROKER_API_KEY", ""))
    parser.add_argument("--api-secret", default=os.getenv("BROKER_API_SECRET", ""))
    parser.add_argument("--quantity", type=float, default=0.0)
    return parser


def main():
    args = build_parser().parse_args()

    config = StrategyConfig(
        symbol=args.symbol,
        broker_name=args.broker,
        broker_testnet=args.testnet,
        api_key=args.api_key,
        api_secret=args.api_secret,
        live_trading=args.live_trading,
        live_trade_quantity=args.quantity,
        dry_run=args.dry_run,
    )
    config.apply_env()
    config.validate()

    data = fetch_market_data(
        symbol=config.symbol,
        timeframe=config.timeframe,
        limit=args.limit,
        use_mock=args.use_mock,
    )

    if args.mode == "backtest":
        metrics, trades, _ = run_backtest(data, config)
        print("Backtest results")
        print(f"Initial cash: ${metrics['initial_cash']:.2f}")
        print(f"Final value: ${metrics['final_value']:.2f}")
        print(f"Total PnL: ${metrics['total_pnl']:.2f}")
        print(f"Return: {metrics['return_pct']:.2f}%")
        print(f"Trades: {metrics['total_trades']}")
        print(f"Win rate: {metrics['win_rate']:.2f}%")
        print("Last 5 trades:")
        for trade in trades[-5:]:
            print(trade)

    elif args.mode == "paper":
        from .paper_trade import PaperTrader
        bot = PaperTrader(config=config, market_data=data)
        bot.run(limit=args.limit, use_mock=args.use_mock)

    else:
        if not config.api_key or not config.api_secret:
            raise ValueError("For live mode set BROKER_API_KEY and BROKER_API_SECRET or pass --api-key and --api-secret.")
        broker = get_broker(config)
        run_live_strategy(config, broker)


if __name__ == "__main__":
    main()
