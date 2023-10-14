import json
from sklearn.model_selection import train_test_split


def load_and_process_data():
    file_path = 'data.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    reviews = []
    labels = []

    for item in data:
        reviews.append(item['content'])
        if item['score'] > 3:
            labels.append('positif')
        elif item['score'] < 3:
            labels.append('negatif')
        else:
            labels.append('netral')

    train_reviews, test_reviews, train_labels, test_labels = train_test_split(
        reviews, labels, test_size=0.1, random_state=42)

    # Serialize and print the data
    serialized_data = [train_reviews, test_reviews, train_labels, test_labels]
    print(json.dumps(serialized_data))

    return train_reviews, test_reviews, train_labels, test_labels
