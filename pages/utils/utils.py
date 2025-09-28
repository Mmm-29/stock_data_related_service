import plotly.graph_objects as go
import dateutil
import pandas as pd
import pandas_ta as pta
import datetime


def filter_data(dataframe, num_period):
    # Ensure 'Date' is datetime
    if 'Date' not in dataframe.columns:
        dataframe = dataframe.reset_index()
    dataframe['Date'] = pd.to_datetime(dataframe['Date'])

    # Get last date
    last_date = dataframe['Date'].iloc[-1]

    # Calculate start date based on period
    if num_period == '1mo':
        date = last_date - dateutil.relativedelta.relativedelta(months=1)
    elif num_period == '5d':
        date = last_date - dateutil.relativedelta.relativedelta(days=5)
    elif num_period == '6mo':
        date = last_date - dateutil.relativedelta.relativedelta(months=6)
    elif num_period == '1y':
        date = last_date - dateutil.relativedelta.relativedelta(years=1)
    elif num_period == '5y':
        date = last_date - dateutil.relativedelta.relativedelta(years=5)
    elif num_period == 'ytd':
        date = datetime.datetime(last_date.year, 1, 1)
    else:
        date = dataframe['Date'].iloc[0]

    # Filter data
    return dataframe[dataframe['Date'] > date]


def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=dataframe['Date'],
        open=dataframe['Open'], high=dataframe['High'],
        low=dataframe['Low'], close=dataframe['Close'],
        increasing_line_color='green', decreasing_line_color='red'
    ))
    fig.update_layout(
        showlegend=False,
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='black',
        paper_bgcolor='#17181A'
    )
    return fig


def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe.RSI,
                             line=dict(width=2, color='blue'), name='RSI'))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[70]*len(dataframe),
                             line=dict(width=2, color='red', dash='dash'), name='Overbought'))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[30]*len(dataframe),
                             line=dict(width=2, color='green', dash='dash'), name='Oversold'))
    fig.update_layout(
        yaxis_range=[0, 100],
        height=250,
        plot_bgcolor='black',
        paper_bgcolor='#17181A',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation='h', y=1.02, x=1, xanchor='right')
    )
    return fig


def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                             mode='lines', line=dict(width=2, color="blue"), name='Open'))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines', line=dict(width=2, color='white'), name='Close'))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             mode='lines', line=dict(width=2, color='orange'), name='High'))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             mode='lines', line=dict(width=2, color='red'), name='Low'))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='black',
        paper_bgcolor="#17181A"
    )
    return fig


def Moving_average(dataframe, num_period):
    dataframe['SMA_50'] = pta.sma(dataframe['Close'], 50)
    dataframe = filter_data(dataframe, num_period)
    fig = close_chart(dataframe)
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],
                             mode='lines', line=dict(width=2, color='purple'), name='SMA 50'))
    return fig


def MACD(dataframe, num_period):
    macd = pta.macd(dataframe['Close']).iloc[:, 0]
    macd_signal = pta.macd(dataframe['Close']).iloc[:, 1]
    dataframe['MACD'] = macd
    dataframe['MACD Signal'] = macd_signal
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MACD'],
                             line=dict(width=2, color='blue'), name='MACD'))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MACD Signal'],
                             line=dict(width=2, color='red', dash='dash'), name='Signal'))
    fig.update_layout(
        height=250,
        plot_bgcolor='black',
        paper_bgcolor='#17181A',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", y=1.02, x=1, xanchor='right')
    )
    return fig
import plotly.graph_objects as go

def Moving_average_forecast(forecast, horizon=30):
    fig = go.Figure()

    # Historical close price
    fig.add_trace(go.Scatter(
        x=forecast.index[:-horizon],
        y=forecast['Close'].iloc[:-horizon],
        mode='lines',
        name='Close Price',
        line=dict(width=2, color='white')
    ))

    # Forecasted close price
    fig.add_trace(go.Scatter(
        x=forecast.index[-horizon:],
        y=forecast['Close'].iloc[-horizon:],
        mode='lines',
        name='Future Close Price',
        line=dict(width=2, color='red')
    ))
    
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=20, b=0),
        plot_bgcolor='black',
        paper_bgcolor='#17181A',
        legend=dict(x=1, y=1, xanchor='right', yanchor='top')
    )

    return fig

