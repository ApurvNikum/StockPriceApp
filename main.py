# import yfinance as yf
# import streamlit as st
#
# st.write("""
# # Simple Stock Price App
#
# Shown are the stock **closing price** and ***volume*** of Google!
#
# """)
#
# # https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
# #define the ticker symbol
# tickerSymbol = 'GOOGL'
# #get data on this ticker
# tickerData = yf.Ticker(tickerSymbol)
# #get the historical prices for this ticker
# tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
# # Open	High	Low	Close	Volume	Dividends	Stock Splits
#
# st.write("""
# ## Closing Price
# """)
# st.line_chart(tickerDf.Close)
# st.write("""
# ## Volume Price
# """)
# st.line_chart(tickerDf.Volume)


import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.write("""
# Simple Stock Price App

Shown are the stock **closing price** and ***volume*** of a selected stock, along with an interactive candlestick chart!

""")

# User inputs

# tickerSymbol = st.text_input('Enter Stock Symbol (e.g., GOOGL):')
input_symbols = st.text_input('Enter Stock Symbols (comma-separated):')
start_date = st.date_input('Start Date', pd.to_datetime('2010-01-01'))
end_date = st.date_input('End Date', pd.to_datetime('2020-12-31'))


if input_symbols:
    # Split the user input into a list of stock symbols
    symbols = [symbol.strip() for symbol in input_symbols.split(',')]

    for symbol in symbols:
        # Get data for the selected stock
        tickerData = yf.Ticker(symbol)
        tickerDf = tickerData.history(period='1d', start='2020-01-01', end='2021-01-01')
# if tickerSymbol:
#     # Get data for the selected stock and date range
#     tickerData = yf.Ticker(tickerSymbol)
#     tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

        if not tickerDf.empty:
# Display stock information
            st.write(f"## Stock Information for {symbol}")
            st.write(f"Company Name: {tickerData.info['longName']}")

        # Display closing price chart
        #     st.write("## Closing Price")
        #     st.line_chart(tickerDf['Close'], use_container_width=True)
    # if not tickerDf.empty:
        # Display stock information
            st.write(f"## Stock Information for {input_symbols}")
            st.write(f"Company Name: {tickerData.info['longName']}")
            st.write(f"Description: {tickerData.info['longBusinessSummary']}")

        # # Display closing price chart
        # st.write("## Closing Price")
        # st.line_chart(tickerDf['Close'])
        # Create a custom line chart with specified color
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=tickerDf.index, y=tickerDf['Close'], mode='lines', name='Closing Price',
                                 line=dict(color='green')))
            fig.update_layout(title='Closing Price Chart', xaxis_title='Date', yaxis_title='Price')
            st.plotly_chart(fig)

        # Display volume chart
            st.write("## Volume Price")
            st.line_chart(tickerDf['Volume'], use_container_width=True)

        # # Create an interactive candlestick chart
        #     st.write("## Interactive Candlestick Chart")
        #     fig = go.Figure(data=[go.Candlestick(
        #     x=tickerDf.index,
        #     open=tickerDf['Open'],
        #     high=tickerDf['High'],
        #     low=tickerDf['Low'],
        #     close=tickerDf['Close']
        # )])

        # Create an enhanced candlestick chart
        fig = go.Figure(data=[go.Candlestick(
            x=tickerDf.index,
            open=tickerDf['Open'],
            high=tickerDf['High'],
            low=tickerDf['Low'],
            close=tickerDf['Close'],
            name='Candlesticks',
            increasing_line_color='green',  # Color for bullish days
            decreasing_line_color='red',    # Color for bearish days
            hoverinfo='x+y+name',           # Additional info on hover
            hoverlabel=dict(font=dict(size=12)),
            text=tickerDf.index.strftime('%Y-%m-%d'),  # Date as text on hover
            whiskerwidth=0.2,               # Width of whiskers
            line=dict(width=1),             # Width of candlestick lines
        )])

        # Customize the layout
        fig.update_layout(
            title=f'Candlestick Chart for {input_symbols}',
            xaxis_title='Date',
            yaxis_title='Price',
            xaxis_rangeslider_visible=True,  # Enable zooming
            margin=dict(l=20, r=20, t=30, b=20),  # Add margins for readability
            plot_bgcolor='white',           # Background color
        )
        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected stock and date range.")

