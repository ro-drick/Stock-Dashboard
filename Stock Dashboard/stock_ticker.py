#Importing the libraries I will be using
import os
from dotenv import dotenv_values
import pandas as pd
import streamlit as st 
import numpy as np
import seaborn as sns
import yfinance as yf
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from email.message import EmailMessage
from datetime import datetime
import smtplib, ssl
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews
# Page configuration and adding an icon
st.set_page_config(page_title="Stock Dashboard", page_icon=":chart_with_upwards_trend:")

secrets = dotenv_values('config.env')

# The title and introduction
st.title('Stock Dashboard')
st.write("Welcome to the Stock Dashboard. This dashboard provides insights into stock data, including visualizations, statistics, and custom alerts.")

# Sidebar section to input stock ticker and enter the date range that you want to see the data
st.sidebar.header("Select Stock and Date Range")
ticker = st.sidebar.text_input('Enter Ticker Symbol', value='AAPL')
# Define the start and end date ranges
start_date = st.sidebar.date_input('Start Date', value=datetime(2023, 5, 15))#Default start date is 15/05/2023
end_date = st.sidebar.date_input('End Date')

# Custom alerts 
st.sidebar.header("Custom Alerts")

# Fetch ticker current price
current_price = yf.Ticker(ticker).history(period="1d").iloc[-1]['Close']

# Defining a function to calculate Long term Exponential Moving Average for the ticker
def calculate_long_term_ema(ticker, window):
    data = yf.download(ticker, period="1y")['Adj Close']
    ema = data.ewm(span=window, adjust=False).mean()
    return ema.iloc[-1]

# Calculating the Long-term EMA
long_term_ema_window = 200
long_term_ema = calculate_long_term_ema(ticker, long_term_ema_window)

# Function for sending an email notification when the Long-term EMA crosses 
def send_email_notification(stock_name, alert_type, current_price, long_term_ema, sender_email, receiver_email, password):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    # Create the body of the email message
    message = f"Subject: Alert - {stock_name}\n\n{alert_type} alert for {stock_name}. Current price: {current_price}. Long-term EMA: {long_term_ema}"
    # Establish a secure connection with the SMTP server
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        # Log in to the sender's email account
        server.login(sender_email, password)
        # Send the email
        server.sendmail(sender_email, receiver_email, message)

# Check for the Long-term EMA crossover, compose and send the email
if current_price > long_term_ema:
    st.sidebar.info(f"Alert: {ticker} has crossed above the long-term EMA ({long_term_ema:.2f}). Current Price: {current_price}")
    sender_email = "cheruiyotrodrix@gmail.com"  # Enter your email address
    receiver_email = "bettrodrickcheruiyot@gmail.com"  # Enter recipient email address
    password = secrets["PASSW"]
    send_email_notification(ticker, "EMA Crossover (Above)", current_price, long_term_ema, sender_email, receiver_email, password)

elif current_price < long_term_ema:
    st.sidebar.info(f"Alert: {ticker} has crossed below the long-term EMA ({long_term_ema:.2f}). Current Price: {current_price}")
    sender_email = "cheruiyotrodrix@@gmail.com"
    receiver_email = "bettrodrickcheruiyot@gmail.com"
    password = secrets["PASSW"]
    send_email_notification(ticker, "EMA Crossover (Below)", current_price, long_term_ema, sender_email, receiver_email, password)

# Fetch Current Price
current_price = yf.Ticker(ticker).history(period="1d").iloc[-1]['Close']

# Display Stock Price and Long-term EMA
st.header("Stock Overview")
st.subheader("Stock Price and Long-term EMA")
st.write(f"Current Price: {current_price}")
st.write(f"Long-term EMA ({long_term_ema_window}): {long_term_ema}")

# Fetch stock data from start_date and end_date
@st.cache
def load_data(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)

