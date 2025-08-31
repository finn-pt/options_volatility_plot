import streamlit as st
import yfinance as yf
from data import get_option_chain
from plotter import plot

if __name__ == "__main__":
    st.set_page_config(page_title="Implied Volatility Surface", layout="centered")
    st.title("Implied Volatility Surface")
    option_type: str = st.radio("Select Option Type", ["Call", "Put"])
    ticker = st.text_input("Enter Ticker")
    if st.button("Display Plot"):
        df = get_option_chain(ticker, option_type)
        st.plotly_chart(plot(df))
