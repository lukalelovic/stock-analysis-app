from flask import render_template, flash, redirect, url_for, request
from app import app
import yfinance as yf
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import feedparser
import requests

CNN_RSS = 'http://rss.cnn.com/rss/money_markets.rss'
YAHOO_RSS = 'https://finance.yahoo.com/news/rssindex.rss'
BLOOMBERG_RSS = 'https://feeds.bloomberg.com/markets/news.rss'
REUTERS_RSS = 'https://www.reutersagency.com/feed/?best-topics=business-finance'

@app.route('/')
def index():
  current_date = datetime.now()
  seven_months_prior = current_date - relativedelta(months=7)

  sp500 = yf.download('^GSPC', start=seven_months_prior.strftime('%Y-%m-%d'), end=current_date.strftime('%Y-%m-%d'))
  sp500.reset_index(inplace=True)

  data = sp500[['Date', 'Close']].to_dict(orient='records')

  return render_template('index.html', data=data)
  
@app.route('/cnn')
def cnn():
  return render_template('feed.html', news_title='CNN', feed=fetch_rss_feed(CNN_RSS))

@app.route('/yahoo')
def yahoo():
  return render_template('feed.html', news_title='Yahoo', feed=fetch_rss_feed(YAHOO_RSS))

@app.route('/bloomberg')
def bloomberg():
  return render_template('feed.html', news_title='Bloomberg', feed=fetch_rss_feed(BLOOMBERG_RSS))

@app.route('/reuters')
def reuters():
  return render_template('feed.html', news_title='Reuters', feed=fetch_rss_feed(REUTERS_RSS))

def fetch_rss_feed(url):
  entries = []
  feed = feedparser.parse(url)

  if not feed.entries:
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    xml = requests.get(url, headers=headers).text
    xml = xml.replace("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", "")
    feed = feedparser.parse(xml)

  for entry in feed.entries:
    title = entry.title
    link = entry.link
    published = entry.published
    summary = entry.summary if 'summary' in entry else None
    thumbnail_url = None

    if 'media_thumbnail' in entry:
        thumbnail_url = entry.media_thumbnail[0].get('url')
    elif 'media_content' in entry:
        # For media content, check if a thumbnail URL is present
        for content in entry.media_content:
            thumbnail_url = content.get('url')
            print(thumbnail_url)
    elif 'enclosures' in entry:
        # Check enclosure for media content
        for enclosure in entry.enclosures:
            if enclosure.get('type', '').startswith('image'):
                thumbnail_url = enclosure.get('url')
    
    entries.append({
      'title': title,
      'link': link,
      'published': published,
      'summary': summary,
      'thumbnail_url': thumbnail_url
    })
  
  return entries