import sys
from sklearn.externals import joblib


def main():
    try:
        model = joblib.load('count_vectorizer.pkl')
        review = sys.argv[1]
        predicted_label = model.predict([review])[0]
        print(predicted_label)

    except Exception as e:
        print("Error:", str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
