import sys
import joblib


def main():
    try:
        # Load the trained model from the file
        model = joblib.load('model.pkl')

        test_review = input("Enter a review: ")
        predicted_label = model.predict([test_review])
        print("Predicted Label:", predicted_label[0])

    except Exception as e:
        print("Error:", str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
