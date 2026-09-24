import numpy as np

def Option_price_call(S0, S_up, S_down, K):
    """Computes basic call option price using a single-step replication portfolio."""
    C_up = max(0.0, S_up - K)
    C_down = max(0.0, S_down - K)
    
    delta = (C_up - C_down) / (S_up - S_down)
    option_price = C_down + delta * (S0 - S_down)
    return option_price

def Option_prices_with_interest(S0, S_up, S_down, K, r, T):
    """Computes single-step call option price incorporating a risk-free interest rate and discount factor."""
    C_up = max(0.0, S_up - K)
    C_down = max(0.0, S_down - K)
    
    delta = (C_up - C_down) / (S_up - S_down)
    discount_factor = 1.0 / (1.0 + r / T)
    
    option_price = C_down * discount_factor + delta * (S0 - S_down * discount_factor)
    return option_price

def binomial_tree_pricing(S0, K, T, r, sigma, N, option_type='call'):
    """
    Computes European option prices using a multi-step binomial tree 
    (Cox-Ross-Rubinstein / Wilmott framework via Backward Induction).
    """
    dt = T / N
    
    # Up and Down multiplicative factors
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    
    # Risk-neutral probability
    p = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)
    
    # Initialize Underlying Stock Price Matrix S
    S = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        for j in range(i + 1):
            S[i, j] = S0 * (u ** j) * (d ** (i - j))
            
    # Initialize Option Value Matrix V at maturity (t = T)
    V = np.zeros((N + 1, N + 1))
    for j in range(N + 1):
        if option_type == 'call':
            V[N, j] = max(0.0, S[N, j] - K)
        elif option_type == 'put':
            V[N, j] = max(0.0, K - S[N, j])
            
    # Backward Induction loop from maturity back to t = 0
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            holding_value = discount * (p * V[i + 1, j + 1] + (1.0 - p) * V[i + 1, j])
            V[i, j] = holding_value
            
    option_price = V[0, 0]
    return option_price, S, V

def calculate_delta(stock_matrix, option_matrix):
    """Computes option Delta at t=0 using the first step nodes of the tree."""
    dS = stock_matrix[1, 1] - stock_matrix[1, 0]
    dV = option_matrix[1, 1] - option_matrix[1, 0]
    return dV / dS

def calculate_gamma(S0, K, T, r, sigma, N, option_type='call'):
    """Computes option Gamma (curvature) using nodes at t=2."""
    if N < 2:
        raise ValueError("Number of steps N must be at least 2 to compute Gamma.")
    
    _, S_matrix, V_matrix = binomial_tree_pricing(S0, K, T, r, sigma, N, option_type)
    
    delta_up = (V_matrix[2, 2] - V_matrix[2, 1]) / (S_matrix[2, 2] - S_matrix[2, 1])
    delta_down = (V_matrix[2, 1] - V_matrix[2, 0]) / (S_matrix[2, 1] - S_matrix[2, 0])
    
    gamma = (delta_up - delta_down) / (0.5 * (S_matrix[2, 2] - S_matrix[2, 0]))
    return gamma

def calculate_theta(S0, K, T, r, sigma, N, option_type='call'):
    """Computes option Theta (time decay) via finite differences with respect to time T."""
    dt = T / N
    eps_t = dt / 2.0
    
    price_base, _, _ = binomial_tree_pricing(S0, K, T, r, sigma, N, option_type)
    price_less_time, _, _ = binomial_tree_pricing(S0, K, T - eps_t, r, sigma, N, option_type)
    
    theta = (price_less_time - price_base) / eps_t
    return theta   

def calculate_vega(S0, K, T, r, sigma, N, option_type='call'):
    """Computes option Vega (volatility sensitivity) via finite differences."""
    eps = 0.001
    price_up, _, _ = binomial_tree_pricing(S0, K, T, r, sigma + eps, N, option_type)
    price_down, _, _ = binomial_tree_pricing(S0, K, T, r, sigma - eps, N, option_type)
    
    vega = (price_up - price_down) / (2 * eps)
    return vega  # Fixed bug: returning lowercase 'vega'