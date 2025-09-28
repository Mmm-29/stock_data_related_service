import streamlit as st
from pages.utils.models_trainer import (
    get_data,
    get_rolling_mean,
    get_differencing_order,
    scaling,
    evaluate_model,
    get_forecast,
    inverse_scaling
)
from pages.utils.utils import Moving_average_forecast
import pandas as pd
import datetime

# --- Page Config ---
st.set_page_config(
    page_title="Stock Prediction",
    page_icon="chart_with_downwards_trend",
    layout="wide",
)

st.title("Stock Prediction (ARIMA Forecast)")

# --- Input Layout ---
col1, col2, col3 = st.columns([1, 3, 1])
today = datetime.date.today()

# Ticker selection + custom input
with col1:
    ticker = st.selectbox(
        "Select a Ticker",
        ["TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "NFLX", "META", "NVDA", "IBM", "ORCL"],
        index=1
    )
    custom_ticker = st.text_input("Or Enter Custom Ticker", "")
    if custom_ticker.strip():
        ticker = custom_ticker.strip().upper()

# Period selection (like in analysis)
with col2:
    period = st.selectbox(
        "Select Period",
        ["6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
        index=2
    )

with col3:
    st.write("Today's Date:")
    st.info(today.strftime("%d %B %Y"))

st.subheader(f"Predicting Next 30 days Close Price for: {ticker}")

# --- Data Prep ---
close_price = get_data(ticker, period)['Close']
rolling_price = get_rolling_mean(close_price)

# Differencing order
differencing_order = get_differencing_order(rolling_price)

# Scaling
scaled_data, scaler = scaling(rolling_price)

# RMSE Evaluation
rmse = evaluate_model(scaled_data, differencing_order)
st.write("**Model RMSE Score:**", rmse)

# --- Forecast next 30 days ---
forecast_scaled = get_forecast(scaled_data, differencing_order)
forecast_scaled['Close'] = inverse_scaling(scaler, forecast_scaled['Close'])

# --- Display Forecast ---
st.write("#### Forecast Data (Next 30 Days)")
st.dataframe(forecast_scaled.sort_index(ascending=True).round(3), height=250)

# --- Merge for Visualization ---
visual_df = pd.concat([rolling_price[-60:], forecast_scaled])  # last 60 days + forecast
st.plotly_chart(Moving_average_forecast(visual_df), use_container_width=True)
