import sys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

if len(sys.argv) > 1:
    text = sys.argv[1]
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    print(json.dumps(sentiment))
