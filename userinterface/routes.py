from flask import render_template, redirect, Response, request, jsonify
from userinterface import userinterface, boolean_search, vector_space_search, corpus_access, autocomplete_models
from userinterface.forms import SearchForm
import json

# Controller functions to handle the routes for the user interface website and renders the html templates
# Modified from https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms


@userinterface.route('/', methods=['GET', 'POST'])
@userinterface.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        search_results = perform_search(
            form.search.data, form.models.data, form.dictionary_modes.data, form.classification.data)
        return render_template('results.html', results=search_results, model=form.models.data, query=form.search.data, classification=form.classification.data)
    return render_template('search.html', form=form)


@userinterface.route('/result/<doc_id>')
def get_result(doc_id):
    return render_template('result.html', result=corpus_access.get_doc([doc_id]))


@userinterface.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q').strip().lower()
    term_to_search = search.split()[-1].strip()
    if term_to_search not in autocomplete_models:
        return jsonify(matching_results=[])
    autocomplete_options = autocomplete_models[term_to_search]
    sorted_autocomplete_options = sorted(
        autocomplete_options.items(), key=lambda kv: kv[1], reverse=True)
    sorted_autocomplete_options = sorted_autocomplete_options[:(10 if len(
        sorted_autocomplete_options) > 10 else len(sorted_autocomplete_options) - 1)]
    autocomplete_display = [
        f"{search} {key}" for key, _ in sorted_autocomplete_options]
    return jsonify(matching_results=autocomplete_display)


def perform_search(query, model, mode, classification):
    if (model == 'b'):
        return corpus_access.access(boolean_search.extraction(query, mode), classification)
    else:
        extraction = vector_space_search.extraction(query, mode)
        results = []
        for doc_score_pair in extraction:
            extraction = corpus_access.access(
                [doc_score_pair[0]], classification)
            if len(extraction) == 0:
                continue
            corpus_doc = extraction[0]
            corpus_doc['score'] = doc_score_pair[1]
            results.append(corpus_doc)

        return results
