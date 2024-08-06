from flask import render_template, flash, redirect, url_for, request
from app import app, models, news

graphs = models.load_graphs()

@app.route('/')
def index():
  return render_template('index.html', gpt_summary=news.summary, graphs=graphs)
  
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
