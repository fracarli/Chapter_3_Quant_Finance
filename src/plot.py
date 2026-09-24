import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def plot_option_prices(option_prices, T):
    """Plots 2D option price evolution across business days."""
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, T), option_prices, label='Option Price with Interest', color='blue', linewidth=2)
    plt.title('Option Price Evolution Over Time')
    plt.xlabel('Time (Days)')
    plt.ylabel('Option Price')
    plt.legend()
    plt.grid(True)
    plt.show()

def print_tree(matrix, name="Tree"):
    """Pretty prints the binomial tree matrix, filtering out unused structural zeros."""
    print(f"--- {name} ---")
    N = matrix.shape[0] - 1
    for i in range(N + 1):
        row_values = [f"{matrix[i, j]:8.2f}" if matrix[i, j] != 0 or (i == 0 and j == 0) else "   .  " for j in range(i + 1)]
        indent = " " * (3 * (N - i))
        print(f"t = {i}: {indent}{'  '.join(row_values)}")
    print()

def plot_option_surface(K, r, sigma, N, T_max, binomial_pricing_func):
    """Generates a 3D Wilmott-style option pricing surface in terms of S0 and T."""
    S0_range = np.linspace(K * 0.5, K * 1.5, 40) 
    T_range = np.linspace(0.001, T_max, 40)         
    
    S_grid, T_grid = np.meshgrid(S0_range, T_range)
    V_grid = np.zeros_like(S_grid)
    
    for i in range(S_grid.shape[0]):
        for j in range(S_grid.shape[1]):
            s_val = S_grid[i, j]
            t_val = T_grid[i, j]
            price, _, _ = binomial_pricing_func(s_val, K, t_val, r, sigma, N, 'call')
            V_grid[i, j] = price
            
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(S_grid, T_grid, V_grid, cmap='plasma', edgecolor='none', alpha=0.9)
    
    ax.set_xlabel('Underlying Price (S0)', labelpad=10)
    ax.set_ylabel('Time to Maturity (T)', labelpad=10)
    ax.set_zlabel('Call Option Price (V)', labelpad=10)
    ax.set_title('Option Pricing Surface: From Expiry Payoff to Time Value', fontsize=12, pad=15)
    
    ax.view_init(elev=30, azim=-125)
    fig.colorbar(surf, shrink=0.5, aspect=5, pad=0.1)
    plt.show()