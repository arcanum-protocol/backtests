import datetime
import pandas as pd
from uniswap_lp_strategy import UniswapLPStrategy

if __name__ == "__main__":
    candles = pd.read_csv('candles.csv')

    init_price = 19420.0
    usdc = 1_000_000.0 * 0.5
    btc = usdc / init_price

    lower_bound = 10374.3
    upper_bound = 36353.417

    strategy_backtest = UniswapLPStrategy(
        candles, 
        init_price,
        lower_bound,
        upper_bound,
        btc,
        usdc,
        interval=(datetime.datetime(2020, 12, 1), datetime.datetime(2022, 6, 1))
    )

    strategy_backtest.run()