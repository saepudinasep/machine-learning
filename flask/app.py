from flask import Flask, render_template, request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            data = pd.read_csv(file, delimiter=';')
            if 'Minat Teknologi' in data.columns and 'Minat Bisnis' in data.columns:
                data['Minat Teknologi'] = data['Minat Teknologi'].apply(
                    lambda x: 1 if x == 'Tinggi' else 0)
                data['Minat Bisnis'] = data['Minat Bisnis'].apply(
                    lambda x: 1 if x == 'Tinggi' else 0)

                # Load model Decision Tree yang sudah dilatih sebelumnya
                model = joblib.load('model_decision_tree.pkl')

                # Lakukan prediksi menggunakan model
                predictions = model.predict(
                    data.drop(['Jurusan Aktual'], axis=1))
                data['Prediksi Jurusan'] = predictions

                # Menghitung tingkat akurasi
                # Nilai sebenarnya dari data pengujian
                y_test = data['Jurusan Aktual']
                accuracy = accuracy_score(y_test, predictions)

                return render_template('result.html', data=data.to_html(), accuracy=accuracy)
            else:
                return "Kolom 'Minat Teknologi' tidak ditemukan dalam file."
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
