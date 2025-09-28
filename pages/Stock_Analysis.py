# Stock Analysis
import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from pages.utils.utils import candlestick, RSI, MACD, close_chart, Moving_average

# --- Page Config ---
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="chart_with_upwards_trend",
    layout="wide"
)

st.title("Stock Analysis Dashboard")
st.markdown("""
View historical stock data, key metrics, and visualize price trends with technical indicators.  
Use the options below to select the stock, date range, and chart settings.
""")

# --- Sidebar: Stock Selection ---
st.sidebar.header("Select or Enter Stock")

# Popular tickers for dropdown
popular_tickers = ["TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "NFLX"]

# Dropdown
selected_ticker = st.sidebar.selectbox("Choose a stock from list", popular_tickers, index=0)

# Optional text input
custom_ticker = st.sidebar.text_input("Or type a ticker if not in the list", "")

# Final ticker
ticker = custom_ticker.upper() if custom_ticker else selected_ticker

# --- Sidebar: Historical Data Period ---
st.sidebar.header("Select Data Period")
period_option = st.sidebar.selectbox("Period for Table & Chart", 
                                     ["Last 10 days", "Last 50 days", "Last 100 days", 
                                      "5D", "1M", "6M", "YTD", "1Y", "5Y", "MAX"])

# Map period selection to yfinance or row counts
period_map = {
    "Last 10 days": 10,
    "Last 50 days": 50,
    "Last 100 days": 100,
    "5D": "5d",
    "1M": "1mo",
    "6M": "6mo",
    "YTD": "ytd",
    "1Y": "1y",
    "5Y": "5y",
    "MAX": "max"
}

num_period = period_map[period_option]

# --- Fetch Historical Data ---
if isinstance(num_period, int):
    data = yf.Ticker(ticker).history(period="max").tail(num_period).reset_index()
else:
    data = yf.Ticker(ticker).history(period="max").reset_index()

# Remove timezone for plotting
data['Date'] = data['Date'].dt.tz_localize(None)

st.subheader(f"Historical Data for {ticker}")
st.dataframe(data)

# --- Company Info ---
ticker_info = yf.Ticker(ticker).info
st.subheader(f"Company Information: {ticker}")
st.write(ticker_info.get("longBusinessSummary", "No description available."))
st.write("**Sector:**", ticker_info.get("sector", "N/A"))
st.write("**Industry:**", ticker_info.get("industry", "N/A"))
st.write("**Website:**", ticker_info.get("website", "N/A"))
st.write("**Full Time Employees:**", ticker_info.get("fullTimeEmployees", "N/A"))

# --- Key Metrics ---
st.subheader("Key Financial Metrics")
col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame(index=["Market Cap", "Beta", "EPS", "PE Ratio"])
    df['Value'] = [
        ticker_info.get("marketCap") or "N/A",
        ticker_info.get("beta") or "N/A",
        ticker_info.get("trailingEps") or "N/A",
        ticker_info.get("trailingPE") or "N/A"
    ]
    st.dataframe(df)

with col2:
    df2 = pd.DataFrame(index=["Quick Ratio", "Revenue per Share", "Profit Margins", "Debt to Equity", "Return on Assets"])
    df2['Value'] = [
        ticker_info.get("quickRatio") or "N/A",
        ticker_info.get("revenuePerShare") or "N/A",
        ticker_info.get("profitMargins") or "N/A",
        ticker_info.get("debtToEquity") or "N/A",
        ticker_info.get("returnOnAssets") or "N/A"
    ]
    st.dataframe(df2)

# --- Latest Close Price ---
st.subheader("Latest Close Price")
col1, col2, col3 = st.columns(3)
if len(data) >= 2:
    latest_close = float(data['Close'].iloc[-1])
    previous_close = float(data['Close'].iloc[-2])
    daily_change = latest_close - previous_close
    col1.metric("Close Price", f"${latest_close:.2f}", f"${daily_change:.2f}")
elif len(data) == 1:
    latest_close = float(data['Close'].iloc[-1])
    col1.metric("Close Price", f"${latest_close:.2f}", "N/A")
else:
    st.warning("No data available for the selected date range.")

# --- Table: Last N Days ---
st.subheader(f"Historical Table: {period_option}")
st.dataframe(data.tail(10).sort_index(ascending=False).round(4))

# --- Chart Type & Indicator ---
st.subheader("Price Trend & Technical Indicators")
col1, col2, _ = st.columns([2, 2, 6])
with col1:
    chart_type = st.selectbox("Select Chart Type", ["Line", "CandleStick"])
with col2:
    if chart_type == "CandleStick":
        indicator = st.selectbox("Select Indicator", ['RSI', "MACD"])
    else:
        indicator = st.selectbox("Select Indicator", ['RSI', "MACD", "Moving Average"])

# --- Plot Charts ---
if chart_type == 'CandleStick' and indicator == 'RSI':
    st.plotly_chart(candlestick(data, num_period), use_container_width=True)
    st.plotly_chart(RSI(data, num_period), use_container_width=True)

elif chart_type == 'CandleStick' and indicator == 'MACD':
    st.plotly_chart(candlestick(data, num_period), use_container_width=True)
    st.plotly_chart(MACD(data, num_period), use_container_width=True)

elif chart_type == 'Line' and indicator == 'RSI':
    st.plotly_chart(close_chart(data, num_period), use_container_width=True)
    st.plotly_chart(RSI(data, num_period), use_container_width=True)

elif chart_type == 'Line' and indicator == 'Moving Average':
    st.plotly_chart(Moving_average(data, num_period), use_container_width=True)

elif chart_type == 'Line' and indicator == 'MACD':
    st.plotly_chart(close_chart(data, num_period), use_container_width=True)
    st.plotly_chart(MACD(data, num_period), use_container_width=True)

# --- Footer ---
st.markdown("---")
st.markdown("Dashboard powered by **Streamlit** | Data Source: **Yahoo Finance**")
