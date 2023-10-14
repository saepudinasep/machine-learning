from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
from data_processing import load_and_process_data


def train_model(train_reviews, train_labels):
    # train_reviews, test_reviews, train_labels, test_labels = load_and_process_data()

    pipeline = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('classifier', MultinomialNB())
    ])

    pipeline.fit(train_reviews, train_labels)

    # Save the trained model to a file
    joblib.dump(pipeline, 'model.pkl')


# train_model(train_reviews, train_labels)
