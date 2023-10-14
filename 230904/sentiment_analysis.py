import sys
from textblob import TextBlob


def analyze_sentiment(text):
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity
    return {
        'polarity': sentiment,
        'compound': sentiment  # For simplicity, we're using 'polarity' as 'compound'
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = sys.argv[1]
        sentiment_data = analyze_sentiment(text)
        print(sentiment_data)
