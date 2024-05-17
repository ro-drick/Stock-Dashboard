For this project, my goal was to be able to fetch data from an API but I went a little further and tinkered with the data. I ended up creating a simple interactive dashboard.
I designed the stock dashboard with Streamlit to provide insights into stock data in a user-friendly manner. Users can select a date range to explore detailed pricing and volume data. The dashboard also calculates financial metrics such as annual return, standard deviations and risk-adjusted returns. The dashboard also offers fundamental data on balance sheets, income statements and cash flow statements for the stock being assessed. It also keeps you updated with the latest news related to the stock, giving insights on sentiment.
The dashboard has a portfolio section where users can input their portfolio holdings and weights to assess portfolio metrics, correlations and composition. 
Also included are custom email alerts for me to receive a notification when a stock crosses above or below the long-term Exponential Moving Average.

In the project, I fetch data from:
Alpha vantage
yFinance
StockNews

Libraries I used for the project:

pandas for data manipulation
streamlit for building the dashboard interface
numpy for numerical computations
seaborn, plotly, and matplotlib for data visualization
yfinance for fetching stock data
alpha_vantage for fundamental data analysis
stocknews for retrieving news related to stocks
smtplib, ssl, and email for sending email notifications
datetime for date and time manipulation
