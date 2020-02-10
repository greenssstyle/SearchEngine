import json
from utilities import *
from collections import defaultdict
import string
from nltk import word_tokenize


class InvertedIndex():
    def __init__(self):
        with open('UO_corpus.json') as information:
            self.UO_corpus = json.load(information)
        with open('reuters.json') as information:
            self.reuters = json.load(information)
        with open('dictionary.json') as fragmentation:
            self.fragmentation = json.load(fragmentation)

    def invertedindex_function(self, wordlist):
        invertedindex_list = defaultdict(list)

        for word in wordlist:
            for index, corpus in enumerate([self.UO_corpus, self.reuters]):
                for document in corpus:
                    if if_contains(document['fulltext'], word) or if_contains(document['title'], word):
                        count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word.lower()),
                                                           (document['fulltext']).lower())) + \
                                sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word.lower()),
                                                           (document['title']).lower()))
                        appearance = Appearence(document['doc_id'], count)
                        invertedindex_list[word].append(appearance)
        return invertedindex_list

    def invertedindex_form(self):
        invertedindex_list = defaultdict(list)

        for index, corpus in enumerate([self.UO_corpus, self.reuters]):
            for document in corpus:
                bow = set(word.lower() for word in word_tokenize(document['title'])
                          if word not in string.punctuation and not any(i.isdigit() for i in word) and word != "")
                bow |= set(word.lower() for word in word_tokenize(document['fulltext'])
                           if word not in string.punctuation and not any(i.isdigit() for i in word) and word != "")
                for word in bow:
                    if if_contains(document['fulltext'], word) or if_contains(document['title'], word):
                        count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word.lower()),
                                                           (document['fulltext']).lower())) + \
                                sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word.lower()),
                                                           (document['title']).lower()))
                        appearance = Appearence(document['doc_id'], count)
                        invertedindex_list[word].append(json.dumps(appearance.__dict__))

        with open('invertedindex.json', 'w') as outfile:
            json.dump(invertedindex_list, outfile, ensure_ascii=False, indent=4)
        return invertedindex_list


class Appearence():
    def __init__(self, doc_id, frequency):
        self.doc_id = doc_id
        self.frequency = frequency

    def __contains__(self, element):
        return element == self.doc_id

    def __repr__(self):
        return str(self.__dict__)
