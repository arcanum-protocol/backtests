from scipy.optimize import minimize
import uniswap_utils
import argparse

def find_price_range(initial_price, initial_amount, lower_bound, upper_bound):     
    def amount_imbalance(x, initial_price, initial_amount):
        Pa, Pb = x
        amount1 = initial_amount * 0.5
        amount0 = amount1 / initial_price

        liq0 = uniswap_utils.liquidity0(amount0, Pb, initial_price)
        liq1 = uniswap_utils.liquidity1(amount1, Pa, initial_price)
        liq = min(liq0, liq1)

        amount0 = uniswap_utils.calc_amount0(liq, Pb, initial_price)
        amount1 = uniswap_utils.calc_amount1(liq, Pa, initial_price)
        return abs(amount0 * initial_price - amount1)

    x = lower_bound
    y = upper_bound

    bounds = [(1, x-x*0.1), (y+y*0.1, 1000000)] # range constraints for Pa and Pb

    x0 = [x - 0.01, y + 0.01] # initial guess

    result = minimize(
        amount_imbalance,
        x0,
        args=(initial_price, initial_amount),
        method='SLSQP',
        bounds=bounds,
    )

    if result.success:
        Pa, Pb = result.x
        return (Pa, Pb)
    else:
        raise ValueError(f"Optimization failed: {result.message}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--initial_price",
        type=float,
        required=True,
    )
    parser.add_argument(
        "-a",
        "--initial_amount",
        type=float,
        required=True,
    )
    parser.add_argument(
        "-l",
        "--lower_bound",
        type=float,
        required=True,
    )
    parser.add_argument(
        "-u",
        "--upper_bound",
        type=float,
        required=True,
    )
    args = parser.parse_args()

    Pa, Pb = find_price_range(
        initial_price=args.initial_price,
        lower_bound=args.lower_bound,
        upper_bound=args.upper_bound
    )
    
    print("Optimal price range for 50/50 token amount:")
    print(f"Lower bound Pa: {Pa:.6f}")
    print(f"Upper bound Pb: {Pb:.6f}")
    print(f"Range width: {Pb - Pa:.6f}")
