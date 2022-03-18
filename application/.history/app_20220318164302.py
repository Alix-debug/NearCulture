from flask import Flask, redirect, url_for
from flask import render_template
import requests

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/<name>")
def user(name):
	return f"Hello {name}!"	

@app.route("/Museum")
def Museum():
	query = """

	PREFIX schema: <http://schema.org/>
	PREFIX sc: <http://purl.org/science/owl/sciencecommons/>
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

	SELECT ?identifier ?name ?longitude ?latitude WHERE {
		?Instance 
		rdf:type schema:Museum; schema:name ?name; 			       
								schema:identifier ?identifier;
								schema:longitude ?longitude;
								schema:latitude ?latitude;
		} LIMIT 100

	"""
	header = {'Content-type': 'application/sparql-query'}
	response = requests.post('http://localhost:3030/Museums/', data=query, headers = header)
	data_museum = response.json()
	print(type(data_museum.head))
	#results.bindings[0].name.value
	return render_template("index.html",content = response.json())

@app.route("/queries")
def query():
	query ="""
	PREFIX schema: <http://schema.org/>
	PREFIX sc: <http://purl.org/science/owl/sciencecommons/>
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

	SELECT ?identifier WHERE {
		?Instance 
		rdf:type schema:Museum; schema:name "musee Chintreuil"; 			       
		schema:identifier ?identifier .}

	"""
	header = {'Content-type': 'application/sparql-query'}
	response = requests.post('http://localhost:3030/Museums/', data=query, headers = header)
	print(response.json())
	return render_template("index.html",content = response.json())


if __name__ == "__main__" :
	app.run(debug=True)