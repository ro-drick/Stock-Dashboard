<h1>Stock Ticker Dashboard</h1>
For this project, my goal was to be able to fetch data from an API but I went a little further and tinkered with the data. I ended up creating a simple interactive dashboard.

I designed the stock dashboard with Streamlit to provide insights into stock data in a user-friendly manner. Users can select a date range to explore detailed pricing and volume data. The dashboard also calculates financial metrics such as annual return, standard deviations, and risk-adjusted returns. Additionally, it offers fundamental data on balance sheets, income statements, and cash flow statements for the stock being assessed. Furthermore, it keeps you updated with the latest news related to the stock, providing insights on sentiment.

The dashboard has a portfolio section where users can input their portfolio holdings and weights to assess portfolio metrics, correlations, and composition.

Also included are custom email alerts for me to receive a notification when a stock crosses above or below the long-term Exponential Moving Average.

In the project, I fetch data from:
- <a href="https://www.alphavantage.co/">Alpha Vantage</a>
- <a href="https://github.com/ranaroussi/yfinance">Yahoo Finance</a>(This leads to a github repository that explains how to use the API)
- <a href="https://stocknewsapi.com/">StockNews</a>
<hr/>
<img src="https://images.pexels.com/photos/6801648/pexels-photo-6801648.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1" alt="Photo by Anna Nekrashevich from Pexels">
<h2>Requirements</h2>
<a href="https://www.python.org/">Python</a>
<h2>Documents</h2>
<a href="https://github.com/ro-dricks/Tickers/blob/master/Stock_Dashboard/stock_ticker.py">Python Code</a>

<h2>Python Libraries I used for the project:</h2>

<ul>
    <li><a href="https://pandas.pydata.org/">pandas</a></li>
    <li><a href="https://streamlit.io/">Streamlit</a></li>
    <li><a href="https://numpy.org/">numpy</a></li>
    <li><a href="https://seaborn.pydata.org/">seaborn</a></li>
    <li><a href="https://plotly.com/">plotly</a></li>
    <li><a href="https://matplotlib.org/">matplotlib</a></li>
    <li><a href="https://github.com/ranaroussi/yfinance">yfinance</a></li>
    <li><a href="https://www.alphavantage.co/">alpha_vantage</a></li>
    <li><a href="https://stocknewsapi.com/">stockews</a></li>
    <li>smtplib</li>
    <li>ssl</li>
    <li>email</li>
    <li>datetime</li>
</ul>
