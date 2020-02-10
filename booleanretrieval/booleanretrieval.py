# This class inspired and modified from https://www.codeproject.com/Articles/375219/Boolean-Retrieval-Model

from utilities import *
from nltk import word_tokenize


class booleanretrieval:

    def __init__(self):
        with open('UO_corpus.json') as UO_corpus, open('reuters.json') as reuters:
            doc_uo = json.load(UO_corpus)
            doc_re = json.load(reuters)
            self.all_doc = {document['doc_id'] for document in doc_uo}
            self.all_doc |= {document['doc_id'] for document in doc_re}
        with open('invertedindex.json') as invertedindex:
            self.inverted_index = json.load(invertedindex)
        self.boolean_tokens = ["and", "or", "not"]
        self.mode = 'unaltered'

    def extraction(self, query, mode):

        query = [word.lower()
                 for word in word_tokenize(query) if word not in string.punctuation]
        self.mode = mode

        if mode == 'normalized':
            query = normalize(query)
        elif mode == 'stemmed':
            query = stem(query)
        elif mode == 'stopwords_removed':
            query = remove_stopwords(query)

        query = self.infix_to_postfix(query)
        return self.postfix_retrieval(query)


# Inspired and modified from http://interactivepython.org/runestone/static/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
    def infix_to_postfix(self, query):
        opstack = []
        postfix_list = []
        information_list = query

        for infor in information_list:
            length_infor = len(infor)
            if infor in self.boolean_tokens:
                opstack.append(infor)
            elif infor.startswith('('):
                opstack.append(infor[0])
                if (length_infor > 1):
                    postfix_list.append(infor[1:])
            elif infor.endswith(')'):
                if (length_infor > 1):
                    postfix_list.append(infor[:-1])
                top_token = opstack.pop()
                while top_token != '(':
                    postfix_list.append(top_token)
                    top_token = opstack.pop()
            else:
                postfix_list.append(infor)

        while len(opstack) != 0:
            postfix_list.append(opstack.pop())
        return " ".join(postfix_list)

    def postfix_retrieval(self, postfix_query):
        opstack = []
        querystack = []
        token_list = postfix_query.split()

        for token in token_list:
            if token in self.boolean_tokens:
                opstack.append(token)
            else:
                if '*' in token:
                    permutations = self.check_permutations(token)
                    permutations_query = ' or '.join(permutations)
                    querystack.append(
                        self.extraction(permutations_query, self.mode))
                else:
                    querystack.append(self.information_extraction(token))

        for operation in opstack:
            if operation == 'and':
                if len(querystack) >= 2:
                    queries, querystack = querystack[:2], querystack[2:]
                    operand1, operand2 = queries[0], queries[1]
                    intersect_between = operand1.intersection(operand2)
                    querystack.insert(0, intersect_between)
            elif operation == 'or':
                if len(querystack) >= 2:
                    queries, querystack = querystack[:2], querystack[2:]
                    operand1, operand2 = queries[0], queries[1]
                    union_between = operand1.union(operand2)
                    querystack.insert(0, union_between)
            elif operation == 'not':
                if len(querystack) >= 1:
                    query, querystack = querystack[:1], querystack[1:]
                    difference_between = self.all_doc - query
                    querystack.insert(0, difference_between)

        while(len(querystack) > 1):
            queries, querystack = querystack[:2], querystack[2:]
            operand1, operand2 = queries[0], queries[1]
            intersect_between = operand1.intersection(operand2)
            querystack.insert(0, intersect_between)

        return querystack.pop()

    def information_extraction(self, token):

        doc_ids = set()
        if token in self.inverted_index:
            appearances = self.inverted_index[token]
            for appearance in appearances:
                a = json.loads(appearance, object_hook=lambda d: namedtuple(
                    'X', d.keys())(*d.values()))
                doc_ids.add(a.doc_id)
            return doc_ids
        return set()

    def check_permutations(self, token):

        bigram_index = build_bigram_index(
            self.inverted_index, token)
        permutation_set = set()
        for _, ind_list in bigram_index.items():
            if len(permutation_set) == 0:
                permutation_set.update(ind_list)
            else:
                permutation_set.intersection(ind_list)

        if token.startswith('*'):
            return [k for k in permutation_set if k.endswith(token[1:])]
        elif token.endswith('*'):
            return [k for k in permutation_set if k.startswith(token[:len(token) - 1])]
        else:
            portions = token.split('*')
            for index, portion in enumerate(portions):
                if index == 0:
                    permutation_set = [
                        k for k in permutation_set if k.startswith(portion)]
                elif index == len(portions) - 1:
                    permutation_set = [
                        k for k in permutation_set if k.endswith(portion)]
                else:
                    permutation_set = [
                        k for k in permutation_set if portion in k]
            return permutation_set

