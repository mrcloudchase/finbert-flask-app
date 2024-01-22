from flask import Flask, request, jsonify
import feedparser
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Initialize tokenizer and model for FinBERT from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

# Create a new Flask web application
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """
    Home route.
    When visited, it returns a welcome message.
    Accessible via HTTP GET request.
    """
    return jsonify({
        'message': 'Welcome to my FinBERT App!',
        'model': model  # Name of the model being used
    })

@app.route('/sentiment_analysis', methods=['POST'])
def sentiment_analysis():
    """
    Sentiment Analysis route.
    Expects a JSON with a 'url' key pointing to an RSS feed.
    Processes the titles in the feed and returns their sentiment analysis.
    Accessible via HTTP POST request.
    """
    # Extract the URL from the received JSON data
    url = request.json['url']

    # Fetch and parse the RSS feed using the URL
    feed = feedparser.parse(url)

    # Mapping of numerical sentiment values to human-readable labels
    sentiment_mapping = {0: 'negative', 1: 'neutral', 2: 'positive'}

    # Extract article titles from the feed
    titles = [entry.title for entry in feed.entries]

    # Prepare the titles for sentiment analysis
    inputs = tokenizer(titles, padding=True, truncation=True, return_tensors="pt")

    # Analyze the sentiment of each title
    outputs = model(**inputs)
    predictions = outputs.logits.argmax(dim=1)

    # Convert numerical predictions to human-readable labels
    predicted_sentiments = [sentiment_mapping[pred.item()] for pred in predictions]

    # Combine each title with its predicted sentiment
    return jsonify(dict(zip(titles, predicted_sentiments)))

@app.route('/fetch_rss_feed', methods=['POST'])
def fetch_rss_feed():
    """
    Fetch RSS Feed route.
    Expects a JSON with a 'url' key pointing to an RSS feed.
    Returns the parsed feed data as JSON.
    Accessible via HTTP POST request.
    """
    # Extract the URL from the received JSON data
    url = request.json['url']

    # Fetch and parse the RSS feed using the URL
    feed = feedparser.parse(url)

    # Format the feed data to be returned as JSON
    formatted_feed = [{'title': entry.title,
                       'link': entry.link,
                       'summary': entry.summary,
                       'published': entry.published} for entry in feed.entries]

    return jsonify(formatted_feed)

# Start the Flask web application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
