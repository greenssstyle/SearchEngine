from .PreprocessingBase import PreprocessingBase
from bs4 import BeautifulSoup
import json
import os


class ReutersPreporcessing(PreprocessingBase):

    def __init__(self):
        super().__init__()
        self.reutersfiles = os.path.join(os.getcwd(), "reuters")

    def preprocess_collections(self):
        for filename in os.listdir(self.reutersfiles):
            with open(os.path.join(self.reutersfiles, filename), 'r') as reuterfile:
                data = reuterfile.read()
                soup = BeautifulSoup(data, "html.parser")
                articles = soup.find_all('reuters')

                for index, article in enumerate(articles, 1):
                    title = article.find('title').text if article.find(
                        'title') is not None else ""
                    description = article.find('body').text if article.find(
                        'body') is not None else ""
                    new_document = self.Document(f'{filename}-article #{index}', title, description.strip(
                    ) if description is not None else '')
                    self.file_form.append(new_document)

        dictionary_form = [file_form._asdict() for file_form in self.file_form]

        with open('reuters.json', 'w') as outfile:
            json.dump(dictionary_form, outfile, ensure_ascii=False, indent=3)
