import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_ta as ta

def calculate_zfscore(data):
    numerator = (data['Close'] - data['Open']) + 2 * (data['Close'] - data['Low']) - 2 * (data['High'] - data['Close'])
    zfscore = numerator / data['Volume']
    return zfscore * 1e6  # Moltiplica per un fattore di scala per rendere il valore più maneggiabile

def identify_wyckoff_phases(data):
    data['Phase'] = 'None'  # Initialize the column for phases
    for i in range(2, len(data)):
        if data['Close'].iloc[i-2] < data['Close'].iloc[i-1] > data['Close'].iloc[i] and data['Volume'].iloc[i-1] > data['Volume'].iloc[i-2]:
            data['Phase'].iloc[i-1] = 'Distribution'
        if data['Close'].iloc[i-2] > data['Close'].iloc[i-1] < data['Close'].iloc[i] and data['Volume'].iloc[i-1] > data['Volume'].iloc[i-2]:
            data['Phase'].iloc[i-1] = 'Accumulation'
    return data

def generate_signals(data):
    data['ZFScore'] = calculate_zfscore(data)
    data = identify_wyckoff_phases(data)
    data['Signal'] = 'Hold'
    for i in range(1, len(data)):
        if data['Phase'].iloc[i] == 'Accumulation' and data['ZFScore'].iloc[i] > 0 and data['ZFScore'].iloc[i-1] <= 0:
            data['Signal'].iloc[i] = 'Buy'
        elif data['Phase'].iloc[i] == 'Distribution' and data['ZFScore'].iloc[i] < 0 and data['ZFScore'].iloc[i-1] >= 0:
            data['Signal'].iloc[i] = 'Sell'
    return data

def plot_candlestick(data):
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])
    st.plotly_chart(fig, use_container_width=True)

def add_technical_indicators(data):
    # Simple Moving Averages
    data['SMA_20'] = ta.sma(data['Close'], length=20)
    data['SMA_50'] = ta.sma(data['Close'], length=50)

    # Exponential Moving Averages
    data['EMA_20'] = ta.ema(data['Close'], length=20)
    data['EMA_50'] = ta.ema(data['Close'], length=50)

    # Bollinger Bands
    bbands = ta.bbands(data['Close'], length=20, std=2)
    data = pd.concat([data, bbands], axis=1)

    # MACD
    # The ta.macd function returns a DataFrame with three columns: MACD, MACDh (histogram), and MACDs (signal)
    macd = ta.macd(data['Close'], fast=12, slow=26, signal=9)
    data['MACD'] = macd['MACD_12_26_9']
    data['MACD_signal'] = macd['MACDs_12_26_9']
    data['MACD_histogram'] = macd['MACDh_12_26_9']

    # RSI - Relative Strength Index
    data['RSI'] = ta.rsi(data['Close'], length=14)

    # ATR - Average True Range
    data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'], length=14)

    # Stochastic Oscillator
    stoch = ta.stoch(data['High'], data['Low'], data['Close'])
    data['STOCH_k'] = stoch['STOCHk_14_3_3']
    data['STOCH_d'] = stoch['STOCHd_14_3_3']

    # OBV - On-Balance Volume
    data['OBV'] = ta.obv(data['Close'], data['Volume'])

    # MFI - Money Flow Index
    data['MFI'] = ta.mfi(data['High'], data['Low'], data['Close'], data['Volume'], length=14)

    return data

def clean_data(data):
    # Interpola prima per approssimare i valori mancanti
    data.interpolate(method='linear', inplace=True)
    
    # Applica un forward fill per coprire eventuali NaN rimanenti dopo l'interpolazione
    data.fillna(method='ffill', inplace=True)
    
    # In alternativa, considera un backward fill se ci sono ancora NaN
    data.fillna(method='bfill', inplace=True)
    
    return data

def plot_advanced_chart(data):
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.01, 
                        subplot_titles=('Candlestick', 'Volume and OBV', 'RSI and MFI', 'MACD'),
                        specs=[[{"secondary_y": True}], [{"secondary_y": True}], [{"secondary_y": False}], [{"secondary_y": True}]])
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
                                 increasing_line_color='green', decreasing_line_color='red', name='Candlestick'), row=1, col=1, secondary_y=False)
    fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume'), row=2, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(x=data.index, y=data['OBV'], name='OBV', line=dict(color='blue', width=2)), row=2, col=1, secondary_y=True)
    fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI', line=dict(color='red', width=2)), row=3, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(x=data.index, y=data['MFI'], name='MFI', line=dict(color='orange', width=2)), row=3, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], name='MACD', line=dict(color='violet', width=2)), row=4, col=1, secondary_y=False)
    fig.add_trace(go.Scatter(x=data.index, y=data['MACD_signal'], name='MACD Signal', line=dict(color='grey', width=2)), row=4, col=1, secondary_y=False)
    fig.add_trace(go.Bar(x=data.index, y=data['MACD_histogram'], name='MACD Histogram'), row=4, col=1, secondary_y=True)
    fig.update_layout(title='Advanced Stock Analysis', yaxis_title='Price', xaxis_title='Date', showlegend=True, height=1200)
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1, secondary_y=False)
    fig.update_yaxes(title_text="OBV", row=2, col=1, secondary_y=True)
    fig.update_yaxes(title_text="RSI", range=[0,100], row=3, col=1)
    fig.update_yaxes(title_text="MACD", row=4, col=1)
    st.plotly_chart(fig, use_container_width=True)

st.title('Wyckoff Phase and ZFScore Analysis App')
ticker = st.text_input('Enter the stock ticker symbol (e.g., AAPL):', 'AAPL')
start_date = st.date_input('Start date', pd.to_datetime('2020-01-01'))
end_date = st.date_input('End date', pd.to_datetime('2023-01-01'))

if st.button('Analyze'):
    data = yf.download(ticker, start=start_date, end=end_date)
    data.index = pd.to_datetime(data.index)  # Assicurati che l'indice sia datetime
    data.index = data.index.date  # Rimuovi l'ora, modo corretto di assegnazione
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    data.dropna(inplace=True)
    result = generate_signals(data)
    st.write(result[['Close', 'Volume', 'ZFScore', 'Phase', 'Signal']])
    st.write('Filtered Signals:', result[result['Signal'] != 'Hold'][['Close', 'ZFScore', 'Phase', 'Signal']])
    plot_candlestick(data)

if st.button('Analyze PRO'):
    data_pro = yf.download(ticker, start=start_date, end=end_date)
    data_pro.index = pd.to_datetime(data_pro.index)
    data_pro.index = data_pro.index.date
    data_pro = data_pro[['Open', 'High', 'Low', 'Close', 'Volume']]
    data_pro.dropna(inplace=True)
    result_pro = add_technical_indicators(data_pro)
    result_pro = clean_data(result_pro)
    st.write(result_pro)
    plot_advanced_chart(result_pro)
