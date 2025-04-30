import datetime
import pandas as pd
from uniswap_lp_strategy import UniswapLPStrategy
from find_price_range import find_price_range

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

# Case 5: Check price fall
if __name__ == "__main__":
    candles = pd.read_csv('candles.csv')

    init_price = 43369.48
    lower_bound = 32139.47
    upper_bound = 43369.48
    interval = (datetime.datetime(2021, 10, 1), datetime.datetime(2022, 6, 1))

    Pa, Pb = find_price_range(
        initial_price=init_price,
        initial_amount=1_000_000.0,
        lower_bound=lower_bound,
        upper_bound=upper_bound
    )
    print("------------------------------")
    print("LP position for 1 000 000$")
    print("-------------------------------")
    calculate_lp_performance(
        candles,
        init_price=init_price,
        lower_bound=Pa,
        upper_bound=Pb,
        amount0=1_000_000.0 * 0.5 / init_price,
        amount1=1_000_000.0 * 0.5,
        interval=interval
    )

    print("------------------------------")
    print("LP position for 10 000 000$")
    print("-------------------------------")

    Pa, Pb = find_price_range(
        initial_price=init_price,
        initial_amount=10_000_000.0,
        lower_bound=lower_bound,
        upper_bound=upper_bound
    )
    calculate_lp_performance(
        candles,
        init_price=init_price,
        lower_bound=Pa,
        upper_bound=Pb,
        amount0=10_000_000.0 * 0.5 / init_price,
        amount1=10_000_000.0 * 0.5,
        interval=interval
    )

    print("------------------------------")
    print("LP position for 100 000 000$")
    print("-------------------------------")
    Pa, Pb = find_price_range(
        initial_price=init_price,
        initial_amount=100_000_000.0,
        lower_bound=lower_bound,
        upper_bound=upper_bound
    )
    calculate_lp_performance(
        candles,
        init_price=init_price,
        lower_bound=Pa,
        upper_bound=Pb,
        amount0=100_000_000.0 * 0.5 / init_price,
        amount1=100_000_000.0 * 0.5,
        interval=interval
    )