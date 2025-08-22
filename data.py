import yfinance as yf
import pandas as pd
from datetime import datetime as dt
from implied_volatility import est_iv

def get_option_chain(ticker: str, call_or_put: str) -> pd.DataFrame:
    """
    Fetches live option chains and uses implied_volatility.py to estimate
    implied volatility

    Parameters:
        ticker (str) - the ticker of the underlying
        call_or_put (str) - whether the options is a call or put

    Returns: (pd.DataFrame) - a pandas data frame comprised of data 
    for strike price ("strike"), time to expiration ("T") and implied volatility
    estimated to within INSERT ("IV")
    """

    # Create Ticker object and get price
    underlying: yf.Ticker = yf.Ticker(ticker)
    spot_price: float = underlying.history(period = "1d")["Close"].iloc[0]

    # Get expiration dates for options on the stock
    expiration_dates: List[str] = underlying.options

    # Probably delete later
    if not expiration_dates:
        print(f"No options expiration dates found for {ticker_symbol}.")
        return None

    # Create data frame
    option_chain_df: pd.DataFrame = pd.DataFrame()

    # Loop through dates
    if call_or_put == "Call":
        for exp_date in expiration_dates:
            option_chain_entry: pd.DataFrame = underlying.option_chain(exp_date).calls
            option_chain_entry['expDate'] = exp_date
            option_chain_df = pd.concat([option_chain_df, option_chain_entry], ignore_index = True)

    if call_or_put == "Put":
        for exp_date in expiration_dates:
            option_chain_entry: pd.DataFrame = underlying.option_chain(exp_date).puts
            option_chain_entry['expDate'] = exp_date
            option_chain_df = pd.concat([option_chain_df, option_chain_entry], ignore_index = True)

    # Calculate moneyness and C (option price) as average between bid and ask
    option_chain_df["C"] = (option_chain_df["bid"] + option_chain_df["ask"]) / 2

    # Change date format
    option_chain_df["expDate"] = pd.to_datetime(option_chain_df["expDate"])
    option_chain_df["T"] = (option_chain_df["expDate"] - dt.now()).dt.days / 365

    #
    option_chain_df = option_chain_df[
        (option_chain_df["T"] > 0) &
        (option_chain_df["C"] > 0) 
    ]

    # Calculate IV
    risk_free_rate: float = get_risk_free_rate()
    option_chain_df["IV"] = option_chain_df.apply(lambda row: est_iv(
        r = risk_free_rate, C = row["C"], T = row["T"], K = row["strike"],
        S = spot_price, call_or_put = call_or_put), axis = 1)

    # Remove options whose price did not converge
    option_chain_df.dropna(subset=['IV'], inplace=True)


    return option_chain_df[["T", "strike", "IV", "C"]]

def get_risk_free_rate() -> float:
    """
    Fetches the risk free rate (assumed to be the yield of a ten year treasury
    bond)

    Paramters: none

    Returns: (float) - the risk free rate as a decimal
    """
    ten_year_yields: yf.Ticker = yf.Ticker("^TNX")
    risk_free_rate: float = ten_year_yields.history(period = "1d")["Close"].iloc[0]
    return risk_free_rate / 100
