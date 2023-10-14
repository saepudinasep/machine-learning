from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib


# Contoh data latihan (ganti dengan data Anda sendiri)
data = [
    ['Produk ini luar biasa! Saya sangat menyukainya.', 'positive'],
    ['Pelayanan pelanggan yang sangat ramah dan membantu.', 'positive'],
    ['Kualitas produk ini benar-benar bagus.', 'positive'],
    ['Sangat puas dengan pembelian saya, sangat direkomendasikan.', 'positive'],
    ['Tidak sabar untuk membeli lagi, produk ini luar biasa.', 'positive'],
    ['Produk ini sangat buruk kualitasnya, sangat mengecewakan.', 'negative'],
    ['Pengiriman sangat lambat dan barang datang rusak.', 'negative'],
    ['Saya tidak senang dengan produk ini, tidak sebanding dengan harganya.', 'negative'],
    ['Sangat mengecewakan, produknya tidak bekerja sama sekali.', 'negative'],
    ['Barang yang saya terima tidak sesuai dengan deskripsi, sangat mengecewakan.', 'negative'],
    ['Produk ini biasa saja, tidak terlalu baik atau buruk.', 'neutral'],
    ['Pelayanannya cukup baik, tapi produknya biasa saja.', 'neutral'],
    ['Saya tidak memiliki pendapat yang kuat tentang produk ini.', 'neutral'],
    ['Tidak ada yang istimewa tentang produk ini.', 'neutral'],
    ['Saya merasa netral tentang pengalaman berbelanja ini.', 'neutral'],
    # ...tambahkan data latihan lainnya di sini
]

# Membagi data latihan menjadi sampel dan label
samples = [row[0] for row in data]
labels = [row[1] for row in data]

# Membuat instance CountVectorizer
vectorizer = CountVectorizer()

# Mentransformasi data teks menjadi vektor
X = vectorizer.fit_transform(samples)

# Membuat instance Naive Bayes classifier
classifier = MultinomialNB()

# Melatih model dengan data latihan
classifier.fit(X, labels)

# Simpan model dan vectorizer menggunakan joblib
joblib.dump(classifier, 'naive_bayes_model.pkl')
joblib.dump(vectorizer, 'count_vectorizer.pkl')
