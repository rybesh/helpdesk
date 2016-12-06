from flask import Flask, render_template, render_template_string, make_response, redirect
from flask.ext.restful import Api, Resource, reqparse, abort

import json
import string
import random
from datetime import datetime

query_parser = reqparse.RequestParser()


# Define our help request resource.
class MasterRequest(Resource):
    def get(self):
        query = query_parser.parse_args()
        response = make_response(
            render_master_list_as_html(
                filter_and_sort_notebooks(**query)), 200)
        response.headers['Content-Type'] = "text/html"
        return response



# Given the data for a list of help requests, generate an HTML representation
# of that list.
def render_master_list_as_html(notebooks):
    query = query_parser.parse_args()
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


# Load data from disk.
# This simply loads the data from our "database," which is just a JSON file.
with open('notebook.jsonld') as data:
    data = json.load(data)



# Assign URL paths to our resources.
app = Flask(__name__)
api = Api(app)
api.add_resource(MasterRequest, '/notebook')
#api.add_resource(MListAsJSON, '/requests.json')
api.add_resource(MasterRequest, '/notebook/<string:notebook_id>')



# Start the server.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
