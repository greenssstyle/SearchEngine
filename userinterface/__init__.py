# Flask structure is inspired from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

from flask import Flask
from booleanretrieval import booleanretrieval
from corpusacess import CorpusAccess
from vectorspacemodel import VectorSpaceModel
import json

userinterface = Flask(__name__)
userinterface.config['SECRET_KEY'] = 'key'
userinterface.add_template_global(name='zip', f=zip)

with open('bigram_model.json') as bigram_model:
    autocomplete_models = json.load(bigram_model)

boolean_search = booleanretrieval.booleanretrieval()
vector_space_search = VectorSpaceModel.VectorSpaceModel()
corpus_access = CorpusAccess.CorpusAccess()

from userinterface import routes
