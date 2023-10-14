import json
from textblob import TextBlob

# Baca file JSON
with open('data.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

# Fungsi untuk menentukan sentimen


def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positif'
    elif analysis.sentiment.polarity == 0:
        return 'netral'
    else:
        return 'negatif'


# Tambahkan label sentimen ke setiap entri
for entry in data:
    # Gantilah 'text' dengan kunci yang sesuai dalam struktur JSON Anda
    text = entry['content']
    sentiment = analyze_sentiment(text)
    entry['sentiment'] = sentiment

# Simpan data yang telah diberi label sentimen kembali ke file JSON
with open('data_with_sentiment.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Label sentimen berhasil ditambahkan dan disimpan di 'data_with_sentiment.json'.")
