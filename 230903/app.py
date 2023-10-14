import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Contoh data ulasan film
reviews = [
    "Film ini sangat bagus, saya suka ceritanya!",
    "Aku sangat kecewa dengan film ini, ceritanya membosankan.",
    "Film ini biasa saja, tidak terlalu istimewa.",
    "Saya merasa campuran antara senang dan kecewa dengan film ini."
]

# Label sentimen untuk setiap ulasan
labels = ["positif", "negatif", "netral", "campuran"]

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


preprocessed_reviews = [preprocess_text(review) for review in reviews]

# Tahap Pembobotan Kata (TF-IDF)
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(preprocessed_reviews)

# Tahap Pembentukan Model
model = MultinomialNB()
model.fit(tfidf_matrix, labels)

# Contoh ulasan yang akan diuji
test_reviews = [
    "Saya sangat menyukai film ini!",
    "Film ini benar-benar buruk, saya tidak merekomendasikannya."
]

# Preprocessing untuk ulasan uji
preprocessed_test_reviews = [
    preprocess_text(review) for review in test_reviews]

# Mengubah ulasan uji menjadi vektor TF-IDF
tfidf_test_matrix = vectorizer.transform(preprocessed_test_reviews)

# Tahap Klasifikasi Sentimen
predicted_sentiments = model.predict(tfidf_test_matrix)

# Menampilkan hasil
for i, review in enumerate(test_reviews):
    print(f"Review: {review}")
    print(f"Sentimen: {predicted_sentiments[i]}")
    print()

# Data validasi atau tes yang terpisah
true_labels_validation = ["positif", "negatif"]

# Prediksi sentimen pada data validasi atau tes yang terpisah
predicted_sentiments_validation = model.predict(tfidf_test_matrix)

# Evaluasi performa model dengan menggunakan data validasi
accuracy = accuracy_score(true_labels_validation,
                          predicted_sentiments_validation)
print(f"Akurasi: {accuracy}")

# Menampilkan laporan klasifikasi yang mencakup presisi, recall, dan F1-score
classification_rep = classification_report(
    true_labels_validation, predicted_sentiments_validation, zero_division=0)
print("Laporan Klasifikasi:")
print(classification_rep)

# Menampilkan matriks konfusi untuk lebih memahami hasil klasifikasi
confusion_mat = confusion_matrix(
    true_labels_validation, predicted_sentiments_validation)
print("Matriks Konfusi:")
print(confusion_mat)
