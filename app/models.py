from dateutil.relativedelta import relativedelta
from datetime import datetime
import yfinance as yf
import feedparser
import time
import random

CNN_RSS = 'http://rss.cnn.com/rss/money_markets.rss'
YAHOO_RSS = 'https://finance.yahoo.com/news/rssindex.rss'
BLOOMBERG_RSS = 'https://feeds.bloomberg.com/markets/news.rss'
REUTERS_RSS = 'https://www.reutersagency.com/feed/?best-topics=business-finance'

def load_graphs():
  sp = {
    'title': 'S&P 500 Price Index',
    'data': fetchIndex('^GSPC'),
    'id': 'sp500',
    'color': 'rgb(75, 192, 192)'
  }

  nsdq = {
     'title': 'NASDAQ Composite Index',
     'data': fetchIndex('^IXIC'),
     'id': 'nsdq',
     'color': 'rgb(75, 94, 192)'
  }

  dow = {
    'title': 'Dow Jones Industrial Average',
    'data': fetchIndex('^DJI'),
    'id': 'dowJones',
    'color': 'rgb(75, 192, 141)'
  }

  btc = {
    'title': 'Bitcoin',
    'data': fetchIndex('BTC-USD'),
    'id': 'btcUSD',
    'color': 'rgb(192, 141, 192)'
  }

  return [sp, nsdq, dow, btc]

def fetchIndex(index):
  current_date = datetime.now()
  seven_months_prior = current_date - relativedelta(months=7)
  startDate = seven_months_prior.strftime('%Y-%m-%d')
  endDate = current_date.strftime('%Y-%m-%d')

  response = yf.download(index, start=startDate, end=endDate)
  response.reset_index(inplace=True)

  time.sleep(random.uniform(0.2, 2))

  return response[['Date', 'Close']].to_dict(orient='records')