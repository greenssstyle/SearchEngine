from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
import numpy as np
import json

"""
    This class is inspired from https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/
"""

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


class naivebayes:

    def __init__(self):
        with open('reuters.json') as corpus:
            corpus_reuters = json.load(corpus)
            self.training_set = [
                article for article in corpus_reuters if article["topic"] != ""]
            self.test_set = [
                article for article in corpus_reuters if article["topic"] == ""]
            self.true_topic_labels = list(
                set(article["topic"] for article in corpus_reuters if article["topic"] != ""))
            self.numeric_topic_labels = {
                label: index for index, label in enumerate(self.true_topic_labels)}

    def process(self):
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(
            [clean(corpus["fulltext"]) for corpus in self.training_set])
        y_training = np.fromiter([
            self.numeric_topic_labels[corpus["topic"]] for corpus in self.training_set], int)
        modalnaivebayes = GaussianNB()
        modalnaivebayes.fit(X.toarray(), y_training)

        test_set_lookup = {article["doc_id"]: clean(
            article["fulltext"]) for article in self.test_set}
        Test = vectorizer.transform(test_set_lookup.values())
        predicted_labels_knn = modalnaivebayes.predict(Test.toarray())

        updated_articles = []
        for index, article in enumerate(self.test_set):
            article["topic"] = self.true_topic_labels[np.int(
                predicted_labels_knn[index])]
            updated_articles.append(article)

        with open('new_nb.json', 'w') as outfile:
            json.dump(self.training_set + updated_articles,
                      outfile, ensure_ascii=False, indent=4)

        with open('final_nb.json', 'w') as outfile:
            json.dump(updated_articles,
                      outfile, ensure_ascii=False, indent=4)


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word)
                          for word in punc_free.split())
    processed = re.sub(r"\d+", "", normalized)
    return processed
