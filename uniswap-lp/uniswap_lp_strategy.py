import datetime
import pandas
import uniswap_utils
import matplotlib.pyplot as plt

FEE_TIER = 0.003  # 0.3% fee tier for Uniswap V3 BTC-USDC pool

class UniswapLPStrategy:
    def __init__(
            self, 
            feed: pandas.DataFrame,
            init_price: float,
            lower_bound: float,
            upper_bound: float,
            amount0: float,
            amount1: float,
            interval: tuple[datetime.datetime, datetime.datetime] = None
        ):
        self.feed = feed
        self.current_price = init_price
        self.interval = interval

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        liq0 = uniswap_utils.liquidity0(amount0, self.upper_bound, self.current_price)
        liq1 = uniswap_utils.liquidity1(amount1, self.lower_bound, self.current_price)
        self.liq = min(liq0, liq1)

        self.amount0 = uniswap_utils.calc_amount0(self.liq, self.upper_bound, self.current_price)
        self.amount1 = uniswap_utils.calc_amount1(self.liq, self.lower_bound, self.current_price)
        self.fees0 = 0
        self.fees1 = 0
        print(f"Initial BTC: {self.amount0:.2f} | Initial USDC: {self.amount1:.2f}")

    def run(self):
        dates = []
        lp_position_values = []
        lp_position_values_including_fees = []
        volume0 = 0
        volume1 = 0

        prev_amount0 = 0
        prev_amount1 = 0
        for row in self.feed.itertuples(index=False):
            ts = datetime.datetime.strptime(row.ts, "%Y-%m-%d %H:%M:%S")

            if self.interval is not None:
                if ts < self.interval[0]:
                    continue
                elif ts > self.interval[1]:
                    break

            self.current_price = row.Close

            if self.current_price > self.lower_bound and self.current_price < self.upper_bound:
                self.amount0 = uniswap_utils.calc_amount0(self.liq, self.upper_bound, self.current_price)
                self.amount1 = uniswap_utils.calc_amount1(self.liq, self.lower_bound, self.current_price)
                delta_amount0 = self.amount0 - prev_amount0
                delta_amount1 = self.amount1 - prev_amount1
                if delta_amount0 > 0:
                    volume0 += delta_amount0
                    delta_fees0 = delta_amount0 * FEE_TIER
                    self.fees0 += delta_fees0
                else:
                    volume1 += delta_amount1
                    delta_fees1 = delta_amount1 * FEE_TIER
                    self.fees1 += delta_fees1
            elif self.current_price <= self.lower_bound:
                self.amount0 = uniswap_utils.calc_amount0(self.liq, self.upper_bound, self.lower_bound)
                self.amount1 = 0
            elif self.current_price >= self.upper_bound:
                self.amount0 = 0
                self.amount1 = uniswap_utils.calc_amount1(self.liq, self.lower_bound, self.upper_bound)
            
            dates.append(ts)
            lp_position_values.append(self.amount0 * self.current_price + self.amount1)
            lp_position_values_including_fees.append(self.amount0 * self.current_price + self.amount1 + self.fees0 * self.current_price + self.fees1)
            prev_amount0 = self.amount0
            prev_amount1 = self.amount1
        
        print(f"LP Position Value: {lp_position_values[-1]:.2f} USDC")
        print(f"LP Position Value (Including Fees): {lp_position_values_including_fees[-1]:.2f} USDC")
        change = (lp_position_values[-1] - lp_position_values[0]) / lp_position_values[0] * 100
        print(f"Change in Value: {change:.2f}%")
        change = (lp_position_values_including_fees[-1] - lp_position_values_including_fees[0]) / lp_position_values_including_fees[0] * 100
        print(f"Change in Value (Including fees): {change:.2f}%")
        print(f"Fees Earned: {self.fees0:.2f} BTC | {self.fees1:.2f} USDC")
        print(f"Fees Earned (in USDC): {self.fees0 * self.current_price + self.fees1:.2f} USDC")
        print(f"Volume (in USDC): {volume0 * self.current_price + volume1:.2f} USDC")
        
        # self.plot(dates, lp_position_values, lp_position_values_including_fees)

    # def plot(self, dates, lp_position_values, lp_position_values_including_fees):
    #     plt.plot(dates, lp_position_values)
    #     plt.plot(dates, lp_position_values_including_fees)
    #     plt.legend(['LP Position Value', 'LP Position Value (Including Fees)'])
    #     plt.xlabel('Time')
    #     plt.ylabel('Value')
    #     plt.title('Uniswap Backtesting')
    #     plt.show()

