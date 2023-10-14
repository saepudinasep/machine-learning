import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB  # Model Naive Bayes
from sklearn.svm import SVC  # Model SVM
from sklearn.ensemble import RandomForestClassifier  # Model Random Forest
from sklearn.neighbors import KNeighborsClassifier  # Model K-Nearest Neighbors
from sklearn.linear_model import LogisticRegression  # Model Logistic Regression
from sklearn.metrics import accuracy_score, classification_report

# Baca data dari 'data_with_sentiment.json'
with open('data_with_sentiment.json', 'r') as file:
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

# Vektorisasi teks (TF-IDF)
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Inisialisasi model-model
models = {
    'Naive Bayes': MultinomialNB(),  # Model Naive Bayes
    'SVM': SVC(),  # Model SVM
    # Model Random Forest
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'KNN': KNeighborsClassifier(n_neighbors=5),  # Model K-Nearest Neighbors
    # Model Logistic Regression
    'Logistic Regression': LogisticRegression(max_iter=1000)
}

# Membuat dictionary untuk menyimpan hasil klasifikasi untuk setiap model
results = {}

# Latih dan evaluasi setiap model
for model_name, model in models.items():
    model.fit(X_train_tfidf, y_train)
    y_pred = model.predict(X_test_tfidf)

    accuracy = accuracy_score(y_test, y_pred)
    classification_rep = classification_report(
        y_test, y_pred, target_names=label_mapping.keys(), zero_division=0)

    # Simpan hasil evaluasi ke dalam file JSON
    evaluation_result = {
        'accuracy': accuracy,
        'classification_report': classification_rep
    }
    with open(f'{model_name}_evaluation.json', 'w') as json_file:
        json.dump(evaluation_result, json_file, indent=4)

    # Ganti nilai numerik dalam y_test dengan label sentimen
    y_test_sentiment = [key for val in y_test for key,
                        value in label_mapping.items() if value == val]

    # Ganti nilai numerik dalam y_pred dengan label sentimen
    y_pred_sentiment = [key for val in y_pred for key,
                        value in label_mapping.items() if value == val]

    # Buat DataFrame pandas untuk menampilkan hasil klasifikasi dalam bentuk tabel
    classification_df = pd.DataFrame({
        'text': X_test,
        'sentiment': y_test_sentiment,
        'predict': y_pred_sentiment
    })

    # Simpan tabel hasil klasifikasi ke dalam file JSON
    classification_df.to_json(
        f'{model_name}_classification.json', orient='records')

# Tampilkan hasil evaluasi
for model_name in models.keys():
    with open(f'{model_name}_evaluation.json', 'r') as json_file:
        evaluation_result = json.load(json_file)
    print(f'{model_name} Model:')
    print(f'Accuracy: {evaluation_result["accuracy"]:.2f}')
    print('Classification Report:')
    print(evaluation_result['classification_report'])
    print('-' * 50)
