import json
from collections import defaultdict, namedtuple
from nltk import word_tokenize


class thesaurus():


    def __init__(self):
        with open('invertedindex.json') as inverted_index:
            self.inverted_index = json.load(inverted_index)

        with open('reuters.json') as corpus:
            self.corpus_reuters = json.load(corpus)

    def generate_documentation(self):
        documentation = defaultdict(lambda: defaultdict(lambda: 0))
        term_freq_dict = defaultdict(int)

        for word, appearances in self.inverted_index.items():
            total_appearances = 0
            for appearance in appearances:
                a = json.loads(appearance, object_hook=lambda d: namedtuple(
                    'X', d.keys())(*d.values()))
                total_appearances += a.frequency
            term_freq_dict[word] = total_appearances

        highest_frequency_words = [(k, term_freq_dict[k]) for k in sorted(
            term_freq_dict, key=term_freq_dict.get, reverse=True)][:2000]

        for article in self.corpus_reuters:
            doc_id, fulltext = article["doc_id"], word_tokenize(
                article["fulltext"])
            for pair in highest_frequency_words:
                word_count = fulltext.count(pair[0])
                if word_count > 0:
                    documentation[doc_id][pair[0]] = word_count

        wordlist = [pair[0] for pair in highest_frequency_words]

        with open('documentation.json', 'w') as doc_term:
            json.dump(documentation, doc_term,
                      ensure_ascii=False, indent=4)

        with open('wordlist.json', 'w') as wordlistjson:
            json.dump(wordlist, wordlistjson, ensure_ascii=False, indent=3)

    def generate_thesaurus(self):
        with open('documentation.json') as doc_term:
            documentation = json.load(doc_term)

        with open('wordlist.json') as wordlist:
            terms = json.load(wordlist)

        total_occurences = defaultdict(lambda: 0)
        thesaurus = defaultdict(lambda: defaultdict(lambda: 0))
        for _, wordlist in documentation.items():
            for word, occurences in wordlist.items():
                total_occurences[word] += occurences

        for index1, word1 in enumerate(terms[:len(terms) - 1]):
            for _, word2 in enumerate(terms[index1 + 1:]):
                num_doc_pair_occurences = sum((min(wordlist[word1], wordlist[word2]) for _, wordlist in documentation.items(
                ) if word1 in wordlist and word2 in wordlist), 0)
                if num_doc_pair_occurences > 0:
                    thesaurus[word1][word2] = (
                        num_doc_pair_occurences / (total_occurences[word1] + total_occurences[word2]))
        with open('thesaurus.json', 'w') as information:
            json.dump(thesaurus, information,
                      ensure_ascii=False, indent=3)
