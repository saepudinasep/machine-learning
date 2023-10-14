import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib
from sklearn.metrics import accuracy_score

# Load dataset
# Ganti 'dataset.csv' dengan nama file dataset Anda
data = pd.read_csv('data.csv', delimiter=';')
# Konversi nilai 'Minat Teknologi' dan 'Minat Bisnis' menjadi angka biner
data['Minat Teknologi'] = data['Minat Teknologi'].apply(
    lambda x: 1 if x == 'Tinggi' else 0)
data['Minat Bisnis'] = data['Minat Bisnis'].apply(
    lambda x: 1 if x == 'Tinggi' else 0)

# Pisahkan atribut dan target
X = data.drop(['Jurusan Aktual'], axis=1)
y = data['Jurusan Aktual']

# Bagi data menjadi data pelatihan dan data pengujian
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Inisialisasi model Decision Tree
model = DecisionTreeClassifier()

# Latih model menggunakan data pelatihan
model.fit(X_train, y_train)


# Prediksi menggunakan model pada data pengujian
y_pred = model.predict(X_test)

# Hitung tingkat akurasi
accuracy = accuracy_score(y_test, y_pred)
print(f'Tingkat Akurasi: {accuracy:.2f}')

# Simpan model ke dalam file .pkl
joblib.dump(model, 'model_decision_tree.pkl')
