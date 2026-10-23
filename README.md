import argparse

from .backtest import run_backtest
from .config import StrategyConfig
from .data import fetch_market_data


def build_parser():
    parser = argparse.ArgumentParser(description="Zeta Scalper trading robot")
    parser.add_argument("--mode", choices=["backtest", "paper"], default="backtest")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--use_mock", action="store_true", default=True)
    return parser


def main():
    args = build_parser().parse_args()

    config = StrategyConfig(symbol=args.symbol)
    data = fetch_market_data(symbol=config.symbol, timeframe=config.timeframe, limit=args.limit, use_mock=args.use_mock)

    if args.mode == "backtest":
        metrics, trades, df = run_backtest(data, config)
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

    else:
        from .paper_trade import PaperTrader
        bot = PaperTrader(config=config, market_data=data)
        bot.run(limit=args.limit, use_mock=args.use_mock)


if __name__ == "__main__":
    main()
