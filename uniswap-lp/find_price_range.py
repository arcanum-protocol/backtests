from scipy.optimize import minimize
import uniswap_utils

current_price = 19420.0

# Target: equal amounts of tokens
def amount_imbalance(x, current_price, initial_amount):
    Pa, Pb = x
    amount1 = initial_amount * 0.5
    amount0 = amount1 / current_price
    
    liq0 = uniswap_utils.liquidity0(amount0, Pb, current_price)
    liq1 = uniswap_utils.liquidity1(amount1, Pa, current_price)
    liq = min(liq0, liq1)
    
    amount0 = uniswap_utils.calc_amount0(liq, Pb, current_price)
    amount1 = uniswap_utils.calc_amount1(liq, Pa, current_price)
    return abs(amount0 * current_price - amount1)

x = 19420.0  # upper limit for Pa
y = 32139.47 # lower limit for Pb

# Bounds: sqrtPa < sqrtP_upper, sqrtPb > sqrtP_lower
bounds = [(1, x-x*0.1), (y+y*0.1, 100000)]  # reasonable upper limit

# Initial guess: some range between constraints
x0 = [x - 0.01, y + 0.01]

# Run optimization
result = minimize(
    amount_imbalance,
    x0,
    args=(current_price, 1_000_000.0),
    method='SLSQP',
    bounds=bounds,
    # options={'ftol': 1e-10}
)

if result.success:
    Pa, Pb = result.x
    print("Optimal price range for 50/50 token amount:")
    print(f"Lower bound Pa: ${Pa:.6f}")
    print(f"Upper bound Pb: ${Pb:.6f}")
    print(f"Range width: ${Pb - Pa:.6f}")
else:
    print("Optimization failed:", result.message)
