from transformers import pipeline
import feedparser
import requests

CNN_RSS = 'http://rss.cnn.com/rss/money_markets.rss'
YAHOO_RSS = 'https://finance.yahoo.com/news/rssindex.rss'
BLOOMBERG_RSS = 'https://feeds.bloomberg.com/markets/news.rss'
REUTERS_RSS = 'https://www.reutersagency.com/feed/?best-topics=business-finance'

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

cnnFeed=fetch_rss_feed(CNN_RSS)
yahooFeed=fetch_rss_feed(YAHOO_RSS)
bloombergFeed=fetch_rss_feed(BLOOMBERG_RSS)
reutersFeed=fetch_rss_feed(REUTERS_RSS)

def get_all_headlines(feed):
  all_headlines = []
  
  for entry in feed:
    if 'summary' in entry and entry['summary'] is not None:
      all_headlines.append(entry['summary'])
    else:
      all_headlines.append(entry['title'])
  
  return all_headlines

all_headlines = []
all_headlines.extend(get_all_headlines(cnnFeed))
all_headlines.extend(get_all_headlines(yahooFeed))
all_headlines.extend(get_all_headlines(bloombergFeed))
all_headlines.extend(get_all_headlines(reutersFeed))

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_headlines(max_length=512, chunk_size=400):
    text = " ".join(all_headlines)
    
    tokens = summarizer.tokenizer.tokenize(text)
    
    if len(tokens) > max_length:
      chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]
      chunked_texts = [summarizer.tokenizer.convert_tokens_to_string(chunk) for chunk in chunks]
      
      summaries = [summarizer(chunk, max_length=max_length, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunked_texts]
      
      combined_summary = " ".join(summaries)
      return combined_summary
    else:
      summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)[0]['summary_text']
      return summary