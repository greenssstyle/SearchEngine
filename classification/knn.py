from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
import numpy as np
import json

"""
    This class is inspired from https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/
"""

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


class knn():

    def __init__(self):
        with open('reuters.json') as reuters:
            reuters = json.load(reuters)
            self.doc = reuters
            self.numeric_topic_labels = {label: index for index, label in enumerate(self.doc)}

    def process(self):
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(
            [clean(corpus["fulltext"]) for corpus in self.doc])
        y_training = np.fromiter([
            self.numeric_topic_labels[corpus["topic"]] for corpus in self.doc], int)
        modelknn = KNeighborsClassifier(n_neighbors=5, metric="euclidean")
        modelknn.fit(X, y_training)

        test_set_lookup = {article["doc_id"]: clean(
            article["fulltext"]) for article in self.doc}
        Test = vectorizer.transform(test_set_lookup.values())
        predicted_labels_knn = modelknn.predict(Test)

        updated_articles = []
        for index, article in enumerate(self.doc):
            article["topic"] = self.doc[np.int(
                predicted_labels_knn[index])]
            updated_articles.append(article)

        with open('new_knn.json', 'w') as outfile:
            json.dump(self.doc + updated_articles,
                      outfile, ensure_ascii=False, indent=4)

        with open('final_knn.json', 'w') as outfile:
            json.dump(updated_articles,
                      outfile, ensure_ascii=False, indent=4)


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word)
                          for word in punc_free.split())
    processed = re.sub(r"\d+", "", normalized)
    return processed
