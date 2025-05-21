import feedparser
import requests
import os
import sys

def log(message):
    print(message, file=sys.stderr, flush=True)  # flush ensures immediate output

# Configuration
LIST_ID = "1324465914159505414"
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
NITTER_INSTANCE = "https://nitter.net"  # Primary instance
FALLBACK_INSTANCE = "https://nitter.it"  # Backup if primary fails

def get_feed_url(instance):
    return f"{instance}/i/lists/{LIST_ID}/rss"

def send_to_discord(content):
    try:
        response = requests.post(
            WEBHOOK_URL,
            json={"content": content},
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        log(f"Discord post failed: {str(e)}")
        return False

def process_feed(feed_url):
    log(f"Fetching {feed_url}")
    feed = feedparser.parse(feed_url)
    
    if feed.bozo:
        log(f"Feed error: {feed.bozo_exception}")
        return False
    
    if not feed.entries:
        log("No tweets found in feed")
        return False
    
    latest = feed.entries[0]
    message = f"**New Tweet**\n{latest.title}\n🔗 {latest.link}"
    
    log(f"Posting: {latest.link}")
    return send_to_discord(message)

if __name__ == "__main__":
    log("\n=== STARTING RUN ===")
    
    # Try primary instance first
    if not process_feed(get_feed_url(NITTER_INSTANCE)):
        log("Trying fallback instance...")
        process_feed(get_feed_url(FALLBACK_INSTANCE))
    
    log("=== RUN COMPLETE ===")
