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
	result_query=""
	for i in range(0, len(data_museum['results']["bindings"])) :
		result_query += data_museum['results']["bindings"][0]["name"]["value"] 
	#results
	return render_template("index.html",content = response.json())

@app.route("/Travelers")
def Traveler():
	query = """
	
		prefix :      <http://www.semanticweb.org/protegee> 
		prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
		prefix owl:   <http://www.w3.org/2002/07/owl#> 
		prefix xml:   <http://www.w3.org/XML/1998/namespace> 
		prefix xsd:   <http://www.w3.org/2001/XMLSchema#> 
		prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> 
	
	SELECT  ?age ?birthDate ?familyName ?givenName ?latitude ?longitude WHERE {
			?Instance 
			rdf:type owl:NamedIndividual  ; :age ?age; 	
	                             	:birthDate ?birthDate; 
	                             	:familyName ?familyName; 
									:givenName ?givenName;
	        						:latitude ?latitude;
									:longitude ?longitude;
									
	} 

	"""
	header = {'Content-type': 'application/sparql-query'}
	response = requests.post('http://localhost:3030/Travelers/', data=query, headers = header)
	data_traveler = response.json()
	result_query=""
	for i in range(0, len(data_traveler['results']["bindings"])) :
		result_query += data_traveler['results']["bindings"] 
	#results
	return render_template("index.html",content = response.json())
@app.route("/Libraries")
def Library():
	query = """

	PREFIX schema: <http://schema.org/>
PREFIX sc: <http://purl.org/science/owl/sciencecommons/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?identifier ?name ?longitude ?latitude WHERE {
		?Instance 
		rdf:type schema:Library; schema:name ?name; 			       
								schema:identifier ?identifier;
								schema:longitude ?longitude;
								schema:latitude ?latitude;
		} LIMIT 100

	"""
	header = {'Content-type': 'application/sparql-query'}
	response = requests.post('http://localhost:3030/Libraries/', data=query, headers = header)
	data_library = response.json()
	result_query="<tr>"
	for i in range(0, len(data_library['results']["bindings"])) :
		result_query += "<td>"+data_library['results']["bindings"][i]["name"]["value"]+"</td>"
	#results
	result_query+="</tr>"
	return render_template("index.html",content = result_query)


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