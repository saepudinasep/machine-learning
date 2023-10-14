from textblob import TextBlob
import sys

text = sys.argv[1]
blob = TextBlob(text)

if blob.sentiment.polarity > 0:
    sentiment = "positive"
elif blob.sentiment.polarity < 0:
    sentiment = "negative"
else:
    sentiment = "neutral"

print(sentiment)
