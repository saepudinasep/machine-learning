import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
from sklearn.model_selection import train_test_split

# Membaca data dari file JSON dengan encoding utf-8
with open('data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Mengambil data array content dan label sentimen sebagai data latihan
samples = [item['content'] for item in data]
labels = [item['label_sentiment']
          for item in data]  # Ubah menjadi field yang sesuai disni error


# Membagi data menjadi 90% data latihan dan 10% data uji
train_samples, test_samples, train_labels, test_labels = train_test_split(
    samples, labels, test_size=0.1, random_state=42)

# Membuat instance CountVectorizer
vectorizer = CountVectorizer()

# Mentransformasi data teks menjadi vektor
X_train = vectorizer.fit_transform(train_samples)

# Membuat instance Naive Bayes classifier
classifier = MultinomialNB()

# Melatih model dengan data latihan
classifier.fit(X_train, train_labels)

# Simpan model dan vectorizer menggunakan joblib
joblib.dump(classifier, 'naive_bayes_model.pkl')
joblib.dump(vectorizer, 'count_vectorizer.pkl')
