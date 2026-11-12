from http.server import BaseHTTPRequestHandler
import feedparser
import json
import datetime

FEEDS = [
    {"url": "https://www.filgoal.com/rss/", "cat": "football", "source": "FilGoal"},
    {"url": "https://www.yallakora.com/rss/", "cat": "football", "source": "Yalla Kora"},
    {"url": "https://arabic.goal.com/ar/rss/news/", "cat": "football", "source": "Goal عربي"},
    {"url": "https://www.masrawy.com/rss/news", "cat": "politics", "source": "مصراوي"},
    {"url": "https://www.youm7.com/rss/Section/1/0", "cat": "politics", "source": "اليوم السابع"},
    {"url": "https://gate.ahram.org.eg/rss/RssFeeds.aspx?feedName=1", "cat": "politics", "source": "الأهرام"},
    {"url": "https://www.amwalalghad.com/feed/", "cat": "economy", "source": "أموال الغد"},
    {"url": "https://www.youm7.com/rss/Section/97/0", "cat": "economy", "source": "اليوم السابع اقتصاد"},
]

def parse_date(entry):
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        return datetime.datetime(*entry.published_parsed[:6]).isoformat()
    return datetime.datetime.now().isoformat()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        all_news = []
        for feed in FEEDS:
            try:
                parsed = feedparser.parse(feed["url"])
                for entry in parsed.entries[:10]:
                    all_news.append({
                        "title": entry.get("title", ""),
                        "link": entry.get("link", ""),
                        "date": parse_date(entry),
                        "cat": feed["cat"],
                        "source": feed["source"],
                    })
            except Exception as e:
                print(f"Error: {e}")

        all_news.sort(key=lambda x: x["date"], reverse=True)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(all_news).encode())
