from flask import Flask, render_template, render_template_string, make_response, redirect
from flask.ext.restful import Api, Resource, reqparse, abort

import json
import string
import random
from datetime import datetime

query_parser = reqparse.RequestParser()

# Load data from disk.
# This simply loads the data from our "database," which is just a JSON file.
with open('notebook.jsonld') as data:
    data = json.load(data)

# Raises an error if the string x is empty (has zero length).
def nonempty_string(x):
    s = str(x)
    if len(x) == 0:
        raise ValueError('string is empty')
    return s


# Generate a unique ID for a new help request.
# By default this will consist of six lowercase numbers and letters.
def generate_id(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Respond with 404 Not Found if no notebook with the specified ID exists.
def error_if_notebook_not_found(notebook_id):
    if notebook_id not in data['notebooks']:
        message = "No notebook request with ID: {}".format(notebook_id)
        abort(404, message=message)


# Specify the data necessary to create a new notebook request.
# "author", "title", and "description" are all required values.
new_notebook_parser = reqparse.RequestParser()
for arg in ['author', 'title', 'description']:
    new_notebook_parser.add_argument(
        arg, type=nonempty_string, required=True,
        help="'{}' is a required value".format(arg))


# Define our notebook resource.
class Notebook(Resource):

    def get(self, notebook_id):
        response = make_response(
        render_notebook_as_html(
            data['notebooks'][notebook_id]), 200)
        response.headers['Content-Type'] = "text/html"
        return response


# Define a resource for getting a JSON representation of a help request.
class NotebookAsJSON(Resource):

    # If a  request with the specified ID does not exist,
    # respond with a 404, otherwise respond with a JSON representation.
    def get(self, notebook_id):
        error_if_notebook_not_found(notebook_id)
        notebook = data['notebooks'][notebook_id]
        notebook['@context'] = data['@context']
        return notebook


# Define our help request list resource.
class MasterNotebookList(Resource):

    # Respond with an HTML representation of the help request list, after
    # applying any filtering and sorting parameters.
    def get(self):
        query = query_parser.parse_args()
        response = make_response(
            render_master_list_as_html(
                filter_and_sort_notebooks(**query)), 200)
        response.headers['Content-Type'] = "text/html"
        return response

        # Add a new help request to the list, and respond with an HTML
    # representation of the updated list.
    def post(self):
        notebook = new_notebook_parser.parse_args()
        notebook_id = generate_id()
        notebook['@id'] = 'request/' + notebook_id
        notebook['@type'] = 'notebook:notebook'
        notebook['time'] = datetime.isoformat(datetime.now())
        data['notebooks'][notebook_id] = notebook
        return make_response(
            render_master_list_as_html(
                filter_and_sort_notebooks()), 201)


def render_notebook_as_html(notebook):
    return render_template('notebook+microdata+rdfa.html', 
                            notebook=notebook)


# Given the data for a list of help requests, generate an HTML representation
# of that list.
def render_master_list_as_html(notebooks):
    query = query_parser.parse_args()
    print(notebooks)
    return render_template(
        'notebooks+microdata+rdfa.html',
        notebooks=notebooks)


# Filter and sort a list of helprequests.
def filter_and_sort_notebooks(query='', sort_by='time'):

    # Returns True if the query string appears in the help request's
    # title or description.
    def matches_query(item):
        (notebook_id, notebook) = item
        text = notebook['title'] + notebook['description']
        return query.lower() in text

    # Returns the help request's value for the sort property (which by
    # default is the "time" property).
    def get_sort_value(item):
        (notebook_id, notebook) = item
        return notebook[sort_by]

    filtered_notebooks = filter(matches_query, data['notebooks'].items())

    return sorted(filtered_notebooks, key=get_sort_value, reverse=True)

# Assign URL paths to our resources.
app = Flask(__name__)
api = Api(app)
api.add_resource(MasterNotebookList, '/notebook')
#api.add_resource(MListAsJSON, '/requests.json')
api.add_resource(Notebook, '/notebook/<string:notebook_id>')
api.add_resource(NotebookAsJSON, '/notebook.json/<string:notebook_id>')



# Start the server.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
