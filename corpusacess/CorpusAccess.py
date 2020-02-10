import json


class CorpusAccess():

    def __init__(self):
        with open('UO_corpus.json') as UO_corpus:
            self.corpus = json.load(UO_corpus)

        with open('new_knn.json') as new_knn:
            self.new_knn = json.load(new_knn)

        with open('new_nb.json') as new_nb:
            self.new_nb = json.load(new_nb)

    def access(self, doc_ids, classification):
        UO_access = [document for document in self.corpus if document['doc_id'] in doc_ids]
        accessed_docs = UO_access + [
            document for document in (self.new_knn if classification == "knn" else self.new_nb) if document['doc_id'] in doc_ids]
        return accessed_docs


    def get_doc(self, doc_id):
        accessed_docs = [document for document in self.corpus if document['doc_id'] in doc_id] + [
            document for document in self.new_knn if document['doc_id'] in doc_id] + [
            document for document in self.new_nb if document['doc_id'] in doc_id]
        return [document for document in accessed_docs if document['doc_id'] == doc_id][0]