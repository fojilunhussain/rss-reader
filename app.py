#!/usr/bin/env python

from rich.console import Console
from rich.table import Table
import feedparser
from dotenv import load_dotenv
import os

load_dotenv()

rss_url = os.getenv('TRAINER_RSS')
console = Console()

def fetch_podcast():
    return feedparser.parse(rss_url).entries

def display_podcasts():
    podcasts = fetch_podcast()
    
    table = Table(title="🎧 Latest Podcast Episodes", show_header=True, header_style="bold magenta")
    table.add_column("Index", style="cyan", justify="center")
    table.add_column("Title", style="green", justify="left")
    table.add_column("Published", style="yellow", justify="left")

    for idx, entry in enumerate(podcasts, start=1):
        table.add_row(str(idx), entry.title, entry.published)

    console.print(table)

if __name__ == "__main__":
    display_podcasts()
