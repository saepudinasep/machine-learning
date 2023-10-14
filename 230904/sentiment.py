import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from random import choice

# Membaca data dari file JSON
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Menyimpan konten dari data
contents = [item['content'] for item in data]

# Membuat label sentimen acak ('Negatif', 'Netral', 'Positif') untuk setiap data
labels = [choice(['Negatif', 'Netral', 'Positif']) for _ in contents]

# Menggunakan CountVectorizer untuk mengubah teks menjadi fitur numerik
vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(contents)

# Membuat model Naive Bayes
naive_bayes_classifier = MultinomialNB()
naive_bayes_classifier.fit(X_vectorized, labels)

# Mencetak hasil klasifikasi dalam bentuk tabel
data_table = pd.DataFrame({
    'Text': contents,
    'Actual Sentiment': labels,
    'Predicted Sentiment': naive_bayes_classifier.predict(X_vectorized)
})

print(data_table)

# Mencetak laporan evaluasi (pada data yang sama, karena tidak ada data pengujian)
y_pred = naive_bayes_classifier.predict(X_vectorized)
report = classification_report(labels, y_pred, target_names=[
                               'Negatif', 'Netral', 'Positif'])
print("Laporan Evaluasi:")
print(report)
