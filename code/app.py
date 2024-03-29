from flask import Flask, request, jsonify
import feedparser
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Define model name
model_name = "ProsusAI/finbert"

# Load the tokenizer and model from the Hugging Face model hub
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Only run this code if you want to download the model and tokenizer to your local machine
# # Download and save the tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# tokenizer.save_pretrained('./code/models/finbert/')

# model = AutoModelForSequenceClassification.from_pretrained(model_name)
# model.save_pretrained('./code/models/finbert/')

# # Load the tokenizer and model from the model directory
# tokenizer = AutoTokenizer.from_pretrained('./model/finbert/')
# model = AutoModelForSequenceClassification.from_pretrained('./model/finbert/')

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
        'model': model_name,  # Name of the model being used
        'endpoints': { "/sentiment_analysis": "Sentiment Analysis", "/fetch_rss_feed": "Fetch RSS Feed" },
        'usage': "Send a POST request to the desired endpoint with the required data.",
        'example_request': 'curl -X POST -H "Content-Type: application/json" -d \'{"url": "https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines"}\' http://<fqdn_or_ip>:8080/sentiment_analysis',
        'required_data': { "/sentiment_analysis": "JSON with a 'url' key pointing to an RSS feed", "/fetch_rss_feed": "JSON with a 'url' key pointing to an RSS feed" }
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
    app.run(debug=True)
