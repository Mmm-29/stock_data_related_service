import yfinance as yf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import pandas as pd


# --- Fetch stock data ---
def get_data(ticker, period="1y"):
    """
    Fetch stock data for a given ticker and period.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL").
        period (str): Data period (e.g., "6mo", "1y", "5y", "ytd", "max").
    
    Returns:
        pd.DataFrame: Stock data with Close column.
    """
    stock_data = yf.download(ticker, period=period)
    return stock_data[['Close']]


# --- Stationarity test (ADF) ---
def stationary_check(close_price):
    adf_test = adfuller(close_price)
    p_value = round(adf_test[1], 3)
    return p_value


# --- Rolling mean (7-day moving average) ---
def get_rolling_mean(close_price):
    rolling_price = close_price.rolling(window=7).mean().dropna()
    return rolling_price




# --- Differencing order finder ---
def get_differencing_order(close_price):
    p_value = stationary_check(close_price)
    d = 0
    while True:
        if p_value > 0.05:
            d += 1
            close_price = close_price.diff().dropna()
            p_value = stationary_check(close_price)
        else:
            break
    return d


# --- Fit ARIMA model ---
def fit_model(data, differencing_order):
    model = ARIMA(data, order=(30, differencing_order, 30))
    model_fit = model.fit()
    forecast_steps = 30
    forecast = model_fit.get_forecast(steps=forecast_steps)
    predictions = forecast.predicted_mean
    return predictions

# --- Evaluate model ---
def evaluate_model(original_price, differencing_order):
    train_data, test_data = original_price[:-30], original_price[-30:]
    predictions = fit_model(train_data, differencing_order)
    rmse = np.sqrt(mean_squared_error(test_data, predictions))
    return round(rmse, 2)



# --- Get future forecast (30 days ahead) ---
def get_forecast(original_price, differencing_order):
    predictions = fit_model(original_price, differencing_order)
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=29)).strftime('%Y-%m-%d')
    forecast_index = pd.date_range(start=start_date, end=end_date, freq='D')
    forecast_df = pd.DataFrame(predictions, index=forecast_index, columns=['Close'])
    return forecast_df



# --- Scale the close price series ---
def scaling(close_price):
    """
    Scales the stock prices to have mean=0 and std=1.
    
    Args:
        close_price (pd.Series): Series of stock closing prices.
        
    Returns:
        scaled_data (np.ndarray): Scaled prices (2D array).
        scaler (StandardScaler): Fitted scaler to inverse transform later.
    """
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(np.array(close_price).reshape(-1, 1))
    return scaled_data, scaler


# --- Inverse scaling to original price ---
def inverse_scaling(scaler, scaled_data):
    """
    Converts scaled prices back to the original scale.
    
    Args:
        scaler (StandardScaler): Fitted scaler.
        scaled_data (np.ndarray or pd.Series): Scaled data to inverse transform.
        
    Returns:
        close_price (np.ndarray): Prices in original scale.
    """
    close_price = scaler.inverse_transform(np.array(scaled_data).reshape(-1, 1))
    return close_price
