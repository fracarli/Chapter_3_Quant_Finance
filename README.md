# Quantitative Finance: Binomial Tree Option Pricing & Greeks

A Python framework for pricing European options and calculating risk sensitivities (The Greeks) using the **Binomial Tree Model (Cox-Ross-Rubinstein)**, inspired by the quantitative foundations presented in Paul Wilmott's textbooks on derivatives (Chapter 3).

This repository serves as an educational library and sandbox to visualize recursive derivative pricing, backward induction, and the multi-dimensional structure of option values.

---

## Simulation Preview

*(Example output illustrating the 3D call option pricing surface as a function of the underlying asset price $S_0$ and time to maturity $T$, highlighting the transition from the expiration payoff to time value).*

---

## Theoretical Background & Chapter 3 Summary (Paul Wilmott)

Pricing complex financial derivatives requires the ability to model the future uncertainty of the underlying asset and price contracts by eliminating market risk. This script translates four fundamental pillars of Chapter 3 into code:

### 1. The Binomial Tree (Cox-Ross-Rubinstein Framework)
Unlike a simple random walk, the binomial tree model for options captures constant asset volatility through a recombining grid structure:
* **Up and Down Factors ($\mathbf{u, d}$):** Over a time step $\Delta t$, the underlying asset price can either move up by a factor $u = e^{\sigma \sqrt{\Delta t}}$ or down by a factor $d = 1 / u$, where $\sigma$ is the annualized volatility.
* **Matrix Structure:** The tree nodes branch out from the initial price $S_0$ up to maturity $T$, mapping all possible future paths of the asset.

### 2. Risk-Neutral Valuation & Backward Induction
To price an option without estimating investors' absolute risk preferences, we assume a **risk-neutral world**:
* **Risk-Neutral Probability ($\mathbf{p}$):** The theoretical probability of an upward price movement is defined as:
  $$p = \frac{e^{r \Delta t} - d}{u - d}$$
* **Backward Induction:** The option value is computed starting from maturity $T$ (where the value is known and equal to the intrinsic payoff, e.g., $\max(S_T - K, 0)$ for a Call) and working backward recursively to $t = 0$. At each preceding node, the option value is the discounted expected value of the subsequent nodes weighted by probability $p$ and discounted at the risk-free rate $r$.

### 3. The Option Greeks (Sensitivities)
The Greeks measure how the option price changes relative to shifts in key market parameters:
* **Delta ($\Delta$):** Measures the sensitivity of the option price to changes in the underlying asset price ($dS$).
* **Gamma ($\Gamma$):** Measures the curvature of Delta, representing how rapidly Delta changes as the underlying price moves.
* **Theta ($\Theta$):** Represents time decay, capturing the loss of option value as time to maturity approaches.
* **Vega ($\nu$):** Measures sensitivity to changes in underlying volatility ($\sigma$).

### 4. The 3D Surface (From Expiry Payoff to Time Value)
The three-dimensional plot clearly demonstrates the transition between the **expiration payoff** (the sharp, piecewise-linear "hockey stick" shape when $T \approx 0$) and the **smooth curve** of the time value when there is ample time remaining until maturity.

---

## Repository Structure

```text
Chapter_3_code/
│
├── main.py              # Main execution script (tree, Greeks, console logs, and plots)
├── src/
│   ├── definition.py    # Mathematical core modules (binomial tree engine and Greeks)
│   └── plot.py          # Visualization tools (ASCII trees, 2D curves, and 3D surfaces)
└── README.md            # Project documentation and theoretical guide