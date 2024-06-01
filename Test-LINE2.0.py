import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import pandas_ta as ta

sp500_tickers = ['AAPL', 'MSFT', 'GOOGL', 'FB', 'AMZN']  # Esempio di elenco, estendilo all'intero S&P 500 per un uso reale

def calculate_zfscore(data):
    numerator = (data['Close'] - data['Open']) + 2 * (data['Close'] - data['Low']) - 2 * (data['High'] - data['Close'])
    zfscore = numerator / data['Volume']
    return zfscore * 1e6

def identify_wyckoff_phases(data):
    data['Phase'] = 'None'
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
    data = data[data['Signal'] != 'Hold']
    return data.sort_index()

def calculate_transactions(data, budget):
    shares_owned = {}
    transactions = []

    for index, row in data.iterrows():
        ticker = row['Ticker']
        if ticker not in shares_owned:
            shares_owned[ticker] = 0
        
        if row['Signal'] == 'Buy' and budget >= row['Close']:
            shares_to_buy = budget // row['Close']
            shares_owned[ticker] += shares_to_buy
            budget -= shares_to_buy * row['Close']
            transactions.append((index, ticker, 'Buy', shares_to_buy, row['Close'], shares_owned[ticker], budget))

        elif row['Signal'] == 'Sell' and shares_owned[ticker] > 0:
            shares_to_sell = shares_owned[ticker]  # Decide to sell all or some
            shares_owned[ticker] -= shares_to_sell
            budget += shares_to_sell * row['Close']
            transactions.append((index, ticker, 'Sell', shares_to_sell, row['Close'], shares_owned[ticker], budget))

    transactions_df = pd.DataFrame(transactions, columns=['Date', 'Ticker', 'Type', 'Quantity', 'Price', 'Shares Owned', 'Budget Left'])
    return transactions_df, shares_owned, budget

def plot_candlestick(data, signals):
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])

    buy_signals = signals[signals['Signal'] == 'Buy']
    sell_signals = signals[signals['Signal'] == 'Sell']
    
    fig.add_trace(go.Scatter(
        x=buy_signals.index, y=buy_signals['Close'],
        mode='markers', name='Buy Signal',
        marker=dict(symbol='triangle-up', size=10, color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=sell_signals.index, y=sell_signals['Close'],
        mode='markers', name='Sell Signal',
        marker=dict(symbol='triangle-down', size=10, color='red')
    ))
    
    st.plotly_chart(fig, use_container_width=True)

st.title('Call Analyze Stock App')
selected_tickers = st.multiselect('Select up to 5 stock tickers:', sp500_tickers, default=['AAPL'])
start_date = st.date_input('Start date', pd.to_datetime('2020-01-01'))
end_date = st.date_input('End date', pd.to_datetime('2023-01-01'))
budget = st.number_input('Enter your budget for stock purchase:', value=1000)
initial_shares = st.number_input('Enter initial shares owned:', value=0)

if st.button('Analyze and Trade'):
    combined_data = pd.DataFrame()
    for ticker in selected_tickers:
        data = yf.download(ticker, start=start_date, end=end_date)
        data['Ticker'] = ticker
        combined_data = pd.concat([combined_data, data])

    combined_data.index = pd.to_datetime(combined_data.index)
    combined_data.index = combined_data.index.date
    combined_data = combined_data[['Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]
    combined_data.dropna(inplace=True)
    result = generate_signals(combined_data)

    # Execute trades based on signals
    transaction_log, final_shares, final_budget = calculate_transactions(result, budget)
    st.write(transaction_log)
    st.write(f"Final shares owned: {final_shares}, Final budget: {final_budget}")
    plot_candlestick(combined_data, result)
