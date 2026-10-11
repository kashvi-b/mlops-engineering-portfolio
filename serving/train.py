"""Train a TF-IDF + Logistic Regression spam classifier and save it to model.pkl.

This mirrors the Spam Detection project on the resume, packaged so it can be
served, streamed, and deployed by the other modules in this repo.
"""
import csv
import os

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "data", "messages.csv")
OUT = os.path.join(HERE, "model.pkl")


def load_dataset():
    texts, labels = [], []
    with open(DATA, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            texts.append(row["text"])
            labels.append(row["label"])
    return texts, labels


def main():
    texts, labels = load_dataset()
    clf = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english")),
        ("lr", LogisticRegression(max_iter=1000)),
    ])
    clf.fit(texts, labels)
    joblib.dump(clf, OUT)
    print(f"Trained on {len(texts)} messages -> {OUT}")


if __name__ == "__main__":
    main()
