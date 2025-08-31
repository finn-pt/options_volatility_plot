import numpy as np
from typing import Tuple
from scipy.stats import norm

def est_iv(r: float, S: float, C: float, K: float, T: float, call_or_put: str) -> float:
    """
    Uses Newton's Method to estimate implied volatility (via the Black-Scholes
    formula) to within INSERT with INSERT

    Paramaters:
        r (float) - risk free rate
        S (float) - spot price
        C (float) - option price
        K (float) - strike price
        T (float) - time to expiration in years

    Returns: (float) - the estimate for implied volatility
    """
    # Initial guess for IV
    sigma_estimate: float = C * np.sqrt(2 * np.pi / T) / S

    # Iterate through Newton's Method 10 times
    for iteration in range(10):
        est_price, vega = Black_Scholes(r = r, S = S, K = K, T = T, 
        sigma = sigma_estimate, call_or_put = call_or_put)

        # Filter out options that caused Black Scholes to overflow
        if est_price == None:
            break

        # Check Convergence
        loss = est_price - C

        if abs(loss) < 0.0001:
            return sigma_estimate

        # Update estimated volatility according to Newton's Method
        with np.errstate(over = "raise", divide = "raise"):
            try:
                sigma_estimate = sigma_estimate - loss / vega
            except:
                break

    # Options that do not converge within 10 iterations are likely far enough
    # removed from the assumptions of the Black-Scholes model that they should
    # be excluded. These columns with None will later be removed
    return None

def Black_Scholes(r: float, S: float, sigma: float, K: float, T: float, 
    call_or_put: str) -> Tuple[float | None, float | None]:
    """
    Uses the Black Scholes formula to price an option and calculate its vega
    (derivative or price with respect to volatility)

    Paramaters:
        r (float) - risk free rate
        S (float) - spot price
        sigma (float) - volatility
        K (float) - strike price
        T (float) - time to expiration in years


    Returns: (Tuple[float, float]) - the calculated price of the 
    option and its vega
    """
    with np.errstate(over = "raise", divide = "raise"):
        try:
            d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)
        except: 
            return (None, None)

    if call_or_put == "Call":
        return (S * norm.cdf(d1) - np.exp(-r * T) * K * norm.cdf(d2), 
        S * norm.pdf(d1) * np.sqrt(T))
    elif call_or_put == "Put":
        return (np.exp(-r * T) * K * norm.cdf(-d2) - S * norm.cdf(-d1), 
        S * norm.pdf(d1) * np.sqrt(T))
