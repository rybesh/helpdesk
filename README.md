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
	"comment": "http://schema.org/comment",
    "creator": "http://schema.org/creator",
    "description": "http://schema.org/description",
    "notebook": "https://rawgit.com/sils-webinfo/notebook/master/vocab.ttl#",
    "references": "https://schema.org/collection"
	"reference": "https://schema.org/citation",
    "time": "http://schema.org/dateCreated",
    "title": "http://schema.org/name",
    "url": "http://schema.org/URL"
