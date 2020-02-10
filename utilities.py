import string
import re
import pickle
import math
import json
from collections import defaultdict, namedtuple
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from preprocessing import UOPreprocessing, ReutersPreprocessing
from dictionary import dictionary
from invertedindex import InvertedIndex
from bigram import bigramsearch
from thesaurus import thesaurus
from classification import naivebayes, knn


def generate_UO_corppus():
    json = UOPreprocessing.UOPreprocessing()
    json.preprocess_collections()
    print("UO_corpus.json is generated")


def generate_reuters():
    json = ReutersPreprocessing.ReutersPreporcessing()
    json.preprocess_collections()
    print("reuters.json is generated")


def generate_dictionary():
    json = dictionary.Dictionary()
    json.make_dictionary()
    print("dictionary.json is generated")


def generate_invertedindex():
    json = InvertedIndex.InvertedIndex()
    json.invertedindex_form()
    print("invertedindex.json is generated")


def generate_bigrammodel():
    bigram = bigramsearch.bigramsearch
    bigram.bigram_form()
    print("bigram_model.json is generated")


def generate_documentation():
    json = thesaurus.thesaurus()
    json.generate_documentation()
    print("documentation.json is generated")


def generate_thesaurus():
    json = thesaurus.thesaurus()
    json.generate_thesaurus()
    print("thesaurus.json is generated")


def generate_knn():
    json = knn.knn()
    json.process()
    print("new_knn.json and final_knn.json is generated")


def generate_nb():
    json = naivebayes.naivebayes()
    json.process()
    print("new_nb.json and final_nb.json is generated")


def generate_list():
    topic_choice = []
    with open('topics.txt') as topics:
        for topic in topics:
            topic_choice.append((topic.rstrip(), topic.rstrip()))

    with open('topic_chosen.pickle', 'wb') as fp:
        pickle.dump(topic_choice, fp)


def normalize(text):
    return {word.translate(str.maketrans('', '', string.punctuation)).lower() for word in text}


def remove_stopwords(text):
    stop_words = set(stopwords.words('english')) | set(
        stopwords.words('french'))
    return set([w.lower() for w in text if not w in stop_words])


def stem(text):
    stemmer = PorterStemmer()
    return set([stemmer.stem(w).lower() for w in text])


def contains_element(fulltext, element):
    escape_pattern = re.escape(element.lower())
    compile_pattern = re.compile(r'\b({0})\b'.format(escape_pattern), re.IGNORECASE)
    return compile_pattern.search(fulltext.lower())


def if_contains(fulltext, word):
    return word in fulltext


def is_empty(list):
    if list:
        return False
    else:
        return True


def build_bigram_index(inv_index, token):
    bigrams = [token[i:i + 2] for i in range(1, len(
        token) - 1, 2)]
    bigrams.append(token[0])
    bigrams.append(token[-1])
    bigrams = [''.join(b for b in bigram if b not in '*')
               for bigram in bigrams]
    return {bigram: [index for index in inv_index.keys() if bigram in index] for bigram in bigrams}


def compute_idf(all_doc, invertedindex):
    return {word: math.log10(len(all_doc) / len(docs)) for word, docs in invertedindex.items()}


def compute_tf_idf(all_doc, invertedindex, idf_index):
    tf_idf = defaultdict(lambda: defaultdict(int))
    for word, docs in invertedindex.items():
        placeholder = defaultdict(int)
        for appearance in docs:
            a = json.loads(appearance, object_hook=lambda d: namedtuple(
                'X', d.keys())(*d.values()))
            placeholder[a.doc_id] = a.frequency * \
                idf_index[word]
        tf_idf[word] = placeholder

    return tf_idf


def compute_doc_vectors(all_doc, tf_idf_matrix, tokens):

    doc_vectors = defaultdict(tuple)

    for doc_id in all_doc:
        vector = []
        for token in tokens:
            set_of_docweights = tf_idf_matrix[token]
            weight = set_of_docweights[doc_id]
            vector.append(weight)
        doc_vectors[doc_id] = vector

    return doc_vectors


def compute_vector_scores(query_vector, doc_vectors):

    scores = []
    for doc_id, vector in doc_vectors.items():
        score = 0
        for query_vector_weight, doc_tf_idf in zip(query_vector, vector):
            score += query_vector_weight * doc_tf_idf
        scores.append((doc_id, score))
    scores.sort(key=lambda tup: tup[1], reverse=True)
    return [score for score in scores if score[1] != 0]

"""
generate_UO_corppus()
generate_reuters()
generate_dictionary()
generate_invertedindex()
generate_list()
generate_bigrammodel()
generate_documentation()
generate_thesaurus()
generate_knn()
generate_nb()
"""
