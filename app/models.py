from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import yfinance as yf
import feedparser
import time
import pandas as pd
import numpy as np
import random
import json

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
  response = load_data(index[1:] + '.json')

  # data is not recent enough
  if response is None:
    current_date = datetime.now()
    seven_months_prior = current_date - relativedelta(months=7)
    startDate = seven_months_prior.strftime('%Y-%m-%d')
    endDate = current_date.strftime('%Y-%m-%d')

    response = yf.download(index, start=startDate, end=endDate)
    response.reset_index(inplace=True)

    time.sleep(random.uniform(0.2, 2))

    save_data(response, index[1:] + '.json')
  else:
    print('Loaded data file ', index[1:] + '.json')

  return response[['Date', 'Close', 'Open']].to_dict(orient='records')

def goodOutlook(data):
  df = pd.DataFrame(data)
  df.set_index('Date', inplace=True)

  return df['Close'].iloc[-1] > df['Open'].iloc[-1]

def trend(data):
  df = pd.DataFrame(data)
  df.set_index('Date', inplace=True)

  return round((df['Close'].iloc[-1] / df['Close'].rolling(window=20).mean().iloc[-1]) * 100, 2)

def volatility(data):
  df = pd.DataFrame(data)
  df.set_index('Date', inplace=True)

  daily_returns = df['Close'].pct_change()
  return round(daily_returns.std() * np.sqrt(252) * 100, 2)  # Percentage

def load_data(filename, max_age_days=1):
  try:
    with open(filename, 'r') as f:
      data_dict = json.load(f)
    
    timestamp = datetime.strptime(data_dict['timestamp'], "%Y-%m-%d %H:%M:%S")
    data_age = datetime.now() - timestamp
    
    if data_age < timedelta(days=max_age_days):
      data = data_dict['data']
      df = pd.DataFrame(data)
      df['Date'] = pd.to_datetime(df['Date'])
      return df
    else:
      return None
  except FileNotFoundError:
    return None

def save_data(data, filename):
  df = pd.DataFrame(data)

  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  df['Date'] = df['Date'].astype(str)
  data_list = df.to_dict(orient='records')

  out = {'timestamp': timestamp, 'data': data_list}
  
  with open(filename, 'w') as f:
    json.dump(out, f)