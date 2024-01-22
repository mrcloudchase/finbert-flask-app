
# FinBERT Flask Application

This Flask application utilizes the FinBERT model from Hugging Face to perform sentiment analysis on financial news articles obtained via RSS feeds.

## Features

- Fetch RSS feeds from provided URLs.
- Perform sentiment analysis on article titles using the FinBERT model.
- Return sentiment analysis results in JSON format.

## Prerequisites

- Python 3.8 or later.
- `pip` for installing Python packages.
- Access to the internet for downloading the FinBERT model (on first run).

## Installation

Clone the repository and navigate to the application's directory:

```bash
git clone [your-repository-url]
cd [your-app-directory]
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Application

To start the Flask server, run:

```bash
python app.py
```

The server will start on `http://localhost:5000` by default as this is the Flask default.

## Endpoints

- `GET /`: Home route that returns a welcome message.
- `POST /sentiment_analysis`: Takes a JSON payload with a 'url' key for an RSS feed and returns sentiment analysis of the feed's titles.
- `POST /fetch_rss_feed`: Takes a JSON payload with a 'url' key for an RSS feed and returns the parsed feed data.

## Example Usage

Sending a request to the `/sentiment_analysis` endpoint:

```bash
curl -X POST http://<FQDN_OR_IP:<PORT>/sentiment_analysis \
-H 'Content-Type: application/json' \
-d '{"url": "http://feeds.bbci.co.uk/news/rss.xml"}'
```

## License

[Specify your license or licensing terms here]
