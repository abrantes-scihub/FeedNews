import feedparser
import requests
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
RSS_FEED_URL = "https://nitter.net/i/lists/1324465914159505414"

def check_rss():
    feed = feedparser.parse(RSS_FEED_URL)
    for entry in feed.entries[-5:]:  # Check latest 5 tweets
        message = f"**New Tweet by {entry.author}**\n{entry.title}\n🔗 {entry.link}"
        requests.post(WEBHOOK_URL, json={"content": message})

if __name__ == "__main__":
    check_rss()
