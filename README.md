This is a simple notekeeping application.
[Flask](http://flask.pocoo.org/) and
[Flask-RESTful](http://flask-restful.readthedocs.org/en/latest/).

**To run the app:**

1. Install required dependencies:
   ```
   $ pip install -r requirements.txt
   ``` 
   [Flask](http://flask.pocoo.org/docs/0.10/installation/#installation)
   and
   [Flask-RESTful](http://flask-restful.readthedocs.org/en/latest/installation.html) to run `server.py`

2. Run the notebook server:
   ```
   $ python notebook-server.py
   ```
   This service is not currently accessible online, so you must run it locally.
   
3. View, post, and update notebooks and references in the notebook application.

4. View JSON-LD data
	
	*In a browser, click the link to view JSON-LD for a given notebook or reference.
	*View the data in the browser or use the JSON-LD Playground at http://json-ld.org/playground/
		*To use the JSON-LD playground, copy and paste data from the browser to the playground.


**JSON-LD data properties**  
    "@container": "@index",  
    "@id": "http://www.w3.org/2000/01/rdf-schema#member",  
    "comment": "http://schema.org/comment",  
    "creator": "http://schema.org/creator",  
    "description": "http://schema.org/description",  
    "notebook": https://schema.org/collection,  
    "references": "https://schema.org/collection"  
    "reference": "https://schema.org/citation",  
    "time": "http://schema.org/dateCreated",  
    "title": "http://schema.org/name",  
    "url": "http://schema.org/URL"
	
**Classes**  
    notebook-editor: an element that changes or creates a notebook
	update: an element that updates the current resource
	search: an element that searchs through the present data
		
**Relationships**  
	alternate: specifies an alternate verson of the resource (in our app, this will be represented in JSON-LD)  
	item: an item in a collection  
	collection: the parent collection of the present resource
	url: the URL for a cited resource

