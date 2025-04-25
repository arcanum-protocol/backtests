import datetime
import pandas
import uniswap_utils
import matplotlib.pyplot as plt

class UniswapBacktesting:
    def __init__(self, feed: pandas.DataFrame, init_price: float, lower_bound: float, upper_bound: float, amount0: float, amount1: float):
        self.feed = feed
        self.current_price = init_price

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        liq0 = uniswap_utils.liquidity0(amount0, self.upper_bound, self.current_price)
        liq1 = uniswap_utils.liquidity1(amount1, self.lower_bound, self.current_price)
        self.liq = min(liq0, liq1)

        self.amount0 = uniswap_utils.calc_amount0(self.liq, self.upper_bound, self.current_price)
        self.amount1 = uniswap_utils.calc_amount1(self.liq, self.lower_bound, self.current_price)
        print(f"Initial BTC: {self.amount0:.2f} | Initial USDC: {self.amount1:.2f}")

    def run(self):
        x_values = []
        y_values = []
        for row in self.feed.itertuples(index=False):
            ts = datetime.datetime.strptime(row.ts, "%Y-%m-%d %H:%M:%S")

            if ts < datetime.datetime(2020, 12, 1):
                continue
            elif ts > datetime.datetime(2022, 6, 1):
                break

            self.current_price = row.Close
            if self.current_price > self.lower_bound and self.current_price < self.upper_bound:
                self.amount0 = uniswap_utils.calc_amount0(self.liq, self.upper_bound, self.current_price)
                self.amount1 = uniswap_utils.calc_amount1(self.liq, self.lower_bound, self.current_price)
            elif self.current_price <= self.lower_bound:
                self.amount0 = uniswap_utils.calc_amount0(self.liq, self.upper_bound, self.lower_bound)
                self.amount1 = 0
            elif self.current_price >= self.upper_bound:
                self.amount0 = 0
                self.amount1 = uniswap_utils.calc_amount1(self.liq, self.lower_bound, self.upper_bound)
            
            x_values.append(ts)
            y_values.append(self.amount0 * self.current_price + self.amount1)
        
        self.plot(x_values, y_values)

    def plot(self, x_values, y_values):
        plt.plot(x_values, y_values)
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('Uniswap Backtesting')
        plt.show()

if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv('candles.csv')

    init_price = 19420.0
    usdc = 1_000_000.0 * 0.5
    btc = usdc / init_price

    lower_bound = 17478.0
    upper_bound = 35353.417

    backtest = UniswapBacktesting(df, init_price, lower_bound, upper_bound, btc, usdc)

    backtest.run()