import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Set the maximum number of rows to display
pd.set_option('display.max_rows', None)
# Mengembalikan pengaturan penampilan ke nilai default
pd.reset_option('display.max_rows')


# Baca data dari 'data_with_sentiment.json'
with open('data_with_sentiment.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

# Konversi label sentimen menjadi nilai numerik
label_mapping = {'positif': 1, 'netral': 0, 'negatif': -1}
for entry in data:
    entry['sentiment'] = label_mapping[entry['sentiment']]

# Pisahkan data menjadi fitur (teks) dan label (sentimen)
X = [entry['content'] for entry in data]
y = [entry['sentiment'] for entry in data]

# Bagi data menjadi data latih dan data uji
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Data latih
train_data = {'X_train': X_train, 'y_train': y_train}

# Simpan data latih ke dalam file JSON
with open('train_data_naive_bayes.json', 'w') as train_file:
    json.dump(train_data, train_file, indent=4)

# Data uji
test_data = {'X_test': X_test, 'y_test': y_test}

# Simpan data uji ke dalam file JSON
with open('test_data_naive_bayes.json', 'w') as test_file:
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
classification_rep = classification_report(
    y_test, y_pred, target_names=label_mapping.keys(), zero_division=0)

print(f'Akurasi model Naive Bayes: {accuracy:.2f}')
print('Laporan Klasifikasi:')
print(classification_rep)

# Kamus pemetaan antara nilai numerik dan label sentimen
label_mapping = {-1: 'negatif', 1: 'positif', 0: 'netral'}

# Ganti nilai numerik dalam y_test dengan label sentimen
y_test_sentiment = [label_mapping[val] for val in y_test]

# Ganti nilai numerik dalam y_pred dengan label sentimen
y_pred_sentiment = [label_mapping[val] for val in y_pred]

# Buat DataFrame pandas untuk menampilkan data uji dalam bentuk tabel
test_data_df = pd.DataFrame(
    {'text': X_test, 'sentiment': y_test_sentiment, 'predict': y_pred_sentiment})

# Tampilkan tabel data uji
print(test_data_df[['text', 'sentiment', 'predict']])

# Evaluasi model Naive Bayes
naive_bayes_evaluation = {
    'akurasi': accuracy,
    'laporan_klasifikasi': classification_rep
}

# Simpan evaluasi model Naive Bayes ke dalam file JSON
with open('naive_bayes_evaluation.json', 'w') as nb_eval_file:
    json.dump(naive_bayes_evaluation, nb_eval_file, indent=4)

# Hasil klasifikasi dari model Naive Bayes
naive_bayes_results = {
    'text': X_test,
    'sentiment_true': y_test_sentiment,
    'sentiment_predicted': y_pred_sentiment
}

# Simpan hasil klasifikasi dari model Naive Bayes ke dalam file JSON
with open('naive_bayes_results.json', 'w') as nb_file:
    json.dump(naive_bayes_results, nb_file, indent=4)
