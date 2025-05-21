import feedparser
import requests
import os
import sys

def log(message):
    print(message, file=sys.stderr)

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
RSS_FEED_URL = "https://nitter.it/i/lists/1324465914159505414/rss"  # Using reliable instance

log("=== STARTING ===")

try:
    # 1. Fetch feed
    log("Fetching RSS feed...")
    feed = feedparser.parse(RSS_FEED_URL)
    
    if feed.bozo:
        log(f"⚠️ Feed error: {feed.bozo_exception}")
    else:
        log(f"Found {len(feed.entries)} tweets")
        
        # 2. Process newest 3 tweets
        for entry in feed.entries[:3]:
            tweet_text = entry.title.split('http')[0]  # Remove any URLs from text
            message = f"🐦 **New Tweet**\n{tweet_text}\n🔗 {entry.link}"
            
            log(f"Posting: {tweet_text[:50]}...")
            
            # 3. Send to Discord
            try:
                response = requests.post(
                    WEBHOOK_URL,
                    json={"content": message},
                    timeout=10
                )
                response.raise_for_status()
                log("✅ Posted successfully")
            except Exception as e:
                log(f"❌ Failed to post: {str(e)}")

except Exception as e:
    log(f"🔥 Critical error: {str(e)}")

log("=== FINISHED ===")
