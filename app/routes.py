from flask import render_template, jsonify, flash, redirect, url_for, request
from app import app, models, news
import datetime

graphs = models.load_graphs()
goodOutlook = models.goodOutlook(graphs[0]['data'])
trend = models.trend(graphs[0]['data'])
volatility = models.volatility(graphs[0]['data'])

summary = None

def load_summary():
  global summary
  if summary is None:
    summary = news.summarize_headlines()
  return summary

@app.route('/')
def index():
  return render_template('index.html', graphs=graphs, goodOutlook=goodOutlook, trend=trend, volatility=volatility)
  
@app.route('/cnn')
def cnn():
  return render_template('feed.html', news_title='CNN', feed=news.cnnFeed)

@app.route('/yahoo')
def yahoo():
  return render_template('feed.html', news_title='Yahoo', feed=news.yahooFeed)

@app.route('/bloomberg')
def bloomberg():
  return render_template('feed.html', news_title='Bloomberg', feed=news.bloombergFeed)

@app.route('/reuters')
def reuters():
  return render_template('feed.html', news_title='Reuters', feed=news.reutersFeed)

@app.route('/ai-analysis')
def ai_analysis():
  load_summary()
  return jsonify({ "data": summary })