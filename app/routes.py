from flask import render_template, flash, redirect, url_for, request
import feedparser
from app import app

CNN_RSS = 'http://rss.cnn.com/rss/money_markets.rss'
YAHOO_RSS = 'https://finance.yahoo.com/news/rssindex.rss'
BLOOMBERG_RSS = 'https://feeds.bloomberg.com/markets/news.rss'

@app.route('/')
def index():
  return render_template('index.html')
  
@app.route('/cnn')
def cnn():
  return render_template('feed.html', news_title='CNN', logo='cnn.png', feed=fetch_rss_feed(CNN_RSS))

@app.route('/yahoo')
def yahoo():
  return render_template('feed.html', news_title='Yahoo', logo='yahoo.png', feed=fetch_rss_feed(YAHOO_RSS))

@app.route('/bloomberg')
def bloomberg():
  return render_template('feed.html', news_title='Bloomberg', logo='bloomberg.jpg', feed=fetch_rss_feed(BLOOMBERG_RSS))

def fetch_rss_feed(url):
  entries = []
  feed = feedparser.parse(url)

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