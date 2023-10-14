from sklearn.feature_extraction.text import TfidfVectorizer
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Baca data dari 'data_with_sentiment.json'
with open('data_with_sentiment.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

# Pisahkan data menjadi fitur (teks) dan label (sentimen)
X = [entry['content'] for entry in data]
y = [entry['sentiment'] for entry in data]

# Konversi label sentimen menjadi nilai numerik
label_mapping = {'positif': 1, 'netral': 0, 'negatif': -1}
y = [label_mapping[label] for label in y]

# Bagi data menjadi data latih dan data uji
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
# Data latih
train_data = {'X_train': X_train, 'y_train': y_train}

# Simpan data latih ke dalam file JSON
with open('train_data.json', 'w') as train_file:
    json.dump(train_data, train_file, indent=4)

# Data uji
test_data = {'X_test': X_test, 'y_test': y_test}

# Simpan data uji ke dalam file JSON
with open('test_data.json', 'w') as test_file:
    json.dump(test_data, test_file, indent=4)

# Vektorisasi teks (contoh: TF-IDF)
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Latih model Naive Bayes
naive_bayes_classifier = MultinomialNB()
naive_bayes_classifier.fit(X_train_tfidf, y_train)

# Prediksi sentimen pada data uji
y_pred = naive_bayes_classifier.predict(X_test_tfidf)

# Evaluasi model
accuracy = accuracy_score(y_test, y_pred)
print(f'Akurasi model Naive Bayes: {accuracy:.2f}')
