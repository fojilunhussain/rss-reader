#!/usr/bin/env python

import feedparser
from dotenv import load_dotenv
import os

load_dotenv()

rss_url = os.getenv('TRAINER_RSS')

def fetch_podcast():
    feed = feedparser.parse(rss_url)
    return feed.entries

def display_podcasts():
    podcasts = fetch_podcast()
    
    print("Latest Podcast Episodes:")
    for idx, entry in enumerate(podcasts, start=1):
        print(f"{idx}. {entry.title}")
        print(f"   {entry.link}")
        print(f"   {entry.published}")
        print()

if __name__ == "__main__":
    display_podcasts()
