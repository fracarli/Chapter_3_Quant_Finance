"""
Author: Francesco Carli
Year: 2026
Description: 
    Quantitative Finance project implementing single-step and multi-step 
    binomial tree models (Cox-Ross-Rubinstein), option pricing with interest rates, 
    finite-difference Greeks calculation, and 2D/3D visualizations.
"""

import numpy as np
import matplotlib.pyplot as plt

from src.definition import (
    Option_price_call,
    Option_prices_with_interest,
    binomial_tree_pricing,
    calculate_delta,
    calculate_gamma,
    calculate_vega,
    calculate_theta
)
from src.plot import (
    plot_option_prices,
    print_tree,
    plot_option_surface
)

# --------------------------------------------------
# MODEL PARAMETERS
# --------------------------------------------------
S0 = 100        # Current underlying asset price
S_up = 101      # Upward node price (single step)
S_down = 99     # Downward node price (single step)
K = 100         # Strike price
r = 0.05        # Risk-free interest rate (5%)

T_days = 252    # Time horizon in business days
T_years = 1.0   # Time horizon in years
sigma = 0.2     # Volatility (20%)
N = 10          # Number of time steps in the binomial tree

# --------------------------------------------------
# EXECUTION & CONSOLE OUTPUT
# --------------------------------------------------
print(f"Single-step Call Option Price: {Option_price_call(S0, S_up, S_down, K):.4f}")
print(f"Single-step Call Option Price with Interest: {Option_prices_with_interest(S0, S_up, S_down, K, r, T_days):.4f}")

# Multi-step Binomial Tree Pricing (Cox-Ross-Rubinstein)
price, stock_matrix, option_matrix = binomial_tree_pricing(S0, K, T_years, r, sigma, N, 'call')
print(f"Binomial Tree Call Price (N={N}): {price:.4f}\n")

# Print Binomial Trees to Console
print_tree(stock_matrix, "Underlying Asset Price Tree (S)")
print_tree(option_matrix, "Option Value Tree (V)")

# Compute option prices over time (daily decay simulation)
option_prices_over_time = []
for i in range(1, T_days):
    option_prices_over_time.append(Option_prices_with_interest(S0, S_up, S_down, K, r, i))

# Greeks calculation at t=0
delta_today = calculate_delta(stock_matrix, option_matrix)
gamma_today = calculate_gamma(S0, K, T_years, r, sigma, N, 'call')
vega_today = calculate_vega(S0, K, T_years, r, sigma, N, 'call')
theta_today = calculate_theta(S0, K, T_years, r, sigma, N, 'call')

print(f"Delta (t=0): {delta_today:.4f}")
print(f"Gamma (t=0): {gamma_today:.4f}")
print(f"Vega  (t=0): {vega_today:.4f}")
print(f"Theta (t=0): {theta_today:.4f}")

# --------------------------------------------------
# PLOTS GENERATION
# --------------------------------------------------
# 2D Plot: Option price evolution over time
plot_option_prices(option_prices_over_time, T_days)

# 3D Plot: Option price surface (Wilmott style)
plot_option_surface(K, r, sigma, N, T_years, binomial_tree_pricing)