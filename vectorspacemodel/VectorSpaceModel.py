# This class is inspired from http://blog.christianperone.com/2013/09/machine-learning-cosine-similarity-for-vector-space-models-part-iii/
# Calculation functions are called from utilities.py

from nltk.tokenize import word_tokenize
from utilities import *


class VectorSpaceModel():

    def __init__(self):
        with open('UO_corpus.json') as UO_corpus, open('reuters.json') as reuters:
            doc_uo = json.load(UO_corpus)
            doc_re = json.load(reuters)
            self.all_doc = {document['doc_id'] for document in doc_uo}
            self.all_doc |= {document['doc_id'] for document in doc_re}
        with open('invertedindex.json') as invindex:
            self.inverted_index = json.load(invindex)
        with open('thesaurus.json') as thesaurus:
            self.thesaurus = json.load(thesaurus)
        self.mode = 'unaltered'
        self.tf_idf_matrix = compute_tf_idf(
            self.all_doc,
            self.inverted_index,
            compute_idf(self.all_doc, self.inverted_index))

    def extraction(self, query, mode):
        query = query.lower()
        self.mode = mode

        if mode == 'normalized':
            query = normalize(query)
        elif mode == 'stemmed':
            query = stem(query)
        elif mode == 'stopwords_removed':
            query = remove_stopwords(query)

        tokens = word_tokenize(query)
        query_vector = [1] * len(tokens)
        expanded_tokens, expanded_query_vector = self.processing_thesaurus(tokens, query_vector)
        doc_vectors = compute_doc_vectors(self.all_doc, self.tf_idf_matrix, expanded_tokens)

        return compute_vector_scores(expanded_query_vector, doc_vectors)

    def processing_thesaurus(self, informations, query_vector):
        new_tokens, new_query_vector = [
            i for i in informations], [v for v in query_vector]
        for i in informations:
            if i not in self.thesaurus:
                continue
            related_terms = sorted(
                self.thesaurus[i].items(), key=lambda kv: kv[1], reverse=True)
            related_terms = related_terms[:(2 if len(
                related_terms) > 2 else len(related_terms) - 1)]
            import pprint
            pprint.pprint(related_terms)
            for related_term, score in related_terms:
                if related_term in new_tokens:
                    continue
                new_tokens.append(related_term)
                new_query_vector.append(score)
        show_new_query = zip(new_tokens, new_query_vector)
        new_query = f"New Query: {' '.join(f'{t[0]} ({t[1]})' for t in show_new_query)}"
        print(new_query)
        return new_tokens, new_query_vector
