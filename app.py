#!/usr/bin/env python

import os
import feedparser
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich import box
from dotenv import load_dotenv
import sys
import termios
import tty
import webbrowser

load_dotenv()
TRAINER_RSS = os.getenv('TRAINER_RSS')

console = Console()

def fetch_feed():
    feed = feedparser.parse(TRAINER_RSS)
    return feed.entries[:10]

def create_table(entries, selected_index):
    table = Table(title="🎧 Latest Podcast Episodes", box=box.SIMPLE)

    table.add_column("Index", justify="center", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta", min_width=40)
    table.add_column("Published", style="green", min_width=20)
    table.add_column("Author", style="yellow", min_width=20)

    for i, entry in enumerate(entries):
        author = entry.get("author", "Unknown")
        if i == selected_index:
            table.add_row(
                f"[reverse]{i + 1}[/reverse]",
                f"[reverse]{entry.title}[/reverse]",
                f"[reverse]{entry.published}[/reverse]",
                f"[reverse]{author}[/reverse]"
            )
        else:
            table.add_row(
                f"{i + 1}",
                entry.title,
                entry.published,
                author
            )

    return table

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

def get_link(entry):
    for link in entry.get('links', []):
        if link.get('rel') == 'alternate':
            return link.get('href')
    return None

def open_link(url):
    if url:
        console.print(f"\n[green]Opening:[/green] {url}\n")
        webbrowser.open(url)
    else:
        console.print("\n[red]No link available for this episode.[/red]\n")

def main():
    entries = fetch_feed()
    if not entries:
        console.print("[red]No episodes found![/red]")
        return

    selected_index = 0

    live = Live(auto_refresh=False)
    live.start()

    while True:
        live.update(create_table(entries, selected_index), refresh=True)

        key = get_key()

        if key == '\x1b':  # Arrow keys
            key += get_key()
            key += get_key()
            if key == '\x1b[A':  # Up arrow
                selected_index = (selected_index - 1) % len(entries)
            elif key == '\x1b[B':  # Down arrow
                selected_index = (selected_index + 1) % len(entries)
        elif key == 's':
            selected_entry = entries[selected_index]
            link = get_link(selected_entry)
            open_link(link)
        elif key.lower() == 'q':
            console.print("\n[bold]Exiting...[/bold]")
            break

if __name__ == "__main__":
    main()
