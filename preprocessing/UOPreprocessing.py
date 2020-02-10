from .PreprocessingBase import PreprocessingBase
from bs4 import BeautifulSoup
import requests
import json


class UOPreprocessing(PreprocessingBase):


    def __init__(self):
        super().__init__()
        self.url = 'https://catalogue.uottawa.ca/en/courses/csi/'

    def preprocess_collections(self):

        web_infor = requests.get(self.url)
        soup = BeautifulSoup(web_infor.text, 'html.parser')
        courseblocks = soup.find_all('div', attrs={'class': 'courseblock'})

        for index, courseblock in enumerate(courseblocks, 1):
            title_with_credit = courseblock.find(
                'p', attrs={'class': 'courseblocktitle'}).text
            sep = '('
            title = title_with_credit.split(sep, 1)[0]
            description = courseblock.find('p', attrs={'class': 'courseblockdesc'})
            if description is None:
                docID = self.Document(f'CSI_Course_{index}', title, '')
            else:
                docID = self.Document(f'CSI_Course_{index}', title, description.text.strip())
            self.file_form.append(docID)

        dictionary_form = [file_form._asdict() for file_form in self.file_form]

        with open('UO_corpus.json', 'w') as outfile:
            json.dump(dictionary_form, outfile, ensure_ascii=False, indent=3)
