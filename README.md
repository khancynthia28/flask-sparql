# flask-sparql
web app using python-flask with sparql on nobeldata.owl ontology.

Contains the following endpoints:

/nobel/nations
GET: Return sorted names of all nations

/nobel/categories
GET: Return sorted names of all nobel categories

/nobel/years
GET: Return sorted years nobels are awarded

/nobel/<year>
GET: Return list of all nobel winners for the given year

/nobel/nations/<nation>
GET: Return list of all nobel winners for the given nation

/nobel/categories/<category>
GET: Return list of all nobel winners for the given category

/nobel/<year>/<category>
GET: Return list of all nobel winners for the given year and category
  
### Requirements
Python 3
RDFLib
  
### Instructions to run:
python3 nobel.py
