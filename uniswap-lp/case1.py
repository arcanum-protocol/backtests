import datetime
import pandas as pd
from uniswap_lp_strategy import UniswapLPStrategy

def calculate_lp_performance(
        candles: pd.DataFrame,
        init_price: float,
        lower_bound: float,
        upper_bound: float,
        amount0: float,
        amount1: float,
        interval: tuple[datetime.datetime, datetime.datetime] = None
    ):
    strategy_backtest = UniswapLPStrategy(
        candles, 
        init_price,
        lower_bound,
        upper_bound,
        amount0,
        amount1,
        interval
    )
    strategy_backtest.run()


if __name__ == "__main__":
    candles = pd.read_csv('candles.csv')

    print("------------------------------")
    print("LP position for 1 000 000$")
    print("-------------------------------")
    calculate_lp_performance(
        candles,
        init_price=19420.0,
        lower_bound=10666.673653,
        upper_bound=35356.514342,
        amount0=1_000_000.0 * 0.5 / 19420.0,
        amount1=1_000_000.0 * 0.5,
        interval=(datetime.datetime(2020, 12, 1), datetime.datetime(2022, 6, 1))
    )

    print("------------------------------")
    print("LP position for 10 000 000$")
    print("-------------------------------")

    calculate_lp_performance(
        candles,
        init_price=19420.0,
        lower_bound=10655.147421,
        upper_bound=35394.761339,
        amount0=10_000_000.0 * 0.5 / 19420.0,
        amount1=10_000_000.0 * 0.5,
        interval=(datetime.datetime(2020, 12, 1), datetime.datetime(2022, 6, 1))
    )

    print("------------------------------")
    print("LP position for 100 000 000$")
    print("-------------------------------")
    
    calculate_lp_performance(
        candles,
        init_price=19420.0,
        lower_bound=10647.556726,
        upper_bound=35419.994438,
        amount0=100_000_000.0 * 0.5 / 19420.0,
        amount1=100_000_000.0 * 0.5,
        interval=(datetime.datetime(2020, 12, 1), datetime.datetime(2022, 6, 1))
    )