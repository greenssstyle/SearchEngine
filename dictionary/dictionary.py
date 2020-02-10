import json
import string
from nltk.tokenize import word_tokenize


class Dictionary:
    def __init__(self):
        self.ALLcorpus = ["UO_corpus.json", "reuters.json"]
        self.frag = {
            'unaltered': set(),
            'stopwords_removed': set(),
            'stemmed': set(),
            'normalized': set()
        }

    def make_dictionary(self):

        for index, ALLcorpus in enumerate(self.ALLcorpus):
            with open(ALLcorpus) as information:
                data = json.load(information)

            for i in data:

                title_token = [word.lower() for word in word_tokenize(i['title'])
                               if word not in string.punctuation and not any(i.isdigit() for i in word) and word != ""]
                self.frag['unaltered'] |= set(title_token)
                self.frag['stopwords_removed'] |= set(title_token)
                self.frag['stemmed'] |= set(title_token)
                self.frag['normalized'] |= set(title_token)

                fulltext_token = [word.lower() for word in word_tokenize(i['fulltext'])
                                if word not in string.punctuation and not any(i.isdigit() for i in word) and word != ""]
                self.frag['unaltered'] |= set(fulltext_token)
                self.frag['stopwords_removed'] |= set(fulltext_token)
                self.frag['stemmed'] |= set(fulltext_token)
                self.frag['normalized'] |= set(fulltext_token)

        with open('dictionary.json', 'w') as outfile:
            uo_fragment = {a: list(b) for (a, b) in self.frag.items()}
            json.dump(uo_fragment, outfile, ensure_ascii=False, indent=3)
