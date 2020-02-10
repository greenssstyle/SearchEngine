from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired
import pickle


class SearchForm(FlaskForm):

    with open('topic_chosen.pickle', 'rb') as handle:
        topic_choices = pickle.load(handle)

    search = StringField('Search Field', validators=[
                         DataRequired()], id='search_autocomplete')
    models = RadioField('Search Model', choices=[
        ('b', 'Boolean Model'), ('v', 'Vector Space Model')], default='b', validators=[DataRequired()])
    classification = RadioField('Classification', choices=[
        ('knn', 'KNN Algorithm'), ('nb', 'Naive Bayes Algorithm')], default='knn', validators=[DataRequired()])
    dictionary_modes = RadioField('Dictionary Mode', choices=[('unaltered', 'Unaltered'),
        ('stopwords_removed', 'Stopwords Removed'), ('stemmed', 'Stemmed'), ('normalized', 'Normalized')], default='unaltered', validators=[DataRequired()])
    submit = SubmitField('Submit')
