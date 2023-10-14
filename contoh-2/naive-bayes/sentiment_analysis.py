import joblib
import sys

text = sys.argv[1]

# Load the trained model and vectorizer
classifier = joblib.load('naive_bayes_model.pkl')
vectorizer = joblib.load('count_vectorizer.pkl')

# Transform the input text using the same vectorizer
text_transformed = vectorizer.transform([text])

# Predict sentiment using the trained model
predicted_label = classifier.predict(text_transformed)[0]

print(predicted_label)
