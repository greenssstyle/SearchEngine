from nltk import bigrams
from utilities import *
import json
from collections import defaultdict
from nltk import  word_tokenize

"""
    This class is inspired from https://nlpforhackers.io/language-models/
"""


class bigramsearch():

    def __init__(self):
        with open('UO_corpus.json') as UO_corpus, open('reuters.json') as reuters:
            doc_uo = json.load(UO_corpus)
            doc_re = json.load(reuters)
            self.all_doc = [document for document in doc_uo] + [document for document in doc_re]

    def bigram_form(self):
        bigram = defaultdict(lambda: defaultdict(lambda: 0))
        for document in self.all_doc:
            fulltext = remove_stopwords([word.lower() for word in word_tokenize(document['fulltext']) if word not in string.punctuation and not any(i.isdigit() for i in word) and word != ""])

            for i, j in bigrams(fulltext):
                bigram[i][j] += 1

            for i in bigram:
                count = float(sum(bigram[i].values()))
                print('1')
                for j in bigram[i]:
                    print('2')
                    bigram[i][j] /= count
        with open('bigram_model.json', 'w') as outfile:
            json.dump(bigram, outfile, ensure_ascii=False, indent=3)
        return bigram