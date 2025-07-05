from flask import Flask, request, render_template
from textblob import TextBlob
import requests
import re

app = Flask(__name__)

def fetch_youtube_comments(video_url, api_key):
    try:
        video_id = re.search(r"v=([a-zA-Z0-9_-]{11})", video_url).group(1)
    except:
        return []

    url = f"https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&textFormat=plainText&part=snippet&videoId={video_id}&maxResults=20"
    response = requests.get(url)
    comments = []

    if response.status_code == 200:
        data = response.json()
        for item in data.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            polarity = TextBlob(comment).sentiment.polarity
            sentiment = "Positive" if polarity > 0.2 else "Negative" if polarity < -0.2 else "Neutral"
            fake = "Fake" if len(comment.split()) < 5 else "Genuine"
            comments.append((comment, sentiment, fake))
    return comments

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/youtube', methods=['GET', 'POST'])
def youtube_input():
    comments = []
    if request.method == 'POST':
        video_url = request.form['video_url']
        api_key = "YOUR_YOUTUBE_API_KEY"
        comments = fetch_youtube_comments(video_url, api_key)
        return render_template('youtube_result.html', comments=comments)
    return render_template('youtube_input.html')