try:
    data = yf.download(ticker,start=start_date,end=end_date)
    if data.empty:
        st.error("No data found for the provided ticker symbol and date range.")
    else:
        selected_chart = st.sidebar.selectbox("Select Chart", ["Candlestick Chart", "Line Chart"])
        # Plot candlestick chart
        if selected_chart == "Candlestick Chart":
            candlestick = go.Candlestick(x=data.index,
                                        open=data['Open'],
                                        high=data['High'],
                                        low=data['Low'],
                                        close=data['Close'],
                                        name="Candlestick")

            candlestick_fig = go.Figure(data=[candlestick])

            candlestick_fig.update_traces(
                increasing_fillcolor='#00cc94',  
                decreasing_fillcolor='#ff6666',  
                line=dict(width=1),  
            )
            candlestick_fig.update_layout(
                title=f"{ticker} Candlestick Chart",
                xaxis_title="Date",
                yaxis_title="Price",
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                font=dict(color="white"),
            )
            st.plotly_chart(candlestick_fig)

        else:
            colors = px.colors.qualitative.Plotly            
            line_chart = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Price", template='plotly_dark')
            line_chart.update_traces(
                line=dict(color=colors[0], width=2),
                mode='lines+markers',
                marker=dict(color=colors[0], size=2),
            )
            line_chart.update_layout(
                xaxis=dict(title="Date"),
                yaxis=dict(title="Price"),
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                font=dict(color="white"),
                showlegend=False,
                xaxis_showgrid=True,
                yaxis_showgrid=True,
            )
            st.plotly_chart(line_chart)

        # Financial ratios
        st.subheader('Financial Ratios')
        market_cap = yf.Ticker(ticker).info.get('marketCap', 'N/A')
        pe_ratio = yf.Ticker(ticker).info.get('forwardPE', 'N/A')
        roe_ratio = yf.Ticker(ticker).info.get('returnOnEquity', 'N/A')
        st.write('**Market Cap:**', market_cap)
        st.write('**P/E Ratio:**', pe_ratio)
        st.write('**Return on Equity (ROE):**', roe_ratio)

        #Pricing data
        pricing_data, fundamental_data, news, basic_statistics, daily_returns, correlations = st.tabs(['Pricing Data', 'Fundamental Data', 'Top 10 News','Basic Statistics', 'Daily Returns', 'Correlations'])
        with pricing_data:
            st.header('Pricing Data')
            data['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1)-1
            data.dropna(inplace=True)
            st.write(data)
            annual_return = data['% Change'].mean()*252*100
            st.write('**Annual Return:** ',round(annual_return,2),'%')
            stdev = np.std(data['% Change'])*np.sqrt(252)
            st.write('Standard Deviation is ',round(stdev*100,2),'%')
            st.write('Risk Adj. Return is ',round(annual_return/(stdev*100),2))

        #News data
        with news:
            st.header(f'Top 10 News {ticker}')
            sn = StockNews(ticker, save_news=False)
            df_news = sn.read_rss()
            for i in range(10):
                st.subheader(f'News {i+1}')
                st.write(df_news['published'][i])
                st.write(df_news['title'][i])
                st.write(df_news['summary'][i])
                title_sentiment = df_news['sentiment_title'][i]
                st.write(f'Title Sentiment {title_sentiment}')
                news_sentiment = df_news['sentiment_summary'][i]
                st.write(f'News Sentiment {news_sentiment}')

        # Basic statistics
        with basic_statistics:
            st.subheader('Basic Statistics')
            statistics = data.describe()
            st.write(statistics)
            # Data export
            st.subheader('Data Export')
            if st.button("Export Data as CSV"):
                data.to_csv(f"{ticker}_data.csv", index=True)
                st.success("Data exported successfully!")

            # Volume chart
            volume_fig = go.Figure()
            volume_fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name="Volume"))
            volume_fig.update_layout(title=f"{ticker} Trading Volume", xaxis_title="Date", yaxis_title="Volume")
            st.plotly_chart(volume_fig)

        # Daily returns
        with daily_returns:
            st.subheader('Daily Returns')
            data['Daily Return'] = data['Close'].pct_change()
            st.line_chart(data['Daily Return'].dropna(), use_container_width=True)
            # Distribution of daily returns
            st.subheader('Distribution of Daily Returns')
            st.plotly_chart(go.Figure(data=[go.Histogram(x=data['Daily Return'].dropna(), nbinsx=50)],
                                        layout=go.Layout(title=f"Distribution of Daily Returns for {ticker}",
                                                        xaxis_title="Daily Return", yaxis_title="Frequency")))

        # Correlation analysis
        with correlations:
            st.subheader('Correlation Analysis')
            index_ticker = st.text_input('Enter Index Ticker (e.g., ^GSPC for S&P 500)', value='^GSPC')
            index_data = yf.download(index_ticker, start=start_date, end=end_date)
            st.subheader('Correlation Matrix Heatmap')
            financials = ['Open', 'High', 'Low', 'Close', 'Volume']
            corr_matrix = data[financials].corr()
            sns.set(font_scale=1.2)
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='crest', fmt=".2f", annot_kws={"size": 10}, linewidths=0.5)
            st.pyplot(plt.gcf())
            if not index_data.empty:
                merged_data = pd.merge(data['Close'], index_data['Close'], left_index=True, right_index=True, suffixes=('_stock', '_index'))
                correlation = merged_data.corr().iloc[0, 1]
                st.write(f"Correlation between {ticker} and {index_ticker}: {correlation:.2f}")
            else:
                st.error("No data found for the provided index ticker symbol and date range.")

        #Fundamental data   
        with fundamental_data:
            key = secrets["API"]
            fd = FundamentalData(key,output_format = 'pandas')
            st.subheader('Fundamental Data')
            st.write('**Balance Sheet**')
            balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
            bs = balance_sheet.T[2:]       
            bs_columns = list(balance_sheet.T.iloc[0])
            st.write(bs)
            #Income Statement
            st.write('Income Statement')
            income_statement = fd.get_income_statement_annual(ticker)[0]
            print(type(income_statement))
            isl = income_statement.T[2:]
            isl.columns = list(income_statement.T.iloc[0])
            st.write(isl)
            #Cashflow Statement
            st.write('Cash Flow Statement')
            cash_flow = fd.get_cash_flow_annual(ticker)[0]
            cf = cash_flow.T[2:]
            cf_columns = list(cash_flow.T.iloc[0])
            st.write(cf)
            st.write('Fundamental')

