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

load_dotenv()
TRAINER_RSS = os.getenv('TRAINER_RSS')

console = Console()

def fetch_feed():
    feed = feedparser.parse(TRAINER_RSS)
    return feed.entries[:10]

def create_table(entries, selected_index):
    table = Table(title="Latest Podcast Episodes", box=box.SIMPLE)

    table.add_column("Index", justify="center", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta", min_width=60)
    table.add_column("Published", style="green")

    for i, entry in enumerate(entries):
        if i == selected_index:
            table.add_row(
                f"[reverse]{i + 1}[/reverse]",
                f"[reverse]{entry.title}[/reverse]",
                f"[reverse]{entry.published}[/reverse]"
            )
        else:
            table.add_row(
                f"{i + 1}",
                entry.title,
                entry.published
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

def main():
    entries = fetch_feed()
    if not entries:
        console.print("[red]No episodes found![/red]")
        return

    selected_index = 0

    with Live(auto_refresh=False) as live:
        while True:
            live.update(create_table(entries, selected_index), refresh=True)

            key = get_key()

            if key == '\x1b':
                key += get_key()
                key += get_key()
                if key == '\x1b[A':
                    selected_index = (selected_index - 1) % len(entries)
                elif key == '\x1b[B':
                    selected_index = (selected_index + 1) % len(entries)
            elif key == '\n':
                console.print(f"\n[bold]You selected:[/bold] {entries[selected_index].title}\n")
                break
            elif key == 'q':
                break

if __name__ == "__main__":
    main()
