import json
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# Baca data dari file JSON
with open('data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)


# Fungsi untuk mengubah label sentimen ke dalam 5 kelas


def map_sentiment(sentiment):
    if sentiment == "sangat negatif":
        return "sangat negatif"
    elif sentiment == "negatif":
        return "negatif"
    elif sentiment == "netral":
        return "netral"
    elif sentiment == "positif":
        return "positif"
    elif sentiment == "sangat positif":
        return "sangat positif"
    else:
        return "netral"  # Jika label tidak valid, asumsikan sebagai netral


# Pisahkan data menjadi teks ulasan dan label sentimen (jika tersedia)
reviews = [item['content'] for item in data]
labels = [item.get('sentiment', 'netral') for item in data]


# Membuat label sentimen baru
new_labels = [map_sentiment(label) for label in labels]

# Bagi data menjadi data pelatihan (90%) dan data uji (10%)
train_reviews, test_reviews, train_labels, test_labels = train_test_split(
    reviews, new_labels, test_size=0.10, random_state=42)

# Tahap Pre-processing
nltk.download('punkt')
nltk.download('stopwords')

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))


def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    cleaned_tokens = [ps.stem(
        token) for token in tokens if token.isalnum() and token not in stop_words]
    return ' '.join(cleaned_tokens)


preprocessed_train_reviews = [
    preprocess_text(review) for review in train_reviews]
preprocessed_test_reviews = [
    preprocess_text(review) for review in test_reviews]

# Tahap Pembobotan Kata (TF-IDF)
vectorizer = TfidfVectorizer()
tfidf_train_matrix = vectorizer.fit_transform(preprocessed_train_reviews)
tfidf_test_matrix = vectorizer.transform(preprocessed_test_reviews)

# Tahap Pembentukan Model
model = MultinomialNB()
model.fit(tfidf_train_matrix, train_labels)

# Tahap Klasifikasi Sentimen
predicted_sentiments = model.predict(tfidf_test_matrix)

# Menampilkan hasil
for i, review in enumerate(test_reviews):
    print(f"Review: {review}")
    print(f"Sentimen Prediksi: {predicted_sentiments[i]}")
    print(f"Sentimen Sebenarnya: {test_labels[i]}")
    print()

# Evaluasi performa model
accuracy = accuracy_score(test_labels, predicted_sentiments)
print(f"Akurasi: {accuracy}")

classification_rep = classification_report(test_labels, predicted_sentiments)
print("Laporan Klasifikasi:")
print(classification_rep)

confusion_mat = confusion_matrix(test_labels, predicted_sentiments)
print("Matriks Konfusi:")
print(confusion_mat)