except Exception as e:
    st.error(f"An error occurred: {str(e)}")

#Portfolio Section
try:
    st.header("Portfolio Analysis")
    st.sidebar.subheader("Enter Portfolio Holdings")

    holdings = []
    weights = []

    num_holdings = st.sidebar.number_input("Number of Holdings", min_value=1, max_value=10, value=3, step=1)
    for i in range(num_holdings):
        col1, col2 = st.sidebar.columns(2)
        with col1:
            holdings.append(st.text_input(f"Holding {i+1} (Ticker Symbol)", value="AAPL"))
        with col2:
            weights.append(st.number_input(f"Weight {i+1} (0-1)", min_value=0.0, max_value=1.0, value=0.25, step=0.01))
    if sum(weights) != 1.0:
        st.error("Weights should sum up to 1.0. Please adjust the weights.")

    portfolio_metrics, portfolio_correlation, portfolio_composition = st.tabs(['Portfolio Metrics', 'Portfolio Correlation', 'Portfolio Composition'])
    #Portfolio metrics
    with portfolio_metrics:
        st.subheader("Portfolio Metrics")
        portfolio_returns = data.pct_change().mean(axis=1)
        portfolio_volatility = data.pct_change().std(axis=1)
        correlation_matrix = data.pct_change().corr()
        col1, col2 = st.columns(2)  
        #Portfolio returns          
        with col1:
            st.write("**Portfolio Returns:**")
            st.write(portfolio_returns)
            #Portfolio volatility
        with col2:
            st.write("**Portfolio Volatility:**")
            st.write(portfolio_volatility)

    # Visualization: Correlation Matrix Heatmap
    with portfolio_correlation:
        st.subheader("Correlation Matrix Heatmap")
        fig_heatmap, ax_heatmap = plt.subplots(figsize=(10,4))
        sns.heatmap(correlation_matrix, annot=True, cmap='crest', fmt=".2f", annot_kws={"size": 10}, linewidths=0.5)
        st.pyplot(fig_heatmap)

    # Visualization: Portfolio Composition
    with portfolio_composition:
        st.subheader("Portfolio Composition")
        fig_pie, ax_pie = plt.subplots(figsize=(6,5))
        ax_pie.pie(weights, labels=holdings, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 5})
        ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig_pie)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")