from flask import Flask, render_template, request
import feedparser
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['TRAINER_RSS'] = os.getenv('TRAINER_RSS')

FEEDS = {
    'trainer': app.config['TRAINER_RSS']
}

@app.route('/')
def home():
    feed = feedparser.parse(FEEDS['trainer'])
    return render_template('home.html', entries=feed.entries)

if __name__ == '__main__':
    app.run(debug=True)
