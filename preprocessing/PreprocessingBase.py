from abc import ABC, abstractmethod
from collections import namedtuple


class PreprocessingBase(ABC):

    def __init__(self):
        self.Document = namedtuple("Document", "doc_id title fulltext")
        self.file_form = []
        super().__init__()

    @abstractmethod
    def preprocess_collections(self):
        pass
